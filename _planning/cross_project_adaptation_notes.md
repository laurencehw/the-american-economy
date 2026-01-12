# Cross-Project Adaptation Notes

How to adapt materials from other book projects for The American Economy.

---

## Public Econ Ch15 (Education) → American Economy Ch15 (Education)

### Source File
`G:\My Drive\book drafts\public econ\chapters\ch15_education\ch15_education_v1.md`

### What's Already There (Usable)
- Human capital theory framework
- Returns to education evidence
- K-12 system structure, funding, inequality
- School choice (charters, vouchers) analysis
- Higher education: access, financing, student debt
- Early childhood education evidence
- International comparisons (PISA data)
- Achievement gaps analysis

### What Needs to Be Added/Changed

**Add industry structure elements:**
- For-profit education sector (K12 Inc., Grand Canyon, etc.)
- Education technology companies
- Textbook and curriculum publishers
- Testing companies (College Board, ACT, ETS, Pearson)
- Major education management organizations (EMOs)
- Education lobbying (NEA, AFT, school boards associations)

**Add geographic dimension:**
- Map of per-pupil spending by state
- Geographic distribution of charter schools
- Higher ed concentration (college towns, research universities)
- State variation in education governance

**Add workforce details:**
- Teacher labor market (shortages, wages, turnover)
- Higher ed faculty (tenure track vs. adjunct)
- Education administration growth

**Reframe:**
- Less emphasis on policy evaluation
- More emphasis on "how the system works"
- Add firm profiles: Pearson, College Board, major university systems

### Estimated Effort
Medium - significant material to reuse, but needs restructuring and additions.

---

## Macro Ch11 (Banking) → American Economy Ch8 + Ch16

### Source File
`G:\My Drive\book drafts\macroeconomics\chapters\part3_financial\ch11_banking.md`

### What's Already There (Usable)
- Bank balance sheet fundamentals
- Net interest margin, deposit betas
- Maturity transformation concept
- Diamond-Dybvig model (simplified)
- Capital and leverage
- March 2023 bank runs (SVB, Signature, First Republic)
- Shadow banking
- Post-crisis regulation

### What Needs to Be Added/Changed

**Add industry structure elements:**
- Ranking of largest banks by assets, deposits
- Geographic distribution of banking (money centers, regionals, community banks)
- Bank holding company structure
- Major non-bank financial companies
- Insurance industry overview (needs separate development)

**Add institutional detail:**
- Fed structure (12 regional banks, Board)
- OCC, FDIC, state regulators
- CFPB and consumer finance
- Fintech/neobank sector

**Split into two chapters:**
- Ch8: Finance and Insurance sector overview (industry structure focus)
- Ch16: How American Finance Works (system mechanics)

### Estimated Effort
Medium-High - good conceptual material but needs industry data overlay.

---

## 2008 Crisis Chapters → American Economy Ch5 + Ch8

### Source Files
- `Chapter_05_Mortgage_Finance_Industry_Structure`
- `Chapter_06_Financial_Accelerator_and_Shadow_Banking`
- `Chapter_07_Leverage_and_Securitization`

### Usable Material
- Mortgage finance chain (originators → securitizers → investors)
- GSE structure (Fannie Mae, Freddie Mac)
- Shadow banking entities (money market funds, repo, SIVs)
- MBS/CDO structure

### What Needs Updating
- Post-crisis reforms (Dodd-Frank effects)
- Current state of mortgage market (2020s)
- Non-bank mortgage originators (Rocket Mortgage, etc.)
- Housing market post-COVID

### For Chapter
- Ch5 (Real Estate): Mortgage system section
- Ch8 (Finance): Shadow banking, securitization

---

## Antitrust IO Toolkit → All Sector Chapters

### Source File
`G:\My Drive\book drafts\antitrust\chapters\04-io-toolkit.qmd`

### Usable Concepts
- Market definition methodology
- Concentration measures (HHI, CR4)
- Entry barriers analysis
- Competitive effects framework

### Application
Every sector chapter should include:
- Concentration data (HHI or CR4 where available)
- Major player market shares
- Entry barrier discussion
- Competitive dynamics

### Template Addition
Add to sector chapter template:
```
### Market Concentration
[HHI or CR4 data]
[Description of competitive dynamics]
[Entry barriers]
```

---

## City Economies → American Economy Ch3, Ch5, Ch21-25

### Source Files
- `03_housing_markets/` - Housing chapter
- `04_transportation/` - Urban transportation
- `09_financing_cities/` - Municipal finance

### Usable Material
- Agglomeration economics concepts
- Urban vs. suburban vs. rural distinctions
- Housing market dynamics
- Urban transportation economics

### For Chapters
- Ch3 (Geography of Production): Agglomeration theory
- Ch5 (Real Estate): Housing markets section
- Ch21-25 (Regional): Urban economic frameworks

---

## Public Econ Budget/Fiscal Chapters → American Economy Ch4

### Source Files
- `ch22_federal_budget/`
- `ch23_fiscal_federalism/`

### Usable Material
- Federal budget structure and process
- Mandatory vs. discretionary spending
- Federal-state-local fiscal relationships
- Tax system overview

### What Needs Adding
- Government as employer (federal, state, local workforce)
- Government as purchaser (procurement, contracting)
- Regulatory agencies overview
- Defense industrial base

---

## Jesse Jenkins Electricity Course → American Economy Ch14

### Source Files
`G:\My Drive\book drafts\the american economy\_3industries\0. Infrastructure\energy\Intro to Electricity 2024 lectures for sharing\`
- Princeton ENE 522 syllabus and lecture materials

### What Was Used
- Course structure for electricity section organization
- Regulated vs. restructured market framework
- ISO/RTO system overview
- Generation mix transformation narrative
- Grid interconnections (Eastern, Western, ERCOT)

### What Was Added
- Oil and gas sector (shale revolution, value chain, major basins)
- Renewables buildout (IRA incentives, storage deployment)
- Industry structure (utilities, oil majors, independents, renewable developers)
- Geographic patterns (producing vs. consuming states)
- Firm profiles (NextEra, ExxonMobil, Duke Energy)

### Status
**COMPLETED** (Session 2, Jan 11 2026) → Ch14 drafted (~7,500 words)

---

## Priority Order for Adaptation

1. ~~**Education (Public Econ Ch15)**~~ - **COMPLETED** (Session 2, Jan 11 2026)
2. ~~**Banking (Macro Ch11)**~~ - **COMPLETED** (Session 2, Jan 11 2026) → Ch8 drafted; Ch16 pending
3. ~~**Federal Budget (Public Econ Ch22/23)**~~ - **COMPLETED** (Session 2, Jan 11 2026) → Ch4 drafted
4. ~~**Energy (Jenkins Course)**~~ - **COMPLETED** (Session 2, Jan 11 2026) → Ch14 drafted
5. **Housing (City Economies)** - Useful for Real Estate chapter
6. **IO Toolkit (Antitrust)** - Framework for all sector chapters

---

## Technical Notes

When adapting:
- Strip LaTeX commands incompatible with GitBook (`\newpage`, `\vspace`, etc.)
- Convert footnotes to inline or endnotes
- Ensure $$ math blocks are on own lines
- Update data to 2022-2023 where possible
- Add firm profiles and geographic maps
- Reframe policy discussions as descriptive rather than normative
