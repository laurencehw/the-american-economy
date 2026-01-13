"""
Create figures for Part V regional chapters using fresh data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Paths
DATA_DIR = Path(r"G:\My Drive\book drafts\the american economy\_data\regional")
FIG_DIR = Path(r"G:\My Drive\book drafts\the american economy\_figures")

# Regional groupings
NORTHEAST = ['NY', 'PA', 'NJ', 'MA', 'CT', 'MD']
SUNBELT = ['TX', 'FL', 'GA', 'NC', 'AZ', 'TN', 'CO']
MIDWEST = ['IL', 'OH', 'MI', 'IN', 'WI', 'MN', 'MO']
WEST = ['CA', 'WA', 'CO', 'AZ', 'OR']

# Style settings
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'


def save_figure(fig, name, chapter_dir):
    """Save figure in both PNG and PDF formats."""
    out_dir = FIG_DIR / chapter_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_dir / f'{name}.png', dpi=150, bbox_inches='tight', facecolor='white')
    fig.savefig(out_dir / f'{name}.pdf', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  Saved {name}')


def create_state_gdp_comparison():
    """Create state GDP comparison chart."""
    df = pd.read_csv(DATA_DIR / 'fred_state_gdp.csv')

    # Get latest year
    df['year'] = pd.to_datetime(df['date']).dt.year
    latest = df[df['year'] == df['year'].max()].copy()
    latest['gdp_billions'] = latest['gdp_millions'] / 1000
    latest = latest.sort_values('gdp_billions', ascending=True).tail(15)

    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ['#2c7fb8' if s in ['CA', 'TX', 'NY', 'FL'] else '#7fcdbb'
              for s in latest['state']]
    ax.barh(latest['state'], latest['gdp_billions'], color=colors)
    ax.set_xlabel('GDP ($ Billions)')
    ax.set_title(f'Top 15 State Economies by GDP ({latest["year"].iloc[0]})')
    ax.set_xlim(0, latest['gdp_billions'].max() * 1.1)

    fig.text(0.5, 0.01, 'Source: Bureau of Economic Analysis via FRED',
             ha='center', fontsize=8, style='italic')
    plt.tight_layout()
    save_figure(fig, 'state_gdp_top15', 'regional')


def create_population_growth():
    """Create population growth comparison."""
    df = pd.read_csv(DATA_DIR / 'fred_state_population.csv')
    df['year'] = pd.to_datetime(df['date']).dt.year

    # Calculate growth 2019 to latest
    pivot = df.pivot(index='state', columns='year', values='population_thousands')
    if 2019 in pivot.columns and 2024 in pivot.columns:
        growth = ((pivot[2024] - pivot[2019]) / pivot[2019] * 100).dropna()
    elif 2019 in pivot.columns and 2023 in pivot.columns:
        growth = ((pivot[2023] - pivot[2019]) / pivot[2019] * 100).dropna()
    else:
        cols = sorted(pivot.columns)
        growth = ((pivot[cols[-1]] - pivot[cols[0]]) / pivot[cols[0]] * 100).dropna()

    growth = growth.sort_values()

    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ['#e34a33' if g < 0 else '#2ca25f' for g in growth.values]
    ax.barh(growth.index, growth.values, color=colors)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_xlabel('Population Change (%)')
    ax.set_title('Population Growth by State (2019-2024)')

    fig.text(0.5, 0.01, 'Source: Census Bureau via FRED',
             ha='center', fontsize=8, style='italic')
    plt.tight_layout()
    save_figure(fig, 'population_growth', 'regional')


def create_sunbelt_growth():
    """Create Sunbelt migration/growth chart."""
    df = pd.read_csv(DATA_DIR / 'fred_state_gdp.csv')
    df['year'] = pd.to_datetime(df['date']).dt.year

    sunbelt = ['TX', 'FL', 'GA', 'NC', 'AZ', 'TN']
    df_sun = df[df['state'].isin(sunbelt)].copy()

    pivot = df_sun.pivot(index='year', columns='state', values='gdp_millions')
    # Normalize to 2019 = 100
    if 2019 in pivot.index:
        base = pivot.loc[2019]
        indexed = (pivot / base * 100)
    else:
        base = pivot.iloc[0]
        indexed = (pivot / base * 100)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for state in sunbelt:
        if state in indexed.columns:
            ax.plot(indexed.index, indexed[state], marker='o', label=state, linewidth=2)

    ax.set_xlabel('Year')
    ax.set_ylabel('GDP Index (2019=100)')
    ax.set_title('Sunbelt State GDP Growth')
    ax.legend(loc='upper left', ncol=3)
    ax.grid(True, alpha=0.3)

    fig.text(0.5, 0.01, 'Source: Bureau of Economic Analysis via FRED',
             ha='center', fontsize=8, style='italic')
    plt.tight_layout()
    save_figure(fig, 'ch22_sunbelt_gdp_growth', 'ch22')


def create_midwest_manufacturing():
    """Create Midwest manufacturing focus chart - unemployment trends."""
    df = pd.read_csv(DATA_DIR / 'fred_state_unemployment.csv')
    df['date'] = pd.to_datetime(df['date'])

    midwest = ['IL', 'OH', 'MI', 'IN', 'WI']
    df_mw = df[df['state'].isin(midwest)].copy()

    # Monthly average by state
    monthly = df_mw.groupby(['state', pd.Grouper(key='date', freq='Q')])['unemployment_rate'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for state in midwest:
        state_data = monthly[monthly['state'] == state]
        ax.plot(state_data['date'], state_data['unemployment_rate'], label=state, linewidth=1.5)

    ax.set_xlabel('Date')
    ax.set_ylabel('Unemployment Rate (%)')
    ax.set_title('Midwest State Unemployment Rates')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    fig.text(0.5, 0.01, 'Source: Bureau of Labor Statistics via FRED',
             ha='center', fontsize=8, style='italic')
    plt.tight_layout()
    save_figure(fig, 'ch23_midwest_unemployment', 'ch23')


def create_west_california_dominance():
    """Create chart showing California's dominance in Western economy."""
    df = pd.read_csv(DATA_DIR / 'fred_state_gdp.csv')
    df['year'] = pd.to_datetime(df['date']).dt.year

    west = ['CA', 'WA', 'CO', 'AZ', 'OR', 'NV', 'UT']
    latest = df[df['year'] == df['year'].max()]
    west_data = latest[latest['state'].isin(west)].copy()
    west_data['gdp_billions'] = west_data['gdp_millions'] / 1000
    west_data = west_data.sort_values('gdp_billions', ascending=True)

    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ['#2c7fb8' if s == 'CA' else '#a6bddb' for s in west_data['state']]
    ax.barh(west_data['state'], west_data['gdp_billions'], color=colors)
    ax.set_xlabel('GDP ($ Billions)')
    ax.set_title(f'Western State Economies ({west_data["year"].iloc[0]})')

    # Add annotation for CA
    ca_gdp = west_data[west_data['state'] == 'CA']['gdp_billions'].values[0]
    other_gdp = west_data[west_data['state'] != 'CA']['gdp_billions'].sum()
    ax.annotate(f'CA = {ca_gdp/other_gdp:.1f}x all other Western states combined',
                xy=(ca_gdp * 0.5, 6.2), fontsize=9, style='italic')

    fig.text(0.5, 0.01, 'Source: Bureau of Economic Analysis via FRED',
             ha='center', fontsize=8, style='italic')
    plt.tight_layout()
    save_figure(fig, 'ch24_west_gdp', 'ch24')


