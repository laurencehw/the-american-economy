# Session Log: The American Economy Book Project

---

## Session 1: January 11, 2026

### Accomplishments

**1. Project Planning**
- Created comprehensive book plan (29 chapters, 6 parts, 400-600 pages target)
- Established GitBook/online-first publication approach
- Set up folder structure: `book/`, `_data/`, `_figures/`, `_scripts/`, `_templates/`, `_planning/`

**2. Infrastructure**
- Created SUMMARY.md with full chapter structure
- Created README.md (book introduction)
- Created how-to-use.md (reader guide)
- Created sector chapter template (`_templates/sector_chapter_template.md`)
- Created data pull scripts (`_scripts/pull_bea_data.py`, `_scripts/mapping_utils.py`)

**3. Materials Inventory**
- Used Gemini to inventory 471 existing PDFs
- Created `_data/materials_inventory.md` mapping files to chapters
- Identified coverage: Strong (Ch1-2, Ch6, Ch11), Critical gaps (Ch7, Ch13, Ch15, Ch27)

**4. Cross-Project Resources**
- Discovered extensive relevant materials in other book projects
- Created `_data/cross_project_resources.md` mapping connections
- Key finds:
  - Public Econ Ch15 (Education) - complete chapter, fills critical gap
  - Macro Ch11 (Banking) - extensive, fills finance gaps
  - 2008 Crisis chapters - mortgage finance, shadow banking
  - Antitrust IO toolkit - applicable across sectors

**5. Chapter Drafts**
- **Ch6: Healthcare** - First draft complete (~4,500 words)
- **Ch7: Professional Services** - First draft complete (~5,500 words)

**6. Research**
- Used Gemini to find professional services sources
- Created `_data/professional_services_sources.md`
- Key sources identified: Hadfield (2022) JEL, Bloom & Van Reenen (2010) JEP, Evans (2009) JEP

### Files Created This Session

```
book/
├── SUMMARY.md
├── README.md
├── how-to-use.md
├── part1/ (empty, ready for chapters)
├── part2/
│   ├── ch06-healthcare.md ✓
│   └── ch07-professional-services.md ✓
├── part3-6/ (empty, ready for chapters)
├── conclusion/
└── appendices/

_data/
├── materials_inventory.md
├── cross_project_resources.md
├── professional_services_sources.md
└── pdf_inventory_raw.txt

_scripts/
├── pull_bea_data.py
└── mapping_utils.py

_templates/
└── sector_chapter_template.md

_planning/
├── source_tracking.md
└── session_log.md (this file)
```

### Decisions Made
- Target audience: Mixed (accessible prose + technical appendices)
- Scope: 400-600 pages
- Temporal focus: Contemporary (2010s-2020s)
- Geography: Both integrated in chapters AND dedicated regional chapters
- Case studies: Half-page firm profiles (2-3 per sector chapter)
- Data year: 2022-2023 as primary reference

### Next Session Priorities

1. **Connect cross-project resources formally**
   - Read and adapt public econ education chapter
   - Extract relevant material from macro banking chapter
   - Pull IO toolkit concepts from antitrust book

2. **Draft next chapters** (in priority order)
   - Ch14: Energy (strong existing materials)
   - Ch5: Real Estate (city economies + 2008 crisis connections)
   - Ch4: Government (public econ connections)

3. **Fill critical gaps**
   - Research construction industry sources
   - Research retail/wholesale trade sources
   - Compile regional Fed resources

4. **Data infrastructure**
   - Pull actual BEA GDP by industry data
   - Download Census shapefiles for mapping
   - Create first visualization (GDP composition treemap)

---

## Session 2: January 11, 2026 (continued)

### Accomplishments

**1. Education Chapter Adapted**
- Read and adapted `public econ/chapters/ch15_education/ch15_education_v1.md` (~800 lines)
- Created `book/part2/ch15-education.md` (~6,500 words)
- Reframed from policy lens to structural/industry lens

**2. Added Industry Structure Elements**
- For-profit education sector (Stride, University of Phoenix, Grand Canyon)
- Ed-tech companies (Coursera, Chegg, 2U)
- Textbook publishers (Pearson, McGraw-Hill, Cengage)
- Testing companies (College Board, ACT, ETS)
- Market concentration analysis for commercial education

