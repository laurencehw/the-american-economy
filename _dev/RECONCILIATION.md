# Data Reconciliation Report

Generated 2026-09-01 by `_dev/refresh_data.py`. Mode: **offline**.

> **Series values were not retrieved.** This environment blocks outbound
> connections to fred.stlouisfed.org, api.bls.gov and apps.bea.gov, so the
> comparison columns below are empty. Run this script somewhere with network
> access to populate them. Everything else in this report — the vintage audit,
> the worklist, and the book's own stated values — is derived from the
> manuscript and is complete.

## 1. Registry health

All 11 registry locators still match the manuscript.

All 189 tables parsed cleanly: caption, source line, and reference year.

## 2. Headline claims

What the book says, against the series its source line names. `book_scale` in the registry converts the book's units to the series' units before comparing.

The **Divergence** column compares the book against the series *for the year the book claims*, so it answers whether the figure was right as stated. The **Latest** column is the newest complete year, and is what a refresh would move the figure to.

| Claim | Book says | Year | Series | Series (same yr) | Divergence | Latest | Status |
|-------|----------:|:----:|--------|-----------------:|-----------:|-------:|--------|
| U.S. nominal GDP | 27.8 | 2023 | `GDP` | — | — | — | ❔ not fetched |
| U.S. real GDP (chained 2017 dollars) | 22.4 | — | `GDPC1` | — | — | — | ❔ not fetched |
| Total nonfarm payroll employment | 157 | — | `PAYEMS` | — | — | — | ❔ not fetched |
| Manufacturing employment | 12.9 | 2023 | `MANEMP` | — | — | — | ❔ not fetched |
| Outstanding student loan debt | 1.77 | 2024 | `SLOAS` | — | — | — | ❔ not fetched |
| Union membership rate (all wage and salary workers) | 9.9% | — | `_manual_` | — | — | — | 🔍 manual check |
| National health expenditure as a share of GDP | 17.6% | 2023 | `_manual_` | — | — | — | 🔍 manual check |
| Manufacturing value added as a share of GDP | 10.1% | 2023 | `_manual_` | — | — | — | 🔍 manual check |
| U.S. goods trade deficit | 1.2 | — | `BOPGTB` | — | — | — | ❔ not fetched |
| Housing share of household consumption | 33% | — | `_manual_` | — | — | — | 🔍 manual check |

### Claims needing a manual check

No single machine-readable series carries these. Each names where to look.

- **Union membership rate (all wage and salary workers)** — book says **9.9%**, at `book/part6/ch30-labor.md:7`.
  Check: https://www.bls.gov/news.release/union2.htm
  BLS publishes this each January; no clean FRED series.
- **National health expenditure as a share of GDP** — book says **17.6%** (2023), at `book/part2/ch06-healthcare.md:5`.
  Check: https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data
  CMS National Health Expenditure Accounts, released each December.
- **Manufacturing value added as a share of GDP** — book says **10.1%** (2023), at `book/part2/ch09-manufacturing.md:13`.
  Check: https://www.bea.gov/data/gdp/gdp-industry
  BEA GDP-by-Industry Table 1. Anchors Ch 1, Ch 9 and Appendix B; check all three together.
- **Housing share of household consumption** — book says **33%**, at `book/part1/ch02-how-it-fits.md:271`.
  Check: https://www.bls.gov/cex/tables.htm
  BLS Consumer Expenditure Survey. The April 2026 audit put this at 32.9%; still stated as 33%.

### Series not retrieved

- `GDP` — offline and no cached copy of fred:GDP
- `GDPC1` — offline and no cached copy of fred:GDPC1
- `PAYEMS` — offline and no cached copy of fred:PAYEMS
- `MANEMP` — offline and no cached copy of fred:MANEMP
- `SLOAS` — offline and no cached copy of fred:SLOAS
- `BOPGTB` — offline and no cached copy of fred:BOPGTB

## 3. Sector tables

### Employment by sector (Table 1.3)

BLS CES supersectors. 'Mining & Utilities' is a book-specific combination.

Compared against **2023**, the year this table declares. The Latest column shows where a refresh would move each row.

