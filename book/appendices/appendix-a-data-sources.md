# Appendix A: Data Sources Guide

This appendix provides an overview of the primary data sources used throughout this book, along with guidance on how to access and interpret them.

## Bureau of Economic Analysis (BEA)

The BEA, housed within the Department of Commerce, produces the foundational measures of the U.S. economy.

### Key Products

**Gross Domestic Product (GDP)**
- Quarterly and annual estimates of U.S. economic output
- Released monthly (advance, second, and third estimates)
- Access: [bea.gov/data/gdp](https://www.bea.gov/data/gdp)

**Industry Accounts**
- GDP by industry (NAICS-based)
- Input-output tables showing inter-industry flows
- Annual and benchmark tables
- Access: [bea.gov/industry](https://www.bea.gov/industry)

**Regional Economic Accounts**
- State GDP (quarterly and annual)
- Metropolitan area GDP (annual)
- Personal income by state and county
- Access: [bea.gov/regional](https://www.bea.gov/regional)

**International Transactions**
- Balance of payments
- Trade in goods and services
- Foreign direct investment
- Access: [bea.gov/international](https://www.bea.gov/international)

### How to Access

- **Interactive Tables**: BEA's website offers customizable data retrieval
- **API**: Free API access for programmatic retrieval (registration required)
- **FRED**: Many BEA series available through Federal Reserve Economic Data

---

## Bureau of Labor Statistics (BLS)

The BLS, within the Department of Labor, produces employment and price statistics.

### Key Products

**Current Employment Statistics (CES)**
- Monthly employment by industry (nonfarm payrolls)
- Average hourly earnings
- Hours worked
- The "jobs report" released first Friday of each month
- Access: [bls.gov/ces](https://www.bls.gov/ces)

**Quarterly Census of Employment and Wages (QCEW)**
- Employment and wages by industry and geography
- Derived from unemployment insurance records
- Covers 95%+ of jobs
- Access: [bls.gov/qcew](https://www.bls.gov/qcew)

**Occupational Employment and Wage Statistics (OEWS)**
- Employment and wages by detailed occupation
- Metropolitan area detail
- Access: [bls.gov/oes](https://www.bls.gov/oes)

**Consumer Price Index (CPI)**
- Monthly inflation measure
- Multiple series (all items, core, by region)
- Access: [bls.gov/cpi](https://www.bls.gov/cpi)

**Producer Price Index (PPI)**
- Wholesale/producer-level prices by industry
- Access: [bls.gov/ppi](https://www.bls.gov/ppi)

**Productivity and Costs**
- Labor productivity by sector
- Unit labor costs
- Access: [bls.gov/lpc](https://www.bls.gov/lpc)

### How to Access

- **Data Retrieval Tools**: BLS offers customizable series selection
- **API**: Free API access for bulk retrieval
- **FRED**: Most major BLS series available through FRED

---

## Census Bureau

The Census Bureau, within the Commerce Department, conducts surveys and the decennial census.

### Key Products

**Economic Census** (every 5 years)
- Comprehensive establishment-level data by industry
- Employment, payroll, revenue by NAICS code
- Geographic detail to county level
- Access: [census.gov/econ](https://www.census.gov/econ)

**Annual Business Survey**
- Annual updates between Economic Censuses
- Business characteristics and innovation

**County Business Patterns**
- Annual employment and establishments by industry and county
- Access: [census.gov/programs-surveys/cbp](https://www.census.gov/programs-surveys/cbp)

**American Community Survey (ACS)**
- Annual demographic, housing, and economic characteristics
- 1-year and 5-year estimates
- Access: [census.gov/acs](https://www.census.gov/acs)

**Trade Data**
- USA Trade Online: Detailed imports and exports
- Access: [usatrade.census.gov](https://usatrade.census.gov)

---

## Federal Reserve

The Federal Reserve System produces financial and monetary data.

### Key Products

**Financial Accounts of the United States (Z.1)**
- Flow of funds, balance sheets
- Sectoral balances (households, corporations, government)
- Quarterly release
- Access: [federalreserve.gov/releases/z1](https://www.federalreserve.gov/releases/z1)

**H.4.1 Release**
- Federal Reserve balance sheet
- Weekly

**H.8 Release (Assets and Liabilities of Commercial Banks)**
- Weekly data on bank credit, loans, and securities holdings
- Key for tracking lending conditions and bank balance sheets
- Access: [federalreserve.gov/releases/h8](https://www.federalreserve.gov/releases/h8)

**Industrial Production and Capacity Utilization**
- Monthly output by industry
- Capacity utilization rates
- Access: [federalreserve.gov/releases/g17](https://www.federalreserve.gov/releases/g17)

**Survey of Consumer Finances**
- Triennial household wealth and debt survey
- Access: [federalreserve.gov/econres/scfindex.htm](https://www.federalreserve.gov/econres/scfindex.htm)

**FRED (Federal Reserve Economic Data)**
- Aggregates data from BEA, BLS, Census, and many other sources
- Easy-to-use interface, API access
- Access: [fred.stlouisfed.org](https://fred.stlouisfed.org)

---

## Agency-Specific Sources

### Energy

**Energy Information Administration (EIA)**
- Comprehensive energy production, consumption, prices
- State Energy Data System (SEDS)
- Access: [eia.gov](https://www.eia.gov)

### Healthcare

**Centers for Medicare & Medicaid Services (CMS)**
- National Health Expenditure Accounts
- Medicare and Medicaid data
- Access: [cms.gov/data-research](https://www.cms.gov/data-research)

### Agriculture

**USDA Economic Research Service**
- Farm income, food expenditure, rural statistics
- Access: [ers.usda.gov](https://www.ers.usda.gov)

**USDA National Agricultural Statistics Service (NASS)**
- Crop production, prices, farm counts
- Access: [nass.usda.gov](https://www.nass.usda.gov)

### Finance

**FDIC**
- Bank financial data, deposit data
- Access: [fdic.gov/bank/statistical](https://www.fdic.gov/bank/statistical)

**SEC EDGAR**
- Public company filings (10-K, 10-Q, proxy statements)
- Access: [sec.gov/edgar](https://www.sec.gov/edgar)

### Transportation

**Bureau of Transportation Statistics (BTS)**
- Freight, passenger, infrastructure data
- Access: [bts.gov](https://www.bts.gov)

---

## International and Comparative Data

**World Bank Open Data**
- Cross-country economic indicators
- Access: [data.worldbank.org](https://data.worldbank.org)

**OECD Statistics**
- Developed economy comparisons
- Access: [stats.oecd.org](https://stats.oecd.org)

**UN Comtrade**
- Detailed international trade data
- Access: [comtrade.un.org](https://comtrade.un.org)

**IMF Data**
- Balance of payments, financial statistics
- Access: [data.imf.org](https://data.imf.org)

---

## Publication Calendar: Key Economic Data Releases

Knowing when data arrives---and how much it is revised---is essential for interpreting economic statistics in real time.

| Release | Frequency | Typical Timing | Lag | Revision Magnitude |
|---------|-----------|---------------|-----|-------------------|
| Employment Situation (BLS) | Monthly | First Friday of month | ~5 days | ±30,000-100,000 jobs in annual benchmark |
| GDP (BEA advance estimate) | Quarterly | ~30 days post-quarter | 30 days | ±1.0-1.5 pp from advance to third estimate |
| GDP (BEA second estimate) | Quarterly | ~60 days post-quarter | 60 days | ±0.5 pp from second to third |
| GDP (BEA third estimate) | Quarterly | ~90 days post-quarter | 90 days | Further revised in annual/comprehensive revisions |
| CPI (BLS) | Monthly | ~15th of following month | 15 days | Rarely revised; seasonal factors updated annually |
| PPI (BLS) | Monthly | ~15th of following month | 15 days | Minor revisions |
| Industrial Production (Fed) | Monthly | ~15th of following month | 15 days | Frequently revised |
| Personal Income and Spending (BEA) | Monthly | ~30 days post-month | 30 days | ±0.2-0.5 pp on spending |
| JOLTS (BLS) | Monthly | ~55 days post-month | 55 days | Modest revisions |
| State GDP (BEA) | Quarterly | ~6 months lag | 180 days | Substantial revisions possible |
| Economic Census (Census) | Every 5 years | 2-3 years after reference year | 2-3 years | Benchmark data; not revised |
| Census of Agriculture (USDA) | Every 5 years | ~2 years after reference year | 2 years | Benchmark data |

### Revision Caveats

GDP estimates illustrate the revision problem. The advance estimate of Q1 2023 GDP growth was 1.1% (annualized); the third estimate revised this to 2.0%---a near-doubling. Annual comprehensive revisions can change GDP levels by tens of billions of dollars and alter the picture of entire business cycles. The lesson: treat early estimates as useful signals, not settled facts.

### Seasonal vs. Non-Seasonally Adjusted Data

Most monthly and quarterly series are published in both seasonally adjusted (SA) and not seasonally adjusted (NSA) forms. Use seasonally adjusted data for tracking trends and comparing across months. Use non-seasonally adjusted data when analyzing a specific month's level or when seasonal patterns themselves are the object of study. Be aware that seasonal adjustment factors are re-estimated annually and can change historical data retroactively.

## Tips for Using Government Data

1. **Check Vintage**: Economic data is revised frequently. The first release differs from final estimates. Always note the release date of the data you cite.

2. **Understand Seasonal Adjustment**: Most monthly/quarterly data is seasonally adjusted. Use adjusted figures for trend analysis, unadjusted for specific period comparisons.

3. **Note Geographic Coverage**: Some series cover all establishments; others sample. The CES survey covers ~145,000 businesses; the QCEW covers 95%+ of all jobs. Sampling error increases at detailed geographic and industry levels.

4. **Mind NAICS Changes**: The NAICS classification system is revised every 5 years. Historical comparisons may require concordances. The 2022 revision significantly reclassified parts of information and retail.

5. **Use APIs for Reproducibility**: Programmatic access via APIs ensures your analysis can be replicated and updated.

6. **Beware of Coverage Gaps**: The gig economy, informal work, and some financial activities are poorly captured by establishment surveys. The Quarterly Census of Employment and Wages misses self-employment entirely. The Current Population Survey captures it but with measurement error.

---

## Further Resources

- **Data.gov**: Central portal for federal open data
- **USAFacts**: Non-profit aggregating government data
- **IPUMS**: Harmonized Census and survey microdata
- **ICPSR**: Academic data archive with many government series