**3. Added Geographic and Workforce Details**
- Per-pupil spending variation by state
- Charter school concentration by state
- Higher ed geography (research universities, college towns)
- Teacher labor market (shortages, wages, geographic immobility)
- Faculty casualization (tenure-track vs. contingent)
- Administrative growth

**4. Firm Profiles Created**
- College Board (monopoly testing, nonprofit power)
- Pearson (global education company)
- University of California System (public higher ed exemplar)

**5. Recent Trends Section**
- For-profit collapse and nonprofit online pivot
- Testing wars and test-optional movement
- Enrollment cliff (demographic)
- AI disruption potential
- Geographic polarization

**6. Finance and Insurance Chapter Drafted**
- Read and adapted `macroeconomics/chapters/part3_financial/ch11_banking.md` (~750 lines)
- Created `book/part2/ch08-finance-insurance.md` (~7,000 words)
- Added extensive new content beyond source:
  - Industry structure: Big Four banks, insurance markets (life, P&C, health), asset management (Big Three), private equity
  - Geographic patterns: NYC money center, Charlotte banking hub, Hartford insurance
  - Regulatory alphabet soup: Fed, OCC, FDIC, SEC, state insurance commissioners
  - Fintech and neobanks
  - March 2023 banking stress analysis
- Firm profiles: JPMorgan Chase, Berkshire Hathaway Insurance, BlackRock
- Reserved detailed mechanics (shadow banking, credit channels) for Ch16 (How American Finance Works)

**7. Government Chapter Drafted**
- Read `public econ/chapters/ch22_federal_budget/ch22_federal_budget_v1.md` (~260 lines)
- Read `public econ/chapters/ch23_fiscal_federalism/ch23_fiscal_federalism_v1.md` (~630 lines)
- Created `book/part2/ch04-government.md` (~6,500 words)
- Reframed from budget process/fiscal policy → government as economic sector
- Added extensive new content:
  - Government as employer (23M workers breakdown by level and function)
  - Government as purchaser ($700B federal procurement, defense contractors)
  - Geographic distribution (DC concentration, military bases, state variation)
  - Defense industrial base (top 10 contractors, concentration concerns)
  - Regulatory agencies overview
  - Recent trends (contractor state, IRS transformation, industrial policy)
- Profiles: Department of Defense, California State Government, New York City

**8. Energy Chapter Drafted**
- Referenced Jesse Jenkins' Princeton electricity course (24 lectures)
- Created `book/part2/ch14-energy.md` (~7,500 words)
- Comprehensive coverage:
  - Electricity: generation mix, transmission, distribution, regulated vs restructured markets
  - Oil and gas: shale revolution, upstream/midstream/downstream, major basins
  - Renewables: wind, solar, storage, IRA incentives
  - Industry structure: utilities (IOUs, public, co-ops), ISOs/RTOs, oil majors, independents
  - Geographic patterns: producing vs consuming states, grid regions (Eastern/Western/ERCOT)
  - Regulation: FERC, state PUCs, EPA
  - Recent trends: shale maturation, coal collapse, renewable buildout, grid reliability, nuclear question, electrification
- Firm profiles: NextEra Energy, ExxonMobil, Duke Energy

### Files Created/Modified

```
book/part2/
├── ch04-government.md ✓ (NEW - ~6,500 words)
├── ch08-finance-insurance.md ✓ (NEW - ~7,000 words)
├── ch14-energy.md ✓ (NEW - ~7,500 words)
└── ch15-education.md ✓ (NEW - ~6,500 words)

_planning/
├── session_log.md (updated)
├── source_tracking.md (updated)
└── cross_project_adaptation_notes.md (updated)
```

### Key Adaptation Decisions
- Preserved human capital theory and returns evidence from source
- Removed detailed policy debate sections (The Debate boxes)
- Added commercial education ecosystem (~40% new content)
- Firm profiles: chose organizations illustrating different business models (nonprofit monopoly, global corporation, public system)

**9. Visualization Plan Created**
- Created `_planning/visualization_plan.md` (~265 visual elements planned)
- Established style standards: colors, typography, map conventions
- Chapter-by-chapter visualization inventory with data sources
- Production pipeline and technical specifications

**10. Chapter 1 Figures Created**
- `ch01_gdp_treemap.pdf` - GDP composition by industry (with grouped "Other")
- `ch01_employment_bar.pdf` - Employment by industry (horizontal bar)
- `ch01_gdp_vs_employment.pdf` - Capital vs labor intensity comparison (dumbbell)

