"""
Government Employment by Level - Stacked Bar Chart - Chapter 4
The American Economy

Creates a stacked bar chart showing government employment by level and function.
Data: BLS Current Employment Statistics, 2023
"""

from plotnine import *
import pandas as pd
import numpy as np

# Try to import hrbrthemes
try:
    from hrbrthemes import theme_ipsum
    base_theme = theme_ipsum()
except ImportError:
    base_theme = theme_minimal()

# Government employment by level and function, 2023 (thousands)
# Source: BLS CES, Series CES9000000001 and components
# https://www.bls.gov/ces/

data = {
    'level': [
        'Federal', 'Federal', 'Federal',
        'State', 'State', 'State', 'State',
        'Local', 'Local', 'Local', 'Local', 'Local',
    ],
    'function': [
        'Defense', 'Postal Service', 'Other Federal',
        'Education', 'Hospitals', 'Other State', 'Administration',
        'Education', 'Hospitals', 'Police & Fire', 'Other Local', 'Administration',
    ],
    'employment': [
        780,    # Federal - Defense (civilian DOD)
        632,    # Federal - Postal Service
        1488,   # Federal - Other (all other agencies)
        2580,   # State - Education (universities, colleges)
        510,    # State - Hospitals
        1890,   # State - Other (highways, corrections, welfare, etc.)
        520,    # State - Administration
        8320,   # Local - Education (K-12 schools)
        680,    # Local - Hospitals
        1150,   # Local - Police & Fire
        2650,   # Local - Other (utilities, parks, sanitation, etc.)
        800,    # Local - Administration
    ]
}

df = pd.DataFrame(data)

# Aggregate by level for the main chart
level_totals = df.groupby('level')['employment'].sum().reset_index()
level_totals['level'] = pd.Categorical(
    level_totals['level'],
    categories=['Federal', 'State', 'Local'],
    ordered=True
)

# For stacked bar, we need function within level
df['level'] = pd.Categorical(
    df['level'],
    categories=['Federal', 'State', 'Local'],
    ordered=True
)

# Simplify function categories for cleaner visualization
def simplify_function(row):
    if row['function'] == 'Education':
        return 'Education'
    elif row['function'] in ['Hospitals']:
        return 'Healthcare'
    elif row['function'] in ['Defense']:
        return 'Defense'
    elif row['function'] == 'Postal Service':
        return 'Postal Service'
    elif row['function'] == 'Police & Fire':
        return 'Public Safety'
    else:
        return 'Other'

df['func_simple'] = df.apply(simplify_function, axis=1)

# Aggregate by level and simplified function
df_agg = df.groupby(['level', 'func_simple'])['employment'].sum().reset_index()

# Order functions for stacking
func_order = ['Education', 'Healthcare', 'Defense', 'Postal Service', 'Public Safety', 'Other']
df_agg['func_simple'] = pd.Categorical(
    df_agg['func_simple'],
    categories=func_order,
    ordered=True
)

# Colors for functions
func_colors = {
    'Education': '#4E79A7',
    'Healthcare': '#59A14F',
    'Defense': '#E15759',
    'Postal Service': '#F28E2B',
    'Public Safety': '#B07AA1',
    'Other': '#BAB0AC',
}

# Calculate totals for labels
totals = df_agg.groupby('level')['employment'].sum().to_dict()

# Create figure
fig = (
    ggplot(df_agg, aes(x='level', y='employment', fill='func_simple'))
    + geom_col(position='stack', alpha=0.85, width=0.7)
    + geom_text(
        data=pd.DataFrame({
            'level': ['Federal', 'State', 'Local'],
            'employment': [totals['Federal'], totals['State'], totals['Local']],
            'label': [f"{totals['Federal']/1000:.1f}M",
                     f"{totals['State']/1000:.1f}M",
                     f"{totals['Local']/1000:.1f}M"]
        }),
        mapping=aes(x='level', y='employment', label='label'),
        va='bottom',
        nudge_y=200,
        size=9,
        inherit_aes=False
    )
    + scale_fill_manual(values=func_colors, name='Function')
    + base_theme
    + theme(
        figure_size=(6, 5),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        legend_position='right',
        plot_title=element_text(size=11),
    )
    + labs(
        title='Government Employment by Level, 2023',
        subtitle='Total: 23 million workers',
        x='',
        y='Employment (thousands)',
        caption='Source: BLS Current Employment Statistics (2023).\nEducation dominates state and local; defense and postal dominate federal.'
    )
    + scale_y_continuous(
        limits=(0, 16000),
        breaks=[0, 4000, 8000, 12000, 16000],
        labels=['0', '4M', '8M', '12M', '16M']
    )
)

# Save
output_path = r'G:\My Drive\book drafts\the american economy\_figures\ch04\ch04_govt_employment_level.pdf'
fig.save(output_path, dpi=300)
print(f"Saved to {output_path}")

# Also save PNG for preview
png_path = output_path.replace('.pdf', '.png')
fig.save(png_path, dpi=150)
print(f"Preview saved to {png_path}")

# Print summary
print(f"\nGovernment Employment by Level and Function (2023, thousands):")
print("-" * 60)
for level in ['Federal', 'State', 'Local']:
    level_data = df_agg[df_agg['level'] == level]
    print(f"\n{level}: {totals[level]:,.0f}K total")
    for _, row in level_data.sort_values('employment', ascending=False).iterrows():
        print(f"  {row['func_simple']:20} {row['employment']:>6,.0f}K")

total = sum(totals.values())
print(f"\n{'='*60}")
print(f"Total Government Employment: {total:,.0f}K ({total/1000:.1f}M)")
print(f"\nBy Level:")
for level in ['Federal', 'State', 'Local']:
    print(f"  {level:10} {totals[level]:>6,.0f}K  ({totals[level]/total*100:.0f}%)")
