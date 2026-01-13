"""
Create visualizations for economic shock analysis.
Uses data pulled from FRED, BEA, and BLS.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_DIR = Path(r"G:\My Drive\book drafts\the american economy\_data\shock_analysis")
OUTPUT_DIR = Path(r"G:\My Drive\book drafts\the american economy\_figures\shock_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Style settings
plt.style.use('seaborn-v0_8-whitegrid')
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'tertiary': '#2ca02c',
    'negative': '#d62728',
    'neutral': '#7f7f7f'
}

def save_figure(fig, name):
    """Save figure in both PDF and PNG formats."""
    fig.savefig(OUTPUT_DIR / f'{name}.pdf', bbox_inches='tight', dpi=300)
    fig.savefig(OUTPUT_DIR / f'{name}.png', bbox_inches='tight', dpi=150)
    plt.close(fig)
    print(f"  -> Saved {name}")

# ==============================================================================
# 1. OIL PRICE SHOCK (2014-2016)
# ==============================================================================

def create_oil_price_figure():
    """Create oil price collapse visualization."""
    print("Creating oil price shock figure...")

    # Load data
    brent = pd.read_csv(DATA_DIR / 'fred_dcoilbrenteu.csv')
    brent['date'] = pd.to_datetime(brent['date'])

    # Filter to 2010-2020 for context
    mask = (brent['date'] >= '2010-01-01') & (brent['date'] <= '2020-12-31')
    brent = brent[mask]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(brent['date'], brent['DCOILBRENTEU'], color=COLORS['primary'], linewidth=1.5)

    # Shade the collapse period
    ax.axvspan(pd.Timestamp('2014-06-01'), pd.Timestamp('2016-02-01'),
               alpha=0.2, color=COLORS['negative'], label='Oil price collapse')

    # Annotations
    ax.annotate('$115/bbl\nJune 2014', xy=(pd.Timestamp('2014-06-20'), 112),
                fontsize=9, ha='center')
    ax.annotate('$28/bbl\nJan 2016', xy=(pd.Timestamp('2016-01-20'), 30),
                fontsize=9, ha='center')

    ax.set_xlabel('')
    ax.set_ylabel('Brent Crude Oil ($/barrel)')
    ax.set_title('The 2014-2016 Oil Price Collapse', fontsize=12, fontweight='bold')

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    ax.set_ylim(0, 140)
    ax.legend(loc='upper right')

    fig.tight_layout()
    save_figure(fig, 'oil_price_collapse')

def create_oil_shock_unemployment():
    """Create unemployment comparison for energy states."""
    print("Creating oil shock unemployment figure...")

    # Load data
    tx = pd.read_csv(DATA_DIR / 'fred_txur.csv')
    nd = pd.read_csv(DATA_DIR / 'fred_ndur.csv')
    ok = pd.read_csv(DATA_DIR / 'fred_okur.csv')
    us = pd.read_csv(DATA_DIR / 'fred_unrate.csv')

    for df in [tx, nd, ok, us]:
        df['date'] = pd.to_datetime(df['date'])

    # Merge
    merged = tx.rename(columns={'TXUR': 'Texas'})
    merged = merged.merge(nd.rename(columns={'NDUR': 'North Dakota'}), on='date', how='outer')
    merged = merged.merge(ok.rename(columns={'OKUR': 'Oklahoma'}), on='date', how='outer')
    merged = merged.merge(us.rename(columns={'UNRATE': 'U.S.'}), on='date', how='outer')

    # Filter to 2010-2020
    mask = (merged['date'] >= '2010-01-01') & (merged['date'] <= '2020-01-01')
    merged = merged[mask]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(merged['date'], merged['U.S.'], color=COLORS['neutral'], linewidth=2,
            linestyle='--', label='U.S. Average')
    ax.plot(merged['date'], merged['Texas'], color=COLORS['primary'], linewidth=1.5,
            label='Texas')
    ax.plot(merged['date'], merged['North Dakota'], color=COLORS['secondary'], linewidth=1.5,
            label='North Dakota')
    ax.plot(merged['date'], merged['Oklahoma'], color=COLORS['tertiary'], linewidth=1.5,
            label='Oklahoma')

    # Shade the oil shock period
    ax.axvspan(pd.Timestamp('2014-06-01'), pd.Timestamp('2016-12-01'),
               alpha=0.15, color=COLORS['negative'])

    ax.set_xlabel('')
    ax.set_ylabel('Unemployment Rate (%)')
    ax.set_title('Energy State Unemployment During Oil Price Collapse', fontsize=12, fontweight='bold')

    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    ax.legend(loc='upper right')
    ax.set_ylim(0, 12)

    fig.tight_layout()
    save_figure(fig, 'oil_shock_unemployment')

# ==============================================================================
# 2. CHINA SHOCK (Manufacturing Employment)
# ==============================================================================

def create_manufacturing_employment():
    """Create manufacturing employment decline visualization."""
    print("Creating manufacturing employment figure...")

    mfg = pd.read_csv(DATA_DIR / 'fred_manemp.csv')
    mfg['date'] = pd.to_datetime(mfg['date'])

    # Filter 1990-2024
    mask = (mfg['date'] >= '1990-01-01')
    mfg = mfg[mask]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(mfg['date'], mfg['MANEMP'] / 1000, color=COLORS['primary'], linewidth=2)

    # Key periods
    ax.axvspan(pd.Timestamp('2001-12-01'), pd.Timestamp('2010-01-01'),
               alpha=0.15, color=COLORS['negative'], label='China Shock period')
    ax.axvspan(pd.Timestamp('2008-01-01'), pd.Timestamp('2010-06-01'),
               alpha=0.15, color=COLORS['secondary'])

    # Annotations
    ax.annotate('China joins WTO\n(Dec 2001)', xy=(pd.Timestamp('2001-12-01'), 17),
                xytext=(pd.Timestamp('1998-01-01'), 18.5),
                arrowprops=dict(arrowstyle='->', color='gray'),
                fontsize=9, ha='center')
    ax.annotate('2008 Financial\nCrisis', xy=(pd.Timestamp('2008-09-01'), 13.5),
                xytext=(pd.Timestamp('2005-01-01'), 12),
                arrowprops=dict(arrowstyle='->', color='gray'),
                fontsize=9, ha='center')

    ax.set_xlabel('')
    ax.set_ylabel('Manufacturing Employment (millions)')
    ax.set_title('The Decline of American Manufacturing Employment', fontsize=12, fontweight='bold')

    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    ax.set_ylim(10, 20)

    fig.tight_layout()
    save_figure(fig, 'manufacturing_employment')

# ==============================================================================
# 3. MONETARY POLICY SHOCK (2022-2023)
# ==============================================================================

def create_mortgage_rate_figure():
    """Create mortgage rate surge visualization."""
    print("Creating mortgage rate figure...")

    mortgage = pd.read_csv(DATA_DIR / 'fred_mortgage30us.csv')
    mortgage['date'] = pd.to_datetime(mortgage['date'])

    # Filter 2018-present
    mask = mortgage['date'] >= '2018-01-01'
    mortgage = mortgage[mask]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(mortgage['date'], mortgage['MORTGAGE30US'], color=COLORS['primary'], linewidth=2)

    # Shade the tightening period
    ax.axvspan(pd.Timestamp('2022-03-01'), pd.Timestamp('2023-12-01'),
               alpha=0.15, color=COLORS['negative'], label='Fed tightening cycle')

    # Annotations
    ax.annotate('Pre-COVID:\n3.5%', xy=(pd.Timestamp('2020-01-01'), 3.7),
                fontsize=9, ha='center')
    ax.annotate('COVID low:\n2.65%', xy=(pd.Timestamp('2021-01-01'), 2.8),
                fontsize=9, ha='center')
    ax.annotate('Peak:\n7.8%', xy=(pd.Timestamp('2023-10-15'), 7.9),
                fontsize=9, ha='center')

    ax.set_xlabel('')
    ax.set_ylabel('30-Year Fixed Mortgage Rate (%)')
    ax.set_title('The 2022-2023 Mortgage Rate Shock', fontsize=12, fontweight='bold')

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    ax.set_ylim(2, 9)
    ax.legend(loc='upper left')

    fig.tight_layout()
    save_figure(fig, 'mortgage_rate_shock')

def create_housing_starts_figure():
    """Create housing starts response to rate hikes."""
    print("Creating housing starts figure...")

    starts = pd.read_csv(DATA_DIR / 'fred_houst.csv')
    starts['date'] = pd.to_datetime(starts['date'])

    # Filter 2018-present
    mask = starts['date'] >= '2018-01-01'
    starts = starts[mask]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(starts['date'], starts['HOUST'], color=COLORS['primary'], linewidth=2)

    # Shade tightening
    ax.axvspan(pd.Timestamp('2022-03-01'), pd.Timestamp('2023-12-01'),
               alpha=0.15, color=COLORS['negative'])

    ax.set_xlabel('')
    ax.set_ylabel('Housing Starts (thousands, SAAR)')
    ax.set_title('Housing Starts Response to Interest Rate Hikes', fontsize=12, fontweight='bold')

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    fig.tight_layout()
    save_figure(fig, 'housing_starts_shock')

# ==============================================================================
# 4. HOUSING PRICE SHOCK (2006-2009)
# ==============================================================================

def create_house_price_figure():
    """Create house price crash visualization."""
    print("Creating house price figure...")

    csi = pd.read_csv(DATA_DIR / 'fred_csushpinsa.csv')
    csi['date'] = pd.to_datetime(csi['date'])

    # Filter 2000-2015 for the housing crisis context
    mask = (csi['date'] >= '2000-01-01') & (csi['date'] <= '2015-12-31')
    csi = csi[mask]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(csi['date'], csi['CSUSHPINSA'], color=COLORS['primary'], linewidth=2)

    # Shade the bust
    ax.axvspan(pd.Timestamp('2006-07-01'), pd.Timestamp('2012-02-01'),
               alpha=0.15, color=COLORS['negative'], label='Housing bust')

    ax.annotate('Peak: July 2006', xy=(pd.Timestamp('2006-07-01'), 185),
                fontsize=9, ha='center')
    ax.annotate('Trough: Feb 2012\n(-27%)', xy=(pd.Timestamp('2012-02-01'), 134),
                fontsize=9, ha='center')

    ax.set_xlabel('')
    ax.set_ylabel('Case-Shiller Index (Jan 2000 = 100)')
    ax.set_title('The Housing Bust: National Home Prices 2000-2015', fontsize=12, fontweight='bold')

    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    ax.legend(loc='upper left')

    fig.tight_layout()
    save_figure(fig, 'housing_price_crash')

def create_house_price_full():
    """Create full house price history including COVID surge."""
    print("Creating full house price history...")

    csi = pd.read_csv(DATA_DIR / 'fred_csushpinsa.csv')
    csi['date'] = pd.to_datetime(csi['date'])

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(csi['date'], csi['CSUSHPINSA'], color=COLORS['primary'], linewidth=2)

    # Shade key periods
    ax.axvspan(pd.Timestamp('2006-07-01'), pd.Timestamp('2012-02-01'),
               alpha=0.15, color=COLORS['negative'], label='2006-2012 bust')
    ax.axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2022-06-01'),
               alpha=0.15, color=COLORS['tertiary'], label='COVID surge')

    ax.set_xlabel('')
    ax.set_ylabel('Case-Shiller Index')
    ax.set_title('U.S. Home Prices: Two Booms, One Bust', fontsize=12, fontweight='bold')

    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    ax.legend(loc='upper left')

    fig.tight_layout()
    save_figure(fig, 'house_price_full_history')

# ==============================================================================
# 5. MULTI-PANEL SHOCK COMPARISON
# ==============================================================================

def create_shock_comparison_panel():
    """Create multi-panel figure comparing different shocks."""
    print("Creating shock comparison panel...")

    # Load all data
    oil = pd.read_csv(DATA_DIR / 'fred_dcoilbrenteu.csv')
    mfg = pd.read_csv(DATA_DIR / 'fred_manemp.csv')
    mortgage = pd.read_csv(DATA_DIR / 'fred_mortgage30us.csv')
    csi = pd.read_csv(DATA_DIR / 'fred_csushpinsa.csv')

    for df in [oil, mfg, mortgage, csi]:
        df['date'] = pd.to_datetime(df['date'])

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Oil shock (2014-2016)
    ax = axes[0, 0]
    mask = (oil['date'] >= '2012-01-01') & (oil['date'] <= '2018-12-31')
    ax.plot(oil[mask]['date'], oil[mask]['DCOILBRENTEU'], color=COLORS['primary'], linewidth=2)
    ax.axvspan(pd.Timestamp('2014-06-01'), pd.Timestamp('2016-02-01'),
               alpha=0.2, color=COLORS['negative'])
    ax.set_title('A. Oil Price Collapse (2014-16)', fontweight='bold')
    ax.set_ylabel('Brent Crude ($/bbl)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Panel 2: China shock (2000-2010)
    ax = axes[0, 1]
    mask = (mfg['date'] >= '1998-01-01') & (mfg['date'] <= '2012-12-31')
    ax.plot(mfg[mask]['date'], mfg[mask]['MANEMP'] / 1000, color=COLORS['primary'], linewidth=2)
    ax.axvspan(pd.Timestamp('2001-12-01'), pd.Timestamp('2010-01-01'),
               alpha=0.2, color=COLORS['negative'])
    ax.set_title('B. Manufacturing Jobs Lost (2000-10)', fontweight='bold')
    ax.set_ylabel('Employment (millions)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Panel 3: Housing bust (2006-2012)
    ax = axes[1, 0]
    mask = (csi['date'] >= '2002-01-01') & (csi['date'] <= '2015-12-31')
    ax.plot(csi[mask]['date'], csi[mask]['CSUSHPINSA'], color=COLORS['primary'], linewidth=2)
    ax.axvspan(pd.Timestamp('2006-07-01'), pd.Timestamp('2012-02-01'),
               alpha=0.2, color=COLORS['negative'])
    ax.set_title('C. Housing Bust (2006-12)', fontweight='bold')
    ax.set_ylabel('Case-Shiller Index')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Panel 4: Rate shock (2022-2023)
    ax = axes[1, 1]
    mask = mortgage['date'] >= '2019-01-01'
    ax.plot(mortgage[mask]['date'], mortgage[mask]['MORTGAGE30US'], color=COLORS['primary'], linewidth=2)
    ax.axvspan(pd.Timestamp('2022-03-01'), pd.Timestamp('2023-12-01'),
               alpha=0.2, color=COLORS['negative'])
    ax.set_title('D. Mortgage Rate Shock (2022-23)', fontweight='bold')
    ax.set_ylabel('30-Year Rate (%)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    for ax in axes.flat:
        ax.tick_params(axis='x', rotation=0)

    fig.suptitle('Major Economic Shocks: A Comparison', fontsize=14, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_figure(fig, 'shock_comparison_panel')

# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Generate all shock analysis figures."""
    print("=" * 60)
    print("GENERATING SHOCK ANALYSIS FIGURES")
    print("=" * 60)
    print()

    # Oil shock
    create_oil_price_figure()
    create_oil_shock_unemployment()

    # China shock
    create_manufacturing_employment()

    # Monetary policy shock
    create_mortgage_rate_figure()
    create_housing_starts_figure()

    # Housing shock
    create_house_price_figure()
    create_house_price_full()

    # Comparison panel
    create_shock_comparison_panel()

    print()
    print("=" * 60)
    print("FIGURE GENERATION COMPLETE")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == '__main__':
    main()
