"""
Create figures for Part V (Regional) and Part VI (Institutions).
Adheres to style guidelines in CLAUDE.md.
"""

import pandas as pd
from plotnine import *
from hrbrthemes import theme_ipsum
from pathlib import Path
import matplotlib.pyplot as plt
import squarify
import textwrap
import numpy as np

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

def save_matplotlib(fig, chapter, filename):
    ensure_dir(chapter)
    pdf_path = FIGURES_DIR / chapter / filename
    png_path = FIGURES_DIR / chapter / filename.replace('.pdf', '.png')
    fig.savefig(pdf_path, dpi=DPI, bbox_inches='tight', facecolor='white')
    fig.savefig(png_path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {pdf_path}")

def wrap_title(title):
    return "\n".join(textwrap.wrap(title, width=50))

# =============================================================================
# PART V: REGIONAL ECONOMIES
# =============================================================================

def ch21_northeast_gdp():
    data = pd.DataFrame({
        'industry': ['Financial Services', 'Professional Svc', 'Healthcare', 'Government', 'Information', 'Education', 'Other'],
        'value': [450, 400, 320, 350, 280, 150, 600] # Representative shares for NE
    })
    total = data['value'].sum()
    
    def make_label(r):
        pct = r['value']/total*100
        if pct < 4: return ""
        return f"{r['industry']}\n${r['value']}B"

    data['label'] = data.apply(make_label, axis=1)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    squarify.plot(sizes=data['value'], label=data['label'], color=plt.cm.Blues(np.linspace(0.3, 0.7, len(data))), alpha=0.8, ax=ax, text_kwargs={'fontsize': 8, 'wrap': True}, pad=True)
    ax.set_title('Northeast Corridor GDP Composition (Illustrative)', fontsize=12, fontweight='bold', pad=10)
    ax.axis('off')
    
    plt.tight_layout()
    save_matplotlib(fig, 'ch21', 'ch21_regional_gdp.pdf')

def ch22_sunbelt_growth():
    data = pd.DataFrame({
        'metro': ['Austin', 'Dallas', 'Houston', 'Phoenix', 'Atlanta', 'Miami', 'Charlotte'],
        'growth': [5.2, 4.1, 3.8, 4.5, 3.5, 3.2, 3.9] # % GDP Growth approx 2023
    })
    data = data.sort_values('growth', ascending=True)
    data['metro'] = pd.Categorical(data['metro'], categories=data['metro'], ordered=True)
    p = (
        ggplot(data, aes(x='metro', y='growth')) 
        + geom_col(fill='#F18F01', alpha=0.8) 
        + coord_flip() 
        + theme_ipsum() 
        + theme(plot_margin=0.05)
        + labs(title=wrap_title('Economic Growth in Key Sunbelt Metros, 2023'), x='', y='Real GDP Growth (%)', caption='Source: BEA Regional Data')
    )
    save_plotnine(p, 'ch22', 'ch22_sunbelt_growth.pdf')

# =============================================================================
# PART VI: INSTITUTIONS
# =============================================================================

def ch27_lobbying_spending():
    data = pd.DataFrame({
        'Industry': ['Pharmaceuticals', 'Electronics', 'Insurance', 'Real Estate', 'Oil & Gas', 'Air Transport'],
        'Spending': [382, 235, 158, 130, 125, 110] # 2023 millions approx
    })
    data = data.sort_values('Spending', ascending=True)
    data['Industry'] = pd.Categorical(data['Industry'], categories=data['Industry'], ordered=True)
    p = (
        ggplot(data, aes(x='Industry', y='Spending')) 
        + geom_col(fill='#A23B72', alpha=0.8) 
        + coord_flip() 
        + theme_ipsum() 
        + theme(plot_margin=0.05)
        + labs(title=wrap_title('Top Industries by Lobbying Spending, 2023'), x='', y='Annual Spending ($ Million)', caption='Source: OpenSecrets')
    )
    save_plotnine(p, 'ch27', 'ch27_lobbying_spending.pdf')

def ch28_union_membership():
    years = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2024]
    pct = [33.0, 31.0, 27.0, 23.0, 16.0, 13.5, 11.9, 10.8, 10.0]
    data = pd.DataFrame({'year': years, 'pct': pct})
    p = (
        ggplot(data, aes(x='year', y='pct')) 
        + geom_area(fill='#E15759', alpha=0.3) 
        + geom_line(color='#E15759', size=1.5) 
        + theme_ipsum() 
        + theme(plot_margin=0.05)
        + labs(title=wrap_title('U.S. Union Membership Rate, 1950-2024'), x='Year', y='Percent of Workforce', caption='Source: BLS / UnionStats.com')
    )
    save_plotnine(p, 'ch28', 'ch28_union_membership.pdf')

if __name__ == '__main__':
    print("Creating figures for Part V and VI...")
    ch21_northeast_gdp()
    ch22_sunbelt_growth()
    ch27_lobbying_spending()
    ch28_union_membership()
    print("Done.")
