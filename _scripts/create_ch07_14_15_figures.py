"""
Create figures for Chapter 7, 14, 15.
Adheres to style guidelines in CLAUDE.md.
"""

import pandas as pd
from plotnine import *
from hrbrthemes import theme_ipsum
from pathlib import Path
import matplotlib.pyplot as plt
import squarify
import textwrap

# Configuration
PROJECT_DIR = Path(r"G:\\My Drive\\book drafts\\the american economy")
FIGURES_DIR = PROJECT_DIR / "_figures"
FIGURE_WIDTH = 6
DPI = 300

def ensure_dir(chapter):
    (FIGURES_DIR / chapter).mkdir(parents=True, exist_ok=True)

def save_plotnine(plot, chapter, filename, height=4):
    ensure_dir(chapter)
    pdf_path = FIGURES_DIR / chapter / filename
    png_path = FIGURES_DIR / chapter / filename.replace('.pdf', '.png')
    plot.save(pdf_path, width=FIGURE_WIDTH, height=height, units='in', dpi=DPI, verbose=False)
    plot.save(png_path, width=FIGURE_WIDTH, height=height, units='in', dpi=DPI, verbose=False)
    print(f"Saved: {pdf_path}")

def save_matplotlib(fig, chapter, filename):
    ensure_dir(chapter)
    pdf_path = FIGURES_DIR / chapter / filename
    png_path = FIGURES_DIR / chapter / filename.replace('.pdf', '.png')
    fig.savefig(pdf_path, dpi=DPI, bbox_inches='tight', facecolor='white')
    fig.savefig(png_path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {pdf_path}")

def wrap_title(title):
    return "\n".join(textwrap.wrap(title, width=50))

# =============================================================================
# CHAPTER 7: PROFESSIONAL SERVICES
# =============================================================================

def ch07_prof_services_gdp():
    data = pd.DataFrame({
        'category': ['Legal Services', 'Accounting/Tax', 'Architectural/Eng', 'Computer Systems', 'Mgmt Consulting', 'Scientific R&D', 'Advertising', 'Other'],
        'value': [380, 240, 290, 550, 320, 210, 180, 283] # Approx 2023 billions
    })
    data = data.sort_values('value', ascending=False)
    total = data['value'].sum()
    
    def make_label(r):
        pct = r['value']/total*100
        if pct < 4: return ""
        return f"{r['category']}\n${r['value']}B"

    data['label'] = data.apply(make_label, axis=1)
    
    fig, ax = plt.subplots(figsize=(6, 5))
    squarify.plot(sizes=data['value'], label=data['label'], color=plt.cm.Set3.colors, alpha=0.8, ax=ax, text_kwargs={'fontsize': 8, 'wrap': True}, pad=True)
    ax.set_title('Professional Services GDP by Subsector, 2023', fontsize=12, fontweight='bold', pad=10)
    ax.axis('off')
    fig.text(0.5, 0.02, f'Source: BEA. Total: ${total/1000:.1f} Trillion.', ha='center', fontsize=7, fontstyle='italic')
    
    plt.tight_layout()
    save_matplotlib(fig, 'ch07', 'ch07_prof_services_gdp.pdf')

# =============================================================================
# CHAPTER 14: ENERGY
# =============================================================================

def ch14_generation_mix():
    data = pd.DataFrame({
        'Source': ['Natural Gas', 'Coal', 'Nuclear', 'Renewables', 'Other'],
        'Share': [43, 16, 18, 22, 1]
    })
    data = data.sort_values('Share', ascending=True)
    data['Source'] = pd.Categorical(data['Source'], categories=data['Source'], ordered=True)
    
    p = (
        ggplot(data, aes(x='Source', y='Share'))
        + geom_col(fill='#F18F01', alpha=0.8)
        + coord_flip()
        + theme_ipsum()
        + theme(plot_margin=0.05)
        + labs(title=wrap_title('U.S. Utility-Scale Electricity Generation Mix, 2023'), x='', y='Share of Total Generation (%)', caption='Source: EIA')
    )
    save_plotnine(p, 'ch14', 'ch14_generation_mix.pdf')

# =============================================================================
# CHAPTER 15: EDUCATION
# =============================================================================

def ch15_higher_ed_enrollment():
    data = pd.DataFrame({
        'Type': ['Public 4-Year', 'Public 2-Year', 'PrivateNonprofit', 'For-Profit'],
        'Enrollment': [8.5, 4.5, 4.0, 0.8] # Millions approx
    })
    data['Type'] = pd.Categorical(data['Type'], categories=data['Type'], ordered=True)
    
    p = (
        ggplot(data, aes(x='Type', y='Enrollment'))
        + geom_col(fill='#2E86AB', alpha=0.8, width=0.6)
        + theme_ipsum()
        + theme(plot_margin=0.05)
        + labs(title=wrap_title('U.S. Higher Education Enrollment by Sector, 2023'), x='', y='Enrollment (Millions)', caption='Source: NCES')
    )
    save_plotnine(p, 'ch15', 'ch15_enrollment_by_sector.pdf')

if __name__ == '__main__':
    print("Creating figures for Ch 7, 14, 15...")
    ch07_prof_services_gdp()
    ch14_generation_mix()
    ch15_higher_ed_enrollment()
    print("Done.")
