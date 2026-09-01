"""Render the reconciliation report."""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import inventory, registry, sources

# Tables whose figures readers expect to be a snapshot rather than current.
SNAPSHOT_KINDS = {"company filings", "industry body", "academic", "statute"}


@dataclass
class ClaimResult:
    claim: registry.Claim
    book_value: float | None
    book_year: int | None
    line: int | None
    series_year: int | None = None
    series_value: float | None = None
    error: str = ""

    @property
    def comparable(self) -> bool:
        return self.book_value is not None and self.series_value is not None

    @property
    def divergence_pct(self) -> float | None:
        if not self.comparable or self.series_value == 0:
            return None
        scaled = self.book_value * self.claim.book_scale
        return (scaled - self.series_value) / abs(self.series_value) * 100

    @property
    def status(self) -> str:
        if self.claim.provider == registry.MANUAL:
            return "manual"
        if self.error:
            return "error"
        divergence = self.divergence_pct
        if divergence is None:
            return "error"
        return "ok" if abs(divergence) <= self.claim.tolerance_pct else "diverged"


def _sort_key(table: inventory.Table) -> tuple:
    """Sort table numbers naturally: 1.2 before 1.10 before 4.1, appendices last."""
    chapter = table.chapter
    if chapter.isdigit():
        return (0, int(chapter), int(table.number.split(".")[1]))
    # The Interlude sits after Part I; lettered appendices go at the end.
    rank = 1 if chapter == "I" else 2
    return (rank, ord(chapter), int(table.number.split(".")[1]))


def _fmt(value: float | None, units: str = "") -> str:
    if value is None:
        return "—"
    if abs(value) >= 1000:
        return f"{value:,.0f}"
    return f"{value:,.2f}".rstrip("0").rstrip(".")


def reconcile_claims(repo: Path, *, offline: bool, refresh: bool) -> list[ClaimResult]:
    results: list[ClaimResult] = []
    for claim in registry.CLAIMS:
        found = claim.locate(repo)
        if found is None:
            results.append(ClaimResult(claim, None, None, None, error="locator no longer matches"))
            continue
        value, year, line = found
        result = ClaimResult(claim, value, year, line)
        if claim.provider != registry.MANUAL:
            try:
                series = sources.fetch(claim.provider, claim.series_id, offline=offline, refresh=refresh)
                target = year or series.latest_complete_year()
                annual = series.annual()
                if target in annual:
                    result.series_year, result.series_value = target, annual[target]
                elif annual:
                    latest = max(annual)
                    result.series_year, result.series_value = latest, annual[latest]
                else:
                    result.error = "series returned no annual observations"
            except sources.FetchError as exc:
                result.error = str(exc)
        results.append(result)
    return results


def reconcile_tables(repo: Path, *, offline: bool, refresh: bool) -> list[tuple[registry.TableClaim, list[dict]]]:
    out = []
    for table in registry.TABLE_CLAIMS:
        located = table.locate(repo) or []
        rows = []
        for label, value, line in located:
            series_id = table.rows.get(label, "")
            row = {"label": label, "book": value, "line": line, "series_id": series_id,
                   "value": None, "year": None, "error": ""}
            if not series_id:
                row["error"] = "no single series matches this row"
            else:
                try:
                    series = sources.fetch(table.provider, series_id, offline=offline, refresh=refresh)
                    annual = series.annual()
                    year = series.latest_complete_year()
                    if year in annual:
                        row["year"], row["value"] = year, annual[year]
                    else:
                        row["error"] = "series returned no annual observations"
                except sources.FetchError as exc:
                    row["error"] = str(exc)
            rows.append(row)
        out.append((table, rows))
    return out


