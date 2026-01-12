"""
BEA Data Pull Script
Pulls GDP by industry and related data for The American Economy book.

Data sources:
- BEA Industry Accounts: https://apps.bea.gov/iTable/
- FRED API for macroeconomic data
"""

import pandas as pd
import requests
from fredapi import Fred
import os
from pathlib import Path

# Configuration
PROJECT_DIR = Path(r"G:\My Drive\book drafts\the american economy")
DATA_DIR = PROJECT_DIR / "_data"
DATA_DIR.mkdir(exist_ok=True)

# Initialize FRED (uses FRED_API_KEY environment variable)
try:
    fred = Fred()
except:
    print("Note: FRED API key not configured. Set FRED_API_KEY environment variable.")
    fred = None


def pull_gdp_by_industry():
    """
    Pull GDP by industry from BEA.

    Source: BEA Table 1.5.5 - Gross Domestic Product by Major Type of Product
    and NIPA Table 6.1 - National Income by Industry

    For detailed industry breakdown, use BEA Industry Accounts:
    https://apps.bea.gov/iTable/?ReqID=51&step=1
    """
    # BEA provides data via their API or downloadable tables
    # For now, we'll pull key series from FRED which mirrors BEA data

    if fred is None:
        print("FRED not configured, skipping FRED data pull")
        return None

    # Key GDP component series
    series = {
        'GDP': 'GDP',  # Nominal GDP
        'GDPC1': 'GDPC1',  # Real GDP
    }

    data = {}
    for name, series_id in series.items():
        try:
            data[name] = fred.get_series(series_id)
        except Exception as e:
            print(f"Error pulling {name}: {e}")

    if data:
        df = pd.DataFrame(data)
        df.to_csv(DATA_DIR / 'gdp_components.csv')
        print(f"Saved GDP data to {DATA_DIR / 'gdp_components.csv'}")
        return df
    return None


def pull_employment_by_industry():
    """
    Pull employment by industry from FRED/BLS.

    Key series:
    - PAYEMS: Total nonfarm payrolls
    - Various industry-specific payroll series
    """
    if fred is None:
        print("FRED not configured, skipping employment data pull")
        return None

    # Major industry employment series
    series = {
        'Total_Nonfarm': 'PAYEMS',
        'Manufacturing': 'MANEMP',
        'Construction': 'USCONS',
        'Retail_Trade': 'USTRADE',
        'Finance': 'USFIRE',
        'Government': 'USGOVT',
        'Healthcare': 'USPRIV',  # Note: need specific healthcare series
        'Professional_Services': 'USPBS',
    }

    data = {}
    for name, series_id in series.items():
        try:
            data[name] = fred.get_series(series_id)
        except Exception as e:
            print(f"Error pulling {name}: {e}")

    if data:
        df = pd.DataFrame(data)
        df.to_csv(DATA_DIR / 'employment_by_industry.csv')
        print(f"Saved employment data to {DATA_DIR / 'employment_by_industry.csv'}")
        return df
    return None


def download_bea_industry_tables():
    """
    Instructions for downloading BEA Industry Accounts manually.

    The BEA API requires registration for detailed industry data.
    For initial setup, download manually from:
    https://apps.bea.gov/iTable/?ReqID=51&step=1

    Key tables:
    - Value Added by Industry (Table 1)
    - GDP by Industry (Table 5)
    - Employment by Industry (Table 6)
    """
    instructions = """
    BEA Industry Accounts - Manual Download Instructions
    ====================================================

    1. Go to: https://apps.bea.gov/iTable/?ReqID=51&step=1

    2. Select tables:
       - Section 1: Value Added by Industry
       - Section 5: GDP by Industry
       - Section 6: Employment by Industry

    3. Choose years: 2017-2023

    4. Download as CSV

    5. Save to: {data_dir}

    For API access, register at: https://apps.bea.gov/api/signup/
    """.format(data_dir=DATA_DIR)

    print(instructions)

    # Save instructions to file
    with open(DATA_DIR / 'BEA_download_instructions.txt', 'w') as f:
        f.write(instructions)


def pull_healthcare_data():
    """
    Pull healthcare-specific data from CMS and FRED.

    Key sources:
    - CMS National Health Expenditure Accounts
    - FRED healthcare employment series
    """
    if fred is None:
        print("FRED not configured, skipping healthcare data pull")
        return None

    # Healthcare employment series
    series = {
        'Healthcare_Employment': 'USHLTH',  # Health care and social assistance
    }

    data = {}
    for name, series_id in series.items():
        try:
            data[name] = fred.get_series(series_id)
        except Exception as e:
            print(f"Error pulling {name}: {e}")

    if data:
        df = pd.DataFrame(data)
        df.to_csv(DATA_DIR / 'healthcare_employment.csv')
        print(f"Saved healthcare data to {DATA_DIR / 'healthcare_employment.csv'}")
        return df

    # CMS data must be downloaded manually
    cms_instructions = """
    CMS National Health Expenditure Data
    =====================================

    Download from: https://www.cms.gov/research-statistics-data-and-systems/statistics-trends-and-reports/nationalhealthexpenddata

    Key files:
    - NHE Summary (national totals)
    - NHE by Type of Service
    - NHE by Source of Funds
    - State Health Expenditure Accounts

    Save to: {data_dir}
    """.format(data_dir=DATA_DIR)

    with open(DATA_DIR / 'CMS_download_instructions.txt', 'w') as f:
        f.write(cms_instructions)

    return None


if __name__ == '__main__':
    print("BEA/FRED Data Pull Script")
    print("=" * 50)

    # Create data directory
    DATA_DIR.mkdir(exist_ok=True)

    # Pull available data
    print("\n1. GDP by Industry")
    pull_gdp_by_industry()

    print("\n2. Employment by Industry")
    pull_employment_by_industry()

    print("\n3. BEA Industry Tables (manual download)")
    download_bea_industry_tables()

    print("\n4. Healthcare Data")
    pull_healthcare_data()

    print("\n" + "=" * 50)
    print("Data pull complete. Check", DATA_DIR, "for outputs.")
