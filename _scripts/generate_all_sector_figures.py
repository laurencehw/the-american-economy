"""
Generate figures for Chapters 5, 9, 10, 11, 12, 13 using plotnine + theme_ipsum.
Adheres to style guidelines in CLAUDE.md.
"""

import pandas as pd
from plotnine import *
from hrbrthemes import theme_ipsum
from pathlib import Path
import matplotlib.pyplot as plt
import textwrap

# Configuration
PROJECT_DIR = Path(r"G:\\My Drive\\book drafts\\the american economy")
FIGURES_DIR = PROJECT_DIR / "_figures"
FIGURE_WIDTH = 6
DPI = 300

def ensure_dir(chapter):
    (FIGURES_DIR / chapter).mkdir(parents=True, exist_ok=True)

def save_plotnine(plot, chapter, filename, height=4.5):
    ensure_dir(chapter)
    pdf_path = FIGURES_DIR / chapter / filename
    png_path = FIGURES_DIR / chapter / filename.replace('.pdf', '.png')
    plot.save(pdf_path, width=FIGURE_WIDTH, height=height, units='in', dpi=DPI, verbose=False)
    plot.save(png_path, width=FIGURE_WIDTH, height=height, units='in', dpi=DPI, verbose=False)
    print(f"Saved: {pdf_path}")

def wrap_title(title):
    return "\n".join(textwrap.wrap(title, width=50))

# =============================================================================
# CHAPTER 5: REAL ESTATE
# =============================================================================

def ch05_top_homebuilders():
    data = pd.DataFrame({
        'builder': ['D.R. Horton', 'Lennar', 'PulteGroup', 'NVR', 'Toll Brothers', 'Meritage', 'Taylor Morrison', 'KB Home', 'Century', 'Dream Finders'],
        'homes': [94, 73, 31, 25, 10, 14, 13, 11, 10, 8]
    })
    data = data.sort_values('homes', ascending=True)
    data['builder'] = pd.Categorical(data['builder'], categories=data['builder'], ordered=True)
    p = (ggplot(data, aes(x='builder', y='homes')) 
         + geom_col(fill='#2E86AB', alpha=0.8) 
         + coord_flip() 
         + theme_ipsum() 
         + theme(plot_margin=0.05, axis_text_x=element_text(size=8))
         + labs(title=wrap_title('Top 10 U.S. Homebuilders by Closings, 2024'), x='', y='Homes Closed (Thousands)', caption='Source: Company Reports'))
    save_plotnine(p, 'ch05', 'ch05_top_homebuilders.pdf')

def ch05_house_price_trends():
    years = list(range(2000, 2025))
    hpi_real = [100, 104, 109, 118, 127, 138, 141, 128, 107, 103, 104, 102, 104, 108, 112, 118, 124, 128, 132, 138, 150, 168, 175, 173, 174]
    data = pd.DataFrame({'year': years, 'hpi': hpi_real})
    p = (ggplot(data, aes(x='year', y='hpi')) 
         + geom_area(fill='#2E86AB', alpha=0.3) 
         + geom_line(color='#2E86AB', size=1.2) 
         + theme_ipsum() 
         + theme(plot_margin=0.05)
         + labs(title=wrap_title('U.S. Real House Prices, 2000-2024'), x='Year', y='Price Index (2000=100)', caption='Source: S&P/Case-Shiller, deflated by CPI-U'))
    save_plotnine(p, 'ch05', 'ch05_house_price_trends.pdf')

# =============================================================================
# CHAPTER 9: MANUFACTURING
# =============================================================================

def ch09_manufacturing_employment():
    years = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2024]
    emp = [13.0, 15.0, 17.5, 18.5, 17.5, 17.0, 11.5, 12.2, 12.9]
    data = pd.DataFrame({'year': years, 'emp': emp})
    p = (ggplot(data, aes(x='year', y='emp')) 
         + geom_line(color='#2E86AB', size=1.2) 
         + geom_point(color='#2E86AB') 
         + theme_ipsum() 
         + theme(plot_margin=0.05)
         + labs(title=wrap_title('U.S. Manufacturing Employment, 1950-2024'), x='Year', y='Employment (Millions)', caption='Source: BLS CES'))
    save_plotnine(p, 'ch09', 'ch09_manufacturing_employment.pdf')

def ch09_robot_density():
    data = pd.DataFrame({
        'country': ['South Korea', 'Germany', 'Japan', 'China', 'USA'],
        'density': [1012, 429, 419, 470, 295]
    })
    data = data.sort_values('density', ascending=True)
    data['country'] = pd.Categorical(data['country'], categories=data['country'], ordered=True)
    p = (ggplot(data, aes(x='country', y='density')) 
         + geom_col(fill='#76B7B2', alpha=0.8) 
         + coord_flip() 
         + theme_ipsum() 
         + theme(plot_margin=0.05)
         + labs(title=wrap_title('Robot Density in Manufacturing, 2023'), x='', y='Robots per 10,000 Workers', caption='Source: IFR'))
    save_plotnine(p, 'ch09', 'ch09_robot_density.pdf')

# =============================================================================
# CHAPTER 10: RETAIL
# =============================================================================

def ch10_ecommerce_share():
    years = list(range(2010, 2025))
    share = [4.2, 4.7, 5.2, 5.8, 6.5, 7.3, 8.0, 9.0, 9.8, 11.0, 14.0, 13.2, 14.6, 15.4, 16.0]
    data = pd.DataFrame({'year': years, 'share': share})
    p = (ggplot(data, aes(x='year', y='share')) 
         + geom_line(color='#A23B72', size=1.2) 
         + geom_point(color='#A23B72') 
         + theme_ipsum() 
         + theme(plot_margin=0.05)
         + labs(title=wrap_title('E-commerce Share of Total Retail Sales'), x='Year', y='Percent of Total Retail', caption='Source: U.S. Census Bureau'))
    save_plotnine(p, 'ch10', 'ch10_ecommerce_share.pdf')

