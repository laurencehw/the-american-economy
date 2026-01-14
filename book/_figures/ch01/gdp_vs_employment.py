"""
GDP Share vs Employment Share Comparison - Chapter 1
The American Economy

Creates a dot plot comparing GDP share vs employment share by industry.
Highlights capital-intensive vs labor-intensive sectors.
"""

from plotnine import *
import pandas as pd
import numpy as np

# Try to import hrbrthemes, fall back to minimal theme if not available
try:
    from hrbrthemes import theme_ipsum
    base_theme = theme_ipsum()
except ImportError:
    base_theme = theme_minimal()

# Combined data: GDP (BEA 2023) and Employment (BLS 2023)
# Using consistent industry categories

data = {
    'industry': [
        'Real estate',
        'Government',
        'Manufacturing',
        'Professional services',
        'Finance & insurance',
        'Healthcare',
        'Information',
        'Retail trade',
        'Wholesale trade',
        'Construction',
        'Transportation',
        'Accommodation & food',
        'Other services',
        'Educational services',
        'Arts & entertainment',
    ],
    'gdp': [  # Value added, billions
        3851,
        2996,
        2497,
        2453,
        2122,
        1985,
        1686,
        1377,
        1313,
        1087,
        900,
        762,
        568,
        342,
        316,
    ],
    'employment': [  # Thousands
        2484,
        23016,
        12903,
        23198,
        6833,
        21685,
        3030,
        15651,
        6001,
        8025,
        6499,
        16816,
        5851,
        3968,
        2515,
    ]
}

df = pd.DataFrame(data)

# Calculate shares
total_gdp = df['gdp'].sum()
total_emp = df['employment'].sum()
df['gdp_share'] = df['gdp'] / total_gdp * 100
df['emp_share'] = df['employment'] / total_emp * 100

# Calculate ratio (GDP share / Employment share) for sorting
# Higher = more capital intensive, Lower = more labor intensive
df['intensity_ratio'] = df['gdp_share'] / df['emp_share']

# Sort by ratio (most capital-intensive at top)
df = df.sort_values('intensity_ratio', ascending=True).reset_index(drop=True)

# Reshape for plotting
df_long = pd.melt(
    df,
    id_vars=['industry', 'intensity_ratio'],
    value_vars=['gdp_share', 'emp_share'],
    var_name='measure',
    value_name='share'
)

df_long['measure'] = df_long['measure'].map({
    'gdp_share': 'GDP share',
    'emp_share': 'Employment share'
})

# Create ordered categorical for proper sorting
df_long['industry'] = pd.Categorical(
    df_long['industry'],
    categories=df['industry'].tolist(),
    ordered=True
)

# Create figure - dumbbell/dot plot style
fig = (
    ggplot(df_long, aes(x='share', y='industry', color='measure'))
    + geom_line(aes(group='industry'), color='#CCCCCC', size=1)
    + geom_point(size=3, alpha=0.9)
    + scale_color_manual(
        values={'GDP share': '#E15759', 'Employment share': '#4E79A7'},
        name=''
    )
    + base_theme
    + theme(
        figure_size=(6, 6),
        panel_grid_major_y=element_blank(),
        panel_grid_minor=element_blank(),
        legend_position='top',
        legend_direction='horizontal',
        axis_text_y=element_text(size=8),
        plot_title=element_text(size=11),
    )
    + labs(
        title='GDP Share vs. Employment Share by Industry, 2023',
        subtitle='Industries sorted by capital intensity (GDP/worker)',
        x='Share of total (%)',
        y='',
        caption='Source: BEA (GDP), BLS (Employment), 2023.\nLeft side: labor-intensive. Right side: capital-intensive.'
    )
    + scale_x_continuous(limits=(0, 18), breaks=[0, 5, 10, 15])
    # Add annotations for interpretation
    + annotate(
        'text', x=16, y=14.5, label='Capital-\nintensive',
        size=7, color='#666666', ha='center', fontstyle='italic'
    )
    + annotate(
        'text', x=16, y=1.5, label='Labor-\nintensive',
        size=7, color='#666666', ha='center', fontstyle='italic'
    )
)

# Save
output_path = r'G:\My Drive\book drafts\the american economy\_figures\ch01\ch01_gdp_vs_employment.pdf'
fig.save(output_path, dpi=300)
print(f"Saved to {output_path}")

# Also save PNG for preview
png_path = output_path.replace('.pdf', '.png')
fig.save(png_path, dpi=150)
print(f"Preview saved to {png_path}")

# Print summary table
print(f"\nGDP Share vs Employment Share (2023):")
print("-" * 70)
print(f"{'Industry':30} {'GDP %':>8} {'Emp %':>8} {'Ratio':>8}  Type")
print("-" * 70)
for _, row in df.sort_values('intensity_ratio', ascending=False).iterrows():
    intensity = "Capital-int." if row['intensity_ratio'] > 1.5 else \
                "Labor-int." if row['intensity_ratio'] < 0.67 else "Balanced"
    print(f"{row['industry']:30} {row['gdp_share']:>7.1f}% {row['emp_share']:>7.1f}% {row['intensity_ratio']:>8.2f}  {intensity}")
print("-" * 70)
