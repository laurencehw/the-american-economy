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


class TestCacheModes(CacheFixture):
    """Regression tests for the cache TTL, which was previously never enforced."""

    def _age_cache(self, provider: str, series_id: str, days: float) -> None:
        import os
        import time
        path = self.tmp / provider / f"{series_id}.json"
        old = time.time() - days * 86400
        os.utime(path, (old, old))

    def test_default_mode_uses_a_cache_within_ttl(self) -> None:
        seed_cache(self.tmp, "fred", "X", {"2024-01": 1.0})
        series = sources.fetch("fred", "X")           # no network needed
        self.assertTrue(series.from_cache)

    def test_default_mode_refetches_once_the_cache_is_stale(self) -> None:
        seed_cache(self.tmp, "fred", "X", {"2024-01": 1.0})
        self._age_cache("fred", "X", days=3)          # older than CACHE_TTL
        # Egress is unavailable here, so a fetch attempt surfaces as FetchError.
        # That it attempts at all is the point: the stale cache was not returned.
        with self.assertRaises(sources.FetchError):
            sources.fetch("fred", "X")

    def test_offline_accepts_a_cache_of_any_age(self) -> None:
        seed_cache(self.tmp, "fred", "X", {"2024-01": 1.0})
        self._age_cache("fred", "X", days=400)
        self.assertTrue(sources.fetch("fred", "X", offline=True).from_cache)

    def test_refresh_never_returns_the_cache(self) -> None:
        seed_cache(self.tmp, "fred", "X", {"2024-01": 1.0})
        with self.assertRaises(sources.FetchError):
            sources.fetch("fred", "X", refresh=True)


class TestYearSelection(CacheFixture):
    """A stale-but-correct figure must not be reported as a divergence."""

    def test_a_table_is_compared_against_the_year_it_declares(self) -> None:
        # Table 1.3 declares December 2023. Manufacturing employment has moved
        # since; the comparison must still use 2023 and report 2025 separately.
        seed_cache(self.tmp, "fred", "MANEMP", {"2023-01": 12_900.0, "2025-01": 12_100.0})
        tables = report.reconcile_tables(REPO, offline=True, refresh=False)
        _, rows = tables[0]
        row = next(r for r in rows if r["label"] == "Manufacturing")
        self.assertEqual(row["year"], 2023)
        self.assertEqual(row["value"], 12_900.0)
        self.assertEqual(row["latest_year"], 2025)
        self.assertEqual(row["latest_value"], 12_100.0)

    def test_table_reference_year_is_read_from_the_source_line(self) -> None:
        # The caption says only "Employment by Sector"; the year is in the source.
        self.assertEqual(registry.TABLE_CLAIMS[0].reference_year(REPO), 2023)

    def test_a_claim_falls_back_to_the_latest_complete_year_not_a_partial_one(self) -> None:
        # gdp_real states no year. The current year is partial and must not be used.
        current = date.today().year
        seed_cache(self.tmp, "fred", "GDPC1",
                   {f"{current - 1}-01": 23_000.0, f"{current}-01": 99_999.0})
        results = report.reconcile_claims(REPO, offline=True, refresh=False)
        result = next(r for r in results if r.claim.id == "gdp_real")
        self.assertEqual(result.series_year, current - 1)
        self.assertEqual(result.series_value, 23_000.0)


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


class TestTableChecker(unittest.TestCase):
    """The CI table checker, run against a throwaway manuscript."""

    SCRIPT = REPO / ".github" / "scripts" / "check_tables.py"

    def run_on(self, body: str) -> tuple[int, str]:
        import subprocess
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "book" / "part1").mkdir(parents=True)
            (tmp / "book" / "part1" / "ch01-x.md").write_text(body, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(self.SCRIPT)], cwd=tmp,
                capture_output=True, text=True,
            )
            return result.returncode, result.stdout
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    @staticmethod
    def table(caption: str | None) -> str:
        head = f"{caption}\n\n" if caption else "Some prose.\n\n"
        return head + "| A | B |\n|---|---|\n| 1 | 2 |\n\n*Source: Example*\n\n"

    def test_a_well_formed_file_passes(self) -> None:
        body = "# 1. X\n\n" + self.table("**Table 1.1: One**") + self.table("**Table 1.2: Two**")
        code, out = self.run_on(body)
        self.assertEqual(code, 0, out)

    def test_a_missing_caption_does_not_cascade_onto_later_tables(self) -> None:
        # Regression: the sequence counter used to advance only on a parsed
        # caption, so one malformed table reported every later table as out of
        # sequence. Exactly one error should be raised here.
        body = ("# 1. X\n\n" + self.table("**Table 1.1: One**") + self.table(None)
                + self.table("**Table 1.3: Three**") + self.table("**Table 1.4: Four**"))
        code, out = self.run_on(body)
        self.assertEqual(code, 1)
        self.assertEqual(out.count("no numbered caption"), 1, out)
        self.assertNotIn("out of sequence", out)

    def test_a_genuinely_misnumbered_table_is_still_caught(self) -> None:
        body = "# 1. X\n\n" + self.table("**Table 1.1: One**") + self.table("**Table 1.7: Seven**")
        code, out = self.run_on(body)
        self.assertEqual(code, 1)
        self.assertIn("out of sequence", out)

    def test_missing_source_reports_a_one_based_line_number(self) -> None:
        body = "# 1. X\n\n**Table 1.1: One**\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\nProse, not a source.\n"
        code, out = self.run_on(body)
        self.assertEqual(code, 1)
        # The table's last row is line 7, so the report should point at line 8.
        self.assertIn("ch01-x.md:8 — table has no source line", out)

    def test_prose_mentioning_a_source_is_not_an_attribution(self) -> None:
        # Regression: the substring "author" matched "Port Authorities".
        body = ("# 1. X\n\n**Table 1.1: One**\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n"
                "The American Association of Port Authorities lobbies on dredging.\n")
        code, out = self.run_on(body)
        self.assertEqual(code, 1)
        self.assertIn("no source line", out)

    def test_a_note_is_not_an_attribution_but_may_accompany_one(self) -> None:
        note_only = ("# 1. X\n\n**Table 1.1: One**\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n"
                     "*Note: figures are approximate.*\n")
        self.assertEqual(self.run_on(note_only)[0], 1)
        with_both = note_only + "\n*Source: Example*\n"
        self.assertEqual(self.run_on(with_both)[0], 0)

    def test_a_schematic_satisfies_attribution(self) -> None:
        body = ("# 1. X\n\n**Table 1.1: One**\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n"
                "*Author's schematic*\n")
        self.assertEqual(self.run_on(body)[0], 0)


if __name__ == "__main__":
    unittest.main()
