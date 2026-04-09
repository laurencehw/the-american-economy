# Next Session Plan: Moving from 8.2 to 9.5

_Updated April 2026. Prior session plan used a 4/5 scale — now aligned with REVIEW.md (10-point scale)._
_Last major content commits: March 12, 2026 (PR #12)._

---

## What Has Been Completed

All Tier 1 items from the previous session plan are done:
- ✅ Chapter 16: Agriculture and Food Production (added)
- ✅ Chapter 17: Leisure and Hospitality (added)
- ✅ Interlude: Who Benefits — Distribution and Inequality (added)
- ✅ End-of-chapter exercises across all chapters
- ✅ Cross-references and hint boxes added throughout (PR #12)
- ✅ Labor chapter expanded and renamed (Ch30)
- ✅ Data consistency pass (partial — Ch3 "five states" error corrected)
- ✅ CHIPS Act positive shock case study added (Ch2)
- ✅ International comparison table added (Ch31)
- ✅ CI: Figure reference checker + markdown link checker (PR #13)

---

## Tier 1: High-Impact Changes (Target: 8.2 → 8.8)

### 1. Fix 50 Missing Figures (Priority: Critical)

Every chapter after Ch15 — including the two new chapters (16–17), the Inequality Interlude, all of Part III (Finance), Part IV (Trade), Part V (Regional), Part VI (Governance), and Part VII (Conclusion) — references PNG figures that do not exist in the repo. The CI checker (PR #13) will flag these on every future push.

**Affected chapters**: ch11 (3 figs), ch16 (4), ch17 (5), ch18 (2), ch19 (2), ch20 (2), ch21 (2), ch22 (4), ch23 (2), ch24 (2), ch25 (2), ch26 (2), ch27 (3), ch28 (2), ch29 (1), ch30 (2), ch31 (3), ch32 (2), interlude (5)

**Options:**
- Generate placeholder figures programmatically using Python/matplotlib with correct data (preferred — adds real value)
- Replace `<figure>` blocks with descriptive text tables as fallbacks until figures are created
- Estimated effort: 2-3 sessions for full figure generation

### 2. Data Audit Corrections (Priority: High)

A systematic data audit (April 2026) against BEA, BLS, EIA, and CMS found the following issues:

| Statistic | Book Says | Actual | Fix |
|-----------|-----------|--------|-----|
| Manufacturing GDP share (Ch1, Ch9) | 11% | 10.4% nominal / 10.2% real (2023 BEA) | Change to "about 10%" or "10-11%" with source note |
| Coal share of electricity (Ch14) | 16% | ~15% (EIA 2024, Ember) | Update to 15% |
| Solar share of electricity (Ch14) | 6% | ~7% (utility + distributed, EIA 2024) | Update to 7% |
| Ch31 GDP figure | ">$29 trillion" | $29.2T nominal 2024 (BEA) | Already directionally correct; add precise figure |
| Housing % of consumer spending (Ch2) | 33% | 32.9% (BLS CEX 2023) | Essentially correct; remove "roughly" |
| Student debt (Ch15) | $1.77T (2024) | $1.78T (2024, Fed) | Correct |
| Healthcare % of GDP (Ch6) | "nearly 17%" / "nearly 18%" | 17.6% (2023 CMS), 18.0% (2024 CMS) | Clarify which year; 2024 figure is now 18.0% exactly |

**Also fix**: "roughly" appears 221 times across all chapters. Ch14 alone has 48 instances. Target: replace with precise figures wherever official data exists. Reserve "roughly" only for genuinely approximate estimates.

### 3. Analytical Depth Improvements (Priority: High)

Several chapters identified in the REVIEW.md still need the "why" analysis:

- **Ch14 Energy**: Add a multiplier comparison table explaining why energy has high I-O multipliers (~2.5) vs. finance (~1.2). Currently the chapter describes generation but doesn't explain the economic structure behind energy's systemic importance.
- **Ch28 Federal Governance**: Still reads as a reference document. Add a 500-word "Does Regulatory Fragmentation Work?" section evaluating whether overlapping jurisdiction enables or prevents regulatory arbitrage.
- **Ch16 Agriculture**: Environmental externalities section is thin. Add a paragraph quantifying the Gulf dead zone costs and the economic case for externality pricing.
- **Inequality Interlude**: Distinguish wage inequality from capital income inequality more clearly. The top 1% income composition (60% capital income) is missing.

---

## Tier 2: Important Polish (Target: 8.8 → 9.2)

### 4. Cross-Cutting Theme Integration

Four themes need systematic integration via callout boxes in each sector chapter:
- **Inequality**: Connect wage levels to Interlude's framework
- **Demographics/aging**: Add to Ch6 (healthcare demand), Ch30 (labor supply), Ch31 (Social Security)
- **Climate**: Consistent treatment across agriculture, transportation, energy
- **AI/automation**: Extend Ch11's tech analysis to labor effects in Ch30 and productivity in Ch31

Estimated effort: 1 session (add 4 callout boxes per chapter systematically).

### 5. "See Also" Cross-References

A scan of all chapters shows cross-references are still sparse outside the chapters updated in PR #12. Target: 5-10 cross-references per chapter. A single pass adding `> **See also**: [Chapter X](link)` callouts would significantly improve navigability.

### 6. Utilities and Broadband Section (Ch14)

Ch14 already has a utilities and broadband section (added in a prior session). Verify it is complete and properly cross-referenced.

### 7. Interactive Tool Data Timestamps

The `_interactive/data/economic-data.json` file is static. Add a visible "Data as of Q4 2023" note to each interactive visualization so readers know the reference period. The data explorer and regional map are the most important.

---

## Tier 3: Nice-to-Haves (Target: 9.2 → 9.5)

### 8. Arts, Entertainment, and Recreation

Could be folded into an expanded hospitality chapter (Ch17) or a short standalone. Hollywood, music industry, professional sports, and gaming are economically distinctive and analytically interesting (winner-take-all dynamics, geographic concentration in LA/Nashville/NYC).

### 9. Early Childhood Education

The education chapter (Ch15) covers K-12 through graduate education but barely mentions pre-K. The economics of childcare (market failure, subsidy structure, wage suppression in care work) are directly relevant to the labor chapter (Ch30) discussion of female labor force participation.

### 10. Improve Figure Alt Text

Audit all `<figure>` tags across all chapters for descriptive alt text. Replace generic alt text with text that conveys the figure's key insight. Accessibility and screen-reader usability.

### 11. Issue Templates

Add `.github/ISSUE_TEMPLATE/` with:
- `error-report.md` — for factual errors/outdated statistics
- `content-suggestion.md` — for coverage gaps or new chapter ideas

The README already promises this functionality but there are no templates.

---

## Session Priorities

For the next working session, recommended order:
1. Fix the most-referenced missing figures (ch18, ch19, ch31, interlude) — these are in heavily-read sections
2. Apply data audit corrections (manufacturing %, coal %, solar %) — quick wins
3. Add demographics/aging cross-references to Ch6, Ch30, Ch31
