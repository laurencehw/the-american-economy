# Textbook Review: The American Economy — A Structural Geography

**Reviewer**: Claude (Opus 5)
**Date**: September 2026
**Scope**: Full manuscript — 33 chapters, 5 appendices, 118 figures, 189 tables, 6 interactive visualizations
**Prior review**: March 2026, scored 8.2/10 (retained below for comparison)

---

## Overall Score: 8.9 / 10

The book is now clearly better than the 8.2 recorded in March. The intervening
sessions closed the largest structural gaps: all 118 figure references resolve, every
chapter carries Key Takeaways and a three-tier exercise set, the energy chapter has
been rebuilt with generation mix, LCOE, utilities, carbon pricing, and environmental
economics, the labor chapter gained monopsony, immigration, and the childcare–
participation link, education gained student debt and K-12 outcomes, agriculture gained
externalities, and a consolidated references appendix now exists. The glossary has
grown from a stub into a genuine reference.

This session addressed the next tier: the table apparatus, cross-chapter integration,
internal numerical consistency, and the one chapter that was still purely descriptive.
Those changes are summarized under "What Changed This Session" below.

What remains between 8.9 and 9.5 is now a short and specific list, and it is dominated
by a single issue the earlier reviews did not weight heavily enough: **the book is
anchored to 2023 data and it is late 2026.** Everything else is polish.

---

## Scoring Breakdown

| Category | Mar 2026 | Sep 2026 | Notes |
|----------|:--------:|:--------:|-------|
| Scope and Coverage | 8.5 | 9.0 | Utilities, environmental economics, student debt, K-12 outcomes, monopsony all added. Arts/entertainment and early childhood still absent. |
| Writing Quality | 9.0 | 9.0 | Unchanged and strong. Hedging density is the one persistent tic. |
| Data and Evidence | 7.5 | 8.8 | Every table now numbered and sourced; cross-chapter contradictions reconciled; explicit vintage policy. Held below 9 by data currency, not by rigor. |
| Analytical Depth | 7.5 | 8.7 | Ch 14, 15, 16, 30 substantially deepened in prior sessions; Ch 28 this session. Ch 11 platform economics is the remaining thin spot. |
| Pedagogical Design | 8.5 | 9.2 | Numbered tables make the book citable; figure captions are self-sufficient; exercises are well-tiered. |
| Cross-Chapter Integration | 7.5 | 9.2 | From 89 internal links to 280, with a Connections section in all 33 chapters that argues the relationship rather than just naming it. |
| Structure and Organization | 9.0 | 9.2 | Conventions now documented and CI-enforced. |
| Appendices and Reference | 8.0 | 8.8 | Publication calendar, consolidated references, 139-term glossary correctly ordered. NAICS depth still uneven. |
| **Overall** | **8.2** | **8.9** | |

---

## What Changed This Session

1. **Table apparatus.** 189 tables existed; 159 had no number and 74 had no source line.
   In a book whose selling point is data, a reader could not cite a table or trace a
   figure to its origin. All 189 now carry a chapter-scoped number and a source; tables
   that illustrate a mechanism rather than report measured data say so instead of
   carrying a spurious citation. `check_tables.py` in CI keeps it that way and catches
   the out-of-sequence numbering that had already produced a "Table 19.3a".

2. **Cross-chapter integration.** Twelve chapters had zero cross-references and "see
   also" appeared once in 200,000 words — a real problem for a book arguing that the
   economy is interconnected. Every chapter now ends with a Connections section of five
   links that state what the other chapter contributes. These also carry the
   cross-cutting themes (inequality, climate, demographics, automation) into the sector
   chapters, which was Issue 3 of the March review.

3. **Internal consistency.** Four statistics disagreed with themselves across chapters:
   manufacturing value added (Ch 9 said 11%, everywhere else said 10.1%), the CES sample
   size (670,000 vs. 145,000), healthcare's GDP share (17% vs. "nearly 18%" with no
   years attached), and total GDP (Ch 31's "$30 trillion" against Ch 1's $27.8 trillion).
   All reconciled to the BEA/BLS/CMS series with years stated.