**11. Chapter 4 Figures Created**
- `ch04_federal_employment_map.pdf` - Dual choropleth (total & per capita)
- `ch04_top_contractors.pdf` - Top 10 federal contractors by sector
- `ch04_spending_treemap.pdf` - Federal spending by function (mandatory vs discretionary)
- `ch04_govt_employment_level.pdf` - Government employment by level (stacked bar)

### Session 2 Summary Statistics

- **New chapters drafted**: 4 (Ch4, Ch8, Ch14, Ch15)
- **Total chapters drafted**: 7 (including Ch6, Ch7 from Session 1)
- **Total word count**: ~39,500 words across all drafted chapters
- **Cross-project adaptations completed**: 4 (Education, Banking, Federal Budget, Energy)
- **Visualizations planned**: ~265 (maps, charts, tables, boxes)
- **Figures created**: 7 (3 for Ch1, 4 for Ch4)

### Gemini Tasks Delegated (End of Session 2)

Three background tasks sent to Gemini Ultra:
1. **Ch5 Real Estate outline** - Draft detailed chapter outline with institutional detail
2. **Ch13 Construction sources** - Find Syverson/Goolsbee paper, academic sources, industry data
3. **Ch10 Retail sources** - Summarize Syverson JEP (2015), find additional sources

**Results saved to `_data/`:**
- `ch05_real_estate_outline.md` - Full 8-section chapter outline with firm profiles
- `construction_sources.md` - Goolsbee/Syverson (2023), D'Amico/Glaeser (2024), industry data
- `retail_sources.md` - Hortaçsu/Syverson (2015), Neumark Walmart study, Big Four stats

### Next Session Priorities

1. **Review Gemini outputs** and incorporate into:
   - Ch5 Real Estate draft
   - `_data/construction_sources.md`
   - `_data/retail_sources.md`

2. **Continue cross-project adaptation**
   - Housing chapter (City Economies) → Ch5 (Real Estate)
   - 2008 Crisis mortgage chapters → Ch5 mortgage system section
   - IO toolkit concepts → Apply to all sector chapters

3. **Draft next chapters** (in priority order)
   - Ch5: Real Estate (Gemini outline ready to review)
   - Ch11: Tech/Media (100+ sources already collected)
   - Ch9: Manufacturing (partial sources, needs expansion)

4. **Create figures for drafted chapters**
   - Ch6 Healthcare: spending treemap, payment flows
   - Ch8 Finance: bank assets, geographic map
   - Ch14 Energy: generation mix, grid map
   - Ch15 Education: spending choropleth

5. **Data and visualization**
   - Pull actual BEA/BLS data for drafted chapters
   - Replace hardcoded data in figure scripts with API calls

---

## Session 3: January 12, 2026

### Accomplishments

**1. Chapter 5: Real Estate Drafted**
- Created `book/part2/ch05-real-estate.md` (~7,000 words)
- Integrated three source materials:
  - Gemini outline (`_data/ch05_real_estate_outline.md`) - industry structure focus
  - 2008 Crisis mortgage chapter - OTD model, securitization, GSEs, agency problems
  - City Economies housing chapter - supply elasticity, zoning, WRLURI, affordability
- Comprehensive coverage:
  - Mortgage system: 30-year fixed, originate-to-distribute, Fannie/Freddie mechanics
  - Supply economics: elastic vs inelastic markets, zoning tax, Hsieh-Moretti GDP loss estimates
  - Industry structure: homebuilders (D.R. Horton, Lennar), REITs, commercial specialists (Prologis, Equinix)
  - Geographic patterns: coastal-interior divide, Sunbelt shift, donut effect
  - Brokerages: NAR/MLS system, 2024 antitrust settlement
  - Trade associations: NAR, MBA, NAHB, NAREIT
  - Recent trends: affordability crisis, lock-in effect, institutional SFR, office apocalypse, rent control debate
- Firm profiles: Blackstone Real Estate, Fannie Mae, D.R. Horton

### Files Created/Modified

```
book/part2/
└── ch05-real-estate.md ✓ (NEW - ~7,000 words)

_planning/
├── session_log.md (updated)
└── source_tracking.md (updated)
```

### Session 3 Summary Statistics

