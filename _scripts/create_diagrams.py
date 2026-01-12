"""
Create specialized flow diagrams for Chapters 2, 16, and 20.
Uses matplotlib for structured boxes and arrows.
Saves 300 DPI PNGs for GitBook.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
import textwrap

# Configuration
PROJECT_DIR = Path(r"G:\\My Drive\\book drafts\\the american economy")
FIGURES_DIR = PROJECT_DIR / "_figures"
FIGURE_WIDTH = 6
DPI = 300

def ensure_dir(chapter):
    (FIGURES_DIR / chapter).mkdir(parents=True, exist_ok=True)

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
# CHAPTER 2: CIRCULAR FLOW
# =============================================================================

def ch02_circular_flow():
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Draw large circle for flow
    circle = patches.Circle((0.5, 0.5), 0.35, color='lightgray', fill=False, linestyle='--', alpha=0.5)
    ax.add_patch(circle)
    
    # Define main actors
    nodes = {
        'Households': (0.5, 0.85),
        'Product Markets': (0.85, 0.5),
        'Firms': (0.5, 0.15),
        'Resource Markets': (0.15, 0.5)
    }
    
    for name, (x, y) in nodes.items():
        rect = patches.FancyBboxPatch((x-0.1, y-0.05), 0.2, 0.1, boxstyle="round,pad=0.02", fc='white', ec='#2E86AB', lw=2)
        ax.add_patch(rect)
        ax.text(x, y, name, ha='center', va='center', fontweight='bold', fontsize=9)

    # Arrows for Goods/Services (Outer clockwise)
    # Households to Resource Markets (Labor)
    ax.annotate("Labor/Capital", xy=(0.15, 0.55), xytext=(0.4, 0.85), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color='#2E86AB'))
    # Resource Markets to Firms
    ax.annotate("Inputs", xy=(0.4, 0.15), xytext=(0.15, 0.45), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color='#2E86AB'))
    # Firms to Product Markets
    ax.annotate("Goods/Services", xy=(0.85, 0.45), xytext=(0.6, 0.15), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color='#2E86AB'))
    # Product Markets to Households
    ax.annotate("Consumption", xy=(0.6, 0.85), xytext=(0.85, 0.55), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color='#2E86AB'))

    # Inner arrows for Money (Counter-clockwise) - Not shown for simplicity in this version
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title(wrap_title('The Circular Flow of the American Economy'), fontsize=12, fontweight='bold', pad=10)
    save_matplotlib(fig, 'ch02', 'ch02_circular_flow.pdf')

# =============================================================================
# CHAPTER 16: HIERARCHY OF MONEY
# =============================================================================

def ch16_hierarchy_money():
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Pyramid layers
    layers = [
        ('Gold / Reserves', '#FFD700', 0.2),
        ('Federal Reserve Notes', '#C0C0C0', 0.4),
        ('Bank Deposits', '#ADD8E6', 0.6),
        ('Shadow Money / Repo', '#E6E6FA', 0.8)
    ]
    
    for i, (name, color, width) in enumerate(layers):
        y = 0.8 - i * 0.2
        # Draw trapezoid
        poly = patches.Polygon([
            (0.5 - width/2, y), 
            (0.5 + width/2, y), 
            (0.5 + (width+0.2)/2, y-0.18), 
            (0.5 - (width+0.2)/2, y-0.18)
        ], color=color, alpha=0.7, ec='black')
        ax.add_patch(poly)
        ax.text(0.5, y-0.09, name, ha='center', va='center', fontweight='bold', fontsize=10)

    ax.annotate("Most Liquid / Settlement", xy=(0.1, 0.8), xytext=(0.1, 0.9), arrowprops=dict(arrowstyle="->"))
    ax.annotate("Least Liquid / Credit", xy=(0.1, 0.2), xytext=(0.1, 0.1), arrowprops=dict(arrowstyle="->"))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title(wrap_title('The Hierarchy of Money'), fontsize=12, fontweight='bold', pad=10)
    save_matplotlib(fig, 'ch16', 'ch16_hierarchy_money.pdf')

# =============================================================================
# CHAPTER 20: IPHONE SUPPLY CHAIN
# =============================================================================

def ch20_iphone_chain():
    fig, ax = plt.subplots(figsize=(6, 4))
    
    steps = [
        ('Design', 'California', 0.1),
        ('Processors', 'Taiwan (TSMC)', 0.3),
        ('Display/Memory', 'S. Korea / Japan', 0.5),
        ('Assembly', 'China / India', 0.7),
        ('Distribution', 'Global Markets', 0.9)
    ]
    
    for i, (step, loc, x) in enumerate(steps):
        rect = patches.Rectangle((x-0.08, 0.4), 0.16, 0.2, fc='#F0F0F0', ec='#4E79A7', lw=1.5)
        ax.add_patch(rect)
        ax.text(x, 0.55, step, ha='center', va='center', fontweight='bold', fontsize=8)
        ax.text(x, 0.45, loc, ha='center', va='center', fontsize=7, fontstyle='italic')
        
        if i < len(steps) - 1:
            ax.annotate("", xy=(steps[i+1][2]-0.08, 0.5), xytext=(x+0.08, 0.5), arrowprops=dict(arrowstyle="->", color='gray'))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title(wrap_title('Simplified iPhone Global Supply Chain'), fontsize=12, fontweight='bold', pad=10)
    save_matplotlib(fig, 'ch20', 'ch20_iphone_supply_chain.pdf')

if __name__ == '__main__':
    print("Generating Specialized Diagrams...")
    ch02_circular_flow()
    ch16_hierarchy_money()
    ch20_iphone_chain()
    print("Done.")
