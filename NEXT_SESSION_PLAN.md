# Next Session Plan: Moving from 4.0 to 4.5+

This plan prioritizes the improvements most likely to raise the textbook's score, ordered by impact and feasibility. Items are grouped into tiers: **Tier 1** changes would each meaningfully move the score; **Tier 2** changes are important polish; **Tier 3** changes are nice-to-haves.

---

## Tier 1: High-Impact Changes (Target: 4.0 -> 4.5)

These are the changes that address the biggest gaps. Completing Tier 1 would raise the score to 4.5.

### 1. Add Chapter: Agriculture and Food Production
- **Why**: Agriculture is politically central, drives rural economies (Ch 25), and is deeply intertwined with trade policy, environmental regulation, and food manufacturing. Its absence is the most conspicuous gap.
- **Scope**: Follow the existing Part II template. Cover farm economics (crop vs. livestock, farm size distribution), the farm bill and subsidies (SNAP, crop insurance, conservation programs), major firms (Cargill, ADM, Deere as customer), geographic concentration (Corn Belt, Central Valley, Delta), the agricultural workforce (immigration, seasonal labor), and trade (U.S. as major exporter).
- **Data sources**: USDA ERS, Census of Agriculture, BEA GDP by industry.
- **Estimated effort**: 1 full session.
- **Figures needed**: Farm output by commodity treemap, agricultural employment map, farm size distribution, export composition chart.

### 2. Add Chapter: Leisure and Hospitality
- **Why**: 11% of employment. Low-wage, labor-intensive, geographically distinctive (tourism destinations, urban centers). Critical for understanding wage inequality and pandemic impacts.
- **Scope**: Hotels (Marriott, Hilton, franchise models), restaurants (quick-service vs. full-service, franchise economics), entertainment and recreation, tourism economics. Cover the gig/tipped wage workforce, seasonal patterns, and geographic concentration (Las Vegas, Orlando, NYC, coastal resort towns).
- **Data sources**: BLS CES, Census Bureau, American Hotel & Lodging Association, National Restaurant Association.
- **Estimated effort**: 1 full session.
- **Figures needed**: Hospitality employment over time (showing pandemic collapse/recovery), wage distribution, geographic concentration map.

### 3. Add Section/Chapter: Inequality and Distribution
- **Why**: Income and wealth distribution are among the most important structural features of the economy. The book currently treats them as asides rather than as core structure.
- **Scope**: Could be a new Chapter 3.5 in Part I ("Who Benefits: Distribution and Inequality") or a new section in Chapter 29. Cover: income distribution (Gini, top 1% share, labor vs. capital income), wealth distribution (Federal Reserve SCF data), racial wealth gap, gender pay gap, geographic divergence (thriving metros vs. declining communities), intergenerational mobility.
- **Data sources**: CBO income distribution reports, Federal Reserve Survey of Consumer Finances, Census ACS, Chetty/Opportunity Insights data.
- **Estimated effort**: 1 session.
- **Figures needed**: Income share over time (top 1%, middle 60%, bottom 20%), wealth distribution bar chart, racial wealth gap, geographic income map.

### 4. Add End-of-Chapter Exercises (All Chapters)
- **Why**: The single most impactful change for classroom adoption. Without exercises, instructors must create their own materials, which is a significant barrier.
- **Scope**: For each of the 30 chapters, add:
  - 5-8 **Review & Discussion Questions** (mix of factual recall, analytical reasoning, and current-events application)
  - 2-3 **Data Exercises** tied to Appendix A sources (e.g., "Use FRED to find the current unemployment rate in your state. How does it compare to the national rate? What industries might explain the difference?")
  - 1 **Deeper Investigation** prompt for advanced students or term papers
- **Example exercises**:
  - Ch 1: "Look up the 3-digit NAICS code for an industry of your choice using bls.gov/oes. What occupations does it include? What is the median wage?"
  - Ch 2: "Using the BEA input-output tables, identify the three largest suppliers to the automobile industry. What would happen to these suppliers if auto production fell 20%?"
  - Ch 6: "The U.S. spends 17% of GDP on healthcare while Germany spends 12%. Using the chapter's framework, identify three structural reasons for this gap."
  - Ch 16: "Explain why the Silicon Valley Bank run happened in hours rather than days. What structural features of SVB's deposit base made it uniquely vulnerable?"
- **Estimated effort**: 2-3 sessions (can be done incrementally, a few chapters per session).

---

## Tier 2: Important Polish (Target: 4.5 -> 4.75)

### 5. Data Consistency Pass
- **Task**: Audit all chapters for statistical consistency. Reconcile manufacturing GDP share (11% in Ch 1 vs. 10% in Ch 9), align reference years across tables, and add footnotes where different years are used.
- **Approach**: Create a master data table with key statistics (GDP share, employment, major firms) for each sector, then cross-check against all chapter references.
- **Estimated effort**: 1 session.