4. **Ch 28.** Was the most purely descriptive chapter in the book — it catalogued
   agencies without evaluating them, and could not answer its own exercise about
   jurisdictional overlap. Added ~1,200 words arguing whether regulatory fragmentation
   works, from both sides, with a defensible conclusion (gaps matter more than overlaps;
   supervisor choice is the mechanism that fails; funding independence predicts
   behaviour better than the org chart).

5. **Perishable facts.** Ch 28 named sitting officeholders and dated one by a term that
   has since expired. Quick Facts now give durable structure — term lengths, appointment
   process, commission composition.

6. **Glossary.** Twelve entries were out of alphabetical order and two sat under the
   wrong letter while that letter's section read "No terms in this section." Rebuilt and
   re-sorted; added 17 terms the book uses as load-bearing concepts but never defined,
   including imputed rent, location quotient, multiplier, endogenous money, and the
   establishment/firm distinction that Chapter 1 leans on heavily.

7. **Conventions.** `how-to-use.md` described a ten-part chapter template that no longer
   matched the chapters, and dated the book's figures to "the 2022-2023 period", which
   had stopped being true. It now states an explicit data-vintage policy, the table and
   figure numbering scheme, and the full appendix list.

8. **Housekeeping.** Interactive visualizations now state their data vintage. Issue
   templates the README has promised since the repo went public now exist.

---

## What Works Well (Preserve)

The strengths identified in March are intact and are the reason this book is worth
finishing to a 9.5.

1. **It fills a genuine gap.** No competing book assembles this institutional detail in
   one place: 0.3% of firms employ 54% of workers; three PBMs control 80% of drug
   pricing; four meatpackers process 80% of U.S. beef; 7% of farms produce 73% of
   agricultural output.

2. **The Part II template is the book's spine.** Overview → how it works → structure →
   geography → workforce → regulation → trends → firms → takeaways → connections →
   exercises. It makes cross-sector comparison natural and turns the book into a
   reference you can navigate blind.

3. **Systems thinking as organizing principle.** The I-O framework (Ch 2), the three
   value chains, the sectoral balance identity, and the four-channel shock analysis
   (Ch 32) elevate this above a reference encyclopedia. Ch 32 remains the best synthesis
   chapter in the book; Ch 18 remains the best chapter overall.

4. **Intellectual honesty.** Healthcare's dysfunction described without polemic. The
   China shock with both the efficiency gains and the devastation. The money multiplier
   corrected with the endogenous money view. This builds trust, and it is rarer in
   textbooks than it should be.

5. **Regional analysis.** Part V is a highlight — the Northeast as one mega-region, the
   Sunbelt's extensive-vs-intensive growth distinction, the rural typology.

---

## The Path from 8.9 to 9.5

Five items, in priority order. The first is worth more than the other four combined.

### 1. Data currency (Impact: +0.30)

**This is now the book's binding constraint.** The manuscript is anchored to 2023
national accounts. It is late 2026. BEA has published complete, revised 2024 and 2025
annual industry accounts; BLS has two more years of employment and wage data; CMS,
EIA, and USDA have all moved on. A living textbook three years behind its own sources
cannot claim the authority its data-forward framing asserts.

The vintage convention added this session makes the situation *honest* — every table
states its year, and `how-to-use.md` explains the policy — but honesty is not currency.

The work is mechanical but large, and it should be done as a data refresh rather than a
prose rewrite:

- Roll the national accounts anchor from 2023 to 2025 (or 2024, if 2025 is not yet
  fully revised at the time of the pass). This touches Ch 1, Ch 3, Appendix B, and the
  interactive JSON, plus every chapter's Overview section.
