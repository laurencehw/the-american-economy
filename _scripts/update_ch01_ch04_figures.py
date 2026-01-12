"""
Update Chapter 1 and 4 figures to adhere to style guidelines (plotnine + theme_ipsum).
Saves 300 DPI PNGs for GitBook.
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
# CHAPTER 1
# =============================================================================

def ch01_employment_bar():
    data = pd.DataFrame({
        'industry': ['Healthcare', 'Government', 'Professional Svc', 'Retail', 'Leisure & Hosp.', 
                     'Manufacturing', 'Construction', 'Finance', 'Transportation', 'Wholesale', 
                     'Education', 'Information', 'Real Estate', 'Other'],
        'employment': [21.7, 23.0, 23.2, 15.7, 16.8, 12.9, 8.0, 6.8, 6.5, 6.0, 4.0, 3.0, 2.5, 9.0]
    })
    data = data.sort_values('employment', ascending=True)
    data['industry'] = pd.Categorical(data['industry'], categories=data['industry'], ordered=True)
    
    p = (
        ggplot(data, aes(x='industry', y='employment'))
        + geom_col(fill='#4E79A7', alpha=0.8)
        + coord_flip()
        + theme_ipsum()
        + theme(figure_size=(6, 5), panel_grid_major_y=element_blank(), plot_margin=0.05)
        + labs(title=wrap_title('U.S. Employment by Industry, 2023'), x='', y='Employment (Millions)', caption='Source: BLS CES')
    )
    save_plotnine(p, 'ch01', 'ch01_employment_bar.pdf', height=5)

def ch01_gdp_treemap():
    data = pd.DataFrame({
        'industry': ['Real Estate', 'Professional Svc', 'Government', 'Manufacturing', 'Finance', 
                     'Healthcare', 'Information', 'Retail', 'Wholesale', 'Construction', 'Other'],
        'gdp': [3851, 2453, 2996, 2497, 2122, 1985, 1686, 1377, 1313, 1087, 3200]
    })
    data = data.sort_values('gdp', ascending=False)
    total = data['gdp'].sum()
    
    # Label logic: hide small
    def make_label(r):
        pct = r['gdp']/total*100
        if pct < 3.5: return ""
        return f"{r['industry']}\n${r['gdp']}B"

    data['label'] = data.apply(make_label, axis=1)
    colors = ['#4E79A7', '#E15759', '#76B7B2', '#59A14F', '#F28E2B', '#EDC948', '#B07AA1', '#FF9DA7', '#9C755F', '#BAB0AC', '#8CD17D']
    
    fig, ax = plt.subplots(figsize=(6, 5))
    squarify.plot(sizes=data['gdp'], label=data['label'], color=colors, alpha=0.8, ax=ax, text_kwargs={'fontsize': 8}, pad=True)
    ax.set_title('U.S. GDP by Industry, 2023', fontsize=12, fontweight='bold', pad=10)
    ax.axis('off')
    fig.text(0.5, 0.02, f'Source: BEA. Total: ${total/1000:.1f} Trillion.', ha='center', fontsize=7, fontstyle='italic')
    
    plt.tight_layout()
    save_matplotlib(fig, 'ch01', 'ch01_gdp_treemap.pdf')

# =============================================================================
# CHAPTER 4
# =============================================================================

def ch04_govt_employment_level():
    data = pd.DataFrame({
        'Level': ['Local', 'State', 'Federal'],
        'Employment': [14.8, 5.4, 2.9]
    })
    data['Level'] = pd.Categorical(data['Level'], categories=['Federal', 'State', 'Local'], ordered=True)
    
    p = (
        ggplot(data, aes(x='Level', y='Employment'))
        + geom_col(fill='#E15759', alpha=0.8, width=0.6)
        + theme_ipsum()
        + theme(figure_size=(6, 4), panel_grid_major_x=element_blank(), plot_margin=0.05)
        + labs(title=wrap_title('Government Employment by Level, 2023'), x='', y='Employment (Millions)', caption='Source: BLS CES')
    )
    save_plotnine(p, 'ch04', 'ch04_govt_employment_level.pdf')

def ch04_federal_spending_treemap():
    data = pd.DataFrame({
        'Category': ['Social Security', 'Health/Medicare', 'Defense', 'Net Interest', 'Income Security', 'Veterans', 'Other'],
        'Spending': [1354, 1493, 820, 659, 775, 302, 700] # Approx 2023 billions
    })
    data = data.sort_values('Spending', ascending=False)
    total = data['Spending'].sum()
    
    def make_label(r):
        pct = r['Spending']/total*100
        if pct < 4: return ""
        return f"{r['Category']}\n${r['Spending']}B"

    data['label'] = data.apply(make_label, axis=1)
    
    fig, ax = plt.subplots(figsize=(6, 5))
    squarify.plot(sizes=data['Spending'], label=data['label'], color=plt.cm.Pastel1.colors, alpha=0.8, ax=ax, text_kwargs={'fontsize': 8}, pad=True)
    ax.set_title('Federal Outlays by Major Category, 2023', fontsize=12, fontweight='bold', pad=10)
    ax.axis('off')
    fig.text(0.5, 0.02, f'Source: OMB. Total: ${total/1000:.1f} Trillion.', ha='center', fontsize=7, fontstyle='italic')
    
    plt.tight_layout()
    save_matplotlib(fig, 'ch04', 'ch04_spending_treemap.pdf')

if __name__ == '__main__':
    print("Updating Chapter 1 and 4 figures...")
    ch01_employment_bar()
    ch01_gdp_treemap()
    ch04_govt_employment_level()
    ch04_federal_spending_treemap()
    print("Done.")
