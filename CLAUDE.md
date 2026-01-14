# The American Economy: A Structural Geography

## Project Overview

A comprehensive, concrete, institutional guide to the American economy - 29 chapters across 6 parts, targeting 400-600 pages. GitBook/online-first publication.

**Core approach**: Regional economics + institutional economics tradition. Concrete rather than abstract: which industries dominate, where they're located, who the major players are, how money flows, what government does with 40% of GDP.

## Current Status (January 2026)

**FIRST DRAFT COMPLETE: 29 chapters drafted (~162,600 words)**

**Part I: The Shape of the Economy (3 chapters, ~17,000 words):**
- Ch1: The American Economy in Numbers (~5,500 words) - GDP, employment, data infrastructure
- Ch2: How It All Fits Together (~6,500 words) - input-output, value chains, sectoral balances, flow of funds
- Ch3: The Geography of Production (~5,000 words) - metros, states, agglomeration, rural

**Part II: The Sectors (12 chapters, ~85,500 words):**
- Ch4: Government (~6,500 words) - adapted from public econ budget/federalism
- Ch5: Real Estate (~7,000 words) - mortgage system, supply elasticity, REITs
- Ch6: Healthcare (~4,500 words)
- Ch7: Professional Services (~5,500 words)
- Ch8: Finance and Insurance (~7,000 words) - adapted from macro banking
- Ch9: Manufacturing (~8,500 words) - productivity paradox, CHIPS/IRA, supply chains
- Ch10: Retail and Wholesale (~7,500 words) - Big Four, format evolution, wholesale
- Ch11: Tech/Media (~8,000 words) - Big Tech, telecom, streaming, antitrust, AI boom
- Ch12: Transportation (~8,000 words) - trucking, rail duopoly, airlines, ports, logistics
- Ch13: Construction (~7,000 words) - productivity puzzle, CHIPS Act supercycle
- Ch14: Energy (~7,500 words) - informed by Jenkins electricity course
- Ch15: Education (~6,500 words) - adapted from public econ

**Part III: The Financial Architecture (3 chapters, ~23,500 words):**
- Ch16: How American Finance Works (~7,500 words) - hierarchy of money, payments, shadow banking, Fed operations
- Ch17: Capital Markets (~8,500 words) - exchanges, bond markets, derivatives, PE/VC, meme stocks
- Ch18: Corporate Finance in Practice (~7,500 words) - pecking order, M&A, governance, activism

**Part IV: Trade and Global Linkages (2 chapters, ~14,500 words):**
- Ch19: America's Trading Relationships (~7,000 words) - trade stats, tariffs, agreements, enforcement
- Ch20: Global Supply Chains (~7,500 words) - value chains, semiconductors, 2021-22 crisis, reshoring

**Part V: Regional Economies (5 chapters, ~13,200 words):**
- Ch21: The Northeast Corridor (~2,200 words) - Acela mega-region, Boston/NYC/Philly/DC pillars
- Ch22: The Sunbelt (~2,800 words) - growth shift, Houston/Dallas/Austin/Miami/Atlanta/Phoenix
- Ch23: The Midwest (~2,500 words) - Chicago, Detroit EV transition, Intel Ohio, Battery Belt
- Ch24: The West (~3,000 words) - California economy, Bay Area AI, water crisis, policy labs
- Ch25: Rural America (~2,700 words) - definitions, agriculture, energy, infrastructure gaps

**Part VI: Institutions and Governance (3 chapters, ~6,700 words):**
- Ch26: Federal Economic Governance (~2,200 words) - Treasury, OMB, CEA, Fed, regulatory agencies
- Ch27: Trade Associations (~2,200 words) - Chamber, NAM, industry associations, lobbying
- Ch28: Labor Organizations (~2,300 words) - unions, collective bargaining, recent actions

**Conclusion (~2,200 words):**
- Ch29: The American Economy in Perspective - distinctive features, ongoing transformations, persistent tensions

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
- ✓ Housing markets (City Economies) + Mortgage finance (2008 Crisis) → Ch5 Real Estate
- ✓ Flow of Funds (Macro Ch3) → Ch2 How It Fits Together (sectoral balances, Z.1 accounts)

**Remaining connections:**

| Need | Other Project | Path |
|------|---------------|------|
| IO toolkit | Antitrust | `G:\My Drive\book drafts\antitrust\chapters\04-io-toolkit.qmd` |
| Capital markets | ✓ Macro Ch12, Int'l Finance Ch12/14 | Used for Ch17 |
| International trade | Int'l Finance textbook | For Ch19-20: Trade chapters |

**Completed in Session 6:**
- ✓ Shadow banking, payments, Fed operations (2008 Crisis Ch6-7, Macro Ch10-11, Finance Ch15) → Ch16 How Finance Works

## Source Gaps (Priority Research Needed)

**All 29 chapters drafted** - First draft complete with Gemini research

**Remaining work:**
- Data verification (pull actual BEA/BLS data)
- Figure creation
- Editorial refinement

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

1. **Create figures and visualizations** for all parts (see `_planning/visualization_plan.md`)
2. **Pull actual BEA/BLS data** to verify/update statistics
3. **Review and refine** earlier chapters for consistency
4. **Draft appendices** (Data Sources, BEA Tables, NAICS Codes)
5. **Editorial pass** for tone, style, cross-references

## Technical Notes

- Use Gemini (`C:\Users\lwils\scripts\gemini_helper.py`) for intensive research
- Follow KaTeX conventions for math (double $$ on own lines)
- PDFs over 3MB: use PyMuPDF to extract, don't read directly
