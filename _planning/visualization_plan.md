# Visualization Plan: The American Economy

**Purpose:** Make institutional detail concrete through maps, charts, tables, and visual elements.

---

## Visual Style Standards

### General Principles (per global CLAUDE.md)
- **Library:** plotnine with hrbrthemes (`theme_ipsum()`) or matplotlib fallback
- **Width:** 6 inches (single column)
- **Format:** Both PDF (print) and PNG (web/GitBook) at 300 DPI
- **Style:** Minimal gridlines, clean axis labels
- **Source notes:** Required at bottom of every figure
- **Time series:** Use real (inflation-adjusted) values for long-term comparisons

### plotnine Setup
```python
from plotnine import *
from hrbrthemes import theme_ipsum

# Base theme for all figures
base_theme = theme_ipsum() + theme(
    figure_size=(6, 4),
    plot_caption=element_text(size=8, style='italic')
)
```

### Color Approach
- Use hrbrthemes default palette where possible
- For categorical: limit to 6-7 distinct colors max
- For sequential (maps, gradients): single-hue progression
- For diverging: use sparingly, centered on meaningful zero

### Map Standards
- State-level choropleth as default
- County-level for detailed analysis
- Use sequential color scales (light to dark)
- Always include legend with units
- Metropolitan areas shown as points when relevant
- Use geopandas + matplotlib for maps (plotnine map support limited)

---

## Visualization Types

### 1. Maps (Geographic Distribution)

**Choropleth Maps** - Show intensity by geography
- Employment concentration by state
- Per capita measures (spending, income, output)
- Industry specialization (location quotients)

**Point Maps** - Show discrete locations
- Major facilities (headquarters, plants, bases)
- Infrastructure (ports, pipelines, data centers)
- Institution locations (universities, hospitals)

**Boundary Maps** - Show jurisdictional divisions
- Federal Reserve districts
- Electric grid interconnections
- Regulatory jurisdictions

### 2. Composition Charts

**Treemaps** - Show hierarchical shares
- GDP by industry
- Employment by sector
- Government spending by function

**Stacked Bar/Area** - Show composition over time
- Energy generation mix
- Healthcare spending by payer
- Trade composition

**Pie/Donut** - Show simple shares (use sparingly)
- Market concentration (top 4 vs rest)
- Revenue breakdown

### 3. Comparison Charts

**Horizontal Bar** - Rankings and comparisons
- Top 10 firms by revenue/employment
- Top states by industry employment
- Wage comparisons across sectors

**Grouped Bar** - Category comparisons
- Public vs private employment
- Regulated vs deregulated prices
- Urban vs rural metrics

### 4. Trend Charts

**Line Charts** - Time series
- Employment trends
- Output growth
- Price indices

**Area Charts** - Cumulative trends
- Cumulative investment
- Market share evolution

### 5. Relationship Charts

**Scatter Plots** - Correlations
- Size vs concentration
- Wages vs productivity
- Spending vs outcomes

**Connected Scatter** - Change over time
- State migration patterns
- Industry evolution

### 6. Flow Diagrams

**Sankey Diagrams** - Value flows
- Healthcare payment flows
- Energy from source to consumer
- Trade flows

**Process Diagrams** - How things work
- Mortgage securitization chain
- Electricity from generator to outlet
- Regulatory approval processes

### 7. Tables

**Ranking Tables** - Top N lists
- Largest firms
- Most concentrated markets
- Highest-paying industries

**Comparison Tables** - Side-by-side
- Regulatory agency jurisdictions
- State policy variations
- Market structure types

**Data Tables** - Reference statistics
- Industry size metrics
- Geographic breakdowns
- Time series data

### 8. Boxes and Callouts

**Firm Profile Boxes** - 2-3 per sector chapter
- Company name, headquarters, key stats
- Business model summary
- Recent developments
- ~200 words each

**"How It Works" Boxes** - Process explainers
- How electricity prices are set
- How a hospital bill gets paid
- How a mortgage gets securitized

**Data Source Boxes** - For key datasets
- What it measures
- Who produces it
- How to access it
- Limitations

**Historical Context Boxes** - Path dependence
- Why the system looks this way
- Key turning points
- Regulatory origins

---

## Chapter-by-Chapter Visualization Plan

### Part I: The Shape of the Economy

#### Chapter 1: The Economy in Numbers

