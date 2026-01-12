"""
Create figures for Chapter 6: Healthcare.
Adheres to style guidelines in CLAUDE.md.
"""

import pandas as pd
from plotnine import *
from hrbrthemes import theme_ipsum
from pathlib import Path
import matplotlib.pyplot as plt
import squarify

# Configuration
PROJECT_DIR = Path(r"G:\\My Drive\\book drafts\\the american economy")
FIGURES_DIR = PROJECT_DIR / "_figures"
FIGURE_WIDTH = 6
DPI = 300

def ensure_dir(chapter):
    (FIGURES_DIR / chapter).mkdir(parents=True, exist_ok=True)

def save_plotnine(plot, chapter, filename, height=4):
    """Save plotnine figure."""
    ensure_dir(chapter)
    pdf_path = FIGURES_DIR / chapter / filename
    png_path = FIGURES_DIR / chapter / filename.replace('.pdf', '.png')
    plot.save(pdf_path, width=FIGURE_WIDTH, height=height, units='in', dpi=DPI, verbose=False)
    plot.save(png_path, width=FIGURE_WIDTH, height=height, units='in', dpi=DPI, verbose=False)
    print(f"Saved: {pdf_path}")

def save_matplotlib(fig, chapter, filename):
    """Save matplotlib figure."""
    ensure_dir(chapter)
    pdf_path = FIGURES_DIR / chapter / filename
    png_path = FIGURES_DIR / chapter / filename.replace('.pdf', '.png')
    fig.savefig(pdf_path, dpi=DPI, bbox_inches='tight', facecolor='white')
    fig.savefig(png_path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {pdf_path}")

# =============================================================================
# FIGURES
# =============================================================================

def ch06_spending_treemap():
    """Healthcare spending by category (2023 CMS Estimate)."""
    # Total NHE ~ $4.8T
    data = pd.DataFrame({
        'category': ['Hospital Care', 'Physician & Clinical', 'Prescription Drugs', 
                     'Dental Services', 'Other Professional', 'Nursing Home Care', 
                     'Home Health Care', 'Admin & Net Cost', 'Other'],
        'spending': [1500, 950, 420, 180, 140, 210, 150, 350, 800] # Approximate Billions
    })
    
    data = data.sort_values('spending', ascending=False)
    total = data['spending'].sum()
    
    # Hide labels for small segments (< 4%)
    def make_label(r):
        pct = r['spending']/total*100
        if pct < 4:
            return ""
        return f"{r['category']}\n${r['spending']}B\n({pct:.1f}%)"

    data['label'] = data.apply(make_label, axis=1)
    
    # Professional colors
    colors = ['#4E79A7', '#E15759', '#76B7B2', '#59A14F', '#F28E2B', '#EDC948', '#B07AA1', '#FF9DA7', '#9C755F']
    
    fig, ax = plt.subplots(figsize=(6, 5))
    squarify.plot(sizes=data['spending'], label=data['label'], color=colors, alpha=0.8, ax=ax, 
                  text_kwargs={'fontsize': 8, 'wrap': True}, pad=True)
    
    ax.set_title('National Health Expenditures by Category (2023 Est.)', fontsize=12, fontweight='bold', pad=10)
    ax.axis('off')
    fig.text(0.5, 0.02, f'Source: CMS Office of the Actuary. Total: ${total/1000:.1f} Trillion.', 
             ha='center', fontsize=7, fontstyle='italic')
    
    plt.tight_layout()
    save_matplotlib(fig, 'ch06', 'ch06_spending_treemap.pdf')

def ch06_spending_over_time():
    """Healthcare spending as % of GDP over time."""
    data = pd.DataFrame({
        'year': [1960, 1970, 1980, 1990, 2000, 2010, 2020, 2023],
        'pct_gdp': [5.0, 6.9, 8.9, 12.1, 13.3, 17.2, 19.5, 17.6]
    })
    
    p = (
        ggplot(data, aes(x='year', y='pct_gdp'))
        + geom_line(color='#E15759', size=1.5)
        + geom_point(color='#E15759', size=3)
        + theme_ipsum()
        + theme(
            figure_size=(6, 4),
            plot_title=element_text(size=12, ha='left'),
            plot_margin=0.05
        )
        + labs(
            title='Healthcare Spending as Share of U.S. GDP',
            x='Year',
            y='NHE as % of GDP',
            caption='Source: CMS National Health Expenditure Accounts'
        )
        + scale_y_continuous(limits=(0, 25))
    )
    save_plotnine(p, 'ch06', 'ch06_spending_over_time.pdf')

def ch06_payer_mix():
    """Healthcare spending by Payer (2023)."""
    data = pd.DataFrame({
        'payer': ['Private Health Insurance', 'Medicare', 'Medicaid', 'Out-of-Pocket', 'Other Private', 'Other Govt'],
        'share': [29, 21, 18, 10, 7, 15]
    })
    
    data = data.sort_values('share', ascending=True)
    data['payer'] = pd.Categorical(data['payer'], categories=data['payer'], ordered=True)
    
    p = (
        ggplot(data, aes(x='payer', y='share'))
        + geom_col(fill='#4E79A7', alpha=0.8)
        + coord_flip()
        + theme_ipsum()
        + theme(
            figure_size=(6, 4), 
            panel_grid_major_y=element_blank(),
            plot_title=element_text(size=12, ha='left'),
            plot_margin=0.05
        )
        + labs(
            title='National Health Expenditures by Source of Funds',
            x='',
            y='Share of Total Spending (%)',
            caption='Source: CMS Office of the Actuary (2023 estimate)'
        )
    )
    save_plotnine(p, 'ch06', 'ch06_payer_mix.pdf')

if __name__ == '__main__':
    print("Creating figures for Chapter 6...")
    ch06_spending_treemap()
    ch06_spending_over_time()
    ch06_payer_mix()
    print("Done.")