| Row | Book says | Series (same yr) | Divergence | Latest |
|-----|----------:|-----------------:|-----------:|-------:|
| Education & Health Services (`USEHS`) | 25.9M | — | — | — |
| Government (`USGOVT`) | 23.1M | — | — | — |
| Professional & Business Services (`USPBS`) | 22.6M | — | — | — |
| Leisure & Hospitality (`USLAH`) | 16.7M | — | — | — |
| Retail Trade (`USTRADE`) | 15.6M | — | — | — |
| Manufacturing (`MANEMP`) | 12.9M | — | — | — |
| Financial Activities (`USFIRE`) | 9.2M | — | — | — |
| Construction (`USCONS`) | 8.1M | — | — | — |
| Transportation & Warehousing (`CES4300000001`) | 6.6M | — | — | — |
| Wholesale Trade (`USWTRADE`) | 6.1M | — | — | — |
| Other Services (`CES8000000001`) | 5.9M | — | — | — |
| Information (`USINFO`) | 3M | — | — | — |
| Mining & Utilities (_manual_) | 1.2M | — | — | — |

## 4. Vintage audit

189 tables. 141 report measured data with a stated reference year and could have a newer vintage today. The rest are schematics, author compilations, undated tables, or benchmarks on a fixed revision cycle.

| Reference year | Tables | Age at end of 2026 |
|:--------------:|-------:|:------------------:|
| 2025 | 1 | 1 yr |
| 2024 | 65 | 2 yr |
| 2023 | 67 | 3 yr |
| 2022 | 6 | 4 yr |
| 2021 | 1 | 5 yr |
| 2018 | 1 | 8 yr |

**9 tables are benchmarks, not measurements.** NAICS, the Economic Census, the Census of Agriculture and treaty text are revised on a fixed multi-year cycle, so their reference year is the vintage of the instrument rather than the age of a number. They are excluded from the staleness count above: `16.3`, `22.4`, `C.1`, `C.2`, `C.3`, `C.4`, `C.5`, `C.6`, `C.7`.

**75 tables are three years old or more.** Grouped by source, since a refresh is done one series at a time:

| Source | Tables | Which |
|--------|-------:|-------|
| company filings | 14 | 6.2, 7.3, 7.4, 7.5, 8.3, 8.6, 9.1, 12.1, 14.8, 16.4, 16.5, 16.6, 17.2, 17.3 |
| BLS | 11 | 1.3, 2.3, 4.7, 4.8, 6.3, 7.1, 8.11, 16.7, 17.1, 17.4, 19.12 |
| BEA | 9 | 1.2, 3.1, 3.2, 8.9, 8.10, B.1, B.2, B.3, B.4 |
| industry body | 9 | 6.4, 7.2, 8.4, 8.5, 12.2, 12.4, 19.1, 19.2, 19.8 |
| NCES | 7 | 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7 |
| Census | 6 | 1.4, 4.2, 4.4, 4.11, 21.2, I.1 |
| Federal Reserve | 4 | 20.1, 20.15, I.2, I.3 |
| OMB | 2 | 4.1, 4.12 |
| USASpending | 2 | 4.9, 4.10 |
| EIA | 2 | 14.2, 14.4 |
| OECD | 2 | 15.9, 30.3 |
| USDA | 2 | 16.1, 16.2 |
| IMF | 1 | 1.1 |
| OPM | 1 | 4.5 |
| DOD | 1 | 4.6 |
| CMS | 1 | 6.1 |
| CBO | 1 | 16.8 |

**23 tables report measured data but state no reference year.** These cannot be refreshed or trusted without opening each one; giving them a year in the caption or source line is a prerequisite to the refresh:

`7.6`, `7.7`, `7.8`, `8.12`, `10.2`, `12.5`, `13.4`, `14.11`, `18.15`, `19.3`, `19.4`, `19.5`, `19.6`, `19.11`, `20.3`, `20.4`, `20.6`, `20.13`, `20.14`, `20.18`, `22.6`, `22.8`, `A.1`

## 5. Refresh worklist

Ordered by how much of the book each step unblocks.

1. **National accounts anchor (56 tables).** BEA, BLS, Census and Federal Reserve tables define the aggregates every other chapter quotes. Refresh these together and in one commit so the book is never transiently inconsistent. Start with Ch 1, Ch 3, Appendix B, and `book/_interactive/data/economic-data.json`.

2. **Undated tables (23).** Give each a reference year before refreshing anything else — an undated table cannot be checked, by this script or by a reader.

3. **Manual claims (4).** The CMS health share, the BEA manufacturing share, the BLS union rate and the CEX housing share have no clean API series. Section 2 lists where each lives and where to look it up.

4. **Sector agencies (25 tables).** EIA, CMS, USDA, NCES and the rest. Independent of each other, so they can be done in any order or split across sessions.

5. **Snapshot tables (50).** Firm revenues, league tables, association memberships. Lowest priority: readers expect firm figures to be a point-in-time snapshot, and they date gracefully as long as the caption states the year.

---

Regenerate with `python3 _dev/refresh_data.py --report`. Add `--offline` to use only cached responses.
