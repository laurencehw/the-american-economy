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

---

## Tier 1: The Data Refresh (8.9 → 9.2)

**This is the whole priority.** The manuscript is anchored to 2023 national accounts
and it is late 2026. The vintage policy adopted this session makes that honest but
does not make it current, and a living textbook cannot stay three years behind its
own sources.

### 1. Build `_dev/refresh_data.py` (do this first)

Every table in the book now names its own source series and reference year. That makes
the refresh enumerable rather than a manual audit — which was much of the point of the
table work. Build the script before doing any manual updating.

The script should:

1. Parse `book/**/*.md` for `**Table N.M: ...**` captions and the `*Source: ...*` line
   beneath each, producing an inventory of (table, series, stated year).
2. Pull the corresponding series from the BEA, BLS, and FRED APIs for the tables backed
   by government data (roughly 110 of the 189; the rest are firm-level or schematic).
3. Emit a reconciliation report: for each table, what the book says vs. what the series
   now says, flagged by magnitude of divergence.
4. Leave the editing to a human — the goal is a reviewable diff, not automated prose
   rewriting.

Estimated effort: one session. Payoff: converts the annual currency problem from a
crisis into a chore.

### 2. Roll the national accounts anchor

Once the reconciliation report exists, move the book's anchor year from 2023 to the
most recent fully revised year. Order of operations:

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

### 3. In-text attribution for contested claims

Appendix E is a good bibliography, but the text rarely points to it. Attach a source to
the 50–80 claims that are research-derived or contested rather than definitional — the
China shock employment estimates, Chetty's mobility work, Lazard's LCOE series, the
concentration ratios. This does not mean converting the book to author-date citation
throughout; it means a reader who wants to check the strongest claims can.

Start with the chapters making the strongest empirical claims: Ch 9 (China shock), the
Interlude (mobility, top income shares), Ch 14 (LCOE, transition costs), Ch 30
(monopsony, immigration wage effects).

### 4. Hedging pass

"Roughly" appears 302 times, 61 in Ch 14 alone. Replace it with the precise figure
wherever an official series exists; keep it where the estimate is genuinely approximate
(pipeline mileage, informal economy size). A book that teaches data literacy should use
its hedges to signal real uncertainty, not as filler.

---

## Tier 3: Remaining Coverage (9.4 → 9.5)

### 5. Arts, entertainment, and recreation
Fold into an expanded Ch 17 rather than adding a standalone chapter. Hollywood, music,
professional sports, and gaming are economically significant and analytically
interesting — winner-take-all dynamics and extreme geographic concentration in
LA/Nashville/NYC. The glossary already defines winner-take-all markets.

### 6. Early childhood education and care
Ch 15 runs K-12 through graduate school and barely mentions pre-K. The economics —
market failure, subsidy structure, wage suppression in care work — connect directly to
Ch 30's childcare and labor force participation section, which already gestures at it.

### 7. Ch 11 platform economics
The thinnest analytical treatment among the large sector chapters relative to the
sector's importance. Two-sided market pricing, the attention economy's measurement
problems, and the antitrust theories actually being litigated.

### 8. Appendix C depth
NAICS coverage is uneven: manufacturing gets 17 subsectors, healthcare 4. Add 4-digit
codes for finance, professional services, and information, and add guidance on
classifying platform companies — the question a student is most likely to actually
have.

---

## Recommended Order for the Next Session

1. Build `refresh_data.py` and generate the first reconciliation report.
2. Read the report and fix whatever it flags as materially wrong — that is a data
   audit, and it takes precedence over the anchor roll.
3. Roll the anchor for Ch 1 / Ch 3 / Appendix B / interactive JSON in one commit.
4. If time remains, start the in-text attribution pass on Ch 9 and the Interlude.
