"""
Top 10 Federal Contractors - Horizontal Bar Chart - Chapter 4
The American Economy

Creates a horizontal bar chart showing top federal contractors by obligations.
Data: USAspending.gov, FY 2023
"""

from plotnine import *
import pandas as pd

# Try to import hrbrthemes
try:
    from hrbrthemes import theme_ipsum
    base_theme = theme_ipsum()
except ImportError:
    base_theme = theme_minimal()

# Top federal contractors FY 2023
# Source: USAspending.gov, Federal Contract Spending by Recipient
# https://www.usaspending.gov/

data = {
    'contractor': [
        'Lockheed Martin',
        'RTX Corporation',
        'General Dynamics',
        'Boeing',
        'Northrop Grumman',
        'Humana',
        'Pfizer',
        'L3Harris Technologies',
        'BAE Systems',
        'Huntington Ingalls',
    ],
    'obligations': [  # Billions USD, FY 2023
        75.0,
        27.4,
        25.8,
        23.7,
        21.5,
        18.2,
        14.9,
        13.8,
        12.1,
        11.2,
    ],
    'sector': [
        'Defense',
        'Defense',
        'Defense',
        'Defense',
        'Defense',
        'Healthcare',
        'Healthcare',
        'Defense',
        'Defense',
        'Defense',
    ]
}

df = pd.DataFrame(data)

# Sort by obligations descending, then reverse for plotting (so largest at top)
df = df.sort_values('obligations', ascending=True).reset_index(drop=True)

# Create ordered categorical
df['contractor'] = pd.Categorical(
    df['contractor'],
    categories=df['contractor'].tolist(),
    ordered=True
)

# Color by sector
sector_colors = {'Defense': '#4E79A7', 'Healthcare': '#59A14F'}

# Calculate total
total = df['obligations'].sum()

# Create figure
fig = (
    ggplot(df, aes(x='contractor', y='obligations', fill='sector'))
    + geom_col(alpha=0.85)
    + geom_text(
        aes(label='obligations'),
        ha='left',
        nudge_y=1,
        size=8,
        format_string='${:.1f}B'
    )
    + coord_flip()
    + scale_fill_manual(values=sector_colors, name='Sector')
    + base_theme
    + theme(
        figure_size=(6, 5),
        panel_grid_major_y=element_blank(),
        panel_grid_minor=element_blank(),
        axis_text_y=element_text(size=9),
        legend_position='top',
        legend_direction='horizontal',
        plot_title=element_text(size=11),
    )
    + labs(
        title='Top 10 Federal Contractors, FY 2023',
        x='',
        y='Contract Obligations ($ billions)',
        caption=f'Source: USAspending.gov (FY 2023).\nTop 10 total: ${total:.0f}B. Defense contractors in blue; healthcare in green.'
    )
    + scale_y_continuous(
        limits=(0, 85),
        breaks=[0, 20, 40, 60, 80]
    )
)

# Save
output_path = r'G:\My Drive\book drafts\the american economy\_figures\ch04\ch04_top_contractors.pdf'
fig.save(output_path, dpi=300)
print(f"Saved to {output_path}")

# Also save PNG for preview
png_path = output_path.replace('.pdf', '.png')
fig.save(png_path, dpi=150)
print(f"Preview saved to {png_path}")

# Print summary
print(f"\nTop 10 Federal Contractors (FY 2023):")
print("-" * 50)
for _, row in df.sort_values('obligations', ascending=False).iterrows():
    print(f"{row['contractor']:25} ${row['obligations']:>5.1f}B  ({row['sector']})")
print("-" * 50)
print(f"{'Top 10 Total':25} ${total:>5.1f}B")

# Defense vs healthcare
defense_total = df[df['sector'] == 'Defense']['obligations'].sum()
health_total = df[df['sector'] == 'Healthcare']['obligations'].sum()
print(f"\nDefense contractors: ${defense_total:.1f}B ({defense_total/total*100:.0f}%)")
print(f"Healthcare contractors: ${health_total:.1f}B ({health_total/total*100:.0f}%)")