- Refresh firm-level tables (revenues, market caps, AUM, headcount) — roughly 60 tables.
- Refresh the series with fast-moving values: energy generation mix and LCOE (Ch 14),
  trade flows (Ch 21-22), housing prices (Ch 5, 23-27), union density (Ch 30).
- Because every table now has a source line naming its series, this pass is
  *enumerable* in a way it was not before. That was much of the point of the table work.

**Recommendation**: build `_dev/refresh_data.py` that pulls the named series from the
BEA, BLS, and FRED APIs and emits a reconciliation report against what the book
currently says. Then the annual refresh becomes a review of a diff rather than a manual
audit. This is the single highest-leverage investment available for this project.

### 2. In-text attribution for empirical claims (Impact: +0.10)

Appendix E is a good bibliography of roughly 120 works, and chapter-level Further
Reading is solid. But specific empirical claims in the text are rarely tied to the
source that established them. The book asserts China shock job losses, mobility
estimates, LCOE trajectories, and concentration ratios without pointing the reader to
Autor–Dorn–Hanson, Chetty, Lazard, or the relevant Census/USDA series.

This does not require converting the book to author-date citation throughout. It
requires attaching a source to the roughly 50–80 claims that are *contested or
research-derived* rather than definitional. A reader who wants to check the strongest
claims should be able to.

### 3. Hedging density (Impact: +0.05)

"Roughly" appears 302 times, 61 in Chapter 14 alone. Many are legitimate — pipeline
mileage and installed capacity genuinely are approximate. But in a book that teaches
data literacy, the hedge should signal real uncertainty rather than serve as verbal
filler. A pass that replaces the hedge with the precise figure wherever an official
series exists, and keeps it where the estimate is genuinely approximate, would sharpen
the prose and reinforce the book's own methodological standard.

### 4. Remaining coverage gaps (Impact: +0.05)

- **Arts, entertainment, and recreation.** Hollywood, music, professional sports, and
  gaming are economically significant and analytically interesting (winner-take-all
  dynamics, extreme geographic concentration in LA/Nashville/NYC). Best folded into an
  expanded Ch 17 rather than added as a standalone chapter.
- **Early childhood education and care.** Ch 15 runs K-12 through graduate school and
  barely mentions pre-K. The economics — market failure, subsidy structure, wage
  suppression in care work — connect directly to Ch 30's treatment of female labor force
  participation, which already gestures at it.
- **Ch 11 platform economics.** The chapter has a platform economics section now, but it
  remains the thinnest analytical treatment among the large sector chapters relative to
  the sector's importance. Two-sided market pricing, the attention economy's measurement
  problems, and the antitrust theories actually being litigated deserve more.

### 5. Appendix C depth (Impact: +0.03)

NAICS coverage is uneven — manufacturing gets 17 subsectors, healthcare 4. Four-digit
codes are missing for finance, professional services, and information. There is still no
guidance on classifying platform companies, which is the question a student is most
likely to actually have (where does Amazon sit? Uber?).

---

## Chapter-by-Chapter Assessment

