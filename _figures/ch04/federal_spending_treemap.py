"""
Federal Spending by Function - Treemap - Chapter 4
The American Economy

Creates a treemap showing federal spending by major function.
Data: OMB Budget FY 2024 (actual FY 2023 outlays)
"""

import matplotlib.pyplot as plt
import squarify
import pandas as pd
import numpy as np

# Federal outlays by function, FY 2023 (billions)
# Source: OMB Historical Tables, Table 3.1
# https://www.whitehouse.gov/omb/budget/historical-tables/
# Note: FY2023 Income Security elevated due to pandemic wind-down

data = {
    'function': [
        'Social Security',
        'Medicare',
        'National Defense',
        'Income Security*',
        'Net Interest',
        'Medicaid',
        'Veterans Benefits',
        'Other**',
        'Education',
        'Transportation',
    ],
    'outlays': [
        1354,   # Social Security (Function 650) - OASI + DI
        848,    # Medicare (Function 570)
        821,    # National Defense (Function 050)
        713,    # Income security (Function 600) - adjusted to typical year
        659,    # Net interest on debt (Function 900)
        616,    # Medicaid federal share (in Function 550)
        302,    # Veterans benefits (Function 700)
        430,    # Other (international, science, agriculture, justice, etc.)
        168,    # Education, training, social services (Function 500)
        115,    # Transportation (Function 400)
    ],
    'category': [
        'Mandatory',
        'Mandatory',
        'Discretionary',
        'Mandatory',
        'Mandatory',
        'Mandatory',
        'Mandatory',
        'Mixed',
        'Discretionary',
        'Discretionary',
    ]
}

df = pd.DataFrame(data)
df = df.sort_values('outlays', ascending=False).reset_index(drop=True)

# Calculate percentages
total_spending = df['outlays'].sum()
df['pct'] = df['outlays'] / total_spending * 100

# Create labels - shorter for small boxes
def make_label(row):
    if row['pct'] >= 8:
        return f"{row['function']}\n${row['outlays']:,.0f}B\n({row['pct']:.1f}%)"
    elif row['pct'] >= 4:
        return f"{row['function']}\n${row['outlays']:,.0f}B"
    else:
        return f"{row['function']}\n{row['pct']:.1f}%"

df['label'] = df.apply(make_label, axis=1)

# Color by category
category_colors = {
    'Mandatory': '#E15759',      # Red for mandatory/entitlements
    'Discretionary': '#4E79A7',  # Blue for discretionary
    'Mixed': '#BAB0AC',          # Gray for mixed
}
colors = [category_colors[cat] for cat in df['category']]

# Create figure
fig, ax = plt.subplots(figsize=(6, 5))

# Create treemap
squarify.plot(
    sizes=df['outlays'],
    label=df['label'],
    color=colors,
    alpha=0.85,
    ax=ax,
    text_kwargs={'fontsize': 7, 'fontweight': 'normal', 'fontfamily': 'sans-serif'},
    pad=True
)

# Style
ax.axis('off')
ax.set_title(
    'Federal Spending by Function, FY 2023',
    fontsize=12,
    fontweight='bold',
    fontfamily='sans-serif',
    pad=10
)

# Add legend below the plot
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#E15759', alpha=0.85, label='Mandatory'),
    Patch(facecolor='#4E79A7', alpha=0.85, label='Discretionary'),
    Patch(facecolor='#BAB0AC', alpha=0.85, label='Mixed'),
]
ax.legend(
    handles=legend_elements,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.02),
    ncol=3,
    fontsize=8,
    frameon=False
)

# Add source note
fig.text(
    0.5, -0.06,
    f'Source: OMB Historical Tables (FY 2023). Total: ${total_spending/1000:.1f} trillion.\n'
    '*Income Security = SNAP, housing, SSI, tax credits, unemployment (not Social Security).\n'
    '**Other = International, science, agriculture, justice, general government.',
    ha='center',
    fontsize=6.5,
    fontstyle='italic',
    fontfamily='sans-serif'
)

plt.tight_layout(rect=[0, 0.02, 1, 1])

# Save
output_path = r'G:\My Drive\book drafts\the american economy\_figures\ch04\ch04_spending_treemap.pdf'
fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Saved to {output_path}")

# Also save PNG for preview
png_path = output_path.replace('.pdf', '.png')
fig.savefig(png_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Preview saved to {png_path}")

plt.close()

# Print summary
print(f"\nFederal Spending by Function (FY 2023):")
print("-" * 55)
for _, row in df.iterrows():
    print(f"{row['function']:25} ${row['outlays']:>6,.0f}B  ({row['pct']:4.1f}%)  [{row['category']}]")
print("-" * 55)
print(f"{'Total':25} ${total_spending:>6,.0f}B  (100.0%)")

# Mandatory vs discretionary
mandatory = df[df['category'] == 'Mandatory']['outlays'].sum()
discretionary = df[df['category'] == 'Discretionary']['outlays'].sum()
other = df[df['category'] == 'Mixed']['outlays'].sum()
print(f"\nMandatory spending: ${mandatory:,.0f}B ({mandatory/total_spending*100:.0f}%)")
print(f"Discretionary spending: ${discretionary:,.0f}B ({discretionary/total_spending*100:.0f}%)")
print(f"Interest + Other: ${659 + other:,.0f}B ({(659+other)/total_spending*100:.0f}%)")
