"""
Federal Employment by State - Choropleth Map - Chapter 4
The American Economy

Creates a choropleth map showing federal civilian employment by state.
Data: OPM FedScope, September 2023
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geopandas as gpd
import pandas as pd
import numpy as np

# Federal civilian employment by state, September 2023
# Source: OPM FedScope (https://www.opm.gov/data/datasets/)
# Excludes military, postal service shown separately

fed_employment = {
    'state': [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
        'DC'
    ],
    'fed_employees': [
        38500, 16200, 47800, 13200, 176400, 57300, 10800, 4200, 97600, 78900,
        25100, 8600, 49100, 24500, 8200, 20100, 26600, 17800, 8900, 147200,
        34800, 27100, 17400, 18400, 36700, 9800, 10800, 15100, 4200, 35000,
        28600, 60300, 46900, 7300, 53700, 36100, 24200, 61700, 5600, 26000,
        10200, 33300, 149200, 38200, 3800, 183400, 60800, 14600, 16100, 4100,
        152300  # DC - federal workforce hub
    ],
    # State population 2023 (thousands) for per-capita calculation
    'population': [
        5108, 733, 7431, 3067, 38965, 5877, 3617, 1018, 22611, 11029,
        1440, 1964, 12582, 6876, 3207, 2940, 4526, 4590, 1395, 6180,
        7001, 10037, 5737, 2940, 6196, 1133, 1978, 3194, 1402, 9290,
        2114, 19571, 10835, 783, 11785, 4053, 4233, 12972, 1096, 5282,
        919, 7126, 30503, 3423, 648, 8683, 7812, 1770, 5910, 584,
        678  # DC
    ]
}

df = pd.DataFrame(fed_employment)
df['fed_per_1000'] = df['fed_employees'] / df['population']

# Load US states shapefile
# Using natural earth data via geopandas
us_states = gpd.read_file(
    'https://www2.census.gov/geo/tiger/GENZ2021/shp/cb_2021_us_state_20m.zip'
)

# Filter to 50 states + DC, exclude territories
us_states = us_states[~us_states['STUSPS'].isin(['PR', 'VI', 'GU', 'AS', 'MP'])]

# Merge with employment data
us_states = us_states.merge(df, left_on='STUSPS', right_on='state', how='left')

# Create figure with two maps: total and per capita
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ----- Map 1: Total Federal Employment -----
ax1 = axes[0]

# Shift Alaska and Hawaii for display
# For simplicity, just plot continental US + note about AK/HI
continental = us_states[~us_states['STUSPS'].isin(['AK', 'HI'])]

continental.plot(
    column='fed_employees',
    ax=ax1,
    legend=True,
    legend_kwds={
        'label': 'Federal employees',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.02,
        'format': lambda x, _: f'{x/1000:.0f}K'
    },
    cmap='Blues',
    edgecolor='white',
    linewidth=0.5,
    missing_kwds={'color': 'lightgray'}
)

ax1.set_xlim(-130, -65)
ax1.set_ylim(24, 50)
ax1.axis('off')
ax1.set_title('Total Federal Civilian Employment', fontsize=10, fontweight='bold')

# Highlight DC/MD/VA cluster
ax1.annotate(
    'DC-MD-VA:\n483K (22%)',
    xy=(-77, 39),
    xytext=(-68, 32),
    fontsize=7,
    ha='center',
    arrowprops=dict(arrowstyle='->', color='#333333', lw=0.8)
)

# ----- Map 2: Federal Employment Per 1,000 Population -----
ax2 = axes[1]

continental.plot(
    column='fed_per_1000',
    ax=ax2,
    legend=True,
    legend_kwds={
        'label': 'Per 1,000 residents',
        'orientation': 'horizontal',
        'shrink': 0.7,
        'pad': 0.02,
    },
    cmap='Oranges',
    edgecolor='white',
    linewidth=0.5,
    missing_kwds={'color': 'lightgray'}
)

ax2.set_xlim(-130, -65)
ax2.set_ylim(24, 50)
ax2.axis('off')
ax2.set_title('Federal Employment Per 1,000 Residents', fontsize=10, fontweight='bold')

# Highlight DC
ax2.annotate(
    'DC: 225\nper 1,000',
    xy=(-77, 39),
    xytext=(-68, 32),
    fontsize=7,
    ha='center',
    arrowprops=dict(arrowstyle='->', color='#333333', lw=0.8)
)

# Main title
fig.suptitle('Federal Civilian Employment by State, 2023', fontsize=12, fontweight='bold', y=1.02)

# Source note
fig.text(
    0.5, -0.02,
    'Source: OPM FedScope (September 2023). Excludes military and postal workers.\n'
    'Alaska (16K) and Hawaii (25K) not shown. Total federal civilian workforce: ~2.2 million.',
    ha='center',
    fontsize=7,
    fontstyle='italic'
)

plt.tight_layout()

# Save
output_path = r'G:\My Drive\book drafts\the american economy\_figures\ch04\ch04_federal_employment_map.pdf'
fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Saved to {output_path}")

# Also save PNG for preview
png_path = output_path.replace('.pdf', '.png')
fig.savefig(png_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Preview saved to {png_path}")

plt.close()

# Print summary statistics
print("\nTop 10 States by Federal Employment:")
print("-" * 50)
top10 = df.nlargest(10, 'fed_employees')
for _, row in top10.iterrows():
    print(f"{row['state']:5} {row['fed_employees']:>8,} employees  ({row['fed_per_1000']:>5.1f} per 1K)")

print("\nTop 10 States by Federal Employment Per Capita:")
print("-" * 50)
top10_pc = df.nlargest(10, 'fed_per_1000')
for _, row in top10_pc.iterrows():
    print(f"{row['state']:5} {row['fed_per_1000']:>6.1f} per 1K  ({row['fed_employees']:>8,} total)")

# DC-MD-VA total
dmv = df[df['state'].isin(['DC', 'MD', 'VA'])]['fed_employees'].sum()
total = df['fed_employees'].sum()
print(f"\nDC-MD-VA cluster: {dmv:,} ({dmv/total*100:.1f}% of total)")
print(f"Total federal civilian employees: {total:,}")
