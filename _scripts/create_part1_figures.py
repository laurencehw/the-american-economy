"""
Create figures for Part I (Chapters 2 & 3) using plotnine and theme_ipsum.
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

# Ensure directory exists helper
def ensure_dir(chapter):
    (FIGURES_DIR / chapter).mkdir(parents=True, exist_ok=True)

def wrap_title(title):
    return "\n".join(textwrap.wrap(title, width=50))

def save_plotnine(plot, chapter, filename):
    """Save plotnine figure in PDF and PNG."""
    ensure_dir(chapter)
    pdf_path = FIGURES_DIR / chapter / filename
    png_path = FIGURES_DIR / chapter / filename.replace('.pdf', '.png')
    
    # Save PDF
    plot.save(pdf_path, width=FIGURE_WIDTH, height=4, units='in', dpi=DPI, verbose=False)
    # Save PNG
    plot.save(png_path, width=FIGURE_WIDTH, height=4, units='in', dpi=DPI, verbose=False)
    
    print(f"Saved: {pdf_path}")

# =============================================================================
# CHAPTER 2: HOW IT FITS TOGETHER
# =============================================================================

def ch02_consumer_expenditure_bar():
    """Consumer Expenditure Breakdown (2023)."""
    data = pd.DataFrame({
        'category': ['Housing', 'Transportation', 'Food', 'Insurance & Pensions', 
                     'Healthcare', 'Entertainment', 'Apparel', 'Education', 'Other'],
        'share': [33.3, 17.0, 12.8, 11.8, 8.0, 4.8, 2.5, 1.3, 8.5]
    })
    
    data = data.sort_values('share', ascending=True)
    data['category'] = pd.Categorical(data['category'], categories=data['category'], ordered=True)
    
    p = (
        ggplot(data, aes(x='category', y='share'))
        + geom_col(fill='#2E86AB', alpha=0.8)
        + coord_flip()
        + theme_ipsum()
        + theme(
            figure_size=(6, 4),
            panel_grid_major_y=element_blank(),
            plot_title=element_text(size=12, face='bold', ha='left'),
            plot_margin=0.05
        )
        + labs(
            title=wrap_title('Average Household Spending Breakdown, 2023'),
            x='',
            y='Share of Annual Expenditure (%)',
            caption='Source: BLS Consumer Expenditure Survey'
        )
    )
    save_plotnine(p, 'ch02', 'ch02_consumer_expenditure_bar.pdf')

# =============================================================================
# CHAPTER 3: GEOGRAPHY OF PRODUCTION
# =============================================================================

def ch03_top_metros_gdp():
    """Top 20 U.S. Metros by GDP."""
    data = pd.DataFrame({
        'metro': ['New York', 'Los Angeles', 'Chicago', 
                  'San Francisco', 'Washington DC', 'Dallas', 
                  'Houston', 'Boston', 'Seattle', 
                  'Philadelphia', 'Atlanta', 'Miami', 
                  'San Jose', 'Phoenix', 'Detroit', 
                  'Minneapolis', 'San Diego', 'Denver', 
                  'Baltimore', 'Charlotte'],
        'gdp': [1900, 1150, 750, 680, 620, 600, 550, 520, 500, 480, 
                470, 430, 410, 320, 280, 290, 270, 260, 230, 220]
    })
    
    data = data.sort_values('gdp', ascending=True)
    data['metro'] = pd.Categorical(data['metro'], categories=data['metro'], ordered=True)
    
    p = (
        ggplot(data, aes(x='metro', y='gdp'))
        + geom_col(fill='#2E86AB', alpha=0.8)
        + coord_flip()
        + theme_ipsum()
        + theme(
            figure_size=(6, 6),
            panel_grid_major_y=element_blank(),
            plot_title=element_text(size=12, face='bold', ha='left'),
            plot_margin=0.05
        )
        + labs(
            title=wrap_title('Top 20 U.S. Metropolitan Economies by GDP'),
            x='',
            y='Real GDP ($ Billion)',
            caption='Source: BEA Regional Data'
        )
    )
    # Custom height for more bars
    ensure_dir('ch03')
    p.save(FIGURES_DIR / 'ch03' / 'ch03_top_metros_gdp.pdf', width=6, height=6, units='in', dpi=DPI, verbose=False)
    p.save(FIGURES_DIR / 'ch03' / 'ch03_top_metros_gdp.png', width=6, height=6, units='in', dpi=DPI, verbose=False)
    print("Saved: ch03_top_metros_gdp")

def ch03_urban_rural_employment():
    """Urban vs Rural Employment Trends."""
    years = [2010, 2015, 2020, 2024]
    
    data = pd.DataFrame({
        'Year': years * 2,
        'Region': ['Metro Areas']*4 + ['Non-Metro (Rural)']*4,
        'Index': [100, 109.4, 110.9, 117.2, 100, 102.4, 98.5, 101.5]
    })
    
    p = (
        ggplot(data, aes(x='Year', y='Index', color='Region', linetype='Region'))
        + geom_line(size=1.2)
        + geom_point(size=3)
        + scale_color_manual(values=['#2E86AB', '#C73E1D'])
        + theme_ipsum()
        + theme(
            figure_size=(6, 4),
            legend_position='bottom',
            plot_title=element_text(size=12, face='bold', ha='left'),
            plot_margin=0.05
        )
        + labs(
            title=wrap_title('Employment Growth: Urban vs. Rural (2010-2024)'),
            x='Year',
            y='Employment Index (2010=100)',
            caption='Source: USDA ERS / BLS'
        )
    )
    save_plotnine(p, 'ch03', 'ch03_urban_rural_employment.pdf')

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("Creating figures for Part I with plotnine...")
    
    ch02_consumer_expenditure_bar()
    ch03_top_metros_gdp()
    ch03_urban_rural_employment()
    
    print("\nDone.")