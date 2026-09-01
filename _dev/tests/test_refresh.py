"""Tests for the reconciliation tooling.

The fetchers cannot be exercised against the live APIs in CI, so these tests
seed the on-disk cache with known series and check that the comparison
arithmetic, unit scaling, and staleness logic are right.

Run: python3 -m unittest discover -s _dev/tests
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from refresh import inventory, registry, report, sources  # noqa: E402

REPO = Path(__file__).resolve().parents[2]


def seed_cache(cache_dir: Path, provider: str, series_id: str, observations: dict[str, float]) -> None:
    path = cache_dir / provider / f"{series_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "series_id": series_id,
                "retrieved": date.today().isoformat(),
                "observations": [{"period": p, "value": v} for p, v in observations.items()],
            }
        ),
        encoding="utf-8",
    )


class CacheFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self._real_cache = sources.CACHE_DIR
        sources.CACHE_DIR = self.tmp

    def tearDown(self) -> None:
        sources.CACHE_DIR = self._real_cache
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestSeries(CacheFixture):
    def test_annual_averages_quarterly_observations(self) -> None:
        seed_cache(self.tmp, "fred", "GDP",
                   {"2023-01": 100.0, "2023-04": 200.0, "2024-01": 300.0, "2024-04": 500.0})
        series = sources.fetch("fred", "GDP", offline=True)
        self.assertEqual(series.annual(), {2023: 150.0, 2024: 400.0})

    def test_latest_complete_year_excludes_the_current_one(self) -> None:
        seed_cache(self.tmp, "fred", "X", {"2024-01": 1.0, "2026-01": 2.0})
        series = sources.fetch("fred", "X", offline=True)
        self.assertEqual(series.latest_complete_year(today=date(2026, 9, 1)), 2024)

    def test_offline_without_cache_raises_rather_than_returning_nothing(self) -> None:
        with self.assertRaises(sources.FetchError):
            sources.fetch("fred", "NOT_CACHED", offline=True)

    def test_unknown_provider_is_rejected(self) -> None:
        with self.assertRaises(sources.FetchError):
            sources.fetch("madeup", "X", offline=False)


class TestClaimComparison(CacheFixture):
    def _result(self, claim_id: str) -> report.ClaimResult:
        results = report.reconcile_claims(REPO, offline=True, refresh=False)
        return next(r for r in results if r.claim.id == claim_id)

    def test_book_trillions_compare_against_series_billions(self) -> None:
        # The book says $27.8 trillion for 2023; book_scale=1000 makes that 27,800
        # to match FRED's GDP series, which is in billions.
        seed_cache(self.tmp, "fred", "GDP", {"2023-01": 27_800.0})
        result = self._result("gdp_nominal")
        self.assertEqual(result.book_value, 27.8)
        self.assertEqual(result.series_value, 27_800.0)
        self.assertAlmostEqual(result.divergence_pct, 0.0)
        self.assertEqual(result.status, "ok")

    def test_divergence_beyond_tolerance_is_flagged(self) -> None:
        seed_cache(self.tmp, "fred", "GDP", {"2023-01": 30_000.0})
        result = self._result("gdp_nominal")
        self.assertAlmostEqual(result.divergence_pct, (27_800 - 30_000) / 30_000 * 100, places=6)
        self.assertEqual(result.status, "diverged")

    def test_book_year_selects_the_matching_observation(self) -> None:
        # The claim states 2023, so the 2023 value must be used even though 2024 exists.
        seed_cache(self.tmp, "fred", "GDP", {"2023-01": 27_800.0, "2024-01": 29_200.0})
        result = self._result("gdp_nominal")
        self.assertEqual(result.series_year, 2023)
        self.assertEqual(result.series_value, 27_800.0)

    def test_negative_scale_handles_a_deficit_stated_as_positive(self) -> None:
        # FRED's goods balance is negative; the book states the deficit as positive.
        seed_cache(self.tmp, "fred", "BOPGTB", {"2024-01": -1_200.0})
        result = self._result("goods_trade_deficit")
        self.assertEqual(result.book_value, 1.2)
        self.assertAlmostEqual(result.divergence_pct, 0.0)

    def test_manual_claims_are_never_reported_as_agreeing(self) -> None:
        result = self._result("union_density")
        self.assertEqual(result.status, "manual")
        self.assertIsNone(result.series_value)

    def test_fetch_failure_is_surfaced_not_swallowed(self) -> None:
        result = self._result("nonfarm_payrolls")   # nothing seeded
        self.assertEqual(result.status, "error")
        self.assertTrue(result.error)


class TestRegistry(unittest.TestCase):
    def test_every_locator_matches_the_manuscript(self) -> None:
        result = registry.verify_locators(REPO)
        self.assertEqual(result.broken, [], "registry locators drifted from the manuscript")

    def test_claims_declare_units_the_comparison_can_use(self) -> None:
        for claim in registry.CLAIMS:
            if claim.provider != registry.MANUAL:
                self.assertTrue(claim.series_id, f"{claim.id} has no series id")
            self.assertGreater(claim.tolerance_pct, 0, f"{claim.id} has no tolerance")


class TestInventory(unittest.TestCase):
    def setUp(self) -> None:
        self.inv = inventory.scan(REPO / "book")

    def test_every_table_parses(self) -> None:
        self.assertEqual(self.inv.problems, [])
        self.assertEqual(len(self.inv.tables), 189)

    def test_schematics_are_excluded_from_staleness(self) -> None:
        schematics = [t for t in self.inv.tables if t.kind == "schematic"]
        self.assertTrue(schematics)
        for table in schematics:
            self.assertFalse(table.dated)
            self.assertIsNone(table.age(2026))

    def test_reference_year_prefers_the_caption_over_the_source_line(self) -> None:
        table = next(t for t in self.inv.tables if t.number == "1.1")
        self.assertEqual(table.year, 2023)   # caption says 2023, source line says October 2023

    def test_age_is_measured_against_the_given_year(self) -> None:
        table = next(t for t in self.inv.tables if t.number == "1.2")
        self.assertEqual(table.age(2026), 2026 - table.year)


if __name__ == "__main__":
    unittest.main()