| Visual | Type | Data Source | Priority | Status |
|--------|------|-------------|----------|--------|
| GDP composition treemap | Treemap | BEA Industry Accounts | HIGH | **DONE** |
| Employment by sector | Horizontal bar | BLS CES | HIGH | **DONE** |
| GDP vs employment shares comparison | Dumbbell | BEA, BLS | HIGH | **DONE** |
| How GDP is measured | Process diagram | Original | MEDIUM |
| NAICS hierarchy | Tree diagram | Census | MEDIUM |
| Data agency overview table | Table | Original | HIGH |

#### Chapter 2: How It Fits Together

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Simplified I-O diagram | Sankey/flow | BEA I-O Tables | HIGH |
| Consumer expenditure breakdown | Treemap | BLS CEX | HIGH |
| Flow of funds overview | Sankey | Fed Z.1 | MEDIUM |
| Major value chains (3) | Process diagrams | Original | HIGH |
| Upstream/downstream linkages | Network diagram | BEA I-O | MEDIUM |

#### Chapter 3: Geography of Production

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| GDP by state choropleth | Map | BEA Regional | HIGH |
| Employment density map | Map | BLS QCEW | HIGH |
| Metro area economic output | Point map | BEA Metro | HIGH |
| Location quotients by industry | Small multiples maps | BLS QCEW | MEDIUM |
| Urban vs rural employment | Grouped bar | BLS | MEDIUM |
| Top 20 metros by GDP | Horizontal bar | BEA | HIGH |

---

### Part II: The Sectors

#### Chapter 4: Government

| Visual | Type | Data Source | Priority | Status |
|--------|------|-------------|----------|--------|
| Government employment by level | Stacked bar | BLS CES | HIGH | **DONE** |
| Federal spending by function | Treemap | OMB Budget | HIGH | **DONE** |
| Federal employment by state | Choropleth | OPM | HIGH | **DONE** |
| Top 10 federal contractors | Horizontal bar | USASpending | HIGH | **DONE** |
| Military installations map | Point map | DOD | MEDIUM |
| Intergovernmental transfers flow | Sankey | Census Gov Finance | MEDIUM |
| Regulatory agencies table | Table | Original | HIGH |
| **Box: Department of Defense** | Firm profile | - | HIGH |
| **Box: California State Government** | Firm profile | - | HIGH |
| **Box: New York City** | Firm profile | - | HIGH |

#### Chapter 5: Real Estate

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Homeownership rate by state | Choropleth | Census ACS | HIGH |
| House price index trends | Line | FHFA, Case-Shiller | HIGH |
| Housing starts time series | Line | Census | MEDIUM |
| Mortgage market structure | Flow diagram | Original | HIGH |
| Commercial real estate by type | Treemap | NCREIF/CoStar | MEDIUM |
| Top REITs by market cap | Horizontal bar | NAREIT | MEDIUM |
| Rent burden by metro | Horizontal bar | Census ACS | HIGH |
| **Box: Blackstone Real Estate** | Firm profile | - | HIGH |
| **Box: Zillow Group** | Firm profile | - | HIGH |
| **Box: Fannie Mae** | Firm profile | - | HIGH |

#### Chapter 6: Healthcare

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Healthcare spending by category | Treemap | CMS NHE | HIGH |
| Healthcare spending over time | Stacked area | CMS NHE | HIGH |
| Hospital systems by beds | Horizontal bar | AHA | HIGH |
| Health insurance coverage sources | Pie/donut | Census | HIGH |
| Healthcare employment by state | Choropleth | BLS QCEW | MEDIUM |
| Payment flow diagram | Sankey | Original | HIGH |
| Top 10 health insurers | Horizontal bar | NAIC | MEDIUM |
| Top 10 pharma companies | Horizontal bar | Company data | MEDIUM |
| **Box: Kaiser Permanente** | Firm profile | - | HIGH |
| **Box: CVS Health** | Firm profile | - | HIGH |
| **Box: Pfizer** | Firm profile | - | HIGH |
| **How It Works: Hospital billing** | Explainer box | - | MEDIUM |

#### Chapter 7: Professional Services

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Professional services GDP breakdown | Treemap | BEA | HIGH |
| Geographic concentration (NYC, DC, SF) | Point map | BLS QCEW | HIGH |
| Top law firms by revenue | Horizontal bar | Am Law 100 | HIGH |
| Big Four accounting revenue | Horizontal bar | Firm reports | HIGH |
| Top consulting firms | Horizontal bar | Various | MEDIUM |
| Advertising spending by medium | Stacked area | eMarketer | MEDIUM |
| Professional employment by state | Choropleth | BLS QCEW | MEDIUM |
| **Box: McKinsey & Company** | Firm profile | - | HIGH |
| **Box: Kirkland & Ellis** | Firm profile | - | HIGH |
| **Box: Deloitte** | Firm profile | - | HIGH |

