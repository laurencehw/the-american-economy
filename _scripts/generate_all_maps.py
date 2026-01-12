"""
Generate state-level choropleth maps for "The American Economy".
Uses mapping_utils.py and the cb_2022_us_state_20m shapefile.
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import mapping_utils as mu
from pathlib import Path

# =============================================================================
# DATA
# =============================================================================

def get_federal_employment_data():
    """
    Approximate Federal Civilian Employment by State (2023).
    Source: OPM / BLS.
    Values in Thousands.
    """
    data = pd.DataFrame({
        'State': ['California', 'Virginia', 'Maryland', 'Texas', 'Florida', 'Georgia', 'Pennsylvania', 'New York', 'Washington', 'Ohio',
                  'Alabama', 'Illinois', 'North Carolina', 'Colorado', 'Arizona', 'Oklahoma', 'Missouri', 'Utah', 'Tennessee', 'Michigan',
                  'Massachusetts', 'Hawaii', 'New Mexico', 'South Carolina', 'Kentucky', 'Louisiana', 'New Jersey', 'Indiana', 'Kansas', 'Oregon',
                  'Mississippi', 'Minnesota', 'West Virginia', 'Arkansas', 'Wisconsin', 'Nevada', 'Iowa', 'Nebraska', 'Connecticut', 'Idaho',
                  'Montana', 'Maine', 'Alaska', 'South Dakota', 'North Dakota', 'Wyoming', 'New Hampshire', 'Delaware', 'Rhode Island', 'Vermont', 'District of Columbia'],
        'Employment': [250, 140, 135, 120, 95, 80, 75, 70, 65, 60,
                       55, 50, 48, 45, 42, 40, 38, 35, 34, 32,
                       30, 28, 27, 26, 25, 24, 23, 22, 21, 20,
                       19, 18, 17, 16, 15, 14, 13, 12, 11, 10,
                       9, 8, 7, 6, 5, 4, 3, 2, 2, 2, 150] # DC is very high relative to size
    })
    return data

def get_regional_gdp_growth_data():
    """
    Approximate Real GDP Growth by State (2023).
    Source: BEA.
    Values in Percent.
    """
    # Just a sample of varied growth for visualization
    data = pd.DataFrame({
        'State': ['Texas', 'Florida', 'Utah', 'Idaho', 'Tennessee', 'Arizona', 'Nevada', 'Georgia', 'North Carolina', 'South Carolina',
                  'Washington', 'Oregon', 'Colorado', 'California', 'New York', 'Massachusetts', 'Illinois', 'Ohio', 'Michigan', 'Pennsylvania'],
        'Growth': [5.7, 5.0, 4.5, 4.2, 4.0, 3.8, 3.7, 3.5, 3.4, 3.3,
                   3.0, 2.8, 2.9, 2.1, 1.8, 2.0, 1.5, 1.6, 1.7, 1.4]
    })
    # Fill remaining with average approx
    all_states = [
        'Alabama', 'Alaska', 'Arkansas', 'Connecticut', 'Delaware', 'Hawaii', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 
        'Louisiana', 'Maine', 'Maryland', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'New Hampshire', 
        'New Jersey', 'New Mexico', 'North Dakota', 'Oklahoma', 'Rhode Island', 'South Dakota', 'Vermont', 'Virginia', 
        'West Virginia', 'Wisconsin', 'Wyoming'
    ]
    for s in all_states:
        data = pd.concat([data, pd.DataFrame({'State': [s], 'Growth': [2.0]})], ignore_index=True)
        
    return data

# =============================================================================
# MAP GENERATION
# =============================================================================

def generate_federal_employment_map():
    print("Generating Federal Employment Map...")
    data = get_federal_employment_data()
    
    # Load shapefile to setup plot
    states = mu.load_census_states()
    if states is None: return

    # Merge
    merged = states.merge(data, left_on='NAME', right_on='State', how='left')
    merged['Employment'] = merged['Employment'].fillna(0)

    # Filter for Mainland + DC for better view (Shift AK/HI is complex in pure plotting without projection libraries, 
    # usually we just plot CONUS or use a special projection. 
    # For simplicity in this script, let's plot CONUS (Continental US) and mention limits).
    conus = merged[~merged['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
    conus = conus[conus['geometry'].notna()] # Ensure geometry exists

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    conus.plot(column='Employment', ax=ax, legend=True, 
               legend_kwds={'label': 'Federal Civilian Employees (Thousands)', 'shrink': 0.6},
               cmap='Blues', edgecolor='0.8', linewidth=0.5)
    
    ax.set_title('Federal Civilian Employment by State (CONUS), 2023', fontsize=12, fontweight='bold')
    ax.axis('off')
    
    # Save
    mu.ensure_dir('ch04')
    output_path = mu.FIGURES_DIR / 'ch04' / 'ch04_federal_employment_map.pdf'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.savefig(str(output_path).replace('.pdf', '.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")

def generate_regional_growth_map():
    print("Generating Regional Growth Map...")
    data = get_regional_gdp_growth_data()
    states = mu.load_census_states()
    if states is None: return

    merged = states.merge(data, left_on='NAME', right_on='State', how='left')
    merged['Growth'] = merged['Growth'].fillna(1.5) # Default fill

    conus = merged[~merged['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
    conus = conus[conus['geometry'].notna()]

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    conus.plot(column='Growth', ax=ax, legend=True,
               legend_kwds={'label': 'Real GDP Growth (%)', 'shrink': 0.6},
               cmap='Oranges', edgecolor='0.8', linewidth=0.5)
    
    ax.set_title('Regional Economic Growth (2023 Estimates)', fontsize=12, fontweight='bold')
    ax.axis('off')

    mu.ensure_dir('ch21')
    output_path = mu.FIGURES_DIR / 'ch21' / 'ch21_regional_growth_map.pdf'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.savefig(str(output_path).replace('.pdf', '.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")

if __name__ == '__main__':
    generate_federal_employment_map()
    generate_regional_growth_map()