- **New chapters drafted**: 1 (Ch5 Real Estate)
- **Total chapters drafted**: 8 (Ch4, Ch5, Ch6, Ch7, Ch8, Ch14, Ch15)
- **Total estimated word count**: ~46,500 words across all drafted chapters
- **Cross-project materials integrated**: City Economies housing, 2008 Crisis mortgage finance

### Next Session Priorities

1. **Draft Ch13 Construction** - Goolsbee/Syverson sources ready in `_data/construction_sources.md`
2. **Draft Ch11 Tech/Media** - 100+ sources already collected
3. **Create figures** for drafted chapters

---

## Session 3 (continued): January 12, 2026

### Additional Accomplishments

**2. Chapter 10: Retail and Wholesale Trade Drafted**
- Created `book/part2/ch10-retail-wholesale.md` (~7,500 words)
- Integrated Gemini sources (`_data/retail_sources.md`) plus expanded content
- Comprehensive coverage:
  - Format evolution: wheel of retailing, Hortaçsu & Syverson JEP framing
  - The Big Four: Walmart ($569B), Amazon ($274B), Costco ($183B), Target ($107B)
  - Wholesale infrastructure: McKesson, Sysco, pharmaceutical distribution oligopoly
  - Geographic patterns: Walmart's rural empire, Amazon's fulfillment archipelago, regional grocery strongholds
  - Workforce: 21.5M total employment, wage dynamics, Amazon $15 wage spillovers
  - Regulation: Kroger-Albertsons blocked (Dec 2024), Tesla direct sales battles, alcohol laws
  - Trade associations: NRF, NADA (auto dealers as powerful state lobby)
  - Recent trends: e-commerce plateau (16-22%), retail apocalypse myth, omnichannel convergence, returns crisis
- Firm profiles: Walmart, Amazon, Costco

**3. Chapter 13: Construction Drafted**
- Created `book/part2/ch13-construction.md` (~7,000 words)
- Integrated Goolsbee/Syverson productivity puzzle framing + D'Amico/Glaeser regulation research
- Comprehensive coverage:
  - Productivity puzzle: construction productivity has FALLEN since 1970 (unique among industries)
  - Why: fragmentation, regulation limiting scale, de-skilling (Allen 1985)
  - Industry structure: 800,000 fragmented firms vs consolidating homebuilders (top 10 = 45%)
  - Major players: Bechtel, Turner, Fluor, Kiewit (heavy civil); D.R. Horton, Lennar (residential)
  - Workforce: 8.3M workers, 30% immigrant labor, aging crisis, 500K+ worker shortage
  - Geographic shift: Sunbelt boom (TX, FL, AZ) vs coastal constraints
  - Recent trends: Manufacturing supercycle (CHIPS Act fabs tripled spending), IIJA infrastructure, cost volatility, modular potential
- Firm profiles: Bechtel (megaprojects), Turner Construction (commercial), D.R. Horton (industrialized homebuilding)

**4. Figures Created (10 total)**
- Created `_scripts/create_chapter_figures.py` for reproducible figure generation
- Ch5 Real Estate (3 figures):
  - `ch05_top_homebuilders.pdf` - Top 10 homebuilders by homes closed
  - `ch05_top_reits.pdf` - Top 10 REITs by market cap
  - `ch05_house_price_trends.pdf` - Case-Shiller index 2000-2024
- Ch10 Retail (3 figures):
  - `ch10_top_retailers.pdf` - Top 10 retailers by revenue
  - `ch10_ecommerce_share.pdf` - E-commerce share trend
  - `ch10_format_evolution.pdf` - Wheel of retailing timeline
- Ch13 Construction (4 figures):
  - `ch13_construction_spending.pdf` - Spending by type
  - `ch13_productivity_puzzle.pdf` - Construction vs manufacturing productivity
  - `ch13_top_contractors.pdf` - Top contractors by revenue
  - `ch13_manufacturing_supercycle.pdf` - CHIPS Act spending surge

### Session 3 Final Statistics

- **New chapters drafted this session**: 3 (Ch5 Real Estate, Ch10 Retail, Ch13 Construction)
- **New figures created this session**: 10
- **Total chapters drafted**: 10 (Ch4, Ch5, Ch6, Ch7, Ch8, Ch10, Ch13, Ch14, Ch15)
- **Total figures created**: 17 (Ch1: 3, Ch4: 4, Ch5: 3, Ch10: 3, Ch13: 4)
- **Total estimated word count**: ~61,000 words across all drafted chapters