def render(repo: Path, *, offline: bool, refresh: bool, as_of: int | None = None) -> str:
    today = date.today()
    as_of = as_of or today.year
    inv = inventory.scan(repo / "book")
    locators = registry.verify_locators(repo)
    claims = reconcile_claims(repo, offline=offline, refresh=refresh)
    tables = reconcile_tables(repo, offline=offline, refresh=refresh)

    fetched = sum(1 for c in claims if c.series_value is not None)
    attempted = sum(1 for c in claims if c.claim.provider != registry.MANUAL)

    L: list[str] = []
    add = L.append

    add("# Data Reconciliation Report")
    add("")
    add(f"Generated {today.isoformat()} by `_dev/refresh_data.py`. "
        f"Mode: **{'offline' if offline else 'online'}**.")
    add("")
    if offline or fetched < attempted:
        add("> **Series values were not retrieved.** This environment blocks outbound")
        add("> connections to fred.stlouisfed.org, api.bls.gov and apps.bea.gov, so the")
        add("> comparison columns below are empty. Run this script somewhere with network")
        add("> access to populate them. Everything else in this report — the vintage audit,")
        add("> the worklist, and the book's own stated values — is derived from the")
        add("> manuscript and is complete.")
        add("")

    # --- 1. Registry health --------------------------------------------------
    add("## 1. Registry health")
    add("")
    if locators.healthy:
        add(f"All {len(locators.ok)} registry locators still match the manuscript.")
    else:
        add("**Locators that no longer match** — the manuscript was edited in a way that "
            "broke the pattern. Fix these in `_dev/refresh/registry.py` before trusting "
            "the rest of this report:")
        add("")
        for broken in locators.broken:
            add(f"- `{broken}`")
    add("")
    if inv.problems:
        add(f"Inventory problems: {len(inv.problems)}")
        for problem in inv.problems[:10]:
            add(f"- {problem}")
    else:
        add(f"All {len(inv.tables)} tables parsed cleanly: caption, source line, and reference year.")
    add("")

    # --- 2. Claim reconciliation --------------------------------------------
    add("## 2. Headline claims")
    add("")
    add("What the book says, against the series its source line names. `book_scale` in the "
        "registry converts the book's units to the series' units before comparing.")
    add("")
    add("| Claim | Book says | Year | Series | Series says | Divergence | Status |")
    add("|-------|----------:|:----:|--------|------------:|-----------:|--------|")
    for result in claims:
        claim = result.claim
        series_label = claim.series_id if claim.series_id else "_manual_"
        divergence = result.divergence_pct
        div_text = f"{divergence:+.1f}%" if divergence is not None else "—"
        status = {
            "ok": "✅ agrees", "diverged": "⚠️ diverged",
            "manual": "🔍 manual check", "error": "❔ not fetched",
        }[result.status]
        book_text = _fmt(result.book_value) + ("%" if claim.units == "percent" else "")
        add(f"| {claim.label} | {book_text} | "
            f"{result.book_year or '—'} | `{series_label}` | {_fmt(result.series_value)} | "
            f"{div_text} | {status} |")
    add("")

    manual = [r for r in claims if r.claim.provider == registry.MANUAL]
    if manual:
        add("### Claims needing a manual check")
        add("")
        add("No single machine-readable series carries these. Each names where to look.")
        add("")
        for result in manual:
            claim = result.claim
            location = f"{claim.path}:{result.line}" if result.line else claim.path
            add(f"- **{claim.label}** — book says **{_fmt(result.book_value)}"
                f"{'%' if claim.units == 'percent' else ''}**"
                f"{f' ({result.book_year})' if result.book_year else ''}, at `{location}`.")
            add(f"  Check: {claim.reference}")
            if claim.note:
                add(f"  {claim.note}")
        add("")

    errors = [r for r in claims if r.status == "error" and r.error]
    if errors:
        add("### Series not retrieved")
        add("")
        for result in errors:
            add(f"- `{result.claim.series_id or result.claim.id}` — {result.error}")
        add("")

    # --- 3. Sector tables ----------------------------------------------------
    add("## 3. Sector tables")
    add("")
    for table, rows in tables:
        add(f"### {table.label}")
        add("")
        if table.note:
            add(f"{table.note}")
            add("")
        add("| Row | Book says | Series | Series says | Divergence |")
        add("|-----|----------:|--------|------------:|-----------:|")
        for row in rows:
            if row["value"] is not None and row["book"] is not None:
                scaled = row["book"] * table.book_scale
                divergence = (scaled - row["value"]) / abs(row["value"]) * 100
                div_text = f"{divergence:+.1f}%"
            else:
                div_text = "—"
            series_label = f"`{row['series_id']}`" if row["series_id"] else "_manual_"
            add(f"| {row['label']} | {_fmt(row['book'])}M | {series_label} | "
                f"{_fmt(row['value'])} | {div_text} |")
        add("")

    # --- 4. Vintage audit ----------------------------------------------------
    add("## 4. Vintage audit")
    add("")
    dated = inv.refreshable()
    benchmarks = inv.benchmarks()
    ages = Counter(t.year for t in dated)
    add(f"{len(inv.tables)} tables. {len(dated)} report measured data with a stated reference "
        f"year and could have a newer vintage today. The rest are schematics, author "
        f"compilations, undated tables, or benchmarks on a fixed revision cycle.")
    add("")
    add("| Reference year | Tables | Age at end of " + str(as_of) + " |")
    add("|:--------------:|-------:|:------------------:|")
    for year in sorted(ages, reverse=True):
        add(f"| {year} | {ages[year]} | {as_of - year} yr |")
    add("")

    if benchmarks:
        add(f"**{len(benchmarks)} tables are benchmarks, not measurements.** NAICS, the "
            "Economic Census, the Census of Agriculture and treaty text are revised on a "
            "fixed multi-year cycle, so their reference year is the vintage of the "
            "instrument rather than the age of a number. They are excluded from the "
            "staleness count above: "
            + ", ".join(f"`{t.number}`" for t in sorted(benchmarks, key=_sort_key)) + ".")
        add("")

    stale = [t for t in dated if (as_of - t.year) >= 3]
    if stale:
        add(f"**{len(stale)} tables are three years old or more.** Grouped by source, since a "
            "refresh is done one series at a time:")
        add("")
        grouped: dict[str, list[inventory.Table]] = defaultdict(list)
        for table in stale:
            grouped[table.kind].append(table)
        add("| Source | Tables | Which |")
        add("|--------|-------:|-------|")
        for kind in sorted(grouped, key=lambda k: -len(grouped[k])):
            numbers = ", ".join(t.number for t in sorted(grouped[kind], key=_sort_key))
            add(f"| {kind} | {len(grouped[kind])} | {numbers} |")
        add("")

    # Benchmarks legitimately have no year (treaty text, classification systems).
    undated = [t for t in inv.tables if t.dated and not t.benchmark and t.year is None]
    if undated:
        add(f"**{len(undated)} tables report measured data but state no reference year.** "
            "These cannot be refreshed or trusted without opening each one; giving them a "
            "year in the caption or source line is a prerequisite to the refresh:")
        add("")
        add(", ".join(f"`{t.number}`" for t in sorted(undated, key=_sort_key)))
        add("")

    # --- 5. Worklist ---------------------------------------------------------
    add("## 5. Refresh worklist")
    add("")
    add("Ordered by how much of the book each step unblocks.")
    add("")

    refreshable = inv.refreshable()
    by_kind: dict[str, list[inventory.Table]] = defaultdict(list)
    for table in refreshable:
        by_kind[table.kind].append(table)
    anchor_kinds = ["BEA", "BLS", "Census", "Federal Reserve"]
    anchor_total = sum(len(by_kind.get(k, [])) for k in anchor_kinds)
    snapshot_total = sum(len(by_kind.get(k, [])) for k in SNAPSHOT_KINDS)

    add(f"1. **National accounts anchor ({anchor_total} tables).** BEA, BLS, Census and "
        "Federal Reserve tables define the aggregates every other chapter quotes. Refresh "
        "these together and in one commit so the book is never transiently inconsistent. "
        "Start with Ch 1, Ch 3, Appendix B, and `book/_interactive/data/economic-data.json`.")
    add("")
    add(f"2. **Undated tables ({len(undated)}).** Give each a reference year before "
        "refreshing anything else — an undated table cannot be checked, by this script or "
        "by a reader.")
    add("")
    manual_count = len(manual)
    add(f"3. **Manual claims ({manual_count}).** The CMS health share, the BEA manufacturing "
        "share, the BLS union rate and the CEX housing share have no clean API series. "
        "Section 2 lists where each lives and where to look it up.")
    add("")
    sector_kinds = ["EIA", "CMS", "USDA", "NCES", "OMB", "CBO", "Treasury", "OPM", "DOD", "DOE", "DOT", "FDIC"]
    sector_total = sum(len(by_kind.get(k, [])) for k in sector_kinds)
    add(f"4. **Sector agencies ({sector_total} tables).** EIA, CMS, USDA, NCES and the rest. "
        "Independent of each other, so they can be done in any order or split across sessions.")
    add("")
    add(f"5. **Snapshot tables ({snapshot_total}).** Firm revenues, league tables, association "
        "memberships. Lowest priority: readers expect firm figures to be a point-in-time "
        "snapshot, and they date gracefully as long as the caption states the year.")
    add("")

    add("---")
    add("")
    add("Regenerate with `python3 _dev/refresh_data.py --report`. "
        "Add `--offline` to use only cached responses.")
    return "\n".join(L) + "\n"