#### Chapter 8: Finance and Insurance

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Financial sector GDP breakdown | Treemap | BEA | HIGH |
| Top 10 banks by assets | Horizontal bar | FDIC | HIGH |
| Bank branch map | Point map | FDIC | MEDIUM |
| Insurance premiums by line | Treemap | NAIC | HIGH |
| Asset manager AUM | Horizontal bar | Company data | HIGH |
| Financial employment geography | Choropleth | BLS QCEW | HIGH |
| Regulatory agency jurisdictions | Table | Original | HIGH |
| Bank balance sheet diagram | Diagram | Original | MEDIUM |
| **Box: JPMorgan Chase** | Firm profile | - | HIGH |
| **Box: Berkshire Hathaway Insurance** | Firm profile | - | HIGH |
| **Box: BlackRock** | Firm profile | - | HIGH |
| **How It Works: How a bank makes money** | Explainer box | - | MEDIUM |

#### Chapter 9: Manufacturing

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Manufacturing GDP by subsector | Treemap | BEA | HIGH |
| Manufacturing employment over time | Line | BLS CES | HIGH |
| Manufacturing employment by state | Choropleth | BLS QCEW | HIGH |
| Auto assembly plant locations | Point map | Company data | HIGH |
| Aerospace facility map | Point map | Company data | MEDIUM |
| Top manufacturers by revenue | Horizontal bar | Fortune | HIGH |
| Trade balance by subsector | Horizontal bar | Census Trade | MEDIUM |
| **Box: General Motors** | Firm profile | - | HIGH |
| **Box: Boeing** | Firm profile | - | HIGH |
| **Box: Procter & Gamble** | Firm profile | - | HIGH |

#### Chapter 10: Retail and Wholesale

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Retail sales by category | Treemap | Census Retail | HIGH |
| E-commerce share over time | Line/area | Census | HIGH |
| Top retailers by revenue | Horizontal bar | NRF | HIGH |
| Retail employment by state | Choropleth | BLS QCEW | MEDIUM |
| Store count trends (Walmart, Amazon) | Line | Company data | MEDIUM |
| Wholesale trade flows | Sankey | Census | MEDIUM |
| **Box: Walmart** | Firm profile | - | HIGH |
| **Box: Amazon** | Firm profile | - | HIGH |
| **Box: Costco** | Firm profile | - | HIGH |

#### Chapter 11: Information and Technology

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Tech sector GDP breakdown | Treemap | BEA | HIGH |
| Big Tech revenue comparison | Horizontal bar | Company data | HIGH |
| Tech employment geography | Choropleth + points | BLS QCEW | HIGH |
| Data center locations | Point map | Various | MEDIUM |
| Digital advertising market share | Treemap | eMarketer | HIGH |
| Telecom market structure | Treemap | FCC | MEDIUM |
| Internet traffic growth | Line | Cisco | MEDIUM |
| **Box: Apple** | Firm profile | - | HIGH |
| **Box: Google/Alphabet** | Firm profile | - | HIGH |
| **Box: AT&T** | Firm profile | - | HIGH |

#### Chapter 12: Transportation and Warehousing

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Transportation GDP by mode | Treemap | BEA | HIGH |
| Freight tonnage by mode | Horizontal bar | BTS | HIGH |
| Major port throughput | Horizontal bar | AAPA | HIGH |
| Port locations map | Point map | AAPA | HIGH |
| Freight rail network map | Line map | STB | MEDIUM |
| Top trucking companies | Horizontal bar | Company data | MEDIUM |
| Airline market share | Treemap | DOT | HIGH |
| Warehouse growth over time | Line | CBRE | MEDIUM |
| **Box: UPS** | Firm profile | - | HIGH |
| **Box: Union Pacific** | Firm profile | - | HIGH |
| **Box: Delta Air Lines** | Firm profile | - | HIGH |

#### Chapter 13: Construction

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Construction spending by type | Treemap | Census Construction | HIGH |
| Construction employment over time | Line | BLS CES | HIGH |
| Construction employment by state | Choropleth | BLS QCEW | HIGH |
| Major construction projects map | Point map | ENR | MEDIUM |
| Top contractors by revenue | Horizontal bar | ENR | HIGH |
| Building permits by metro | Horizontal bar | Census | MEDIUM |
| **Box: Bechtel** | Firm profile | - | HIGH |
| **Box: D.R. Horton** | Firm profile | - | HIGH |
| **Box: Turner Construction** | Firm profile | - | HIGH |