| Part | Chapter | Score | Note |
|------|---------|:-----:|------|
| **I** | 1. Economy in Numbers | 9.0 | Nominal/real now explained; healthcare footnote fixed; CES sample corrected. |
| | 2. How It Fits Together | 9.0 | Best analytical chapter in Part I. CHIPS case study excellent. |
| | 3. Geography | 8.5 | "Five states" error fixed and internally consistent at 41%. |
| | Interlude. Inequality | 8.5 | Wage vs. capital income now distinguished. Best-connected chapter in the book. |
| **II** | 4. Government | 8.5 | Twelve well-sourced tables. Could use state/local fiscal stress. |
| | 5. Real Estate | 8.5 | Housing mechanics strong; 2006-12 crisis section is a good addition. |
| | 6. Healthcare | 9.0 | Outstanding. Years now attached to every share figure. |
| | 7. Professional Services | 8.0 | Solid; consulting dynamics still thin. |
| | 8. Finance & Insurance | 8.5 | Hierarchy of money excellent. Twelve tables now sourced. |
| | 9. Manufacturing | 9.0 | China shock treatment balanced and thorough. Figures reconciled. |
| | 10. Retail & Wholesale | 8.0 | Warehouse/fulfillment economics could go deeper. |
| | 11. Tech & Media | 8.0 | Largest chapter in the book; analytical depth still trails its length. |
| | 12. Transportation | 8.5 | Comprehensive multimodal coverage, 11 figures. |
| | 13. Construction | 8.0 | Productivity puzzle deserves more. |
| | 14. Energy | 9.0 | Transformed since March. Generation mix, LCOE, utilities, carbon pricing, environmental economics all present. Hedging density is its remaining flaw. |
| | 15. Education | 8.5 | Student debt and K-12 outcomes now analyzed. Pre-K absent. |
| | 16. Agriculture | 8.5 | Externalities section added. Concentration data outstanding. |
| | 17. Leisure & Hospitality | 8.0 | Strong opening; arts/entertainment would fit here. |
| **III** | 18. How Finance Works | 9.5 | Best chapter in the book. Essentially complete. |
| | 19. Capital Markets | 8.5 | Clear market structure; private markets well covered. |
| | 20. Corporate Finance | 8.5 | Eighteen tables, now all sourced. |
| **IV** | 21. Trade | 8.5 | Services trade and tariff economics both present. |
| | 22. Supply Chains | 8.5 | Strong post-COVID analysis. |
| **V** | 23. Northeast | 8.5 | Mega-region concept excellent. |
| | 24. Sunbelt | 8.5 | Extensive vs. intensive growth well drawn. |
| | 25. Midwest | 8.0 | Honest about the manufacturing paradox. |
| | 26. West | 8.5 | California analysis excellent; water treated as binding constraint. |
| | 27. Rural | 8.0 | Good typology. Solutions discussion still thin. |
| **VI** | 28. Federal Governance | 8.5 | No longer a reference document. Fragmentation analysis added this session. |
| | 29. Trade Associations | 8.0 | Good K Street coverage. |
| | 30. Labor | 8.5 | Monopsony, immigration, childcare all now covered. |
| **VII** | 31. Perspective | 8.5 | GDP figure reconciled. Demographics still underweighted. |
| | 32. Shock Transmission | 9.0 | Masterful synthesis. Four-channel framework excellent. |
| **App.** | A–E | 8.8 | Publication calendar, references, corrected glossary. NAICS depth uneven. |

---

## Final Assessment

At 8.9 this is a very good textbook with a distinctive contribution that no competing
book makes. The architecture is settled, the analytical framework is coherent, the
apparatus is now professional, and the chapters that were weak in March are no longer
weak.

The gap to 9.5 is not a content gap. It is a **maintenance** gap. A book that stakes its
authority on institutional and numerical detail has to stay current, and the honest
statement of the book's present condition is that its numbers describe 2023.

The good news is that this session's table work makes the refresh tractable: every table
now names its own source and year, so the currency problem is enumerable rather than
diffuse. Building the refresh script and running the first pass is the work that moves
this book to 9.5, and it converts an annual crisis into an annual chore.

| Category | Current | After the data refresh + items 2–5 |
|----------|:-------:|:----------------------------------:|
| Scope and Coverage | 9.0 | 9.3 |
| Writing Quality | 9.0 | 9.3 |
| Data and Evidence | 8.8 | 9.7 |
| Analytical Depth | 8.7 | 9.2 |
| Pedagogical Design | 9.2 | 9.4 |
| Cross-Chapter Integration | 9.2 | 9.3 |
| Structure and Organization | 9.2 | 9.4 |
| Appendices and Reference | 8.8 | 9.2 |
| **Overall** | **8.9** | **~9.5** |