def create_metro_gdp_chart():
    """Create top metros by GDP chart."""
    df = pd.read_csv(DATA_DIR / 'bea_metro_gdp.csv')

    # Get latest year and clean data
    df['DataValue'] = pd.to_numeric(df['DataValue'], errors='coerce')
    latest_year = df['TimePeriod'].max()
    latest = df[df['TimePeriod'] == latest_year].copy()
    latest = latest.dropna(subset=['DataValue'])
    latest['gdp_billions'] = latest['DataValue'] / 1000

    # Get top 20 metros
    top20 = latest.nlargest(20, 'gdp_billions')
    top20 = top20.sort_values('gdp_billions', ascending=True)

    # Shorten names
    top20['GeoName'] = top20['GeoName'].str.replace(r'\s*\(Metropolitan Statistical Area\)', '', regex=True)
    top20['GeoName'] = top20['GeoName'].str.split('-').str[0].str.strip()

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.barh(range(len(top20)), top20['gdp_billions'], color='#3182bd')
    ax.set_yticks(range(len(top20)))
    ax.set_yticklabels(top20['GeoName'])
    ax.set_xlabel('GDP ($ Billions)')
    ax.set_title(f'Top 20 Metropolitan Economies ({latest_year})')

    fig.text(0.5, 0.01, 'Source: Bureau of Economic Analysis',
             ha='center', fontsize=8, style='italic')
    plt.tight_layout()
    save_figure(fig, 'metro_gdp_top20', 'regional')