#### Chapter 14: Energy

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Electricity generation mix | Stacked area | EIA | HIGH |
| Generation mix by state | Small multiples | EIA | MEDIUM |
| Electric grid interconnections map | Boundary map | EIA | HIGH |
| ISO/RTO territories map | Boundary map | FERC | HIGH |
| Oil production by state | Choropleth | EIA | HIGH |
| Major oil/gas basins map | Boundary map | EIA | HIGH |
| Pipeline network map | Line map | EIA | MEDIUM |
| Top utilities by customers | Horizontal bar | EIA | HIGH |
| Top oil companies by production | Horizontal bar | EIA | HIGH |
| Renewable capacity growth | Stacked area | EIA | HIGH |
| Electricity prices: regulated vs deregulated | Comparison chart | EIA | MEDIUM |
| **Box: NextEra Energy** | Firm profile | - | HIGH |
| **Box: ExxonMobil** | Firm profile | - | HIGH |
| **Box: Duke Energy** | Firm profile | - | HIGH |
| **How It Works: How electricity prices are set** | Explainer box | - | HIGH |

#### Chapter 15: Education

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Education spending by level | Treemap | NCES | HIGH |
| Per-pupil spending by state | Choropleth | NCES | HIGH |
| K-12 enrollment over time | Line | NCES | MEDIUM |
| Higher ed enrollment by type | Stacked bar | NCES | HIGH |
| College endowments (top 20) | Horizontal bar | NACUBO | MEDIUM |
| Research university locations | Point map | NSF | MEDIUM |
| Teacher wages vs state average | Scatter | BLS, NCES | MEDIUM |
| For-profit enrollment collapse | Line | NCES | HIGH |
| **Box: College Board** | Firm profile | - | HIGH |
| **Box: Pearson** | Firm profile | - | HIGH |
| **Box: University of California** | Firm profile | - | HIGH |

---

### Part III: The Financial Architecture

#### Chapter 16: How American Finance Works

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Credit flow diagram | Sankey | Fed Z.1 | HIGH |
| Bank types by assets | Treemap | FDIC | HIGH |
| Fed structure diagram | Org chart | Original | HIGH |
| Mortgage securitization flow | Process diagram | Original | HIGH |
| Interest rate transmission | Process diagram | Original | MEDIUM |
| Shadow banking system | Flow diagram | Original | HIGH |
| **How It Works: How the Fed sets interest rates** | Explainer box | - | HIGH |

#### Chapter 17: Capital Markets

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Stock market capitalization over time | Line | SIFMA | HIGH |
| Bond market size by type | Treemap | SIFMA | HIGH |
| IPO activity over time | Line | SEC | MEDIUM |
| Investor base composition | Pie | Fed Z.1 | HIGH |
| PE/VC dry powder | Line | PitchBook | MEDIUM |
| Foreign holdings of US assets | Stacked area | Treasury | MEDIUM |

#### Chapter 18: Corporate Finance in Practice

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Corporate financing sources | Treemap | Fed Z.1 | HIGH |
| M&A activity over time | Line | Refinitiv | HIGH |
| Public vs private companies | Comparison | Various | MEDIUM |
| Shareholder composition | Pie | SEC | MEDIUM |

---

### Part IV: Trade and Global Linkages

#### Chapter 19: Trading Relationships

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Top trading partners | Horizontal bar | Census Trade | HIGH |
| Trade balance over time | Line | BEA | HIGH |
| Exports by category | Treemap | Census Trade | HIGH |
| Imports by category | Treemap | Census Trade | HIGH |
| Trade with China timeline | Line | Census Trade | HIGH |
| Major ports and trade routes | Map | Various | MEDIUM |

#### Chapter 20: Global Supply Chains

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| FDI positions (inward/outward) | Horizontal bar | BEA | HIGH |
| US MNC foreign employment | Horizontal bar | BEA | MEDIUM |
| Supply chain example (iPhone) | Flow diagram | Original | HIGH |
| Critical imports map | Map | Various | MEDIUM |

---

### Part V: Regional Economies

#### Chapter 21-25: Regional Chapters

Each regional chapter should include:

