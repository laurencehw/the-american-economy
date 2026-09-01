# `_dev/` — working files

Not part of the published book. GitBook builds from `book/` only.

| Path | What it is |
|------|------------|
| `REVIEW.md` | Standing manuscript review and score |
| `NEXT_SESSION_PLAN.md` | Prioritized work queue |
| `RECONCILIATION.md` | Generated. Where the book's numbers stand against their sources |
| `table_inventory.csv` | Generated. All 189 tables with source, kind, and reference year |
| `refresh_data.py` | The reconciliation tool (below) |
| `refresh/` | Its modules |
| `tests/` | Tests for the above |
| `build_pdf.py` | PDF build |

---

## `refresh_data.py`

The book states a reference year for every table and names its source beneath
it. That makes the annual data refresh *enumerable*: this tool reads those
declarations, fetches the series that can be fetched, and reports where the book
and its sources disagree.

**It never edits the manuscript.** The output is a diff for you to act on.

### Usage

```bash
python3 _dev/refresh_data.py --report              # fetch and write RECONCILIATION.md
python3 _dev/refresh_data.py --report --offline    # cached responses only
python3 _dev/refresh_data.py --report --refresh    # ignore the cache, re-fetch
python3 _dev/refresh_data.py --check               # verify registry locators (runs in CI)
python3 _dev/refresh_data.py --inventory --out _dev/table_inventory.csv
```

`--as-of 2027` measures table staleness against a year other than the current one.

### Credentials

Neither provider needs a key at this volume. Keys raise the limits and are read
from the environment if present:

```bash
export FRED_API_KEY=...   # https://fredaccount.stlouisfed.org/apikeys
export BLS_API_KEY=...    # https://data.bls.gov/registrationEngine/
```

Without `FRED_API_KEY` the tool uses FRED's public CSV endpoint, which needs no
key. Without `BLS_API_KEY` it uses the BLS v1 API, capped at 25 queries a day.

Responses are cached under `_dev/.cache/` (gitignored) for a day, so you can
regenerate the report without re-fetching.

### What it can and cannot check

Most of the book's 189 tables have no single machine-readable series behind
them — firm revenues, association memberships, league tables, schematics. The
tool is honest about this rather than guessing:

- **Fetched and compared** — headline aggregates and sector tables with a FRED
  or BLS series (GDP, payrolls, manufacturing employment, student debt, the
  employment-by-sector table).
- **Flagged for manual check** — figures with no clean API series (CMS health
  share, BEA manufacturing share, BLS union rate, CEX housing share). The report
  gives the exact file, line, and lookup URL for each.
- **Vintage audit only** — everything else. The report groups tables by source
  and reference year so a refresh can be worked one agency at a time.

Series IDs are asserted, not guaranteed. A wrong ID produces a fetch failure the
report names explicitly, so an error surfaces rather than passing silently as
agreement.

### The registry

`refresh/registry.py` maps book claims to series. Each entry finds the book's
*current* value with a regex rather than storing a copy, so the registry does not
go stale when the manuscript is edited — but it does break if the wording
changes. `--check` catches that, and CI runs it on every push that touches
`book/`.

To add a claim: append a `Claim` to `CLAIMS` with a pattern containing a named
`value` group (and `year` where the book states one), set `book_scale` to convert
the book's units to the series' units, and run `--check`.

### Tests

```bash
python3 -m unittest discover -s _dev/tests -v
```

The fetchers cannot be exercised against live APIs in CI, so the tests seed the
on-disk cache with known series and check the comparison arithmetic, unit
scaling, and staleness logic against it.