def create_northeast_corridor():
    """Create Northeast corridor metro GDP chart."""
    df = pd.read_csv(DATA_DIR / 'bea_metro_gdp.csv')

    df['DataValue'] = pd.to_numeric(df['DataValue'], errors='coerce')
    latest_year = df['TimePeriod'].max()
    latest = df[df['TimePeriod'] == latest_year].copy()

    # Northeast metros
    ne_metros = ['New York', 'Philadelphia', 'Boston', 'Washington', 'Baltimore', 'Providence', 'Hartford']
    ne_data = latest[latest['GeoName'].str.contains('|'.join(ne_metros), case=False, na=False)]
    ne_data = ne_data.drop_duplicates(subset=['GeoName']).copy()
    ne_data['gdp_billions'] = ne_data['DataValue'] / 1000
    ne_data = ne_data.nlargest(7, 'gdp_billions').sort_values('gdp_billions', ascending=True)

    # Shorten names
    ne_data['GeoName'] = ne_data['GeoName'].str.split('-').str[0].str.strip()

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(ne_data['GeoName'], ne_data['gdp_billions'], color='#3182bd')
    ax.set_xlabel('GDP ($ Billions)')
    ax.set_title(f'Northeast Corridor Metropolitan Economies ({latest_year})')

    fig.text(0.5, 0.01, 'Source: Bureau of Economic Analysis',
             ha='center', fontsize=8, style='italic')
    plt.tight_layout()
    save_figure(fig, 'ch21_northeast_metros', 'ch21')


def create_per_capita_income():
    """Create per capita income by state chart."""
    df = pd.read_csv(DATA_DIR / 'bea_state_income.csv')

    df['DataValue'] = pd.to_numeric(df['DataValue'], errors='coerce')
    latest_year = df['TimePeriod'].max()
    latest = df[df['TimePeriod'] == latest_year].copy()
    latest = latest[~latest['GeoName'].str.contains('United States|region', case=False, na=False)]
    latest = latest.dropna(subset=['DataValue'])

    # Top and bottom 10
    top10 = latest.nlargest(10, 'DataValue')
    bottom10 = latest.nsmallest(10, 'DataValue')

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Top 10
    top10_sorted = top10.sort_values('DataValue', ascending=True)
    axes[0].barh(top10_sorted['GeoName'], top10_sorted['DataValue'] / 1000, color='#2ca25f')
    axes[0].set_xlabel('Per Capita Income ($000s)')
    axes[0].set_title('Highest Per Capita Income')

    # Bottom 10
    bottom10_sorted = bottom10.sort_values('DataValue', ascending=True)
    axes[1].barh(bottom10_sorted['GeoName'], bottom10_sorted['DataValue'] / 1000, color='#e34a33')
    axes[1].set_xlabel('Per Capita Income ($000s)')
    axes[1].set_title('Lowest Per Capita Income')

    fig.suptitle(f'State Per Capita Personal Income ({latest_year})', fontsize=12, fontweight='bold')
    fig.text(0.5, 0.01, 'Source: Bureau of Economic Analysis',
             ha='center', fontsize=8, style='italic')
    plt.tight_layout()
    save_figure(fig, 'ch25_income_disparity', 'ch25')


def main():
    print("Creating regional figures...")
    print()

    # General regional figures
    print("General regional figures:")
    create_state_gdp_comparison()
    create_population_growth()
    create_metro_gdp_chart()
    print()

    # Chapter-specific figures
    print("Ch21 Northeast:")
    create_northeast_corridor()
    print()

    print("Ch22 Sunbelt:")
    create_sunbelt_growth()
    print()

    print("Ch23 Midwest:")
    create_midwest_manufacturing()
    print()

    print("Ch24 West:")
    create_west_california_dominance()
    print()

    print("Ch25 Rural:")
    create_per_capita_income()
    print()

    print("Done!")


if __name__ == '__main__':
    main()
