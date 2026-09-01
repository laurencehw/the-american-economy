# Next Session Plan: Moving from 8.9 to 9.5

_Updated September 2026. Aligned with `REVIEW.md` (10-point scale)._

---

## Completed

### Earlier sessions
- ✅ Chapters 16 (Agriculture) and 17 (Leisure and Hospitality) added
- ✅ Interlude on distribution and inequality added
- ✅ Three-tier exercises in all 33 chapters
- ✅ Key Takeaways in all 33 chapters
- ✅ All 118 figures generated; CI figure checker passes
- ✅ Ch 3 "five states = half of GDP" error corrected (now 41%, internally consistent)
- ✅ Ch 14 rebuilt: generation mix, LCOE, utilities and broadband, carbon pricing,
  environmental economics, workforce transition
- ✅ Ch 15 student debt and K-12 outcomes; Ch 16 externalities; Ch 30 monopsony,
  immigration, childcare and labor force participation
- ✅ Appendix A publication calendar; Appendix E consolidated references
- ✅ CI: figure reference checker, markdown link checker

### This session
- ✅ All 189 tables numbered (`Table N.M`) and sourced; illustrative tables labelled
  as such rather than given a spurious citation
- ✅ `check_tables.py` added to CI — enforces caption, source, uniqueness, sequence,
  and correct chapter/appendix prefix
- ✅ Connections section in all 33 chapters; internal links 89 → 280, all resolving
- ✅ Four cross-chapter numerical contradictions reconciled (manufacturing share, CES
  sample size, healthcare GDP share, total GDP)
- ✅ Ch 28 "Does Regulatory Fragmentation Work?" analysis added; perishable
  officeholder facts replaced with durable institutional structure
- ✅ Glossary re-sorted and extended to 139 terms
- ✅ `how-to-use.md` conventions corrected; explicit data-vintage policy adopted
- ✅ Interactive visualizations stamped with data vintage
- ✅ `.github/ISSUE_TEMPLATE/` added (the README had promised it)
- ✅ `_dev/refresh_data.py` built: table inventory, claim registry, FRED/BLS fetchers,
  reconciliation report, 16 tests, CI registry check
- ✅ Fixed a false positive in the table source check — the substring `author` matched
  "Port Authorities", exempting ten tables that had no source line

---

## Tier 1: The Data Refresh (8.9 → 9.2)

**This is the whole priority.** The manuscript is anchored to 2023 national accounts
and it is late 2026. The vintage policy adopted this session makes that honest but
does not make it current, and a living textbook cannot stay three years behind its
own sources.

### 1. ✅ `_dev/refresh_data.py` is built

Done. See `_dev/README.md` for usage. `--check` runs in CI on every push touching
`book/`, so the registry cannot silently drift from the manuscript.

**Run it with network access first.** It was written in an environment that blocks
egress to fred.stlouisfed.org, api.bls.gov and apps.bea.gov, so the comparison columns
in the current `RECONCILIATION.md` are empty:

```bash
python3 _dev/refresh_data.py --report
```

That populates the headline-claim and sector-table comparisons. The vintage audit and
worklist in the report are already complete — they come from the manuscript, not the
network.

**Expect some series IDs to be wrong.** They are asserted from memory, not verified
against FRED. A wrong ID produces a named fetch failure in the report's "Series not
retrieved" section rather than passing silently as agreement, so the first online run
doubles as a validation pass on the registry. Fix any failures in
`_dev/refresh/registry.py` and re-run.

### 2. Give the 24 undated tables a reference year

`RECONCILIATION.md` §4 names them. A table that states no year cannot be checked by
this tool or trusted by a reader, and it blocks everything downstream. Mostly Ch 19–20
(capital markets and corporate finance) and the Ch 7–14 association tables. Cheap work:
open each, establish what year the figures are, and put it in the caption.

### 3. Roll the national accounts anchor

Move the book's anchor year from 2023 to the most recent fully revised year. The report
counts 56 tables in the anchor group and 75 tables three years old or more. Order of
operations:

1. **Ch 1, Ch 3, Appendix B** and `book/_interactive/data/economic-data.json` — these
   define the aggregates every other chapter references. Do them together and in one
   commit so nothing is transiently inconsistent.
2. **Each chapter's Overview section** — GDP contribution and employment, which are the
   figures most often quoted back at the book.
3. **Fast-moving series**: energy generation mix and LCOE (Ch 14), trade flows
   (Ch 21-22), housing prices (Ch 5, 23-27), union density (Ch 30).
4. **Firm-level tables** — revenues, market caps, AUM, headcount. Roughly 60 tables.
   Lowest priority of the four; these date gracefully because readers expect firm
   figures to be a snapshot.

Re-run `check_tables.py` after each stage; update each caption's stated year as you go.

---

## Tier 2: Attribution and Precision (9.2 → 9.4)

### 4. In-text attribution for contested claims

Appendix E is a good bibliography, but the text rarely points to it. Attach a source to
the 50–80 claims that are research-derived or contested rather than definitional — the
China shock employment estimates, Chetty's mobility work, Lazard's LCOE series, the
concentration ratios. This does not mean converting the book to author-date citation
throughout; it means a reader who wants to check the strongest claims can.

Start with the chapters making the strongest empirical claims: Ch 9 (China shock), the
Interlude (mobility, top income shares), Ch 14 (LCOE, transition costs), Ch 30
(monopsony, immigration wage effects).

### 5. Hedging pass

"Roughly" appears 302 times, 61 in Ch 14 alone. Replace it with the precise figure
wherever an official series exists; keep it where the estimate is genuinely approximate
(pipeline mileage, informal economy size). A book that teaches data literacy should use
its hedges to signal real uncertainty, not as filler.

---

## Tier 3: Remaining Coverage (9.4 → 9.5)

### 6. Arts, entertainment, and recreation
Fold into an expanded Ch 17 rather than adding a standalone chapter. Hollywood, music,
professional sports, and gaming are economically significant and analytically
interesting — winner-take-all dynamics and extreme geographic concentration in
LA/Nashville/NYC. The glossary already defines winner-take-all markets.

### 7. Early childhood education and care
Ch 15 runs K-12 through graduate school and barely mentions pre-K. The economics —
market failure, subsidy structure, wage suppression in care work — connect directly to
Ch 30's childcare and labor force participation section, which already gestures at it.

### 8. Ch 11 platform economics
The thinnest analytical treatment among the large sector chapters relative to the
sector's importance. Two-sided market pricing, the attention economy's measurement
problems, and the antitrust theories actually being litigated.

### 9. Appendix C depth
NAICS coverage is uneven: manufacturing gets 17 subsectors, healthcare 4. Add 4-digit
codes for finance, professional services, and information, and add guidance on
classifying platform companies — the question a student is most likely to actually
have.

---

## Recommended Order for the Next Session

1. Run `python3 _dev/refresh_data.py --report` somewhere with network access. Fix any
   series IDs that fail to fetch, and re-run until the registry is clean.
2. Act on whatever the report flags as materially diverged — that is the data audit,
   and it takes precedence over the anchor roll.
3. Check the four manual claims (report §2): CMS health share, BEA manufacturing share,
   BLS union rate, CEX housing share. The last is already known to be wrong — the book
   says 33%, the April 2026 audit put it at 32.9%.
4. Give the 24 undated tables a reference year.
5. Roll the anchor for Ch 1 / Ch 3 / Appendix B / interactive JSON in one commit.
