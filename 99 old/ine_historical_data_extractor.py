"""
INE Historical Data Extractor - ALL YEARS (2011-2024)
======================================================

Extracts HISTORICAL time series data from INE (Portuguese Statistics) API.

Key Discovery: Using op=1 returns ALL historical years (not just latest year).

Historical Coverage:
- Most indicators: 2011-2023 (13 years)
- Unemployment: Q1 2011 - Q4 2024 (quarterly, 58 periods)
- Total records: ~21,000+ with historical data

Author: Claude
Date: October 26, 2025
"""

import requests
import pandas as pd
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class INEHistoricalDataExtractor:
    """Extract historical time series data from INE API"""

    def __init__(self, output_dir: str = 'ine_historical_data'):
        self.base_url = 'https://www.ine.pt/ine/json_indicador/pindica.jsp'
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Create subdirectories for each format
        for fmt in ['json', 'csv', 'xlsx', 'parquet']:
            (self.output_dir / fmt).mkdir(exist_ok=True)
        (self.output_dir / 'metadata').mkdir(exist_ok=True)

        # INE Indicators
        self.indicators = {
            '0008273': {
                'name': 'population_by_region_sex_age',
                'description': 'Population by region, sex and age group',
                'category': 'Demographics'
            },
            '0008258': {
                'name': 'aging_index',
                'description': 'Aging index by region',
                'category': 'Demographics'
            },
            '0008259': {
                'name': 'elderly_dependency_index',
                'description': 'Elderly dependency index',
                'category': 'Demographics'
            },
            '0008261': {
                'name': 'total_dependency_ratio',
                'description': 'Total dependency ratio',
                'category': 'Demographics'
            },
            '0008274': {
                'name': 'fertility_index',
                'description': 'Fertility index',
                'category': 'Demographics'
            },
            '0008275': {
                'name': 'adolescent_fertility_rate',
                'description': 'Adolescent fertility rate',
                'category': 'Demographics'
            },
            '0001228': {
                'name': 'life_expectancy_at_65',
                'description': 'Life expectancy at 65 years',
                'category': 'Demographics'
            },
            '0012136': {
                'name': 'unemployment_rate_by_region',
                'description': 'Unemployment rate by region',
                'category': 'Economics'
            },
            '0010683': {
                'name': 'employment_statistics',
                'description': 'Employment statistics',
                'category': 'Economics'
            },
            '0008277': {
                'name': 'nurses_per_1000_inhabitants',
                'description': 'Nurses per 1000 inhabitants',
                'category': 'Healthcare'
            }
        }

    def get_historical_data(self, indicator_code: str) -> Dict[str, Any]:
        """
        Fetch ALL historical years for an indicator using op=1.

        Returns data structure with all years in 'Pref' field.
        """
        url = f'{self.base_url}?op=1&varcd={indicator_code}&lang=PT'

        try:
            print(f'  Fetching from API: {url}')
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'

            data = response.json()

            if isinstance(data, list) and len(data) > 0:
                return data[0]
            else:
                print(f'  Warning: Unexpected response format')
                return None

        except requests.Timeout:
            print(f'  Error: Request timed out after 30 seconds')
            return None
        except Exception as e:
            print(f'  Error: {str(e)}')
            return None

    def parse_historical_to_dataframe(self, data: Dict[str, Any], indicator_code: str) -> pd.DataFrame:
        """
        Convert historical data structure to long-format DataFrame.

        Input: Data with 'Pref' field containing {year: [records]} structure
        Output: DataFrame with periodo, geocod, geodsg, valor columns
        """
        if not data or 'Pref' not in data:
            return pd.DataFrame()

        all_records = []

        # Extract all years from Pref field
        pref_data = data['Pref']

        if not isinstance(pref_data, dict):
            print(f'  Warning: Pref is not a dictionary')
            return pd.DataFrame()

        print(f'  Years available: {list(pref_data.keys())}')

        for year, year_data in pref_data.items():
            if isinstance(year_data, list):
                for record in year_data:
                    # Add year/period to each record
                    record_with_period = record.copy()
                    record_with_period['periodo'] = year
                    all_records.append(record_with_period)

        df = pd.DataFrame(all_records)

        # Add metadata columns
        if 'IndicadorCod' in data:
            df['indicador_cod'] = data['IndicadorCod']
        if 'IndicadorDsg' in data:
            df['indicador_dsg'] = data['IndicadorDsg']

        print(f'  Total records extracted: {len(df):,}')

        return df

    def save_multiformat(self, df: pd.DataFrame, indicator_code: str, indicator_name: str):
        """Save DataFrame in multiple formats"""

        if df.empty:
            print(f'  Skipping save - no data')
            return

        filename_base = f'ind_{indicator_code}_{indicator_name}_historical'

        # Save JSON (original structure)
        json_file = self.output_dir / 'json' / f'{filename_base}.json'
        df.to_json(json_file, orient='records', force_ascii=False, indent=2)
        print(f'  Saved JSON: {json_file.name} ({json_file.stat().st_size // 1024} KB)')

        # Save CSV (semicolon-delimited, Portuguese standard)
        csv_file = self.output_dir / 'csv' / f'{filename_base}.csv'
        df.to_csv(csv_file, index=False, sep=';', encoding='utf-8-sig')
        print(f'  Saved CSV: {csv_file.name} ({csv_file.stat().st_size // 1024} KB)')

        # Save XLSX
        xlsx_file = self.output_dir / 'xlsx' / f'{filename_base}.xlsx'
        df.to_excel(xlsx_file, index=False, engine='openpyxl')
        print(f'  Saved XLSX: {xlsx_file.name} ({xlsx_file.stat().st_size // 1024} KB)')

        # Save Parquet (most efficient)
        parquet_file = self.output_dir / 'parquet' / f'{filename_base}.parquet'
        df.to_parquet(parquet_file, index=False, engine='pyarrow', compression='snappy')
        print(f'  Saved Parquet: {parquet_file.name} ({parquet_file.stat().st_size // 1024} KB) - MOST EFFICIENT')

    def extract_indicator_historical(self, code: str) -> bool:
        """Extract all historical data for a single indicator"""

        info = self.indicators[code]
        print(f"\n{'='*80}")
        print(f"Indicator {code}: {info['description']}")
        print(f"Category: {info['category']}")
        print('='*80)

        # Fetch data
        data = self.get_historical_data(code)

        if not data:
            print(f'Failed to fetch data for {code}')
            return False

        # Parse to DataFrame
        df = self.parse_historical_to_dataframe(data, code)

        if df.empty:
            print(f'No data extracted for {code}')
            return False

        # Show summary
        print(f'\nData Summary:')
        print(f'  Total records: {len(df):,}')
        if 'periodo' in df.columns:
            unique_periods = df['periodo'].nunique()
            min_period = df['periodo'].min()
            max_period = df['periodo'].max()
            print(f'  Period range: {min_period} to {max_period}')
            print(f'  Unique periods: {unique_periods}')

            # Count records since 2015
            if 'periodo' in df.columns:
                df_2015_plus = df[df['periodo'] >= '2015']
                print(f'  Records since 2015: {len(df_2015_plus):,} ({100*len(df_2015_plus)/len(df):.1f}%)')

        # Save in all formats
        print(f'\nSaving in multiple formats...')
        self.save_multiformat(df, code, info['name'])

        # Save metadata
        metadata = {
            'indicator_code': code,
            'indicator_name': info['name'],
            'description': info['description'],
            'category': info['category'],
            'extraction_date': datetime.now().isoformat(),
            'total_records': len(df),
            'periods': sorted(df['periodo'].unique().tolist()) if 'periodo' in df.columns else [],
            'columns': df.columns.tolist(),
            'source': 'INE API (op=1 - historical)',
            'api_url': f'{self.base_url}?op=1&varcd={code}&lang=PT'
        }

        metadata_file = self.output_dir / 'metadata' / f'ind_{code}_{info["name"]}_metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f'  Saved metadata: {metadata_file.name}')

        return True

    def extract_all(self):
        """Extract all indicators with historical data"""

        print('='*80)
        print('INE HISTORICAL DATA EXTRACTOR')
        print('='*80)
        print(f'Output directory: {self.output_dir.absolute()}')
        print(f'Indicators to extract: {len(self.indicators)}')
        print(f'Method: op=1 (ALL historical years)')
        print('='*80)

        results = {
            'success': [],
            'failed': []
        }

        for i, (code, info) in enumerate(self.indicators.items(), 1):
            print(f'\n[{i}/{len(self.indicators)}] Processing {code}...')

            try:
                success = self.extract_indicator_historical(code)

                if success:
                    results['success'].append(code)
                else:
                    results['failed'].append(code)

                # Rate limiting
                if i < len(self.indicators):
                    print('  Waiting 3 seconds before next request...')
                    time.sleep(3)

            except Exception as e:
                print(f'  Error processing {code}: {str(e)}')
                results['failed'].append(code)

        # Final summary
        print(f"\n{'='*80}")
        print('EXTRACTION COMPLETE')
        print('='*80)
        print(f"Successfully extracted: {len(results['success'])}/{len(self.indicators)}")
        print(f"Failed: {len(results['failed'])}")

        if results['success']:
            print(f"\nSuccessful extractions:")
            for code in results['success']:
                print(f"  ✓ {code}: {self.indicators[code]['description']}")

        if results['failed']:
            print(f"\nFailed extractions:")
            for code in results['failed']:
                print(f"  ✗ {code}: {self.indicators[code]['description']}")

        # Save extraction log
        log_data = {
            'extraction_date': datetime.now().isoformat(),
            'method': 'op=1 (historical)',
            'total_indicators': len(self.indicators),
            'successful': len(results['success']),
            'failed': len(results['failed']),
            'results': results
        }

        log_file = self.output_dir / 'extraction_log_historical.json'
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

        print(f"\nExtraction log saved: {log_file}")
        print(f"\nData saved in: {self.output_dir.absolute()}")
        print(f"  - JSON files: {self.output_dir / 'json'}")
        print(f"  - CSV files: {self.output_dir / 'csv'}")
        print(f"  - XLSX files: {self.output_dir / 'xlsx'}")
        print(f"  - Parquet files: {self.output_dir / 'parquet'} (RECOMMENDED)")


if __name__ == '__main__':
    print('Starting INE Historical Data Extraction...')
    print('This will extract ALL historical years (2011-2024) for each indicator.\n')

    extractor = INEHistoricalDataExtractor(output_dir='ine_historical_data')
    extractor.extract_all()

    print('\nDone! Historical data extracted successfully.')
    print('Check the ine_historical_data/ directory for results.')