def ch10_top_retailers():
    data = pd.DataFrame({
        'retailer': ['Walmart', 'Amazon', 'Costco', 'Kroger', 'Home Depot', 'Target', 'Walgreens', 'CVS', 'Lowes', 'Albertsons'],
        'revenue': [648, 350, 242, 150, 153, 107, 110, 105, 86, 79] # 2024 approximate
    })
    data = data.sort_values('revenue', ascending=True)
    data['retailer'] = pd.Categorical(data['retailer'], categories=data['retailer'], ordered=True)
    p = (ggplot(data, aes(x='retailer', y='revenue')) 
         + geom_col(fill='#A23B72', alpha=0.8) 
         + coord_flip() 
         + theme_ipsum() 
         + theme(plot_margin=0.05, axis_text_x=element_text(size=8))
         + labs(title=wrap_title('Top 10 U.S. Retailers by Revenue, 2024'), x='', y='Revenue ($ Billion)', caption='Source: NRF / Company Reports'))
    save_plotnine(p, 'ch10', 'ch10_top_retailers.pdf')

# =============================================================================
# CHAPTER 11: TECH/MEDIA
# =============================================================================

def ch11_big_tech_revenue():
    data = pd.DataFrame({
        'company': ['Amazon', 'Apple', 'Alphabet', 'Microsoft', 'Meta'],
        'revenue': [575, 383, 307, 245, 135]
    })
    data = data.sort_values('revenue', ascending=True)
    data['company'] = pd.Categorical(data['company'], categories=data['company'], ordered=True)
    p = (ggplot(data, aes(x='company', y='revenue')) 
         + geom_col(fill='#4285F4', alpha=0.8) 
         + coord_flip() 
         + theme_ipsum() 
         + theme(plot_margin=0.05)
         + labs(title=wrap_title('Big Tech Annual Revenue, 2023'), x='', y='Revenue ($ Billion)', caption='Source: SEC Filings'))
    save_plotnine(p, 'ch11', 'ch11_big_tech_revenue.pdf')

# =============================================================================
# CHAPTER 12: TRANSPORTATION
# =============================================================================

def ch12_airline_shares():
    data = pd.DataFrame({
        'airline': ['Delta', 'American', 'Southwest', 'United', 'Alaska', 'JetBlue', 'Spirit', 'Other'],
        'share': [17.8, 17.5, 17.3, 16.0, 5.5, 5.2, 4.8, 15.9]
    })
    data = data.sort_values('share', ascending=True)
    data['airline'] = pd.Categorical(data['airline'], categories=data['airline'], ordered=True)
    p = (ggplot(data, aes(x='airline', y='share')) 
         + geom_col(fill='#4E79A7', alpha=0.8) 
         + coord_flip() 
         + theme_ipsum() 
         + theme(plot_margin=0.05)
         + labs(title=wrap_title('U.S. Domestic Airline Market Share, 2023'), x='', y='Share of Passengers (%)', caption='Source: Bureau of Transportation Statistics'))
    save_plotnine(p, 'ch12', 'ch12_airline_market_share.pdf')

# =============================================================================
# CHAPTER 13: CONSTRUCTION
# =============================================================================

def ch13_manufacturing_supercycle():
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    spending = [75, 72, 80, 110, 190, 235]
    data = pd.DataFrame({'year': years, 'spending': spending})
    p = (ggplot(data, aes(x='year', y='spending')) 
         + geom_col(fill='#C73E1D', alpha=0.8) 
         + theme_ipsum() 
         + theme(plot_margin=0.05)
         + labs(title=wrap_title('The Manufacturing Construction Supercycle'), x='Year', y='Annual Spending ($ Billion)', caption='Source: U.S. Census Bureau (Value Put in Place)'))
    save_plotnine(p, 'ch13', 'ch13_manufacturing_supercycle.pdf')

def ch13_productivity_puzzle():
    years = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
    mfg = [100, 130, 180, 250, 350, 550, 800, 950]
    const = [100, 110, 115, 110, 105, 100, 95, 90]
    data = pd.DataFrame({
        'Year': years * 2,
        'Sector': ['Manufacturing']*8 + ['Construction']*8,
        'Index': mfg + const
    })
    p = (ggplot(data, aes(x='Year', y='Index', color='Sector')) 
         + geom_line(size=1.2) 
         + geom_point() 
         + scale_color_manual(values=['#C73E1D', '#2E86AB']) 
         + theme_ipsum() 
         + theme(plot_margin=0.05, legend_position='bottom')
         + labs(title=wrap_title('The Construction Productivity Puzzle'), x='Year', y='Productivity Index (1950=100)', caption='Source: Goolsbee & Syverson (2023)'))
    save_plotnine(p, 'ch13', 'ch13_productivity_puzzle.pdf')

if __name__ == '__main__':
    print("Generating Sector Figures...")
    ch05_top_homebuilders()
    ch05_house_price_trends()
    ch09_manufacturing_employment()
    ch09_robot_density()
    ch10_ecommerce_share()
    ch10_top_retailers()
    ch11_big_tech_revenue()
    ch12_airline_shares()
    ch13_manufacturing_supercycle()
    ch13_productivity_puzzle()
    print("Done.")
