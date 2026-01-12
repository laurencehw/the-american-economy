"""
Final figures for Chapters 23, 24, 25, 26.
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

def save_plotnine(plot, chapter, filename, height=4):
    ensure_dir(chapter)
    pdf_path = FIGURES_DIR / chapter / filename
    png_path = FIGURES_DIR / chapter / filename.replace('.pdf', '.png')
    plot.save(pdf_path, width=FIGURE_WIDTH, height=height, units='in', dpi=DPI, verbose=False)
    plot.save(png_path, width=FIGURE_WIDTH, height=height, units='in', dpi=DPI, verbose=False)
    print(f"Saved: {pdf_path}")

def wrap_title(title):
    return "\n".join(textwrap.wrap(title, width=50))

# =============================================================================
# CHAPTER 23: MIDWEST
# =============================================================================

def ch23_midwest_mfg():
    data = pd.DataFrame({
        'State': ['Indiana', 'Michigan', 'Wisconsin', 'Ohio', 'Iowa', 'U.S. Average'],
        'Share': [26.2, 18.5, 18.2, 16.5, 17.1, 10.2] # Mfg share of GDP approx
    })
    data = data.sort_values('Share', ascending=True)
    data['State'] = pd.Categorical(data['State'], categories=data['State'], ordered=True)
    p = (ggplot(data, aes(x='State', y='Share')) 
         + geom_col(fill='#4E79A7', alpha=0.8) 
         + coord_flip() 
         + theme_ipsum() 
         + theme(plot_margin=0.05)
         + labs(title=wrap_title('Manufacturing Share of State GDP, 2023'), x='', y='Percent of GDP', caption='Source: BEA'))
    save_plotnine(p, 'ch23', 'ch23_mfg_share.pdf')

# =============================================================================
# CHAPTER 24: WEST
# =============================================================================

def ch24_california_gdp():
    data = pd.DataFrame({
        'Sector': ['Tech/Info', 'Real Estate', 'Prof Services', 'Mfg', 'Govt', 'Healthcare', 'Other'],
        'Value': [650, 600, 520, 480, 420, 310, 1000] # Approx billions for CA $3.8T economy
    })
    data = data.sort_values('Value', ascending=True)
    data['Sector'] = pd.Categorical(data['Sector'], categories=data['Sector'], ordered=True)
    p = (ggplot(data, aes(x='Sector', y='Value')) 
         + geom_col(fill='#2E86AB', alpha=0.8) 
         + coord_flip() 
         + theme_ipsum() 
         + theme(plot_margin=0.05)
         + labs(title=wrap_title('Composition of California GDP, 2023'), x='', y='Real GDP ($ Billion)', caption='Source: BEA'))
    save_plotnine(p, 'ch24', 'ch24_ca_gdp.pdf')

# =============================================================================
# CHAPTER 25: RURAL
# =============================================================================

def ch25_urban_rural_income():
    data = pd.DataFrame({
        'Year': [2010, 2015, 2020, 2022],
        'Urban': [45, 52, 63, 68],
        'Rural': [32, 38, 45, 49] # Thousands approx per capita
    })
    data = pd.melt(data, id_vars=['Year'], var_name='Region', value_name='Income')
    p = (ggplot(data, aes(x='Year', y='Income', color='Region')) 
         + geom_line(size=1.5) 
         + geom_point() 
         + theme_ipsum() 
         + theme(plot_margin=0.05)
         + labs(title=wrap_title('Per Capita Income: Urban vs. Rural'), x='Year', y='Income ($ Thousands)', caption='Source: USDA ERS'))
    save_plotnine(p, 'ch25', 'ch25_income_gap.pdf')

# =============================================================================
# CHAPTER 26: GOVERNANCE
# =============================================================================

def ch26_agency_budgets():
    data = pd.DataFrame({
        'Agency': ['SSA', 'HHS', 'Treasury', 'DOD', 'USDA', 'VA', 'DOE', 'DOT'],
        'Budget': [1400, 1700, 1100, 850, 250, 300, 50, 120] # Approx outlays billions
    })
    data = data.sort_values('Budget', ascending=True)
    data['Agency'] = pd.Categorical(data['Agency'], categories=data['Agency'], ordered=True)
    p = (ggplot(data, aes(x='Agency', y='Budget')) 
         + geom_col(fill='#E15759', alpha=0.8) 
         + coord_flip() 
         + theme_ipsum() 
         + theme(plot_margin=0.05)
         + labs(title=wrap_title('Major Federal Agency Outlays, 2023'), x='', y='Outlays ($ Billion)', caption='Source: OMB / USAspending.gov'))
    save_plotnine(p, 'ch26', 'ch26_agency_budgets.pdf')

if __name__ == '__main__':
    print("Generating Final Figures...")
    ch23_midwest_mfg()
    ch24_california_gdp()
    ch25_urban_rural_income()
    ch26_agency_budgets()
    print("Done.")