| Visual | Type | Notes |
|--------|------|-------|
| Regional GDP composition | Treemap | vs national average |
| Employment by sector | Horizontal bar | vs national |
| Major metros map | Point map | with GDP bubbles |
| Industry specialization | Bar chart | Location quotients |
| Population/migration trends | Line | Census |
| Key infrastructure | Map | Ports, hubs, etc. |
| Top employers table | Table | By metro |
| **3 Firm/Institution profiles** | Boxes | Region-specific |

---

### Part VI: Institutions and Governance

#### Chapter 26: Federal Economic Governance

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Regulatory agencies org chart | Diagram | Original | HIGH |
| Agency budgets comparison | Horizontal bar | OMB | MEDIUM |
| Economic policy apparatus | Diagram | Original | HIGH |
| Congressional committee jurisdictions | Table | Original | MEDIUM |

#### Chapter 27: Trade Associations

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Lobbying spending by industry | Horizontal bar | OpenSecrets | HIGH |
| Top trade associations | Table | Original | HIGH |
| Chamber/Roundtable membership | Diagram | Original | MEDIUM |
| Think tank landscape | Positioning chart | Original | MEDIUM |

#### Chapter 28: Labor Organizations

| Visual | Type | Data Source | Priority |
|--------|------|-------------|----------|
| Union membership over time | Line | BLS | HIGH |
| Union density by state | Choropleth | BLS | HIGH |
| Union membership by sector | Horizontal bar | BLS | HIGH |
| Major unions by membership | Horizontal bar | Union data | HIGH |
| Right-to-work states map | Map | Original | MEDIUM |

---

## Production Pipeline

### Phase 1: Core Infrastructure (Priority)
1. Set up plotting templates (plotnine theme)
2. Create state/county shapefiles
3. Build reusable mapping functions
4. Establish color palette constants

### Phase 2: Chapter 1-3 Figures
- GDP treemap
- Employment bar charts
- Geographic distribution maps
- I-O simplified diagram

### Phase 3: Drafted Chapter Figures
Work through figures for Ch4, Ch6, Ch7, Ch8, Ch14, Ch15 in parallel with refinement

### Phase 4: Remaining Chapters
Create figures as chapters are drafted

---

## Data Source Quick Reference

| Source | URL | Key Data |
|--------|-----|----------|
| BEA | bea.gov | GDP, I-O tables, regional accounts |
| BLS | bls.gov | Employment, wages, QCEW |
| Census | census.gov | Economic Census, trade, ACS |
| EIA | eia.gov | Energy production, consumption, prices |
| CMS | cms.gov | Healthcare spending |
| FDIC | fdic.gov | Bank data |
| Fed | federalreserve.gov | Flow of funds, Beige Book |
| NCES | nces.ed.gov | Education statistics |
| SEC | sec.gov | Company filings |

---

## Technical Notes

### Tools
- **Charts:** plotnine with hrbrthemes (`pip install hrbrthemes`)
- **Theme:** `theme_ipsum()` for all charts
- **Mapping:** geopandas + matplotlib (plotnine map support limited)
- **Diagrams:** draw.io or Mermaid for flows
- **Tables:** pandas to LaTeX/Markdown (booktabs style)

### Standard Figure Script Template
```python
from plotnine import *
from hrbrthemes import theme_ipsum
import pandas as pd

# Load data
df = pd.read_csv('data/source.csv')

# Create figure
fig = (
    ggplot(df, aes(x='category', y='value'))
    + geom_col()
    + theme_ipsum()
    + theme(figure_size=(6, 4))
    + labs(
        title='Title Here',
        x='X Label',
        y='Y Label',
        caption='Source: BEA (2023)'
    )
)

# Save
fig.save('ch##_description_type.pdf', dpi=300)
```

### File Organization
```
_figures/
├── ch01/
│   ├── gdp_treemap.pdf
│   ├── gdp_treemap.py
│   └── data/
├── ch02/
├── ...
└── shared/
    ├── state_shapefile/
    └── figure_utils.py
```

### Naming Convention
`ch##_description_type.pdf`
- Example: `ch04_federal_employment_choropleth.pdf`
- Example: `ch08_top_banks_bar.pdf`

---

## Estimated Totals

| Category | Count |
|----------|-------|
| Choropleth maps | ~25 |
| Point/line maps | ~15 |
| Treemaps | ~20 |
| Bar charts | ~50 |
| Line charts | ~20 |
| Flow diagrams | ~15 |
| Tables | ~30 |
| Firm profile boxes | ~75 (3 per sector chapter) |
| Explainer boxes | ~15 |
| **Total visual elements** | **~265** |