---

## Pending Research Tasks

- [ ] Find JEP survey on retail economics
- [ ] Find JEP survey on transportation/logistics
- [ ] Find construction industry sources (AGC, ENR)
- [ ] Compile Fed Beige Books for regional chapters
- [ ] Download CRS reports on key industries
- [ ] Find FHFA housing data for real estate chapter

---

## Session 4: January 12, 2026

### Accomplishments

**1. Chapter 11: Information, Technology, and Media Drafted**
- Created `book/part2/ch11-tech-media.md` (~8,000 words)
- Used Gemini for contemporary data research (Big Tech financials, telecom shares, streaming, antitrust)
- Saved research to `_data/ch11_tech_media_sources.md`

**Content Coverage:**
- Industry overview: Information sector (NAICS 51), ~$1.8T GDP, market cap dominance
- Business models: Advertising (Google, Meta), subscriptions (Netflix, Spotify), hardware ecosystem (Apple), cloud (AWS/Azure/GCP), telecommunications
- Big Tech profiles: Alphabet ($307B), Apple ($383B), Amazon ($575B), Meta ($135B), Microsoft ($228B)
- Telecom structure: AT&T, Verizon, T-Mobile (wireless); Comcast, Charter (broadband)
- Media/streaming: Netflix (302M subs), Disney+, Max, Paramount+, Peacock
- Music industry: Universal, Sony, Warner (three majors); Spotify dominance
- Newspaper decline: employment collapse from 455K to <100K
- Geographic concentration: Silicon Valley, Seattle, NYC, Austin, Boston
- Regulatory structure: FCC, Section 230, antitrust enforcement
- Recent antitrust: DOJ v Google (guilty Aug 2024), Epic v Apple, FTC v Amazon, FTC v Meta
- AI boom: Microsoft/OpenAI ($13B), Amazon/Anthropic ($8B), Google/Anthropic ($2B)
- Firm profiles: Alphabet/Google, AT&T, Netflix

**2. Research Materials Saved**
- Created `_data/ch11_tech_media_sources.md` with Gemini research data
- Documented cross-project resources (antitrust digital markets chapter)
- Identified additional data needs

### Files Created/Modified

```
book/part2/
└── ch11-tech-media.md ✓ (NEW - ~8,000 words)

_data/
└── ch11_tech_media_sources.md ✓ (NEW - Gemini research)

_planning/
├── session_log.md (updated)
└── source_tracking.md (to update)
```

### Session 4 Summary Statistics

- **New chapters drafted**: 1 (Ch11 Tech/Media)
- **Total chapters drafted**: 11 (Ch4, Ch5, Ch6, Ch7, Ch8, Ch10, Ch11, Ch13, Ch14, Ch15)
- **Total estimated word count**: ~69,000 words across all drafted chapters

### Next Session Priorities

1. **Draft Ch9 (Manufacturing)** - needs source research via Gemini
2. **Draft Ch12 (Transportation)** - needs source research (airlines covered, missing trucking/ports)
3. **Create figures** for Ch11 and other drafted chapters
4. Continue with Part III-VI chapters as sector chapters complete

---

## Session 4 (continued): January 12, 2026

### Additional Accomplishments

**3. Chapter 9: Manufacturing Drafted**
- Created `book/part2/ch09-manufacturing.md` (~8,500 words)
- Extracted text from Supply Chain Review PDF (383 pages, 6.4MB)
- Used Gemini for contemporary data research (GDP, employment, subsectors, companies, geography)
- Saved research to `_data/ch09_manufacturing_data.md` and `_data/supply_chain_review_extract.txt`

