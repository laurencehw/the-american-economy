"""
Pull shock-related data from FRED, BEA, and BLS APIs for economic shock analysis.

Data series:
- Oil shock: Brent crude, rig counts, energy state unemployment
- China shock: Manufacturing employment
- Monetary policy: Mortgage rates, housing starts
- Supply chain: PPI, shipping costs
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

# API Keys from environment or settings
FRED_API_KEY = os.environ.get('FRED_API_KEY', '0f4bac877fca6765d790830074a1797a')
BEA_API_KEY = os.environ.get('BEA_API_KEY', '467BAA6A-9E0B-4C6A-A593-C4E1CFCFA11A')
BLS_API_KEY = os.environ.get('BLS_API_KEY', '3eecd95a6a984e5997893cf438dbe7e9')

# Output directory
OUTPUT_DIR = Path(r"G:\My Drive\book drafts\the american economy\_data\shock_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def pull_fred_series(series_id, start_date='1990-01-01', end_date=None):
    """Pull a single FRED series."""
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': series_id,
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': end_date
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching {series_id}: {response.status_code}")
        return None

    data = response.json()
    if 'observations' not in data:
        print(f"No observations for {series_id}")
        return None

    df = pd.DataFrame(data['observations'])
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df[['date', 'value']].rename(columns={'value': series_id})

    return df

def pull_all_fred_data():
    """Pull all FRED series for shock analysis."""

    series_dict = {
        # Oil shock
        'DCOILBRENTEU': 'Brent Crude Oil Price ($/bbl)',
        'DCOILWTICO': 'WTI Crude Oil Price ($/bbl)',
        'RIGS': 'Baker Hughes Rig Count',
        'TXUR': 'Texas Unemployment Rate (%)',
        'NDUR': 'North Dakota Unemployment Rate (%)',
        'OKUR': 'Oklahoma Unemployment Rate (%)',
        'LAUR': 'Louisiana Unemployment Rate (%)',

        # Manufacturing/China shock
        'MANEMP': 'Manufacturing Employment (thousands)',
        'USRECQ': 'US Recession Indicator',

        # Monetary policy
        'MORTGAGE30US': '30-Year Fixed Mortgage Rate (%)',
        'FEDFUNDS': 'Federal Funds Rate (%)',
        'HOUST': 'Housing Starts (thousands)',
        'PERMIT': 'Building Permits (thousands)',

        # Supply chain / inflation
        'PPIACO': 'Producer Price Index (All Commodities)',
        'CPIAUCSL': 'Consumer Price Index (All Urban)',

        # Housing
        'CSUSHPINSA': 'Case-Shiller Home Price Index (National)',
        'MSPUS': 'Median Sales Price of Houses Sold ($)',

        # General
        'UNRATE': 'Unemployment Rate (%)',
        'PAYEMS': 'Total Nonfarm Payrolls (thousands)',
        'GDP': 'Gross Domestic Product (billions $)',
    }

    all_data = {}

    for series_id, description in series_dict.items():
        print(f"Pulling {series_id}: {description}...")
        df = pull_fred_series(series_id)
        if df is not None:
            all_data[series_id] = df
            # Save individual series
            df.to_csv(OUTPUT_DIR / f'fred_{series_id.lower()}.csv', index=False)
            print(f"  -> Saved {len(df)} observations")
        else:
            print(f"  -> Failed")

    # Create metadata file
    metadata = {
        'source': 'FRED (Federal Reserve Economic Data)',
        'pull_date': datetime.now().isoformat(),
        'series': series_dict
    }
    with open(OUTPUT_DIR / 'fred_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)

    return all_data

def pull_bea_state_gdp():
    """Pull state GDP by industry from BEA."""

    url = 'https://apps.bea.gov/api/data/'

    # Pull state GDP data
    params = {
        'UserID': BEA_API_KEY,
        'method': 'GetData',
        'datasetname': 'Regional',
        'TableName': 'SQGDP2',  # State quarterly GDP by industry
        'LineCode': '1',  # All industry total
        'GeoFips': 'STATE',
        'Year': '2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023',
        'ResultFormat': 'JSON'
    }

    print("Pulling BEA state GDP data...")
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    data = response.json()

    if 'BEAAPI' in data and 'Results' in data['BEAAPI']:
        results = data['BEAAPI']['Results']
        if 'Data' in results:
            df = pd.DataFrame(results['Data'])
            df.to_csv(OUTPUT_DIR / 'bea_state_gdp.csv', index=False)
            print(f"  -> Saved {len(df)} observations")
            return df

    print("  -> Failed to parse BEA response")
    return None

def pull_bea_mining_gdp():
    """Pull mining sector GDP by state (for oil shock analysis)."""

    url = 'https://apps.bea.gov/api/data/'

    params = {
        'UserID': BEA_API_KEY,
        'method': 'GetData',
        'datasetname': 'Regional',
        'TableName': 'SQGDP2',
        'LineCode': '6',  # Mining
        'GeoFips': 'STATE',
        'Year': '2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023',
        'ResultFormat': 'JSON'
    }

    print("Pulling BEA mining GDP data...")
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    data = response.json()

    if 'BEAAPI' in data and 'Results' in data['BEAAPI']:
        results = data['BEAAPI']['Results']
        if 'Data' in results:
            df = pd.DataFrame(results['Data'])
            df.to_csv(OUTPUT_DIR / 'bea_mining_gdp_by_state.csv', index=False)
            print(f"  -> Saved {len(df)} observations")
            return df

    print("  -> Failed to parse BEA response")
    return None

def pull_bls_state_employment():
    """Pull state employment data from BLS."""

    # BLS series IDs for state total nonfarm employment
    # Format: SMU[FIPS][00000][00000001]
    state_series = {
        'TX': 'SMU48000000000000001',  # Texas
        'ND': 'SMU38000000000000001',  # North Dakota
        'OK': 'SMU40000000000000001',  # Oklahoma
        'LA': 'SMU22000000000000001',  # Louisiana
        'PA': 'SMU42000000000000001',  # Pennsylvania
        'OH': 'SMU39000000000000001',  # Ohio
        'MI': 'SMU26000000000000001',  # Michigan
        'CA': 'SMU06000000000000001',  # California
    }

    # Also get manufacturing employment
    mfg_series = {
        'TX_MFG': 'SMU48000003000000001',
        'OH_MFG': 'SMU39000003000000001',
        'MI_MFG': 'SMU26000003000000001',
        'PA_MFG': 'SMU42000003000000001',
    }

    all_series = {**state_series, **mfg_series}
    series_ids = list(all_series.values())

    url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'

    headers = {'Content-type': 'application/json'}
    payload = {
        'seriesid': series_ids,
        'startyear': '2000',
        'endyear': '2024',
        'registrationkey': BLS_API_KEY
    }

    print("Pulling BLS state employment data...")
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    data = response.json()

    if data['status'] == 'REQUEST_SUCCEEDED':
        results = []
        for series in data['Results']['series']:
            series_id = series['seriesID']
            # Find the label
            label = [k for k, v in all_series.items() if v == series_id]
            label = label[0] if label else series_id

            for obs in series['data']:
                results.append({
                    'series': label,
                    'series_id': series_id,
                    'year': obs['year'],
                    'period': obs['period'],
                    'value': obs['value']
                })

        df = pd.DataFrame(results)
        df.to_csv(OUTPUT_DIR / 'bls_state_employment.csv', index=False)
        print(f"  -> Saved {len(df)} observations")
        return df
    else:
        print(f"  -> BLS API error: {data.get('message', 'Unknown error')}")
        return None

def create_combined_oil_shock_dataset():
    """Combine FRED series into oil shock analysis dataset."""

    print("\nCreating combined oil shock dataset...")

    # Load individual series
    oil_price = pd.read_csv(OUTPUT_DIR / 'fred_dcoilbrenteu.csv')
    if (OUTPUT_DIR / 'fred_rigs.csv').exists():
        rig_count = pd.read_csv(OUTPUT_DIR / 'fred_rigs.csv')
    else:
        rig_count = None

    tx_unemp = pd.read_csv(OUTPUT_DIR / 'fred_txur.csv')
    nd_unemp = pd.read_csv(OUTPUT_DIR / 'fred_ndur.csv')

    # Merge on date
    oil_price['date'] = pd.to_datetime(oil_price['date'])
    combined = oil_price.copy()

    for df, col in [(tx_unemp, 'TXUR'), (nd_unemp, 'NDUR')]:
        df['date'] = pd.to_datetime(df['date'])
        combined = combined.merge(df[['date', col]], on='date', how='outer')

    if rig_count is not None:
        rig_count['date'] = pd.to_datetime(rig_count['date'])
        combined = combined.merge(rig_count[['date', 'RIGS']], on='date', how='outer')

    combined = combined.sort_values('date')
    combined.to_csv(OUTPUT_DIR / 'oil_shock_combined.csv', index=False)
    print(f"  -> Saved combined dataset with {len(combined)} observations")

    return combined

def main():
    """Pull all data for shock analysis."""

    print("=" * 60)
    print("SHOCK ANALYSIS DATA PULL")
    print("=" * 60)
    print()

    # 1. FRED data
    print("PHASE 1: FRED DATA")
    print("-" * 40)
    fred_data = pull_all_fred_data()
    print()

    # 2. BEA data
    print("PHASE 2: BEA DATA")
    print("-" * 40)
    bea_state = pull_bea_state_gdp()
    bea_mining = pull_bea_mining_gdp()
    print()

    # 3. BLS data
    print("PHASE 3: BLS DATA")
    print("-" * 40)
    bls_employment = pull_bls_state_employment()
    print()

    # 4. Create combined datasets
    print("PHASE 4: COMBINED DATASETS")
    print("-" * 40)
    try:
        oil_combined = create_combined_oil_shock_dataset()
    except Exception as e:
        print(f"Error creating combined dataset: {e}")
    print()

    print("=" * 60)
    print("DATA PULL COMPLETE")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == '__main__':
    main()
