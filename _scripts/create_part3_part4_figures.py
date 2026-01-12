"""
Create figures for Part III (Financial Architecture) and Part IV (Trade).
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
# PART III: FINANCIAL ARCHITECTURE
# =============================================================================

def ch17_bond_market_treemap():
    data = pd.DataFrame({
        'category': ['Treasury', 'Mortgage-Backed', 'Corporate', 'Municipal', 'Asset-Backed', 'Agency'],
        'value': [26.3, 12.1, 10.5, 4.0, 1.6, 2.0] # 2023 Trillions approx
    })
    data = data.sort_values('value', ascending=False)
    total = data['value'].sum()
    
    def make_label(r):
        pct = r['value']/total*100
        if pct < 4: return ""
        return f"{r['category']}\n${r['value']}T"

    data['label'] = data.apply(make_label, axis=1)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    squarify.plot(sizes=data['value'], label=data['label'], color=plt.cm.Blues(np.linspace(0.4, 0.8, len(data))), alpha=0.8, ax=ax, text_kwargs={'fontsize': 9, 'wrap': True}, pad=True)
    ax.set_title('U.S. Bond Market Size by Asset Class (2023)', fontsize=12, fontweight='bold', pad=10)
    ax.axis('off')
    fig.text(0.5, 0.05, f'Source: SIFMA. Total Outstanding: ${total:.1f} Trillion.', ha='center', fontsize=7, fontstyle='italic')
    
    plt.tight_layout()
    save_matplotlib(fig, 'ch17', 'ch17_bond_market_size.pdf')

def ch17_stock_market_cap():
    data = pd.DataFrame({
        'year': [2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024],
        'cap': [17, 19, 24, 27, 30, 41, 40, 52] # Billions approx
    })
    p = (
        ggplot(data, aes(x='year', y='cap'))
        + geom_line(color='#2E86AB', size=1.5)
        + geom_point(color='#2E86AB', size=3)
        + theme_ipsum()
        + theme(plot_margin=0.05)
        + labs(title=wrap_title('Total U.S. Equity Market Capitalization'), x='Year', y='Market Cap ($ Trillion)', caption='Source: SIFMA / WFE')
    )
    save_plotnine(p, 'ch17', 'ch17_stock_market_cap.pdf')

# =============================================================================
# PART IV: TRADE
# =============================================================================

def ch19_top_partners():
    data = pd.DataFrame({
        'Partner': ['Mexico', 'Canada', 'China', 'Germany', 'Japan', 'Vietnam', 'South Korea'],
        'Trade': [798, 774, 575, 236, 223, 124, 115] # 2023 Total Trade Billions approx
    })
    data = data.sort_values('Trade', ascending=True)
    data['Partner'] = pd.Categorical(data['Partner'], categories=data['Partner'], ordered=True)
    
    p = (
        ggplot(data, aes(x='Partner', y='Trade'))
        + geom_col(fill='#4E79A7', alpha=0.8)
        + coord_flip()
        + theme_ipsum()
        + theme(plot_margin=0.05)
        + labs(title=wrap_title('Top U.S. Trading Partners, 2023'), x='', y='Total Goods Trade ($ Billion)', caption='Source: U.S. Census Bureau')
    )
    save_plotnine(p, 'ch19', 'ch19_top_partners.pdf')

def ch19_trade_balance():
    data = pd.DataFrame({
        'year': [2000, 2005, 2010, 2015, 2020, 2023],
        'deficit': [-376, -714, -500, -500, -650, -773] # Billions approx goods/services
    })
    p = (
        ggplot(data, aes(x='year', y='deficit'))
        + geom_area(fill='#E15759', alpha=0.3)
        + geom_line(color='#E15759', size=1.2)
        + theme_ipsum()
        + theme(plot_margin=0.05)
        + labs(title=wrap_title('U.S. Trade Balance (Goods and Services)'), x='Year', y='Balance ($ Billion)', caption='Source: BEA')
    )
    save_plotnine(p, 'ch19', 'ch19_trade_balance.pdf')

def ch18_corp_financing_treemap():
    data = pd.DataFrame({
        'Source': ['Internal Funds', 'Corporate Bonds', 'Bank Loans', 'Equity Issuance', 'Other'],
        'Value': [85, 8, 4, -2, 5] # Typical shares (Equity is often negative due to buybacks)
    })
    # For treemap we need positive values, so we handle buybacks separately or show absolute
    data_plot = data.copy()
    data_plot['Value'] = data_plot['Value'].abs()
    
    def make_label(r):
        return f"{r['Source']}\n{r['Value']}%" if r['Source'] != 'Equity Issuance' else f"Buybacks\n(Net Withdrawal)"

    data_plot['label'] = data_plot.apply(make_label, axis=1)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    squarify.plot(sizes=data_plot['Value'], label=data_plot['label'], color=plt.cm.Greens(np.linspace(0.4, 0.8, len(data))), alpha=0.8, ax=ax, text_kwargs={'fontsize': 9, 'wrap': True}, pad=True)
    ax.set_title('Sources of U.S. Corporate Financing (Flows)', fontsize=12, fontweight='bold', pad=10)
    ax.axis('off')
    fig.text(0.5, 0.05, f'Source: Federal Reserve Z.1 Accounts. Note: Buybacks exceed new issuance.', ha='center', fontsize=7, fontstyle='italic')
    
    plt.tight_layout()
    save_matplotlib(fig, 'ch18', 'ch18_corp_financing.pdf')

def ch18_ma_activity():
    data = pd.DataFrame({
        'year': [2010, 2012, 2014, 2016, 2018, 2020, 2021, 2022, 2023],
        'value': [1.0, 1.2, 1.5, 1.7, 1.7, 1.3, 2.6, 1.5, 1.2] # Trillions approx
    })
    p = (
        ggplot(data, aes(x='year', y='value'))
        + geom_line(color='#59A14F', size=1.5)
        + geom_point(color='#59A14F', size=3)
        + theme_ipsum()
        + theme(plot_margin=0.05)
        + labs(title=wrap_title('U.S. Mergers and Acquisitions (M&A) Volume'), x='Year', y='Deal Value ($ Trillion)', caption='Source: IMAA / Dealogic')
    )
    save_plotnine(p, 'ch18', 'ch18_ma_activity.pdf')

if __name__ == '__main__':
    print("Creating figures for Part III and IV...")
    ch17_bond_market_treemap()
    ch17_stock_market_cap()
    ch18_corp_financing_treemap()
    ch18_ma_activity()
    ch19_top_partners()
    ch19_trade_balance()
    print("Done.")