**Content Coverage:**
- Industry overview: $2.3T GDP (10.2%), 12.8M employment (down from 17.3M in 2000)
- The productivity paradox: output doubled while employment halved
- Subsectors: Chemicals (#1 value), Transportation Equipment (#1 employment), Electronics, Food, Machinery
- Major manufacturers table: Apple, Ford, GM, Tesla, J&J, Boeing, RTX, Caterpillar, Deere, Pfizer, Intel, Dow
- Geographic patterns: Manufacturing Belt (Midwest), Battery Belt (South), Aerospace clusters, Pharma hubs
- Productivity and automation: US robot density (295) vs China (470), Germany (429), Japan (419)
- Trade: $1.06T goods deficit; CHIPS Act ($52.7B → $200B+ private); IRA ($86B+ clean energy)
- Industrial policy shift: Supply chain resilience, reshoring, strategic investment
- Manufacturing construction boom (doubled to $225B annual)
- Firm profiles: Caterpillar (machinery), Pfizer (pharmaceuticals), Deere (precision ag)

**Source Materials Used:**
- Quadrennial Supply Chain Review (Dec 2024) - extracted first 50 pages
- Gemini research on contemporary data
- Helper & Henderson (2014) GM paper (referenced)

### Session 4 Final Statistics

- **New chapters drafted this session**: 2 (Ch11 Tech/Media, Ch9 Manufacturing)
- **Total chapters drafted**: 12 (Ch4, Ch5, Ch6, Ch7, Ch8, Ch9, Ch10, Ch11, Ch13, Ch14, Ch15)
- **Total estimated word count**: ~77,500 words across all drafted chapters

### Next Session Priorities

1. **Draft Ch12 (Transportation)** - needs Gemini research (trucking, ports, logistics; airlines/railroads partially covered)
2. **Create figures** for newly drafted chapters (Ch9, Ch11)
3. **Begin Part I chapters** (Ch1-3) - Overview chapters
4. Continue with Part III-VI as sector chapters complete

---

## Session 5: January 12, 2026

### Accomplishments

**1. Chapter 12: Transportation and Logistics Drafted**
- Created `book/part2/ch12-transportation.md` (~8,000 words)
- Used Gemini for comprehensive research (trucking, rail, airlines, ports, logistics)
- Saved research to `_data/ch12_transportation_data.md`

**Content Coverage:**
- Industry overview: $935B GDP, 6.58M employment, modal split
- Trucking: 900K carriers, fragmentation, driver shortage, LTL vs TL segments
- Freight Rail: Class I duopoly (UP/BNSF West, CSX/NS East), PSR controversy, 2022 labor crisis
- Airlines: Big Four consolidation (70% share), cargo (FedEx Memphis, UPS Louisville, Amazon Air)
- Ports: LA/Long Beach dominance, Jones Act costs, 2021-22 congestion crisis
- Logistics: 3PL market ($247B), Amazon Logistics (27% parcel share), warehouse boom
- Geographic patterns: Chicago rail nexus, Inland Empire warehouses, freight corridors
- Regulation: Deregulation history (1978-1980), DOT/FMCSA/FRA/STB/FAA
- Recent trends: E-commerce transformation, autonomous trucking, supply chain resilience
- Firm profiles: UPS, Union Pacific, Amazon Logistics

### Session 5 Summary Statistics

- **New chapters drafted**: 1 (Ch12 Transportation)
- **Total chapters drafted**: 13 (Ch4-15, all Part II complete!)
- **Total estimated word count**: ~85,500 words across all drafted chapters
- **Part II Status**: COMPLETE (all 12 sector chapters drafted)

### Milestone Achieved

**All Part II sector chapters are now drafted:**
- Ch4: Government (~6,500 words)
- Ch5: Real Estate (~7,000 words)
- Ch6: Healthcare (~4,500 words)
- Ch7: Professional Services (~5,500 words)
- Ch8: Finance and Insurance (~7,000 words)
- Ch9: Manufacturing (~8,500 words)
- Ch10: Retail and Wholesale (~7,500 words)
- Ch11: Tech/Media (~8,000 words)
- Ch12: Transportation (~8,000 words)
- Ch13: Construction (~7,000 words)
- Ch14: Energy (~7,500 words)
- Ch15: Education (~6,500 words)

### Next Session Priorities

1. **Begin Part I chapters** (Ch1-3) - Overview chapters
   - Ch1: The American Economy in Numbers
   - Ch2: How the Parts Fit Together
   - Ch3: The Geography of American Production
2. **Create figures** for Ch12 and other chapters needing visualizations
3. **Begin Part III** (Financial Architecture: Ch16-18)
4. Pull actual BEA/BLS data for all drafted chapters

---

## Notes for Future Sessions

- User has Gemini Ultra access for intensive research tasks
- Cross-project materials are extensive - prioritize reading over new research
- All Part II sector chapters are now COMPLETE
- City Economies housing materials ready for Ch5 Real Estate adaptation
- 2008 Crisis mortgage chapters available for Ch5 and Ch16
- User prefers: direct communication, skip pleasantries, push back when needed
