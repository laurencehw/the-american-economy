"""
GDP by Industry Treemap - Chapter 1
The American Economy

Creates a treemap showing the composition of US GDP by major industry.
Data: BEA Value Added by Industry, 2023
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import squarify
import pandas as pd
import numpy as np

# BEA GDP by Industry 2023 (Value Added, billions of dollars)
# Source: BEA NIPA Table 1.5.5, Industry Economic Accounts
# https://apps.bea.gov/iTable/?reqid=150&step=2&isuri=1&categories=gdpxind

data = {
    'industry': [
        'Real estate',
        'Professional services',
        'Government',
        'Manufacturing',
        'Finance & insurance',
        'Healthcare',
        'Information',
        'Retail trade',
        'Wholesale trade',
        'Construction',
        'Other services',
        'Transportation',
        'Accommodation & food',
        'Management of companies',
        # Grouped into "Other": Utilities, Mining, Education, Arts, Agriculture
    ],
    'value_added': [
        3851,  # Real estate and rental and leasing
        2453,  # Professional, scientific, and technical services
        2996,  # Government (federal + state/local)
        2497,  # Manufacturing (durable + nondurable)
        2122,  # Finance and insurance
        1985,  # Health care and social assistance
        1686,  # Information
        1377,  # Retail trade
        1313,  # Wholesale trade
        1087,  # Construction
        568,   # Other services (except government)
        900,   # Transportation and warehousing
        762,   # Accommodation and food services
        504,   # Management of companies
    ]
}

df = pd.DataFrame(data)

# Group small sectors into "Other"
# Utilities (396) + Mining (426) + Education (342) + Arts (316) + Agriculture (207) = 1,687
other_total = 396 + 426 + 342 + 316 + 207
other_row = pd.DataFrame({
    'industry': ['Other*'],
    'value_added': [other_total]
})
df = pd.concat([df, other_row], ignore_index=True)

df = df.sort_values('value_added', ascending=False).reset_index(drop=True).copy()

# Calculate percentages
total_gdp = df['value_added'].sum()
df.loc[:, 'pct'] = df['value_added'] / total_gdp * 100

# Create labels - shorter for small boxes
def make_label(row):
    if row['pct'] >= 5:
        return f"{row['industry']}\n${row['value_added']:,.0f}B\n({row['pct']:.1f}%)"
    elif row['pct'] >= 3:
        return f"{row['industry']}\n${row['value_added']:,.0f}B"
    else:
        # Abbreviated labels for tiny boxes
        short_names = {
            'Other services': 'Other svc',
            'Management of companies': 'Mgmt',
            'Accommodation & food': 'Accomm.',
        }
        name = short_names.get(row['industry'], row['industry'])
        return f"{name}\n{row['pct']:.1f}%"

df.loc[:, 'label'] = df.apply(make_label, axis=1)

# Color palette - muted, professional colors (Tableau 10 inspired)
colors = [
    '#4E79A7',  # Real estate - steel blue
    '#E15759',  # Government - red
    '#76B7B2',  # Manufacturing - teal
    '#59A14F',  # Professional services - green
    '#F28E2B',  # Finance - orange
    '#EDC948',  # Healthcare - gold
    '#B07AA1',  # Information - purple
    '#FF9DA7',  # Retail - pink
    '#9C755F',  # Wholesale - brown
    '#BAB0AC',  # Construction - gray
    '#8CD17D',  # Transportation
    '#FABFD2',  # Accommodation
    '#86BCB6',  # Other*
    '#A0CBE8',  # Other services
    '#79706E',  # Management
]

# Create figure
fig, ax = plt.subplots(figsize=(6, 5))

# Create treemap
squarify.plot(
    sizes=df['value_added'],
    label=df['label'],
    color=colors[:len(df)],
    alpha=0.85,
    ax=ax,
    text_kwargs={'fontsize': 7, 'fontweight': 'normal', 'fontfamily': 'sans-serif'},
    pad=True
)

# Style
ax.axis('off')
ax.set_title(
    'U.S. GDP by Industry, 2023',
    fontsize=12,
    fontweight='bold',
    fontfamily='sans-serif',
    pad=10
)

# Add source note
fig.text(
    0.5, 0.02,
    f'Source: Bureau of Economic Analysis, Value Added by Industry (2023). Total: ${total_gdp/1000:.1f} trillion.\n*Other includes: Mining, Utilities, Education, Arts & entertainment, Agriculture.',
    ha='center',
    fontsize=7,
    fontstyle='italic',
    fontfamily='sans-serif'
)

plt.tight_layout(rect=[0, 0.05, 1, 1])

# Save
output_path = r'G:\My Drive\book drafts\the american economy\_figures\ch01\ch01_gdp_treemap.pdf'
fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Saved to {output_path}")

# Also save PNG for preview
png_path = output_path.replace('.pdf', '.png')
fig.savefig(png_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Preview saved to {png_path}")

plt.close()

# Print summary table
print("\nGDP by Industry (2023):")
print("-" * 50)
for _, row in df.iterrows():
    print(f"{row['industry']:25} ${row['value_added']:>6,.0f}B  ({row['pct']:4.1f}%)")
print("-" * 50)
print(f"{'Total':25} ${total_gdp:>6,.0f}B  (100.0%)")
