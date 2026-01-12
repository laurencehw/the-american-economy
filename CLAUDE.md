# The American Economy: A Structural Geography

## Project Overview

A comprehensive, concrete, institutional guide to the American economy - 29 chapters across 6 parts, targeting 400-600 pages. GitBook/online-first publication.

**Core approach**: Regional economics + institutional economics tradition. Concrete rather than abstract: which industries dominate, where they're located, who the major players are, how money flows, what government does with 40% of GDP.

## Current Status (January 2026)

**Chapters drafted (7 total, ~39,500 words):**
- Ch4: Government (~6,500 words) - adapted from public econ budget/federalism
- Ch6: Healthcare (~4,500 words)
- Ch7: Professional Services (~5,500 words)
- Ch8: Finance and Insurance (~7,000 words) - adapted from macro banking
- Ch14: Energy (~7,500 words) - informed by Jenkins electricity course
- Ch15: Education (~6,500 words) - adapted from public econ

**Infrastructure complete:**
- GitBook structure (`book/SUMMARY.md`)
- Chapter template (`_templates/sector_chapter_template.md`)
- Data scripts (`_scripts/`)
- Planning documents (`_planning/`)

**Source inventory complete:**
- 471 PDFs catalogued (`_data/materials_inventory.md`)
- Cross-project resources mapped (`_data/cross_project_resources.md`)
- Professional services sources compiled (`_data/professional_services_sources.md`)

## Key Files to Read First

1. `_planning/session_log.md` - What was done, what's next
2. `_planning/source_tracking.md` - Sources by chapter, gaps identified
3. `_planning/visualization_plan.md` - Maps, charts, tables, boxes (~265 visuals)
4. `_data/materials_inventory.md` - What's in the 471 PDFs
5. `_data/cross_project_resources.md` - Links to other book projects
6. `C:\Users\lwils\.claude\plans\shiny-sprouting-kahn.md` - Original book plan

## Cross-Project Resources

**Completed adaptations:**
- ✓ Education (Public Econ Ch15) → Ch15 Education
- ✓ Banking (Macro Ch11) → Ch8 Finance (mechanics reserved for Ch16)
- ✓ Federal budget/federalism (Public Econ Ch22/23) → Ch4 Government

**Remaining connections:**

| Need | Other Project | Path |
|------|---------------|------|
| Housing markets | City Economies | `G:\My Drive\book drafts\city economies\03_housing_markets\` |
| Mortgage/shadow banking | 2008 Crisis | `G:\My Drive\book drafts\2008 financial crisis\____OUTLINE\chapters\` |
| IO toolkit | Antitrust | `G:\My Drive\book drafts\antitrust\chapters\04-io-toolkit.qmd` |
| Finance mechanics | Macro Ch11 (reserved) | For Ch16: How American Finance Works |

## Source Gaps (Priority Research Needed)

**Critical (no sources):**
- Construction (Ch13)
- Retail/Wholesale Trade (Ch10)

**Important (thin):**
- Manufacturing beyond autos (Ch9)
- Transportation beyond airlines (Ch12)
- Trade associations (Ch27)

**Recently Filled (Session 2):**
- Ch4 Government - adapted from public econ budget/federalism
- Ch8 Finance and Insurance - adapted from macro banking
- Ch14 Energy - informed by Jenkins electricity course
- Ch15 Education - adapted from public econ
- Ch5 Real Estate - Gemini outline ready (`_data/ch05_real_estate_outline.md`)
- Ch10 Retail - Gemini sources (`_data/retail_sources.md`) incl. Syverson JEP
- Ch13 Construction - Gemini sources (`_data/construction_sources.md`) incl. Goolsbee/Syverson NBER

## Data Conventions

- **Primary data year**: 2022-2023
- **Monetary values**: Nominal unless noted
- **Geographic unit**: State/metro level for maps
- **Visualization**: 6-inch width, PDF format, minimal style (per global CLAUDE.md)

## Chapter Template

Each sector chapter (Part II) should include:
1. Overview (size, scope, GDP share)
2. How the industry works (business models)
3. Industry structure (concentration, major players)
4. Geographic distribution
5. The workforce
6. Regulation and policy
7. Trade associations and lobbying
8. Recent trends
9. Firm profiles (2-3 half-page boxes)
10. Data sources and further reading

## Next Priorities

1. **Draft Ch5 (Real Estate)** - Gemini outline ready, expand to full chapter
2. Draft Ch10 (Retail) - Syverson sources compiled
3. Draft Ch13 (Construction) - Goolsbee/Syverson sources compiled
4. Draft Ch11 (Tech/Media) - 100+ sources already collected
5. Create figures for drafted chapters (Ch6, Ch8, Ch14, Ch15)
6. Pull actual BEA/BLS data for drafted chapters
7. Apply IO toolkit concepts across all sector chapters

## Technical Notes

- Use Gemini (`C:\Users\lwils\scripts\gemini_helper.py`) for intensive research
- Follow KaTeX conventions for math (double $$ on own lines)
- PDFs over 3MB: use PyMuPDF to extract, don't read directly
