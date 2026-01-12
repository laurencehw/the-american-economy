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
    """Save figure to chapter directory in both PDF and PNG formats."""
    # Save PDF (for print)
    pdf_path = FIGURES_DIR / chapter / filename
    fig.savefig(pdf_path, dpi=DPI, bbox_inches='tight', facecolor='white')
    print(f"Saved: {pdf_path}")

    # Save PNG (for web/GitBook)
    png_path = FIGURES_DIR / chapter / filename.replace('.pdf', '.png')
    fig.savefig(png_path, dpi=DPI, bbox_inches='tight', facecolor='white')
    print(f"Saved: {png_path}")

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
    """Real (inflation-adjusted) house price index trends over time."""
    years = list(range(2000, 2025))

    # Approximate Case-Shiller national index (nominal, 2000=100)
    hpi_nominal = [100, 107, 115, 126, 140, 158, 165, 155, 130, 125,
                   128, 130, 135, 142, 150, 158, 168, 178, 188, 200,
                   220, 260, 290, 300, 310]

    # CPI index (2000=100), approximate
    cpi = [100, 103, 105, 107, 110, 114, 117, 121, 121, 121,
           123, 127, 130, 132, 134, 134, 136, 139, 142, 145,
           147, 154, 166, 173, 178]

    # Real house prices (deflated by CPI)
    hpi_real = [n / c * 100 for n, c in zip(hpi_nominal, cpi)]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4))

    # Plot both nominal and real
    ax.plot(years, hpi_nominal, color=COLORS['light_gray'], linewidth=1.5,
            linestyle='--', label='Nominal', alpha=0.7)
    ax.plot(years, hpi_real, color=COLORS['primary'], linewidth=2, label='Real (2000$)')
    ax.fill_between(years, hpi_real, alpha=0.2, color=COLORS['primary'])

    # Mark key events
    ax.axvline(2008, color=COLORS['quaternary'], linestyle=':', alpha=0.5)
    ax.text(2008.5, 160, '2008\nCrisis', fontsize=7, color=COLORS['quaternary'])
    ax.axvline(2020, color=COLORS['tertiary'], linestyle=':', alpha=0.5)
    ax.text(2020.5, 145, 'COVID\nSurge', fontsize=7, color=COLORS['tertiary'])

    ax.set_xlabel('Year', fontsize=9)
    ax.set_ylabel('House Price Index (2000=100)', fontsize=9)
    ax.set_title('U.S. Real House Prices, 2000-2024', fontsize=10, fontweight='bold')
    ax.legend(loc='upper left', fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(80, 350)

    ax.text(0, -0.15, 'Source: S&P/Case-Shiller, deflated by CPI-U',
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
# CHAPTER 9: MANUFACTURING
# =============================================================================

def ch09_manufacturing_employment():
    """Manufacturing employment decline over time."""
    years = list(range(1950, 2025, 5))

    # Manufacturing employment in millions (approximate)
    employment = [15.2, 16.8, 17.2, 18.5, 19.4, 19.5, 18.4, 17.7, 17.3, 16.8,
                  15.3, 11.5, 12.1, 12.3, 12.8]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4))

    ax.plot(years, employment, color=COLORS['primary'], linewidth=2, marker='o', markersize=4)
    ax.fill_between(years, employment, alpha=0.2, color=COLORS['primary'])

    # Mark key events
    ax.axvline(2000, color=COLORS['quaternary'], linestyle=':', alpha=0.5)
    ax.text(2001, 18.5, 'China WTO\n(2001)', fontsize=7, color=COLORS['quaternary'])
    ax.axvline(2008, color=COLORS['tertiary'], linestyle=':', alpha=0.5)
    ax.text(2009, 14, '2008\nCrisis', fontsize=7, color=COLORS['tertiary'])

    ax.set_xlabel('Year', fontsize=9)
    ax.set_ylabel('Employment (Millions)', fontsize=9)
    ax.set_title('U.S. Manufacturing Employment, 1950-2024', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(10, 21)

    ax.text(0, -0.15, 'Source: BLS Current Employment Statistics',
            transform=ax.transAxes, fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch09', 'ch09_manufacturing_employment.pdf')


def ch09_subsector_value_added():
    """Manufacturing value added by subsector."""
    data = pd.DataFrame({
        'subsector': ['Chemicals', 'Computer/Electronics', 'Food/Beverage',
                     'Transportation Equip.', 'Machinery', 'Petroleum/Coal',
                     'Fabricated Metals', 'Plastics/Rubber', 'Primary Metals', 'Other'],
        'value_added': [420, 360, 310, 280, 200, 180, 175, 130, 95, 350]
    })

    data = data.sort_values('value_added', ascending=True)

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4.5))
    bars = ax.barh(data['subsector'], data['value_added'], color=COLORS['primary'])

    # Highlight top 3
    for i, (sub, val) in enumerate(zip(data['subsector'], data['value_added'])):
        if sub in ['Chemicals', 'Computer/Electronics', 'Food/Beverage']:
            bars[i].set_color(COLORS['secondary'])

    ax.set_xlabel('Value Added ($ Billion)', fontsize=9)
    ax.set_title('U.S. Manufacturing Value Added by Subsector, 2023', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.text(0, -0.12, 'Source: BEA GDP by Industry', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch09', 'ch09_subsector_value_added.pdf')


def ch09_top_manufacturers():
    """Top manufacturers by revenue."""
    data = pd.DataFrame({
        'company': ['Apple', 'Ford', 'GM', 'Tesla', 'Johnson & Johnson',
                   'Boeing', 'RTX (Raytheon)', 'Caterpillar', 'Lockheed Martin', 'Deere'],
        'revenue': [394, 176, 171, 96, 85, 77, 68, 67, 67, 61],
        'sector': ['Electronics', 'Auto', 'Auto', 'Auto', 'Pharma',
                  'Aerospace', 'Defense', 'Machinery', 'Defense', 'Machinery']
    })

    data = data.sort_values('revenue', ascending=True)

    # Color by sector
    sector_colors = {
        'Electronics': COLORS['tertiary'],
        'Auto': COLORS['primary'],
        'Pharma': COLORS['secondary'],
        'Aerospace': COLORS['quaternary'],
        'Defense': COLORS['gray'],
        'Machinery': '#5C946E'
    }
    colors = [sector_colors.get(s, COLORS['gray']) for s in data['sector']]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4.5))
    bars = ax.barh(data['company'], data['revenue'], color=colors)

    ax.set_xlabel('Revenue ($ Billion)', fontsize=9)
    ax.set_title('Top 10 U.S. Manufacturers by Revenue, 2023', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COLORS['tertiary'], label='Electronics'),
                       Patch(facecolor=COLORS['primary'], label='Auto'),
                       Patch(facecolor=COLORS['secondary'], label='Pharma'),
                       Patch(facecolor=COLORS['quaternary'], label='Aerospace'),
                       Patch(facecolor='#5C946E', label='Machinery')]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=6, ncol=2)

    ax.text(0, -0.12, 'Source: Company reports, Fortune 500', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch09', 'ch09_top_manufacturers.pdf')


def ch09_robot_density():
    """Robot density by country - US vs competitors."""
    data = pd.DataFrame({
        'country': ['China', 'Germany', 'Japan', 'South Korea', 'USA'],
        'robots_per_10k': [470, 429, 419, 1012, 295]
    })

    data = data.sort_values('robots_per_10k', ascending=True)

    # Highlight USA
    colors = [COLORS['gray']] * len(data)
    colors[list(data['country']).index('USA')] = COLORS['quaternary']

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 3.5))
    bars = ax.barh(data['country'], data['robots_per_10k'], color=colors)

    ax.set_xlabel('Industrial Robots per 10,000 Manufacturing Workers', fontsize=9)
    ax.set_title('Robot Density in Manufacturing, 2023', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add value labels
    for bar, val in zip(bars, data['robots_per_10k']):
        ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height()/2,
                f'{val:.0f}', va='center', fontsize=8)

    ax.text(0, -0.18, 'Source: International Federation of Robotics', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch09', 'ch09_robot_density.pdf')


# =============================================================================
# CHAPTER 11: INFORMATION, TECHNOLOGY, AND MEDIA
# =============================================================================

def ch11_big_tech_revenue():
    """Big Tech revenue comparison."""
    data = pd.DataFrame({
        'company': ['Amazon', 'Apple', 'Alphabet', 'Microsoft', 'Meta'],
        'revenue': [575, 383, 307, 228, 135]
    })

    data = data.sort_values('revenue', ascending=True)

    # Distinct colors for each company
    company_colors = {
        'Amazon': '#FF9900',
        'Apple': '#555555',
        'Alphabet': '#4285F4',
        'Microsoft': '#00A4EF',
        'Meta': '#0866FF'
    }
    colors = [company_colors[c] for c in data['company']]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 3.5))
    bars = ax.barh(data['company'], data['revenue'], color=colors)

    # Add value labels
    for bar, val in zip(bars, data['revenue']):
        ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2,
                f'${val}B', va='center', fontsize=8)

    ax.set_xlabel('Revenue ($ Billion)', fontsize=9)
    ax.set_title('"Big Five" Tech Company Revenue, 2023', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(0, 650)

    ax.text(0, -0.18, 'Source: Company annual reports', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch11', 'ch11_big_tech_revenue.pdf')


def ch11_digital_ad_market():
    """Digital advertising market share."""
    data = pd.DataFrame({
        'company': ['Google', 'Meta', 'Amazon', 'Microsoft', 'Others'],
        'share': [27, 22, 14, 5, 32]
    })

    colors = ['#4285F4', '#0866FF', '#FF9900', '#00A4EF', COLORS['light_gray']]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4))

    # Horizontal bar for shares
    data_sorted = data.sort_values('share', ascending=True)
    colors_sorted = [colors[list(data['company']).index(c)] for c in data_sorted['company']]

    bars = ax.barh(data_sorted['company'], data_sorted['share'], color=colors_sorted)

    # Add percentage labels
    for bar, val in zip(bars, data_sorted['share']):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{val}%', va='center', fontsize=8)

    ax.set_xlabel('Market Share (%)', fontsize=9)
    ax.set_title('U.S. Digital Advertising Market Share, 2024', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(0, 40)

    ax.text(0, -0.15, 'Source: eMarketer', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch11', 'ch11_digital_ad_market.pdf')


def ch11_streaming_subscribers():
    """Major streaming services by subscribers."""
    data = pd.DataFrame({
        'service': ['Netflix', 'Amazon Prime', 'Disney+', 'Max', 'Paramount+', 'Peacock', 'Apple TV+'],
        'subscribers': [302, 200, 150, 98, 71, 34, 25]
    })

    data = data.sort_values('subscribers', ascending=True)

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4))
    bars = ax.barh(data['service'], data['subscribers'], color=COLORS['primary'])

    # Color Netflix differently as leader
    bars[-1].set_color(COLORS['quaternary'])

    # Add value labels
    for bar, val in zip(bars, data['subscribers']):
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                f'{val}M', va='center', fontsize=8)

    ax.set_xlabel('Global Subscribers (Millions)', fontsize=9)
    ax.set_title('Major Streaming Services by Subscribers, 2024', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(0, 350)

    ax.text(0, -0.12, 'Source: Company reports', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch11', 'ch11_streaming_subscribers.pdf')


def ch11_telecom_market():
    """Wireless carrier market share."""
    data = pd.DataFrame({
        'carrier': ['Verizon', 'AT&T', 'T-Mobile', 'Others'],
        'share': [30, 28, 27, 15]
    })

    colors = ['#CD040B', '#00A8E0', '#E20074', COLORS['light_gray']]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 3.5))

    bars = ax.barh(data['carrier'], data['share'], color=colors)

    # Add percentage labels
    for bar, val in zip(bars, data['share']):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{val}%', va='center', fontsize=8)

    ax.set_xlabel('Market Share (%)', fontsize=9)
    ax.set_title('U.S. Wireless Carrier Market Share, 2024', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(0, 40)

    ax.text(0, -0.18, 'Source: FCC Communications Marketplace Report', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch11', 'ch11_telecom_market.pdf')


# =============================================================================
# CHAPTER 12: TRANSPORTATION AND LOGISTICS
# =============================================================================

def ch12_freight_mode_share():
    """Freight tonnage by mode."""
    data = pd.DataFrame({
        'mode': ['Truck', 'Rail', 'Water', 'Pipeline', 'Air'],
        'ton_miles_pct': [44, 28, 5, 22, 1],
        'value_pct': [67, 8, 4, 8, 13]
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(FIGURE_WIDTH, 3.5))

    # By ton-miles
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['tertiary'],
              COLORS['gray'], COLORS['quaternary']]
    ax1.barh(data['mode'], data['ton_miles_pct'], color=colors)
    ax1.set_xlabel('Share of Ton-Miles (%)', fontsize=8)
    ax1.set_title('By Ton-Miles', fontsize=9, fontweight='bold')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # By value
    ax2.barh(data['mode'], data['value_pct'], color=colors)
    ax2.set_xlabel('Share of Value (%)', fontsize=8)
    ax2.set_title('By Value', fontsize=9, fontweight='bold')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    fig.suptitle('U.S. Freight by Mode, 2023', fontsize=10, fontweight='bold', y=1.02)

    fig.text(0.5, -0.08, 'Source: Bureau of Transportation Statistics',
             ha='center', fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch12', 'ch12_freight_mode_share.pdf')


def ch12_top_ports():
    """Top container ports by TEUs."""
    data = pd.DataFrame({
        'port': ['Los Angeles', 'NY/New Jersey', 'Long Beach', 'Savannah', 'Houston',
                'Seattle/Tacoma', 'Oakland', 'Charleston', 'Norfolk', 'Miami'],
        'teus': [10.7, 9.5, 9.1, 5.9, 4.0, 3.3, 2.5, 2.7, 3.3, 1.2]
    })

    data = data.sort_values('teus', ascending=True)

    # Highlight West Coast ports
    colors = [COLORS['tertiary'] if p in ['Los Angeles', 'Long Beach', 'Seattle/Tacoma', 'Oakland']
              else COLORS['primary'] for p in data['port']]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4.5))
    bars = ax.barh(data['port'], data['teus'], color=colors)

    ax.set_xlabel('Container Volume (Million TEUs)', fontsize=9)
    ax.set_title('Top 10 U.S. Container Ports by Volume, 2023', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COLORS['tertiary'], label='West Coast'),
                       Patch(facecolor=COLORS['primary'], label='East/Gulf Coast')]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=7)

    ax.text(0, -0.12, 'Source: American Association of Port Authorities', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch12', 'ch12_top_ports.pdf')


def ch12_class_i_railroads():
    """Class I railroad revenue."""
    data = pd.DataFrame({
        'railroad': ['Union Pacific', 'BNSF', 'CSX', 'Norfolk Southern', 'CN (US)', 'CPKC (US)'],
        'revenue': [24.1, 23.4, 14.7, 12.2, 8.5, 6.2],
        'region': ['West', 'West', 'East', 'East', 'Both', 'Both']
    })

    data = data.sort_values('revenue', ascending=True)

    # Color by region
    colors = [COLORS['tertiary'] if r == 'West' else COLORS['primary'] if r == 'East'
              else COLORS['gray'] for r in data['region']]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 3.5))
    bars = ax.barh(data['railroad'], data['revenue'], color=colors)

    ax.set_xlabel('Revenue ($ Billion)', fontsize=9)
    ax.set_title('Class I Railroad Revenue, 2023', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COLORS['tertiary'], label='Western'),
                       Patch(facecolor=COLORS['primary'], label='Eastern'),
                       Patch(facecolor=COLORS['gray'], label='Cross-border')]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=7)

    ax.text(0, -0.18, 'Source: Association of American Railroads', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch12', 'ch12_class_i_railroads.pdf')


def ch12_airline_market_share():
    """Domestic airline market share."""
    data = pd.DataFrame({
        'airline': ['Delta', 'American', 'Southwest', 'United', 'JetBlue', 'Alaska', 'Spirit', 'Others'],
        'share': [17.8, 17.5, 17.3, 16.0, 5.2, 5.5, 4.8, 15.9]
    })

    # Airline brand colors
    colors = ['#E31837', '#0078D2', '#FFBF27', '#005DAA', '#003876', '#01426A', '#FFDC00', COLORS['light_gray']]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4))

    data_sorted = data.sort_values('share', ascending=True)
    colors_sorted = [colors[list(data['airline']).index(a)] for a in data_sorted['airline']]

    bars = ax.barh(data_sorted['airline'], data_sorted['share'], color=colors_sorted)

    # Add percentage labels
    for bar, val in zip(bars, data_sorted['share']):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f'{val}%', va='center', fontsize=8)

    ax.set_xlabel('Domestic Market Share (%)', fontsize=9)
    ax.set_title('U.S. Domestic Airline Market Share, 2023', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(0, 22)

    ax.text(0, -0.12, 'Source: DOT T-100 Domestic Segment Data', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch12', 'ch12_airline_market_share.pdf')


def ch12_top_trucking():
    """Top trucking and logistics companies by revenue."""
    data = pd.DataFrame({
        'company': ['UPS', 'FedEx', 'J.B. Hunt', 'Old Dominion', 'Knight-Swift',
                   'XPO', 'Schneider', 'Landstar', 'Werner', 'Saia'],
        'revenue': [100.3, 92.6, 12.4, 6.3, 6.1, 4.6, 5.5, 6.1, 3.0, 3.0],
        'type': ['Integrated', 'Integrated', 'Intermodal', 'LTL', 'TL',
                'LTL', 'TL', 'Brokerage', 'TL', 'LTL']
    })

    data = data.sort_values('revenue', ascending=True)

    # Color by type
    type_colors = {
        'Integrated': COLORS['quaternary'],
        'LTL': COLORS['primary'],
        'TL': COLORS['secondary'],
        'Intermodal': COLORS['tertiary'],
        'Brokerage': COLORS['gray']
    }
    colors = [type_colors.get(t, COLORS['gray']) for t in data['type']]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4.5))
    bars = ax.barh(data['company'], data['revenue'], color=colors)

    ax.set_xlabel('Revenue ($ Billion)', fontsize=9)
    ax.set_title('Top Trucking & Logistics Companies by Revenue, 2023', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COLORS['quaternary'], label='Integrated'),
                       Patch(facecolor=COLORS['primary'], label='LTL'),
                       Patch(facecolor=COLORS['secondary'], label='Truckload'),
                       Patch(facecolor=COLORS['tertiary'], label='Intermodal')]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=6)

    ax.text(0, -0.12, 'Source: Company reports', transform=ax.transAxes,
            fontsize=7, style='italic', color='gray')

    plt.tight_layout()
    save_figure(fig, 'ch12', 'ch12_top_trucking.pdf')


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("Creating figures for The American Economy")
    print("=" * 50)

    # Ensure directories exist
    for ch in ['ch05', 'ch09', 'ch10', 'ch11', 'ch12', 'ch13']:
        (FIGURES_DIR / ch).mkdir(parents=True, exist_ok=True)

    print("\n--- Chapter 5: Real Estate ---")
    ch05_top_homebuilders()
    ch05_top_reits()
    ch05_house_price_trends()

    print("\n--- Chapter 9: Manufacturing ---")
    ch09_manufacturing_employment()
    ch09_subsector_value_added()
    ch09_top_manufacturers()
    ch09_robot_density()

    print("\n--- Chapter 10: Retail ---")
    ch10_top_retailers()
    ch10_ecommerce_share()
    ch10_retail_format_evolution()

    print("\n--- Chapter 11: Tech/Media ---")
    ch11_big_tech_revenue()
    ch11_digital_ad_market()
    ch11_streaming_subscribers()
    ch11_telecom_market()

    print("\n--- Chapter 12: Transportation ---")
    ch12_freight_mode_share()
    ch12_top_ports()
    ch12_class_i_railroads()
    ch12_airline_market_share()
    ch12_top_trucking()

    print("\n--- Chapter 13: Construction ---")
    ch13_construction_spending()
    ch13_productivity_puzzle()
    ch13_top_contractors()
    ch13_manufacturing_supercycle()

    print("\n" + "=" * 50)
    print("Done! Check _figures/ subdirectories for output.")
