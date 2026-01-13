"""
Pull regional economic data from BEA and BLS APIs for Part V chapters.

Data pulled:
- State GDP by industry (BEA)
- Metro GDP (BEA)
- State employment (BLS)
- State unemployment rates (BLS)
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

# API Keys from environment
FRED_API_KEY = os.environ.get('FRED_API_KEY', '0f4bac877fca6765d790830074a1797a')
BEA_API_KEY = os.environ.get('BEA_API_KEY', '467BAA6A-9E0B-4C6A-A593-C4E1CFCFA11A')
BLS_API_KEY = os.environ.get('BLS_API_KEY', '3eecd95a6a984e5997893cf438dbe7e9')

# Output directory
OUTPUT_DIR = Path(r"G:\My Drive\book drafts\the american economy\_data\regional")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Regional groupings for analysis
REGIONS = {
    'northeast': ['CT', 'ME', 'MA', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA', 'DE', 'MD', 'DC'],
    'sunbelt': ['TX', 'FL', 'AZ', 'GA', 'NC', 'TN', 'SC', 'NV', 'CO'],
    'midwest': ['IL', 'IN', 'MI', 'OH', 'WI', 'MN', 'IA', 'MO', 'KS', 'NE', 'ND', 'SD'],
    'west': ['CA', 'WA', 'OR', 'UT', 'CO', 'AZ', 'NV', 'ID', 'MT', 'WY', 'NM', 'AK', 'HI']
}

# Key metros by region
METROS = {
    'northeast': ['New York', 'Boston', 'Philadelphia', 'Washington'],
    'sunbelt': ['Houston', 'Dallas', 'Atlanta', 'Miami', 'Phoenix', 'Austin', 'Charlotte'],
    'midwest': ['Chicago', 'Detroit', 'Minneapolis', 'Columbus', 'Indianapolis'],
    'west': ['Los Angeles', 'San Francisco', 'Seattle', 'San Diego', 'Denver', 'Portland']
}


def pull_bea_state_gdp():
    """Pull state GDP data from BEA Regional API."""

    url = 'https://apps.bea.gov/api/data/'

    # Pull annual state GDP
    params = {
        'UserID': BEA_API_KEY,
        'method': 'GetData',
        'datasetname': 'Regional',
        'TableName': 'SAGDP2N',  # GDP in current dollars by state
        'LineCode': '1',  # All industry total
        'GeoFips': 'STATE',
        'Year': '2019,2020,2021,2022,2023,2024',
        'ResultFormat': 'JSON'
    }

    print("Pulling BEA state GDP data...")
    response = requests.get(url, params=params, timeout=60)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    data = response.json()

    if 'BEAAPI' in data and 'Results' in data['BEAAPI']:
        results = data['BEAAPI']['Results']
        if 'Data' in results:
            df = pd.DataFrame(results['Data'])
            df.to_csv(OUTPUT_DIR / 'bea_state_gdp_total.csv', index=False)
            print(f"  -> Saved {len(df)} observations")
            return df

    print("  -> Failed to parse BEA response")
    return None


def pull_bea_state_gdp_by_industry():
    """Pull state GDP by major industry from BEA."""

    url = 'https://apps.bea.gov/api/data/'

    # Key industry line codes
    industries = {
        '3': 'Private industries',
        '6': 'Mining',
        '10': 'Manufacturing',
        '34': 'Retail trade',
        '35': 'Finance and insurance',
        '45': 'Real estate',
        '51': 'Professional services',
        '56': 'Health care',
        '59': 'Government'
    }

    all_data = []

    for line_code, industry_name in industries.items():
        params = {
            'UserID': BEA_API_KEY,
            'method': 'GetData',
            'datasetname': 'Regional',
            'TableName': 'SAGDP2N',
            'LineCode': line_code,
            'GeoFips': 'STATE',
            'Year': '2022,2023,2024',
            'ResultFormat': 'JSON'
        }

        print(f"  Pulling {industry_name}...")
        response = requests.get(url, params=params, timeout=60)

        if response.status_code == 200:
            data = response.json()
            if 'BEAAPI' in data and 'Results' in data['BEAAPI']:
                results = data['BEAAPI']['Results']
                if 'Data' in results:
                    df = pd.DataFrame(results['Data'])
                    df['Industry'] = industry_name
                    all_data.append(df)

    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        combined.to_csv(OUTPUT_DIR / 'bea_state_gdp_by_industry.csv', index=False)
        print(f"  -> Saved {len(combined)} total observations")
        return combined

    return None


def pull_bea_metro_gdp():
    """Pull metro area GDP from BEA."""

    url = 'https://apps.bea.gov/api/data/'

    params = {
        'UserID': BEA_API_KEY,
        'method': 'GetData',
        'datasetname': 'Regional',
        'TableName': 'MAGDP2',  # Metro GDP
        'LineCode': '1',
        'GeoFips': 'MSA',
        'Year': '2022,2023',
        'ResultFormat': 'JSON'
    }

    print("Pulling BEA metro GDP data...")
    response = requests.get(url, params=params, timeout=60)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    data = response.json()

    if 'BEAAPI' in data and 'Results' in data['BEAAPI']:
        results = data['BEAAPI']['Results']
        if 'Data' in results:
            df = pd.DataFrame(results['Data'])
            df.to_csv(OUTPUT_DIR / 'bea_metro_gdp.csv', index=False)
            print(f"  -> Saved {len(df)} observations")
            return df

    print("  -> Failed to parse BEA response")
    return None


def pull_bea_personal_income():
    """Pull state personal income data."""

    url = 'https://apps.bea.gov/api/data/'

    params = {
        'UserID': BEA_API_KEY,
        'method': 'GetData',
        'datasetname': 'Regional',
        'TableName': 'SAINC1',  # Personal income summary
        'LineCode': '3',  # Per capita personal income
        'GeoFips': 'STATE',
        'Year': '2020,2021,2022,2023,2024',
        'ResultFormat': 'JSON'
    }

    print("Pulling BEA personal income data...")
    response = requests.get(url, params=params, timeout=60)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    data = response.json()

    if 'BEAAPI' in data and 'Results' in data['BEAAPI']:
        results = data['BEAAPI']['Results']
        if 'Data' in results:
            df = pd.DataFrame(results['Data'])
            df.to_csv(OUTPUT_DIR / 'bea_state_per_capita_income.csv', index=False)
            print(f"  -> Saved {len(df)} observations")
            return df

    return None


def pull_bls_state_employment():
    """Pull state employment data from BLS."""

    # State FIPS codes for BLS series
    state_fips = {
        'CA': '06', 'TX': '48', 'FL': '12', 'NY': '36', 'IL': '17',
        'PA': '42', 'OH': '39', 'GA': '13', 'NC': '37', 'MI': '26',
        'NJ': '34', 'VA': '51', 'WA': '53', 'AZ': '04', 'MA': '25',
        'TN': '47', 'IN': '18', 'MO': '29', 'MD': '24', 'WI': '55',
        'CO': '08', 'MN': '27', 'SC': '45', 'AL': '01', 'LA': '22'
    }

    # Build series IDs for total nonfarm employment
    series_ids = [f'SMS{fips}000000000000001' for fips in state_fips.values()]

    url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'

    headers = {'Content-type': 'application/json'}
    payload = {
        'seriesid': series_ids[:25],  # BLS limits to 25 series per request
        'startyear': '2020',
        'endyear': '2025',
        'registrationkey': BLS_API_KEY
    }

    print("Pulling BLS state employment data...")
    response = requests.post(url, json=payload, headers=headers, timeout=60)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    data = response.json()

    if data.get('status') == 'REQUEST_SUCCEEDED':
        results = []
        fips_to_state = {v: k for k, v in state_fips.items()}

        for series in data['Results']['series']:
            series_id = series['seriesID']
            state_fips_code = series_id[3:5]
            state = fips_to_state.get(state_fips_code, 'Unknown')

            for obs in series['data']:
                results.append({
                    'state': state,
                    'year': obs['year'],
                    'period': obs['period'],
                    'employment': float(obs['value']) * 1000  # In thousands
                })

        df = pd.DataFrame(results)
        df.to_csv(OUTPUT_DIR / 'bls_state_employment.csv', index=False)
        print(f"  -> Saved {len(df)} observations")
        return df
    else:
        print(f"  -> BLS API error: {data.get('message', 'Unknown')}")
        return None


def pull_fred_state_unemployment():
    """Pull state unemployment rates from FRED."""

    states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI',
              'WA', 'AZ', 'MA', 'TN', 'CO', 'MN', 'WI', 'IN', 'MO']

    all_data = []

    for state in states:
        series_id = f'{state}UR'  # State unemployment rate
        url = 'https://api.stlouisfed.org/fred/series/observations'
        params = {
            'series_id': series_id,
            'api_key': FRED_API_KEY,
            'file_type': 'json',
            'observation_start': '2020-01-01',
            'observation_end': '2025-12-31'
        }

        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if 'observations' in data:
                for obs in data['observations']:
                    if obs['value'] != '.':
                        all_data.append({
                            'state': state,
                            'date': obs['date'],
                            'unemployment_rate': float(obs['value'])
                        })

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(OUTPUT_DIR / 'fred_state_unemployment.csv', index=False)
        print(f"Pulled FRED unemployment data: {len(df)} observations")
        return df

    return None


def pull_fred_population():
    """Pull state population estimates from FRED."""

    states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI',
              'WA', 'AZ', 'MA', 'TN', 'CO', 'MN', 'WI', 'IN', 'MO', 'NJ']

    all_data = []

    print("Pulling FRED population data...")
    for state in states:
        series_id = f'{state}POP'
        url = 'https://api.stlouisfed.org/fred/series/observations'
        params = {
            'series_id': series_id,
            'api_key': FRED_API_KEY,
            'file_type': 'json',
            'observation_start': '2020-01-01'
        }

        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if 'observations' in data:
                for obs in data['observations']:
                    if obs['value'] != '.':
                        all_data.append({
                            'state': state,
                            'date': obs['date'],
                            'population': float(obs['value']) * 1000  # In thousands
                        })

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(OUTPUT_DIR / 'fred_state_population.csv', index=False)
        print(f"  -> Saved {len(df)} observations")
        return df

    return None


def main():
    """Pull all regional data."""

    print("=" * 60)
    print("REGIONAL DATA PULL")
    print("=" * 60)
    print()

    # BEA Data
    print("PHASE 1: BEA DATA")
    print("-" * 40)
    state_gdp = pull_bea_state_gdp()
    state_gdp_industry = pull_bea_state_gdp_by_industry()
    metro_gdp = pull_bea_metro_gdp()
    income = pull_bea_personal_income()
    print()

    # BLS Data
    print("PHASE 2: BLS DATA")
    print("-" * 40)
    employment = pull_bls_state_employment()
    print()

    # FRED Data
    print("PHASE 3: FRED DATA")
    print("-" * 40)
    unemployment = pull_fred_state_unemployment()
    population = pull_fred_population()
    print()

    # Save metadata
    metadata = {
        'pull_date': datetime.now().isoformat(),
        'sources': ['BEA Regional', 'BLS', 'FRED'],
        'regions': REGIONS,
        'key_metros': METROS
    }
    with open(OUTPUT_DIR / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)

    print("=" * 60)
    print("REGIONAL DATA PULL COMPLETE")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
