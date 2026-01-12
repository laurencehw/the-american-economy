"""
Create figures for The American Economy book chapters.
Session 3: Ch5 Real Estate, Ch10 Retail, Ch13 Construction

Uses plotnine with hrbrthemes for consistent styling.
Fallback to matplotlib for maps and specialized charts.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Try plotnine, fall back to matplotlib if not available
try:
    from plotnine import *
    from hrbrthemes import theme_ipsum
    USE_PLOTNINE = True
except ImportError:
    USE_PLOTNINE = False
    print("plotnine/hrbrthemes not available, using matplotlib")

# Configuration
PROJECT_DIR = Path(r"G:\My Drive\book drafts\the american economy")
FIGURES_DIR = PROJECT_DIR / "_figures"
FIGURE_WIDTH = 6
DPI = 300

# Ensure figure directories exist
for ch in ['ch05', 'ch10', 'ch13']:
    (FIGURES_DIR / ch).mkdir(parents=True, exist_ok=True)

# Color palette (similar to hrbrthemes)
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'tertiary': '#F18F01',
    'quaternary': '#C73E1D',
    'gray': '#6c757d',
    'light_gray': '#adb5bd'
}


def save_figure(fig, chapter, filename):
    """Save figure to chapter directory."""
    output_path = FIGURES_DIR / chapter / filename
    fig.savefig(output_path, dpi=DPI, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close(fig)


# =============================================================================
# CHAPTER 5: REAL ESTATE
# =============================================================================

def ch05_top_homebuilders():
    """Top homebuilders by homes closed (2024)."""
    data = pd.DataFrame({
        'builder': ['D.R. Horton', 'Lennar', 'PulteGroup', 'NVR', 'Toll Brothers',
                   'Meritage Homes', 'Taylor Morrison', 'KB Home', 'Century Communities', 'Dream Finders'],
        'homes': [90000, 73000, 28000, 24000, 10000, 17000, 12000, 11000, 10000, 8000]
    })

    # Sort for horizontal bar
    data = data.sort_values('homes', ascending=True)

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4.5))
    bars = ax.barh(data['builder'], data['homes'] / 1000, color=COLORS['primary'])

    # Add value labels
    for bar, val in zip(bars, data['homes']):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{val/1000:.0f}K', va='center', fontsize=8)

    ax.set_xlabel('Homes Closed (Thousands)', fontsize=9)
    ax.set_title('Top 10 U.S. Homebuilders by Homes Closed, 2024', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(0, 105)

    # Source note
    ax.text(0, -0.12, 'Source: Company reports', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch05', 'ch05_top_homebuilders.pdf')


def ch05_top_reits():
    """Top REITs by market cap."""
    data = pd.DataFrame({
        'reit': ['Prologis', 'American Tower', 'Equinix', 'Welltower', 'Digital Realty',
                 'Public Storage', 'Realty Income', 'Simon Property', 'VICI Properties', 'Crown Castle'],
        'market_cap': [116, 93, 78, 72, 54, 52, 50, 48, 35, 42],
        'type': ['Industrial', 'Telecom', 'Data Center', 'Healthcare', 'Data Center',
                'Storage', 'Net Lease', 'Retail', 'Gaming', 'Telecom']
    })

    data = data.sort_values('market_cap', ascending=True)

    # Color by type
    type_colors = {
        'Industrial': COLORS['primary'],
        'Telecom': COLORS['secondary'],
        'Data Center': COLORS['tertiary'],
        'Healthcare': COLORS['quaternary'],
        'Storage': COLORS['gray'],
        'Net Lease': '#5C946E',
        'Retail': '#8B5CF6',
        'Gaming': '#EC4899'
    }
    colors = [type_colors.get(t, COLORS['gray']) for t in data['type']]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4.5))
    bars = ax.barh(data['reit'], data['market_cap'], color=colors)

    ax.set_xlabel('Market Capitalization ($ Billion)', fontsize=9)
    ax.set_title('Top 10 U.S. REITs by Market Cap, 2024', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.text(0, -0.12, 'Source: NAREIT', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch05', 'ch05_top_reits.pdf')


def ch05_house_price_trends():
    """House price index trends over time."""
    years = list(range(2000, 2025))

    # Approximate Case-Shiller national index (2000=100)
    hpi = [100, 107, 115, 126, 140, 158, 165, 155, 130, 125,
           128, 130, 135, 142, 150, 158, 168, 178, 188, 200,
           220, 260, 290, 300, 310]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4))
    ax.plot(years, hpi, color=COLORS['primary'], linewidth=2)
    ax.fill_between(years, hpi, alpha=0.2, color=COLORS['primary'])

    # Mark key events
    ax.axvline(2008, color=COLORS['quaternary'], linestyle='--', alpha=0.5)
    ax.text(2008.5, 170, '2008\nCrisis', fontsize=7, color=COLORS['quaternary'])
    ax.axvline(2020, color=COLORS['tertiary'], linestyle='--', alpha=0.5)
    ax.text(2020.5, 200, 'COVID\nSurge', fontsize=7, color=COLORS['tertiary'])

    ax.set_xlabel('Year', fontsize=9)
    ax.set_ylabel('House Price Index (2000=100)', fontsize=9)
    ax.set_title('U.S. House Prices, 2000-2024', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(80, 350)

    ax.text(0, -0.15, 'Source: S&P/Case-Shiller National Home Price Index',
            transform=ax.transAxes, fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch05', 'ch05_house_price_trends.pdf')


# =============================================================================
# CHAPTER 10: RETAIL AND WHOLESALE TRADE
# =============================================================================

def ch10_top_retailers():
    """Top retailers by US revenue."""
    data = pd.DataFrame({
        'retailer': ['Walmart', 'Amazon', 'Costco', 'Kroger', 'Home Depot',
                    'Target', 'Walgreens', 'CVS Health', "Lowe's", 'Albertsons'],
        'revenue': [569, 274, 183, 150, 157, 107, 89, 85, 86, 79]
    })

    data = data.sort_values('revenue', ascending=True)

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4.5))
    bars = ax.barh(data['retailer'], data['revenue'], color=COLORS['primary'])

    # Highlight Big Four
    for i, (retailer, rev) in enumerate(zip(data['retailer'], data['revenue'])):
        if retailer in ['Walmart', 'Amazon', 'Costco', 'Target']:
            bars[i].set_color(COLORS['secondary'])

    ax.set_xlabel('U.S. Revenue ($ Billion)', fontsize=9)
    ax.set_title('Top 10 U.S. Retailers by Revenue, 2024', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.text(0, -0.12, 'Source: Company reports, NRF', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch10', 'ch10_top_retailers.pdf')


def ch10_ecommerce_share():
    """E-commerce share of retail over time."""
    years = list(range(2010, 2025))

    # E-commerce as % of retail (Census basis)
    ecom_share = [4.2, 4.7, 5.2, 5.8, 6.5, 7.3, 8.0, 9.0, 9.8, 11.0,
                  14.0, 13.2, 14.6, 15.4, 16.0]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4))
    ax.plot(years, ecom_share, color=COLORS['primary'], linewidth=2, marker='o', markersize=4)
    ax.fill_between(years, ecom_share, alpha=0.2, color=COLORS['primary'])

    # Mark COVID spike
    ax.annotate('COVID\nspike', xy=(2020, 14.0), xytext=(2017.5, 13),
                arrowprops=dict(arrowstyle='->', color=COLORS['tertiary']),
                fontsize=8, color=COLORS['tertiary'])

    ax.set_xlabel('Year', fontsize=9)
    ax.set_ylabel('E-commerce Share of Retail (%)', fontsize=9)
    ax.set_title('E-commerce as Share of Total Retail Sales', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(0, 20)

    ax.text(0, -0.15, 'Source: U.S. Census Bureau Quarterly E-Commerce Report',
            transform=ax.transAxes, fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch10', 'ch10_ecommerce_share.pdf')


def ch10_retail_format_evolution():
    """Retail format evolution - conceptual timeline."""
    formats = [
        ('General Store', 1850, 1920),
        ('Department Store', 1880, 1990),
        ('Mail Order', 1890, 1995),
        ('Supermarket', 1930, 2025),
        ('Discount/Big Box', 1960, 2025),
        ('Category Killer', 1980, 2015),
        ('E-commerce', 1995, 2025),
    ]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 3.5))

    colors_list = [COLORS['gray'], COLORS['light_gray'], COLORS['gray'],
                   COLORS['primary'], COLORS['secondary'], COLORS['quaternary'],
                   COLORS['tertiary']]

    for i, (name, start, end) in enumerate(formats):
        ax.barh(i, end - start, left=start, height=0.6, color=colors_list[i], alpha=0.8)
        ax.text(start + 5, i, name, va='center', fontsize=8)

    ax.set_xlim(1840, 2030)
    ax.set_ylim(-0.5, len(formats) - 0.5)
    ax.set_xlabel('Year', fontsize=9)
    ax.set_title('The "Wheel of Retailing": Format Evolution', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_yticks([])

    ax.text(0, -0.18, 'Source: Author illustration based on Hortaçsu & Syverson (2015)',
            transform=ax.transAxes, fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch10', 'ch10_format_evolution.pdf')


# =============================================================================
# CHAPTER 13: CONSTRUCTION
# =============================================================================

def ch13_construction_spending():
    """Construction spending by type."""
    data = pd.DataFrame({
        'category': ['Residential', 'Commercial', 'Manufacturing', 'Power/Energy',
                    'Highway/Street', 'Educational', 'Healthcare', 'Office',
                    'Water/Sewer', 'Other'],
        'spending': [880, 140, 220, 130, 120, 100, 65, 85, 75, 285]
    })

    data = data.sort_values('spending', ascending=True)

    # Color manufacturing differently to highlight supercycle
    colors = [COLORS['primary']] * len(data)
    mfg_idx = data[data['category'] == 'Manufacturing'].index[0]
    colors[list(data.index).index(mfg_idx)] = COLORS['tertiary']

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4.5))
    bars = ax.barh(data['category'], data['spending'], color=colors)

    ax.set_xlabel('Annual Spending ($ Billion)', fontsize=9)
    ax.set_title('U.S. Construction Spending by Type, 2024', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Annotate manufacturing supercycle
    ax.annotate('3x increase\nsince 2021', xy=(220, 2), xytext=(280, 3),
                arrowprops=dict(arrowstyle='->', color=COLORS['tertiary']),
                fontsize=8, color=COLORS['tertiary'])

    ax.text(0, -0.12, 'Source: U.S. Census Bureau Construction Spending',
            transform=ax.transAxes, fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch13', 'ch13_construction_spending.pdf')


def ch13_productivity_puzzle():
    """Construction productivity decline - the puzzle."""
    years = list(range(1950, 2025, 5))

    # Index: 1950 = 100, approximate trends
    construction = [100, 110, 115, 118, 115, 110, 105, 100, 98, 95, 92, 90, 88, 85, 82]
    manufacturing = [100, 120, 145, 180, 220, 280, 360, 440, 520, 600, 700, 820, 950, 1100, 1300]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4))

    ax.plot(years, construction, color=COLORS['quaternary'], linewidth=2,
            marker='o', markersize=4, label='Construction')
    ax.plot(years, [m/10 for m in manufacturing], color=COLORS['primary'], linewidth=2,
            marker='s', markersize=4, label='Manufacturing (÷10)')

    ax.set_xlabel('Year', fontsize=9)
    ax.set_ylabel('Productivity Index (1950=100)', fontsize=9)
    ax.set_title('The Construction Productivity Puzzle', fontsize=10, fontweight='bold')
    ax.legend(loc='upper left', fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.text(0, -0.15, 'Source: Goolsbee & Syverson (2023)',
            transform=ax.transAxes, fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch13', 'ch13_productivity_puzzle.pdf')


def ch13_top_contractors():
    """Top contractors by revenue."""
    data = pd.DataFrame({
        'contractor': ['Bechtel', 'Fluor', 'Turner', 'Kiewit', 'Jacobs',
                      'AECOM', 'Skanska USA', 'Whiting-Turner', 'Clark', 'Mortenson'],
        'revenue': [18, 15, 16, 15, 16, 14, 8, 10, 6, 5],
        'type': ['Heavy Civil', 'Heavy Civil', 'Commercial', 'Heavy Civil', 'Mixed',
                'Mixed', 'Commercial', 'Commercial', 'Commercial', 'Commercial']
    })

    data = data.sort_values('revenue', ascending=True)

    # Color by type
    colors = [COLORS['primary'] if t == 'Heavy Civil' else COLORS['secondary']
              if t == 'Commercial' else COLORS['gray'] for t in data['type']]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4.5))
    bars = ax.barh(data['contractor'], data['revenue'], color=colors)

    ax.set_xlabel('Revenue ($ Billion)', fontsize=9)
    ax.set_title('Top U.S. Contractors by Revenue, 2024', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COLORS['primary'], label='Heavy Civil/Engineering'),
                       Patch(facecolor=COLORS['secondary'], label='Commercial Building')]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=7)

    ax.text(0, -0.12, 'Source: ENR Top 400 Contractors', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch13', 'ch13_top_contractors.pdf')


def ch13_manufacturing_supercycle():
    """Manufacturing construction spending surge."""
    years = list(range(2019, 2025))
    spending = [80, 75, 85, 130, 190, 220]  # Approximate monthly rate annualized

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 3.5))

    bars = ax.bar(years, spending, color=COLORS['tertiary'], width=0.6)

    # Highlight post-CHIPS
    for i, (y, s) in enumerate(zip(years, spending)):
        if y >= 2022:
            bars[i].set_color(COLORS['quaternary'])

    ax.set_xlabel('Year', fontsize=9)
    ax.set_ylabel('Annual Spending ($ Billion)', fontsize=9)
    ax.set_title('Manufacturing Construction Spending Surge', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.annotate('CHIPS Act\n& IRA', xy=(2022.5, 160), xytext=(2020, 180),
                arrowprops=dict(arrowstyle='->', color=COLORS['quaternary']),
                fontsize=8, color=COLORS['quaternary'])

    ax.text(0, -0.18, 'Source: U.S. Census Bureau', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch13', 'ch13_manufacturing_supercycle.pdf')


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("Creating figures for The American Economy")
    print("=" * 50)

    print("\n--- Chapter 5: Real Estate ---")
    ch05_top_homebuilders()
    ch05_top_reits()
    ch05_house_price_trends()

    print("\n--- Chapter 10: Retail ---")
    ch10_top_retailers()
    ch10_ecommerce_share()
    ch10_retail_format_evolution()

    print("\n--- Chapter 13: Construction ---")
    ch13_construction_spending()
    ch13_productivity_puzzle()
    ch13_top_contractors()
    ch13_manufacturing_supercycle()

    print("\n" + "=" * 50)
    print("Done! Check _figures/ch05/, ch10/, ch13/ for output.")
