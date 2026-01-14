"""
Employment by Sector - Horizontal Bar Chart - Chapter 1
The American Economy

Creates a horizontal bar chart showing US employment by major industry.
Data: BLS Current Employment Statistics, 2023 annual average
"""

from plotnine import *
import pandas as pd

# Try to import hrbrthemes, fall back to minimal theme if not available
try:
    from hrbrthemes import theme_ipsum
    base_theme = theme_ipsum()
except ImportError:
    base_theme = theme_minimal()

# BLS Employment by Industry 2023 (thousands, annual average)
# Source: BLS CES, Table B-1
# https://www.bls.gov/ces/

data = {
    'industry': [
        'Healthcare & social assistance',
        'Government',
        'Retail trade',
        'Professional & business services',
        'Accommodation & food services',
        'Manufacturing',
        'Construction',
        'Finance & insurance',
        'Transportation & warehousing',
        'Wholesale trade',
        'Other services',
        'Information',
        'Real estate',
        'Educational services',
        'Arts & entertainment',
        'Mining & logging',
        'Utilities',
    ],
    'employment': [
        21685,  # Health care and social assistance
        23016,  # Government (federal + state + local)
        15651,  # Retail trade
        23198,  # Professional and business services
        16816,  # Leisure and hospitality (accommodation & food + arts)
        12903,  # Manufacturing
        8025,   # Construction
        6833,   # Finance and insurance
        6499,   # Transportation and warehousing
        6001,   # Wholesale trade
        5851,   # Other services
        3030,   # Information
        2484,   # Real estate and rental and leasing
        3968,   # Educational services (private)
        2515,   # Arts, entertainment, and recreation (separate from accommodation)
        627,    # Mining and logging
        544,    # Utilities
    ]
}

df = pd.DataFrame(data)

# Sort by employment
df = df.sort_values('employment', ascending=True).reset_index(drop=True)

# Calculate total and percentages
total_emp = df['employment'].sum()
df['pct'] = df['employment'] / total_emp * 100
df['emp_millions'] = df['employment'] / 1000

# Create ordered categorical for proper sorting
df['industry'] = pd.Categorical(df['industry'], categories=df['industry'], ordered=True)

# Create figure
fig = (
    ggplot(df, aes(x='industry', y='emp_millions'))
    + geom_col(fill='#4E79A7', alpha=0.85)
    + geom_text(
        aes(label='employment'),
        ha='left',
        nudge_y=0.3,
        size=7,
        format_string='{:,.0f}K'
    )
    + coord_flip()
    + base_theme
    + theme(
        figure_size=(6, 6.5),
        panel_grid_major_y=element_blank(),
        panel_grid_minor=element_blank(),
        axis_text_y=element_text(size=8),
        plot_title=element_text(size=11, ha='left'),
        plot_margin=0.02,
    )
    + labs(
        title='U.S. Employment by Industry, 2023',
        x='',
        y='Employment (millions)',
        caption=f'Source: Bureau of Labor Statistics, Current Employment Statistics (2023 annual average).\nTotal nonfarm employment: {total_emp/1000:.1f} million.'
    )
    + scale_y_continuous(
        limits=(0, 26),
        breaks=[0, 5, 10, 15, 20, 25]
    )
)

# Save
output_path = r'G:\My Drive\book drafts\the american economy\_figures\ch01\ch01_employment_bar.pdf'
fig.save(output_path, dpi=300)
print(f"Saved to {output_path}")

# Also save PNG for preview
png_path = output_path.replace('.pdf', '.png')
fig.save(png_path, dpi=150)
print(f"Preview saved to {png_path}")

# Print summary
print(f"\nEmployment by Industry (2023):")
print("-" * 55)
for _, row in df.sort_values('employment', ascending=False).iterrows():
    print(f"{row['industry']:35} {row['employment']:>7,}K  ({row['pct']:4.1f}%)")
print("-" * 55)
print(f"{'Total nonfarm':35} {total_emp:>7,}K  (100.0%)")
