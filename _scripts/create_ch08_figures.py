"""
Create figures for Chapter 8: Finance and Insurance.
Adheres to style guidelines in CLAUDE.md.
"""

import pandas as pd
from plotnine import *
from hrbrthemes import theme_ipsum
from pathlib import Path
import matplotlib.pyplot as plt
import squarify
import textwrap

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

def wrap_title(title):
    return "\n".join(textwrap.wrap(title, width=50))

# =============================================================================
# FIGURES
# =============================================================================

def ch08_finance_gdp_treemap():
    """Financial sector GDP breakdown (2023 BEA)."""
    # Total Finance/Insurance GDP ~ $2.1T
    data = pd.DataFrame({
        'category': ['Banking & Credit', 'Insurance Carriers', 'Securities & Investments', 'Funds & Trusts'],
        'value': [720, 610, 750, 40] # Approximate Billions from BEA Value Added
    })
    
    data = data.sort_values('value', ascending=False)
    total = data['value'].sum()
    
    def make_label(r):
        pct = r['value']/total*100
        if pct < 4: return ""
        return f"{r['category']}\n${r['value']}B\n({pct:.1f}%)"

    data['label'] = data.apply(make_label, axis=1)
    
    colors = ['#4E79A7', '#F28E2B', '#76B7B2', '#E15759']
    
    fig, ax = plt.subplots(figsize=(6, 4))
    squarify.plot(sizes=data['value'], label=data['label'], color=colors, alpha=0.8, ax=ax, 
                  text_kwargs={'fontsize': 9, 'wrap': True}, pad=True)
    
    ax.set_title('Finance and Insurance GDP by Subsector (2023)', fontsize=12, fontweight='bold', pad=10)
    ax.axis('off')
    fig.text(0.5, 0.05, f'Source: BEA Industry Accounts. Total: ${total/1000:.1f} Trillion.', 
             ha='center', fontsize=7, fontstyle='italic')
    
    plt.tight_layout()
    save_matplotlib(fig, 'ch08', 'ch08_finance_gdp_treemap.pdf')

def ch08_top_banks():
    """Top 10 U.S. Banks by Assets (2024)."""
    data = pd.DataFrame({
        'bank': ['JPMorgan Chase', 'Bank of America', 'Citigroup', 'Wells Fargo', 
                 'Goldman Sachs', 'Morgan Stanley', 'U.S. Bancorp', 'PNC Bank', 
                 'Truist Bank', 'Charles Schwab'],
        'assets': [3500, 2550, 1720, 1700, 1650, 1200, 670, 560, 530, 480] # Approximate Billions
    })
    
    data = data.sort_values('assets', ascending=True)
    data['bank'] = pd.Categorical(data['bank'], categories=data['bank'], ordered=True)
    
    p = (
        ggplot(data, aes(x='bank', y='assets'))
        + geom_col(fill='#2E86AB', alpha=0.8)
        + coord_flip()
        + theme_ipsum()
        + theme(
            figure_size=(6, 5), 
            panel_grid_major_y=element_blank(),
            plot_title=element_text(size=12, face='bold', ha='left'),
            plot_margin=0.05
        )
        + labs(
            title=wrap_title('Top 10 U.S. Banks by Consolidated Assets, 2024'),
            x='',
            y='Total Assets ($ Billion)',
            caption='Source: Federal Reserve Statistical Release / FDIC'
        )
    )
    save_plotnine(p, 'ch08', 'ch08_top_banks.pdf', height=5)

def ch08_insurance_premiums():
    """Insurance Premiums by Line (2023)."""
    data = pd.DataFrame({
        'line': ['Life / Annuity', 'Health', 'Property / Casualty'],
        'premiums': [980, 1200, 860] # Approximate Billions
    })
    
    data = data.sort_values('premiums', ascending=False)
    total = data['premiums'].sum()
    
    def make_label(r):
        pct = r['premiums']/total*100
        if pct < 4: return ""
        return f"{r['line']}\n${r['premiums']}B\n({pct:.1f}%)"

    data['label'] = data.apply(make_label, axis=1)
    
    colors = ['#59A14F', '#EDC948', '#E15759']
    
    fig, ax = plt.subplots(figsize=(6, 3.5))
    squarify.plot(sizes=data['premiums'], label=data['label'], color=colors, alpha=0.8, ax=ax, 
                  text_kwargs={'fontsize': 10, 'wrap': True}, pad=True)
    
    ax.set_title('U.S. Insurance Premiums by Major Line (2023)', fontsize=12, fontweight='bold', pad=10)
    ax.axis('off')
    fig.text(0.5, 0.05, f'Source: NAIC / A.M. Best. Total: ${total/1000:.1f} Trillion.', 
             ha='center', fontsize=7, fontstyle='italic')
    
    plt.tight_layout()
    save_matplotlib(fig, 'ch08', 'ch08_insurance_premiums.pdf')

if __name__ == '__main__':
    print("Creating figures for Chapter 8...")
    ch08_finance_gdp_treemap()
    ch08_top_banks()
    ch08_insurance_premiums()
    print("Done.")
