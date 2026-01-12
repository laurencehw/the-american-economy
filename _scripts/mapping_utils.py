"""
Mapping Utilities for The American Economy book.

Creates consistent state and metro-level choropleth maps.
Uses geopandas + matplotlib for mapping.
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import cm
from pathlib import Path

# Configuration
PROJECT_DIR = Path(r"G:\\My Drive\\book drafts\\the american economy")
FIGURES_DIR = PROJECT_DIR / "_figures"
FIGURES_DIR.mkdir(exist_ok=True)

# Standard figure settings
FIGURE_WIDTH = 6  # inches
DPI = 300

def ensure_dir(chapter):
    """Ensure chapter directory exists within _figures."""
    (FIGURES_DIR / chapter).mkdir(parents=True, exist_ok=True)

def get_us_states():
    """
    Load US states shapefile from Census Bureau.

    Downloads from: https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
    """
    # Use built-in Natural Earth data via geopandas
    try:
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        us = world[world.name == 'United States of America']
        print("Note: Using simplified world boundaries. For detailed US maps,")
        print("download state boundaries from Census Bureau.")
        return us
    except Exception as e:
        print(f"Error loading base map: {e}")
        return None


def load_census_states():
    """
    Load detailed US states from Census Bureau cartographic boundary files.

    Download manually from:
    https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html

    Choose: cb_2022_us_state_20m.zip (20m resolution is good for most purposes)
    """
    # Specific path where the user placed the file
    possible_paths = [
        PROJECT_DIR / "_data" / "shapefiles" / "cb_2022_us_state_20m" / "cb_2022_us_state_20m.shp",
        PROJECT_DIR / "_data" / "shapefiles" / "cb_2022_us_state_20m.shp",
    ]

    for path in possible_paths:
        if path.exists():
            gdf = gpd.read_file(path)
            # Filter for mainland US + AK/HI for cleaner maps (exclude territories if needed)
            # or keep all. Typically for 'The American Economy', keeping 50 states + DC is standard.
            # Filtering out territories often makes the map projection (Albers USA) cleaner.
            # STATEFP codes: 01-56 are states (with gaps), 60+ are territories usually.
            # But let's just return raw first.
            return gdf

    # If not found, print instructions
    print(f"""
    State shapefile not found at expected paths:
    {possible_paths[0]}
    
    Download from Census Bureau:
    1. Go to: https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
    2. Select: States (cb_2022_us_state_20m.zip)
    3. Extract to: {PROJECT_DIR / "_data" / "shapefiles" / "cb_2022_us_state_20m" }
    """)

    return None


def create_state_choropleth(
    data: pd.DataFrame,
    value_column: str,
    state_column: str = 'state',
    title: str = '',
    cmap: str = 'Blues',
    output_file: str = None,
    label: str = None
):
    """
    Create a state-level choropleth map.

    Parameters:
    -----------
    data : DataFrame with state data
    value_column : column name with values to map
    state_column : column name with state identifiers (FIPS, abbreviation, or name)
    title : map title
    cmap : matplotlib colormap name
    output_file : filename to save (in _figures directory)
    label : colorbar label
    """
    # Load state boundaries
    states = load_census_states()
    if states is None:
        print("Cannot create map without state boundaries.")
        return None

    # Merge data with boundaries
    # Adjust merge key based on state_column format
    if data[state_column].dtype == 'int64' or data[state_column].str.isdigit().all():
        # FIPS codes
        merged = states.merge(data, left_on='STATEFP', right_on=state_column)
    elif data[state_column].str.len().max() == 2:
        # State abbreviations
        merged = states.merge(data, left_on='STUSPS', right_on=state_column)
    else:
        # State names
        merged = states.merge(data, left_on='NAME', right_on=state_column)

    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(FIGURE_WIDTH, FIGURE_WIDTH * 0.6))

    # Plot
    merged.plot(
        column=value_column,
        ax=ax,
        legend=True,
        cmap=cmap,
        edgecolor='white',
        linewidth=0.5,
        legend_kwds={'label': label or value_column, 'shrink': 0.6}
    )

    # Styling
    ax.set_axis_off()
    ax.set_title(title, fontsize=10, fontweight='bold')

    # Tight layout
    plt.tight_layout()

    # Save
    if output_file:
        output_path = FIGURES_DIR / output_file
        plt.savefig(output_path, dpi=DPI, bbox_inches='tight', facecolor='white')
        print(f"Saved map to {output_path}")

    return fig, ax


def create_simple_bar_chart(
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str = '',
    xlabel: str = None,
    ylabel: str = None,
    output_file: str = None,
    top_n: int = None,
    horizontal: bool = True
):
    """
    Create a simple bar chart for rankings.

    Parameters:
    -----------
    data : DataFrame
    x_column : category column
    y_column : value column
    title : chart title
    top_n : show only top N values
    horizontal : if True, horizontal bars (better for state/firm names)
    output_file : filename to save
    """
    # Sort and optionally limit
    plot_data = data.sort_values(y_column, ascending=False)
    if top_n:
        plot_data = plot_data.head(top_n)

    # For horizontal bars, reverse order so largest is at top
    if horizontal:
        plot_data = plot_data.iloc[::-1]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, max(4, len(plot_data) * 0.3)))

    if horizontal:
        ax.barh(plot_data[x_column], plot_data[y_column], color='steelblue')
        ax.set_xlabel(ylabel or y_column)
    else:
        ax.bar(plot_data[x_column], plot_data[y_column], color='steelblue')
        ax.set_ylabel(ylabel or y_column)
        plt.xticks(rotation=45, ha='right')

    ax.set_title(title, fontsize=10, fontweight='bold')

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    if output_file:
        output_path = FIGURES_DIR / output_file
        plt.savefig(output_path, dpi=DPI, bbox_inches='tight', facecolor='white')
        print(f"Saved chart to {output_path}")

    return fig, ax


# Example usage
if __name__ == '__main__':
    print("Mapping Utilities for The American Economy")
    print("=" * 50)

    # Check for shapefile
    states = load_census_states()
    if states is not None:
        print(f"Loaded {len(states)} state boundaries")
    else:
        print("State boundaries not available - see instructions above")

    # Example with fake data
    print("\nCreating example chart...")
    example_data = pd.DataFrame({
        'state': ['California', 'Texas', 'New York', 'Florida', 'Illinois'],
        'gdp': [3.6, 2.0, 1.9, 1.2, 0.9]
    })

    create_simple_bar_chart(
        example_data,
        x_column='state',
        y_column='gdp',
        title='Top 5 States by GDP ($ Trillion)',
        ylabel='GDP ($ Trillion)',
        output_file='example_state_gdp.pdf'
    )

    print("\nDone. Check _figures directory for output.")
