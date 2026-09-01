"""Which claims in the manuscript are checkable against a published series.

Most of the book's 189 tables cannot be reconciled automatically: firm revenues,
association memberships, and schematics have no single machine-readable series
behind them. This registry covers the ones that do — the headline aggregates a
reader is most likely to check, and the sector tables that anchor everything
else.

Each entry locates the book's *current* stated value with a regex rather than
storing it, so the registry does not itself go stale when the manuscript is
edited. ``verify_locators`` fails loudly if a pattern stops matching.

Series IDs are asserted, not guaranteed. A wrong ID produces a fetch failure
that the report names explicitly, so an error surfaces rather than passing
silently as agreement.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import inventory

FRED = "fred"
BLS = "bls"
MANUAL = "manual"


@dataclass
class Claim:
    """A single figure in the prose, checkable against one series."""

    id: str
    label: str
    path: str
    pattern: str
    provider: str
    series_id: str = ""
    book_scale: float = 1.0     # multiply the parsed book value to reach series units
    units: str = ""
    tolerance_pct: float = 1.0
    reference: str = ""
    note: str = ""

    def locate(self, repo: Path) -> tuple[float, int | None, int] | None:
        """Return (book value, stated year, line number), or None if not found."""
        text = (repo / self.path).read_text(encoding="utf-8")
        match = re.search(self.pattern, text)
        if not match:
            return None
        groups = match.groupdict()
        value = float(groups["value"].replace(",", ""))
        year = int(groups["year"]) if groups.get("year") else None
        line = text[: match.start()].count("\n") + 1
        return value, year, line


@dataclass
class TableClaim:
    """A table whose rows each map to a series."""

    id: str
    label: str
    path: str
    table_number: str
    value_column: int              # 0-indexed, counting after the row label
    rows: dict[str, str]           # row label in the book -> series id ("" = manual)
    provider: str = FRED
    book_scale: float = 1.0
    units: str = ""
    tolerance_pct: float = 2.0
    note: str = ""

    def reference_year(self, repo: Path) -> int | None:
        """The year the table's own caption declares, if any.

        The comparison uses this rather than the latest available year, so the
        report answers "is the book right for the year it claims?" before it
        answers "how far has the number moved since?".
        """
        lines = (repo / self.path).read_text(encoding="utf-8").split("\n")
        start = next(
            (i for i, l in enumerate(lines) if l.startswith(f"**Table {self.table_number}:")),
            None,
        )
        if start is None:
            return None
        # The year may sit in the caption or in the source line beneath the table
        # (Table 1.3 says "Employment by Sector" and dates itself in its source).
        source = next(
            (l for l in lines[start:start + 40] if l.strip().lower().startswith("*source")), ""
        )
        return inventory.reference_year(lines[start], source)

    def locate(self, repo: Path) -> list[tuple[str, float, int]] | None:
        """Return [(row label, book value, line number)], or None if not found."""
        lines = (repo / self.path).read_text(encoding="utf-8").split("\n")
        start = next(
            (i for i, l in enumerate(lines) if l.startswith(f"**Table {self.table_number}:")),
            None,
        )
        if start is None:
            return None
        out = []
        for i in range(start, min(start + 40, len(lines))):
            if not lines[i].startswith("|") or re.match(r"^\|[ :|-]+\|\s*$", lines[i]):
                continue
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            label = cells[0].strip("*")
            if label not in self.rows:
                continue
            raw = cells[1 + self.value_column]
            number = re.search(r"[\d,]+\.?\d*", raw)
            if not number:
                continue
            out.append((label, float(number.group(0).replace(",", "")), i + 1))
        return out or None


# --- Headline aggregates -----------------------------------------------------
# book_scale converts the book's unit to the series' unit:
#   trillions -> billions          x1000
#   millions of people -> thousands x1000

CLAIMS: list[Claim] = [
    Claim(
        id="gdp_nominal",
        label="U.S. nominal GDP",
        path="book/part1/ch01-economy-in-numbers.md",
        pattern=r"\*\*Gross Domestic Product \((?P<year>\d{4})\):\*\* \$(?P<value>[\d.]+) trillion",
        provider=FRED, series_id="GDP", book_scale=1000, units="$B", tolerance_pct=1.0,
    ),
    Claim(
        id="gdp_real",
        label="U.S. real GDP (chained 2017 dollars)",
        path="book/part1/ch01-economy-in-numbers.md",
        pattern=r"the same output is approximately \$(?P<value>[\d.]+) trillion",
        provider=FRED, series_id="GDPC1", book_scale=1000, units="$B (2017)", tolerance_pct=1.5,
        note="Book states this as the chained-dollar equivalent of the nominal anchor year.",
    ),
    Claim(
        id="nonfarm_payrolls",
        label="Total nonfarm payroll employment",
        path="book/part1/ch01-economy-in-numbers.md",
        pattern=r"\*\*Employment:\*\* (?P<value>[\d.]+) million nonfarm workers",
        provider=FRED, series_id="PAYEMS", book_scale=1000, units="thousands", tolerance_pct=1.0,
    ),
    Claim(
        id="manufacturing_employment",
        label="Manufacturing employment",
        path="book/part2/ch09-manufacturing.md",
        pattern=r"Manufacturing employed (?P<value>[\d.]+) million workers in (?P<year>\d{4})",
        provider=FRED, series_id="MANEMP", book_scale=1000, units="thousands", tolerance_pct=1.5,
    ),
    Claim(
        id="student_debt",
        label="Outstanding student loan debt",
        path="book/part2/ch15-education.md",
        pattern=r"stands at \$(?P<value>[\d.]+) trillion \((?P<year>\d{4})\)",
        provider=FRED, series_id="SLOAS", book_scale=1_000_000, units="$M", tolerance_pct=2.0,
        note="SLOAS is student loans owned and securitized, outstanding.",
    ),
    Claim(
        id="union_density",
        label="Union membership rate (all wage and salary workers)",
        path="book/part6/ch30-labor.md",
        pattern=r"stands at (?P<value>[\d.]+)%, representing [\d.]+ million workers",
        provider=MANUAL, units="percent", tolerance_pct=0.2,
        reference="https://www.bls.gov/news.release/union2.htm",
        note="BLS publishes this each January; no clean FRED series.",
    ),
    Claim(
        id="health_share_gdp",
        label="National health expenditure as a share of GDP",
        path="book/part2/ch06-healthcare.md",
        pattern=r"rising to \$[\d.]+ trillion and (?P<value>[\d.]+)% of GDP in (?P<year>\d{4})",
        provider=MANUAL, units="percent", tolerance_pct=0.2,
        reference="https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data",
        note="CMS National Health Expenditure Accounts, released each December.",
    ),
    Claim(
        id="manufacturing_va_share",
        label="Manufacturing value added as a share of GDP",
        path="book/part2/ch09-manufacturing.md",
        pattern=r"value added to GDP in (?P<year>\d{4})---(?P<value>[\d.]+)% of the total economy",
        provider=MANUAL, units="percent", tolerance_pct=0.2,
        reference="https://www.bea.gov/data/gdp/gdp-industry",
        note="BEA GDP-by-Industry Table 1. Anchors Ch 1, Ch 9 and Appendix B; check all three together.",
    ),
    Claim(
        id="goods_trade_deficit",
        label="U.S. goods trade deficit",
        path="book/part4/ch21-trade.md",
        pattern=r"\| Trade deficit \| \$(?P<value>[\d.]+) trillion \|",
        provider=FRED, series_id="BOPGTB", book_scale=-1000, units="$B", tolerance_pct=5.0,
        note="BOPGTB is the goods balance and is negative; the book states the deficit as positive.",
    ),
    Claim(
        id="housing_share_consumption",
        label="Housing share of household consumption",
        path="book/part1/ch02-how-it-fits.md",
        pattern=r"\| Housing \| (?P<value>[\d.]+)% \|",
        provider=MANUAL, units="percent", tolerance_pct=0.3,
        reference="https://www.bls.gov/cex/tables.htm",
        note="BLS Consumer Expenditure Survey. The April 2026 audit put this at 32.9%; still stated as 33%.",
    ),
]

# --- Sector tables -----------------------------------------------------------

TABLE_CLAIMS: list[TableClaim] = [
    TableClaim(
        id="employment_by_sector",
        label="Employment by sector (Table 1.3)",
        path="book/part1/ch01-economy-in-numbers.md",
        table_number="1.3",
        value_column=0,
        book_scale=1000,
        units="thousands",
        tolerance_pct=3.0,
        rows={
            "Education & Health Services": "USEHS",
            "Government": "USGOVT",
            "Professional & Business Services": "USPBS",
            "Leisure & Hospitality": "USLAH",
            "Retail Trade": "USTRADE",
            "Manufacturing": "MANEMP",
            "Financial Activities": "USFIRE",
            "Construction": "USCONS",
            "Transportation & Warehousing": "CES4300000001",
            "Wholesale Trade": "USWTRADE",
            "Other Services": "CES8000000001",
            "Information": "USINFO",
            # The book combines mining with utilities; no single series matches.
            "Mining & Utilities": "",
        },
        note="BLS CES supersectors. 'Mining & Utilities' is a book-specific combination.",
    ),
]


@dataclass
class LocatorReport:
    ok: list[str] = field(default_factory=list)
    broken: list[str] = field(default_factory=list)

    @property
    def healthy(self) -> bool:
        return not self.broken


def verify_locators(repo: Path) -> LocatorReport:
    """Confirm every registry pattern still matches the manuscript."""
    report = LocatorReport()
    for claim in CLAIMS:
        (report.ok if claim.locate(repo) else report.broken).append(claim.id)
    for table in TABLE_CLAIMS:
        found = table.locate(repo)
        if not found:
            report.broken.append(table.id)
            continue
        missing = set(table.rows) - {label for label, _, _ in found}
        if missing:
            report.broken.append(f"{table.id} (rows not found: {', '.join(sorted(missing))})")
        else:
            report.ok.append(table.id)
    return report
