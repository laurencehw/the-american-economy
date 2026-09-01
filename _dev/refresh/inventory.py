"""Read the manuscript's tables and figures into structured records.

Every table in book/ carries a caption of the form ``**Table N.M: Title**`` and
a ``*Source: ...*`` line beneath it (enforced by .github/scripts/check_tables.py).
This module turns those declarations into records the reconciliation can work
from, and infers each table's reference year and originating agency.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

CAPTION = re.compile(r"^\*\*Table ([0-9A-Z]+)\.(\d+):\s*(.+?)\*\*\s*$")
SEPARATOR = re.compile(r"^\|[ :|-]+\|\s*$")
SOURCE_LINE = re.compile(
    r"^\*(?:Source|Sources|Note):\s*(.+?)\*\s*$"
    r"|^\*((?:Illustrative|Author's (?:schematic|summary|compilation|synthesis))\b.*?)\*\s*$",
    re.IGNORECASE,
)
YEAR = re.compile(r"(?:FY\s*)?(19|20)\d{2}")

# Ordered: the first pattern that matches a source line wins, so put the
# specific agencies before the generic fallbacks.
AGENCIES: list[tuple[str, re.Pattern[str]]] = [
    ("schematic", re.compile(r"(?i)author's schematic|illustrative|author's summary")),
    ("author", re.compile(r"(?i)author's (compilation|synthesis)")),
    ("BEA", re.compile(r"(?i)\bBEA\b|Bureau of Economic Analysis")),
    ("BLS", re.compile(r"(?i)\bBLS\b|Bureau of Labor Statistics|Occupational Employment|QCEW")),
    ("Census", re.compile(r"(?i)Census Bureau|USA Trade Online|NAICS")),
    ("Federal Reserve", re.compile(r"(?i)Federal Reserve|Financial Accounts|Fedwire|Regulation Q")),
    ("EIA", re.compile(r"(?i)\bEIA\b|Energy Information Administration")),
    ("CMS", re.compile(r"(?i)\bCMS\b|Centers for Medicare")),
    ("USDA", re.compile(r"(?i)\bUSDA\b|Agricultural Statistics|Economic Research Service")),
    ("Treasury", re.compile(r"(?i)TreasuryDirect|Department of the Treasury")),
    ("OPM", re.compile(r"(?i)Office of Personnel Management|FedScope")),
    ("DOD", re.compile(r"(?i)Department of Defense|Defense Manpower")),
    ("DOE", re.compile(r"(?i)Department of Energy")),
    ("USASpending", re.compile(r"(?i)USASpending")),
    ("OECD", re.compile(r"(?i)\bOECD\b|Programme for International Student")),
    ("World Bank", re.compile(r"(?i)World Bank")),
    ("company filings", re.compile(r"(?i)10-K|annual report|company (reports|disclosures|filings|announcements)|proxy statement|Form 990|firm annual review")),
    ("industry body", re.compile(r"(?i)association|league table|PitchBook|Nacha|Clearing House|AM Best|NAIC|Drewry|Fortune 500|PEI 300|Bain")),
    ("academic", re.compile(r"(?i)Journal of|Gorton|Metrick")),
    ("NCES", re.compile(r"(?i)National Center for Education Statistics|Digest of Education")),
    ("OMB", re.compile(r"(?i)Office of Management and Budget")),
    ("CBO", re.compile(r"(?i)Congressional Budget Office")),
    ("DOT", re.compile(r"(?i)Department of Transportation|T-100")),
    ("FDIC", re.compile(r"(?i)\bFDIC\b")),
    ("IMF", re.compile(r"(?i)\bIMF\b|World Economic Outlook")),
    ("IEA", re.compile(r"(?i)International Energy Agency")),
    ("FDA", re.compile(r"(?i)\bFDA\b")),
    ("statute", re.compile(r"(?i)USMCA Agreement|authorizing statutes")),
    ("industry body", re.compile(
        r"(?i)Engineering News-Record|World Federation of Exchanges|SIFMA|Preqin"
        r"|Renaissance Capital|S&P Dow Jones|Treasury Bulletin|OpenSecrets"
        r"|Economic Policy Institute|American Lawyer|Am Law")),
]

# Sources whose figures are a point-in-time snapshot readers do not expect to be
# current, or which have no reference year at all. Excluded from staleness scoring.
UNDATED_KINDS = {"schematic", "author", "academic"}


@dataclass
class Table:
    """One table in the manuscript."""

    number: str           # "14.3"
    chapter: str          # "14"
    title: str
    path: Path
    caption_line: int     # 1-indexed
    source_text: str
    rows: int
    kind: str             # inferred originating agency, or "schematic"/"unknown"
    year: int | None      # reference year declared in caption or source line

    @property
    def dated(self) -> bool:
        return self.kind not in UNDATED_KINDS

    def age(self, as_of: int) -> int | None:
        if self.year is None or not self.dated:
            return None
        return as_of - self.year


@dataclass
class Inventory:
    tables: list[Table] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)

    def dated(self) -> list[Table]:
        return [t for t in self.tables if t.dated and t.year is not None]

    def by_kind(self) -> dict[str, list[Table]]:
        out: dict[str, list[Table]] = {}
        for t in self.tables:
            out.setdefault(t.kind, []).append(t)
        return out


def _classify(source_text: str) -> str:
    for name, pattern in AGENCIES:
        if pattern.search(source_text):
            return name
    return "unknown"


def _reference_year(caption_title: str, source_text: str) -> int | None:
    """Latest year mentioned in the caption, else in the source line.

    The caption wins because a caption year names the data's period, whereas a
    source line may also carry a publication or retrieval year.
    """
    for text in (caption_title, source_text):
        years = [int(m.group(0)[-4:]) for m in YEAR.finditer(text)]
        if years:
            return max(years)
    return None


def _iter_tables(lines: list[str]):
    """Yield (separator_index, end_index) for each Markdown table."""
    i = 0
    while i < len(lines):
        if SEPARATOR.match(lines[i]) and i > 0 and lines[i - 1].startswith("|"):
            j = i + 1
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            yield i, j
            i = j
        else:
            i += 1


def scan(book_dir: Path) -> Inventory:
    """Read every table in the manuscript."""
    inv = Inventory()
    for path in sorted(book_dir.rglob("*.md")):
        if path.name == "SUMMARY.md":
            continue
        lines = path.read_text(encoding="utf-8").split("\n")
        for sep, end in _iter_tables(lines):
            k = sep - 2
            while k >= 0 and not lines[k].strip():
                k -= 1
            caption = lines[k] if k >= 0 else ""
            match = CAPTION.match(caption)
            if not match:
                inv.problems.append(f"{path}:{sep + 1} table has no numbered caption")
                continue

            source_text = ""
            for line in lines[end:end + 4]:
                found = SOURCE_LINE.match(line.strip())
                if found:
                    source_text = found.group(1) or found.group(2)
                    break
            if not source_text:
                inv.problems.append(f"{path}:{end} table has no source line")

            chapter, index, title = match.group(1), match.group(2), match.group(3)
            kind = _classify(source_text)
            inv.tables.append(
                Table(
                    number=f"{chapter}.{index}",
                    chapter=chapter,
                    title=title,
                    path=path,
                    caption_line=k + 1,
                    source_text=source_text,
                    rows=end - sep - 1,
                    kind=kind,
                    year=_reference_year(title, source_text),
                )
            )
    return inv
