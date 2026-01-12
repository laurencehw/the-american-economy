"""
Generate additional thematic maps for "The American Economy":
1. Tech Hubs (Ch 11)
2. Logistics Corridors (Ch 12)
3. Regional Industry Dominance (Ch 3)
4. Metro Job Density (Ch 3)
5. Energy Basins (Ch 14)

Uses mapping_utils.py and the cb_2022_us_state_20m shapefile.
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import mapping_utils as mu
from shapely.geometry import Point, LineString

# =============================================================================
# 1. TECH HUBS (Ch 11)
# =============================================================================

def ch11_tech_hubs_map():
    print("Generating Tech Hubs Map...")
    
    # Major Tech Hubs (Approximate Lat/Lon)
    hubs = pd.DataFrame([
        {'City': 'San Francisco Bay Area', 'Lat': 37.6, 'Lon': -122.2, 'Size': 100}, # Silicon Valley
        {'City': 'Seattle', 'Lat': 47.6, 'Lon': -122.3, 'Size': 60},
        {'City': 'New York City', 'Lat': 40.7, 'Lon': -74.0, 'Size': 55},
        {'City': 'Boston', 'Lat': 42.3, 'Lon': -71.0, 'Size': 50},
        {'City': 'Austin', 'Lat': 30.2, 'Lon': -97.7, 'Size': 40},
        {'City': 'Los Angeles', 'Lat': 34.0, 'Lon': -118.2, 'Size': 45},
        {'City': 'Washington DC', 'Lat': 38.9, 'Lon': -77.0, 'Size': 42},
        {'City': 'Denver/Boulder', 'Lat': 39.7, 'Lon': -105.0, 'Size': 30},
        {'City': 'Raleigh-Durham', 'Lat': 35.8, 'Lon': -78.8, 'Size': 25},
        {'City': 'Salt Lake City', 'Lat': 40.7, 'Lon': -111.9, 'Size': 20},
        {'City': 'Atlanta', 'Lat': 33.7, 'Lon': -84.4, 'Size': 28},
    ])
    
    gdf_hubs = gpd.GeoDataFrame(hubs, geometry=gpd.points_from_xy(hubs.Lon, hubs.Lat))
    
    states = mu.load_census_states()
    if states is None: return
    
    # Filter for CONUS
    conus = states[~states['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
    conus = conus[conus['geometry'].notna()]

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    conus.plot(ax=ax, color='#f0f0f0', edgecolor='white', linewidth=0.5)
    
    # Plot Hubs
    gdf_hubs.plot(ax=ax, markersize=gdf_hubs['Size']*5, color='#4285F4', alpha=0.7, edgecolor='white')
    
    # Labels
    for idx, row in gdf_hubs.iterrows():
        ax.text(row.geometry.x, row.geometry.y + 0.5, row['City'], fontsize=7, ha='center', fontweight='bold', color='#333')

    ax.set_title('Major U.S. Technology Hubs', fontsize=12, fontweight='bold')
    ax.axis('off')
    
    mu.ensure_dir('ch11')
    output_path = mu.FIGURES_DIR / 'ch11' / 'ch11_tech_hubs_map.pdf'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.savefig(str(output_path).replace('.pdf', '.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")

# =============================================================================
# 2. LOGISTICS CORRIDORS (Ch 12)
# =============================================================================

def ch12_logistics_map():
    print("Generating Logistics Map...")
    
    states = mu.load_census_states()
    if states is None: return
    conus = states[~states['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]

    # Major Ports
    ports = pd.DataFrame([
        {'Name': 'LA / Long Beach', 'Lat': 33.7, 'Lon': -118.2},
        {'Name': 'NY / NJ', 'Lat': 40.6, 'Lon': -74.0},
        {'Name': 'Savannah', 'Lat': 32.0, 'Lon': -81.0},
        {'Name': 'Houston', 'Lat': 29.7, 'Lon': -95.3},
        {'Name': 'Seattle / Tacoma', 'Lat': 47.6, 'Lon': -122.3},
        {'Name': 'Norfolk', 'Lat': 36.8, 'Lon': -76.3}
    ])
    gdf_ports = gpd.GeoDataFrame(ports, geometry=gpd.points_from_xy(ports.Lon, ports.Lat))

    # Schematic Routes (simplified LineStrings)
    routes = [
        {'Name': 'I-5 Corridor', 'Path': LineString([(-122.3, 48.0), (-122.6, 45.5), (-121.5, 38.5), (-118.2, 34.0), (-117.1, 32.7)])},
        {'Name': 'I-95 Corridor', 'Path': LineString([(-70.2, 43.6), (-71.0, 42.3), (-74.0, 40.7), (-77.0, 38.9), (-81.0, 32.0), (-80.2, 25.7)])},
        {'Name': 'I-80 Cross-Country', 'Path': LineString([(-122.4, 37.7), (-119.8, 39.5), (-111.8, 40.7), (-104.9, 41.1), (-96.0, 41.2), (-87.6, 41.8), (-81.6, 41.4), (-74.0, 40.8)])},
        {'Name': 'Mississippi River', 'Path': LineString([(-93.2, 44.9), (-90.2, 38.6), (-90.0, 35.1), (-91.1, 30.4), (-90.0, 29.9)])}
    ]
    gdf_routes = gpd.GeoDataFrame(routes, geometry='Path')

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    conus.plot(ax=ax, color='#e0e0e0', edgecolor='white', linewidth=0.5)
    
    # Plot Routes
    gdf_routes.plot(ax=ax, color='#E15759', linewidth=2, alpha=0.6, linestyle='--')
    
    # Plot Ports
    gdf_ports.plot(ax=ax, color='#2E86AB', markersize=80, marker='s', edgecolor='white')

    # Labels
    for idx, row in gdf_ports.iterrows():
        ax.text(row.geometry.x + 1, row.geometry.y, row['Name'], fontsize=7, fontweight='bold', color='#2E86AB')

    ax.set_title('Major Logistics Hubs and Schematic Freight Corridors', fontsize=12, fontweight='bold')
    ax.axis('off')
    
    mu.ensure_dir('ch12')
    output_path = mu.FIGURES_DIR / 'ch12' / 'ch12_logistics_map.pdf'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.savefig(str(output_path).replace('.pdf', '.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")

# =============================================================================
# 3. REGIONAL DOMINANCE (Ch 3)
# =============================================================================

def ch03_regional_dominance_map():
    print("Generating Regional Dominance Map...")
    
    # Dominant sector by state (Illustrative/Generalized)
    # Energy: TX, ND, OK, WY, WV, LA, AK
    # Finance: NY, DE, CT, NC, SD
    # Tech/Info: CA, WA, MA, VA, CO
    # Manufacturing: MI, OH, IN, WI, KY, TN, AL, SC
    # Agriculture: IA, NE, KS, ID, MT, SD
    # Government: DC, MD, NM, HI
    # Services/Tourism: FL, NV, AZ
    
    data = []
    classification = {
        'Energy': ['Texas', 'North Dakota', 'Oklahoma', 'Wyoming', 'West Virginia', 'Louisiana', 'Alaska'],
        'Finance': ['New York', 'Delaware', 'Connecticut', 'North Carolina', 'South Dakota', 'Rhode Island'],
        'Tech & Information': ['California', 'Washington', 'Massachusetts', 'Virginia', 'Colorado', 'Utah'],
        'Manufacturing': ['Michigan', 'Ohio', 'Indiana', 'Wisconsin', 'Kentucky', 'Tennessee', 'Alabama', 'South Carolina', 'Arkansas', 'Mississippi'],
        'Agriculture': ['Iowa', 'Nebraska', 'Kansas', 'Idaho', 'Montana'],
        'Government': ['District of Columbia', 'Maryland', 'New Mexico', 'Hawaii'],
        'Services & Tourism': ['Florida', 'Nevada', 'Arizona', 'Georgia', 'Oregon', 'Maine', 'Vermont', 'New Hampshire']
    }
    
    # Reverse map
    state_sector = {}
    for sector, states_list in classification.items():
        for state in states_list:
            state_sector[state] = sector
            
    # Default others to 'Diversified/Services'
    all_states = [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 
        'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 
        'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 
        'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 
        'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 
        'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
    ]
    
    for s in all_states:
        if s not in state_sector:
            state_sector[s] = 'Diversified/Services'
            
    df = pd.DataFrame(list(state_sector.items()), columns=['State', 'Sector'])
    
    states = mu.load_census_states()
    if states is None: return
    merged = states.merge(df, left_on='NAME', right_on='State', how='left')
    conus = merged[~merged['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
    conus = conus[conus['geometry'].notna()]

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    conus.plot(column='Sector', ax=ax, legend=True, 
               cmap='Set3', edgecolor='gray', linewidth=0.5,
               legend_kwds={'loc': 'lower left', 'title': 'Dominant Sector'})
    
    ax.set_title('Primary Economic Drivers by State (Generalized)', fontsize=12, fontweight='bold')
    ax.axis('off')
    
    mu.ensure_dir('ch03')
    output_path = mu.FIGURES_DIR / 'ch03' / 'ch03_regional_dominance_map.pdf'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.savefig(str(output_path).replace('.pdf', '.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")

# =============================================================================
# 4. METRO JOB DENSITY (Ch 3)
# =============================================================================

def ch03_metro_density_map():
    print("Generating Metro Density Map...")
    
    # Top Metros (Approx)
    metros = pd.DataFrame([
        {'Name': 'NYC Metro', 'Lat': 40.7, 'Lon': -74.0, 'Jobs': 9.5},
        {'Name': 'LA Metro', 'Lat': 34.0, 'Lon': -118.2, 'Jobs': 6.0},
        {'Name': 'Chicago', 'Lat': 41.8, 'Lon': -87.6, 'Jobs': 4.5},
        {'Name': 'Dallas', 'Lat': 32.7, 'Lon': -96.8, 'Jobs': 4.0},
        {'Name': 'Houston', 'Lat': 29.7, 'Lon': -95.3, 'Jobs': 3.2},
        {'Name': 'DC Metro', 'Lat': 38.9, 'Lon': -77.0, 'Jobs': 3.3},
        {'Name': 'Philadelphia', 'Lat': 39.9, 'Lon': -75.1, 'Jobs': 2.9},
        {'Name': 'Miami', 'Lat': 25.7, 'Lon': -80.1, 'Jobs': 2.7},
        {'Name': 'Atlanta', 'Lat': 33.7, 'Lon': -84.4, 'Jobs': 2.9},
        {'Name': 'Boston', 'Lat': 42.3, 'Lon': -71.0, 'Jobs': 2.7},
        {'Name': 'SF/Bay Area', 'Lat': 37.7, 'Lon': -122.4, 'Jobs': 2.4},
        {'Name': 'Phoenix', 'Lat': 33.4, 'Lon': -112.0, 'Jobs': 2.2},
        {'Name': 'Seattle', 'Lat': 47.6, 'Lon': -122.3, 'Jobs': 2.0},
        {'Name': 'Detroit', 'Lat': 42.3, 'Lon': -83.0, 'Jobs': 1.9},
        {'Name': 'Minneapolis', 'Lat': 44.9, 'Lon': -93.2, 'Jobs': 1.9},
        {'Name': 'San Diego', 'Lat': 32.7, 'Lon': -117.1, 'Jobs': 1.5},
        {'Name': 'Tampa', 'Lat': 27.9, 'Lon': -82.4, 'Jobs': 1.4},
        {'Name': 'Denver', 'Lat': 39.7, 'Lon': -104.9, 'Jobs': 1.5},
        {'Name': 'St. Louis', 'Lat': 38.6, 'Lon': -90.1, 'Jobs': 1.3},
        {'Name': 'Charlotte', 'Lat': 35.2, 'Lon': -80.8, 'Jobs': 1.3}
    ])
    gdf_metros = gpd.GeoDataFrame(metros, geometry=gpd.points_from_xy(metros.Lon, metros.Lat))
    
    states = mu.load_census_states()
    if states is None: return
    conus = states[~states['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
    conus = conus[conus['geometry'].notna()]

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    conus.plot(ax=ax, color='#f5f5f5', edgecolor='#bbb', linewidth=0.5)
    
    # Plot Bubbles
    gdf_metros.plot(ax=ax, markersize=gdf_metros['Jobs']*100, color='#2E86AB', alpha=0.5, edgecolor='#2E86AB')
    
    ax.set_title('Employment Concentration in Major Metros (Millions of Jobs)', fontsize=12, fontweight='bold')
    ax.axis('off')
    
    mu.ensure_dir('ch03')
    output_path = mu.FIGURES_DIR / 'ch03' / 'ch03_metro_job_density.pdf'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.savefig(str(output_path).replace('.pdf', '.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")

# =============================================================================
# 5. ENERGY BASINS (Ch 14)
# =============================================================================

def ch14_energy_basins_map():
    print("Generating Energy Basins Map...")
    
    # Major Basins (Centroids)
    basins = pd.DataFrame([
        {'Name': 'Permian Basin', 'Lat': 31.5, 'Lon': -102.5},
        {'Name': 'Bakken Shale', 'Lat': 48.0, 'Lon': -103.0},
        {'Name': 'Marcellus Shale', 'Lat': 41.0, 'Lon': -78.0},
        {'Name': 'Eagle Ford', 'Lat': 28.5, 'Lon': -99.0},
        {'Name': 'Gulf Coast Offshore', 'Lat': 28.0, 'Lon': -91.0},
        {'Name': 'Appalachian', 'Lat': 38.0, 'Lon': -82.0},
    ])
    gdf_basins = gpd.GeoDataFrame(basins, geometry=gpd.points_from_xy(basins.Lon, basins.Lat))
    
    states = mu.load_census_states()
    if states is None: return
    conus = states[~states['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
    conus = conus[conus['geometry'].notna()]

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    conus.plot(ax=ax, color='#fff', edgecolor='#ccc', linewidth=0.5)
    
    # Highlight energy states
    energy_states = conus[conus['NAME'].isin(['Texas', 'North Dakota', 'Pennsylvania', 'West Virginia', 'Louisiana', 'Oklahoma'])]
    energy_states.plot(ax=ax, color='#FFF3E0', edgecolor='#ccc', linewidth=0.5)

    # Plot Basins
    gdf_basins.plot(ax=ax, markersize=300, color='#F18F01', alpha=0.6, marker='o')
    
    for idx, row in gdf_basins.iterrows():
        ax.text(row.geometry.x, row.geometry.y, row['Name'], fontsize=8, ha='center', va='center', fontweight='bold')

    ax.set_title('Major U.S. Oil and Gas Basins', fontsize=12, fontweight='bold')
    ax.axis('off')
    
    mu.ensure_dir('ch14')
    output_path = mu.FIGURES_DIR / 'ch14' / 'ch14_energy_basins_map.pdf'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.savefig(str(output_path).replace('.pdf', '.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")

if __name__ == '__main__':
    ch11_tech_hubs_map()
    ch12_logistics_map()
    ch03_regional_dominance_map()
    ch03_metro_density_map()
    ch14_energy_basins_map()
    print("Done.")