### 6. Reduce Case Study Repetition / Add Positive Shock Example
- **Task**: Differentiate the oil price collapse treatment between Ch 2 and Ch 30. In Ch 2, keep a shorter version focused on I-O mechanics. In Ch 30, focus on the full multi-channel propagation (financial, labor, geographic).
- **Additionally**: Add a positive shock case study to Chapter 2 — the 2022-2023 CHIPS Act / IRA investment boom — showing the multiplier effect in a growth context. Trace how semiconductor fab construction in Arizona creates demand for construction workers, equipment suppliers, local housing, and downstream tech manufacturing.
- **Estimated effort**: 1 session.

### 7. Strengthen Chapter 28: Labor Markets and the Workforce
- **Task**: Expand beyond unions and trade associations to cover:
  - The changing nature of work (remote work post-COVID, freelancing, noncompete agreements)
  - Labor market monopsony and employer market power
  - Immigration's role in the labor market (H-1B, agricultural labor, unauthorized workers)
  - Childcare and eldercare infrastructure as labor force enablers
  - The gig economy's labor implications
- **Rename**: "Labor Organizations" -> "Labor Markets and the Workforce"
- **Estimated effort**: 1 session.

### 8. Expand International Comparisons in Ch 19 and Ch 29
- **Task**: Add a "Deep Dive" callout in Chapter 19 comparing U.S. labor laws, corporate tax structures, and social insurance to OECD peers. Expand Chapter 29 with a structured comparison table (U.S. vs. EU vs. East Asia) covering: role of government, labor market regulation, healthcare model, industrial policy approach, trade policy orientation.
- **Estimated effort**: 0.5 session.

### 9. Print/PDF Readiness Audit
- **Task**: Ensure every interactive HTML visualization has:
  - A high-quality static PNG fallback in `_figures/`
  - A self-sufficient caption that describes the key insight (not just "view interactive version")
  - Extended text descriptions for complex visualizations (circular flow, shock propagation)
- **Check**: Verify all 125 existing PNG figures render correctly and have descriptive alt text.
- **Estimated effort**: 1 session.

---

## Tier 3: Nice-to-Haves (Target: 4.75 -> 5.0)

### 10. Expand Chapter 11: Platform Economy and AI
- **Task**: Add sections on platform economics (network effects, multi-sided markets), the gig economy, data as an economic resource, and AI's emerging economic effects.
- **Estimated effort**: 1 session.

### 11. Add Environmental Economics Coverage
- **Task**: Expand Chapter 14 (Energy) or add a new section covering climate risk costs, carbon pricing, environmental regulation as economic force, and the green transition as structural shift.
- **Estimated effort**: 1 session.

### 12. Expand Utilities Coverage
- **Task**: Add a section on electric grid economics, water systems, and broadband infrastructure to the energy chapter (or as a standalone short chapter).
- **Estimated effort**: 0.5 session.

### 13. Improve Figure Alt Text and Accessibility
- **Task**: Audit all `<figure>` tags across all chapters. Replace generic alt text with descriptive text that conveys the figure's key insight to screen reader users.
- **Estimated effort**: 0.5 session.

### 14. Add Glossary
- **Task**: Compile key terms from all hint boxes and chapter text into a searchable glossary appendix.
- **Estimated effort**: 0.5 session.

---

## Recommended Session Sequence

| Session | Tasks | Status |
|---------|-------|--------|
| **1** | Agriculture chapter + Hospitality chapter + Part I exercises + Quick wins | **DONE** |
| **2** | Inequality interlude + Exercises for Parts II-III (Ch 4-20) | **DONE** |
| **3** | Exercises for Parts IV-VII (Ch 21-32) + Data consistency pass + figure number fixes | **DONE** |
| **4** | Case study revision (Ch 2/32) + Positive shock example + Labor chapter expansion | **DONE** (Score: ~4.6) |
| **5** | International comparisons + Print/PDF audit | Next up |
| **6** | Platform economy expansion + Environmental economics | Pending |
| **7** | Utilities + Alt text audit + Glossary | Pending |

---

## Quick Wins (Can Be Done Anytime)

- [x] Fix manufacturing GDP share inconsistency (Ch 1 vs. Ch 9) — DONE
- [x] Add footnote to Ch 1 Table 1.1 noting rounding — DONE
- [ ] Standardize reference year notation across all tables
- [ ] Add cross-references between Ch 2 and Ch 32 case studies
- [x] Rename Ch 30 title to "Labor Markets and the Workforce" — DONE
- [ ] Renumber chapters 16-30 to 18-32 — DONE (new chapters are 16 and 17)
