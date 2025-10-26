"""
Eurostat Macroeconomic Indicators Extractor
==========================================

Extracts macroeconomic indicators from Eurostat for Portugal:
- Government deficit/surplus and debt
- Health expenditure
- GDP (national and per capita)
- Wages/earnings

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

class EurostatMacroExtractor:
    """Extract macroeconomic indicators from Eurostat API"""

    def __init__(self, output_dir: str = 'eurostat_macro_data'):
        self.base_url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data'
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Create subdirectories
        for fmt in ['json', 'csv', 'xlsx', 'parquet']:
            (self.output_dir / fmt).mkdir(exist_ok=True)
        (self.output_dir / 'metadata').mkdir(exist_ok=True)

        # Priority datasets
        self.datasets = {
            # PRIORITY 1: Government finance (deficit, debt)
            'gov_10dd_edpt1': {
                'name': 'government_deficit_debt',
                'description': 'Government deficit/surplus, debt and associated data',
                'priority': 1,
                'params': {}  # Get all, filter Portugal later
            },

            # PRIORITY 1: Health expenditure
            'hlth_sha11_hf': {
                'name': 'health_expenditure_by_financing',
                'description': 'Health expenditure by financing scheme',
                'priority': 1,
                'params': {}
            },
            'hlth_sha11_hc': {
                'name': 'health_expenditure_by_function',
                'description': 'Health expenditure by function',
                'priority': 1,
                'params': {}
            },

            # PRIORITY 2: GDP
            'nama_10_gdp': {
                'name': 'gdp_main_components',
                'description': 'GDP and main components (output, expenditure and income)',
                'priority': 2,
                'params': {}
            },
            'nama_10_pc': {
                'name': 'gdp_per_capita',
                'description': 'GDP per capita',
                'priority': 2,
                'params': {}
            },

            # PRIORITY 3: Wages
            'earn_nt_net': {
                'name': 'annual_net_earnings',
                'description': 'Annual net earnings',
                'priority': 3,
                'params': {}
            },

            # PRIORITY 3: Taxes
            'gov_10a_main': {
                'name': 'tax_aggregates',
                'description': 'Main national accounts tax aggregates',
                'priority': 3,
                'params': {}
            },
        }

    def fetch_dataset(self, dataset_code: str) -> Dict[str, Any]:
        """Fetch dataset from Eurostat API"""
        url = f'{self.base_url}/{dataset_code}'

        params = self.datasets[dataset_code].get('params', {})

        print(f'  Fetching from API: {dataset_code}')
        print(f'  URL: {url}')

        try:
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()

            data = response.json()
            print(f'  Response received: {len(str(data))} characters')

            return data

        except requests.Timeout:
            print(f'  Error: Request timed out after 60 seconds')
            return None
        except Exception as e:
            print(f'  Error: {str(e)}')
            return None

    def jsonstat_to_dataframe(self, jsonstat_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Convert JSON-stat format to pandas DataFrame.
        Eurostat uses JSON-stat 2.0 format.
        """
        if not jsonstat_data or 'value' not in jsonstat_data:
            return pd.DataFrame()

        # Extract dimensions
        dimensions = jsonstat_data.get('dimension', {})
        values = jsonstat_data.get('value', {})

        # Get dimension IDs in order
        dim_ids = list(jsonstat_data.get('id', []))

        if not dim_ids:
            print('  Warning: No dimension IDs found')
            return pd.DataFrame()

        # Calculate sizes for each dimension
        sizes = []
        for dim_id in dim_ids:
            if dim_id in dimensions:
                categories = dimensions[dim_id].get('category', {}).get('index', {})
                sizes.append(len(categories))
            else:
                sizes.append(1)

        # Calculate total number of records
        total_records = 1
        for size in sizes:
            total_records *= size

        print(f'  Dimensions: {dim_ids}')
        print(f'  Sizes: {sizes}')
        print(f'  Expected records: {total_records:,}')

        # Build records
        records = []

        for i in range(total_records):
            record = {}

            # Calculate index for each dimension
            temp_i = i
            for j, dim_id in enumerate(dim_ids):
                if dim_id not in dimensions:
                    continue

                categories = list(dimensions[dim_id]['category']['index'].keys())
                idx = temp_i % sizes[j]
                temp_i = temp_i // sizes[j]

                # Get category code and label
                cat_code = categories[idx]
                cat_label = dimensions[dim_id]['category'].get('label', {}).get(cat_code, cat_code)

                record[f'{dim_id}'] = cat_code
                record[f'{dim_id}_label'] = cat_label

            # Get value
            record['value'] = values.get(str(i))

            records.append(record)

        df = pd.DataFrame(records)
        print(f'  Total records created: {len(df):,}')

        return df

    def filter_portugal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter DataFrame for Portugal only"""
        if df.empty:
            return df

        # Look for geo column
        if 'geo' in df.columns:
            df_pt = df[df['geo'].str.startswith('PT', na=False)].copy()
            print(f'  Filtered to Portugal: {len(df_pt):,} records')
            return df_pt
        else:
            print('  Warning: No geo column found, returning all data')
            return df

    def save_multiformat(self, df: pd.DataFrame, dataset_code: str, dataset_name: str):
        """Save DataFrame in multiple formats"""

        if df.empty:
            print(f'  Skipping save - no data')
            return

        filename_base = f'{dataset_code}_{dataset_name}'

        # Save JSON
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

        # Save Parquet
        parquet_file = self.output_dir / 'parquet' / f'{filename_base}.parquet'
        df.to_parquet(parquet_file, index=False, engine='pyarrow', compression='snappy')
        print(f'  Saved Parquet: {parquet_file.name} ({parquet_file.stat().st_size // 1024} KB)')

    def extract_dataset(self, dataset_code: str) -> bool:
        """Extract a single dataset"""

        info = self.datasets[dataset_code]
        print(f"\n{'='*80}")
        print(f"Dataset: {dataset_code}")
        print(f"Description: {info['description']}")
        print(f"Priority: {info['priority']}")
        print('='*80)

        # Fetch data
        data = self.fetch_dataset(dataset_code)

        if not data:
            print(f'Failed to fetch data for {dataset_code}')
            return False

        # Parse to DataFrame
        print('\n  Parsing JSON-stat to DataFrame...')
        df = self.jsonstat_to_dataframe(data)

        if df.empty:
            print(f'No data extracted for {dataset_code}')
            return False

        # Filter for Portugal
        print('\n  Filtering for Portugal...')
        df_pt = self.filter_portugal(df)

        if df_pt.empty:
            print(f'No Portugal data found for {dataset_code}')
            return False

        # Show summary
        print(f'\nData Summary:')
        print(f'  Portugal records: {len(df_pt):,}')

        # Show time range if 'time' column exists
        if 'time' in df_pt.columns:
            unique_years = df_pt['time'].nunique()
            min_year = df_pt['time'].min()
            max_year = df_pt['time'].max()
            print(f'  Time range: {min_year} to {max_year}')
            print(f'  Unique years: {unique_years}')

        # Show geo breakdown
        if 'geo' in df_pt.columns:
            unique_geo = df_pt['geo'].nunique()
            geo_codes = sorted(df_pt['geo'].unique())
            print(f'  Geographic units: {unique_geo}')
            print(f'  Codes: {", ".join(geo_codes[:10])}{"..." if len(geo_codes) > 10 else ""}')

        # Save in all formats
        print(f'\nSaving in multiple formats...')
        self.save_multiformat(df_pt, dataset_code, info['name'])

        # Save metadata
        metadata = {
            'dataset_code': dataset_code,
            'dataset_name': info['name'],
            'description': info['description'],
            'priority': info['priority'],
            'extraction_date': datetime.now().isoformat(),
            'total_records': len(df_pt),
            'years': sorted(df_pt['time'].unique().tolist()) if 'time' in df_pt.columns else [],
            'geo_codes': sorted(df_pt['geo'].unique().tolist()) if 'geo' in df_pt.columns else [],
            'columns': df_pt.columns.tolist(),
            'source': 'Eurostat API',
            'api_url': f'{self.base_url}/{dataset_code}'
        }

        metadata_file = self.output_dir / 'metadata' / f'{dataset_code}_{info["name"]}_metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f'  Saved metadata: {metadata_file.name}')

        return True

    def extract_all(self, priorities: List[int] = None):
        """Extract all datasets (optionally filter by priority)"""

        print('='*80)
        print('EUROSTAT MACROECONOMIC INDICATORS EXTRACTOR')
        print('='*80)
        print(f'Output directory: {self.output_dir.absolute()}')
        print(f'Datasets to extract: {len(self.datasets)}')

        if priorities:
            print(f'Filtering by priorities: {priorities}')

        print('='*80)

        results = {
            'success': [],
            'failed': []
        }

        datasets_to_process = [
            (code, info) for code, info in self.datasets.items()
            if priorities is None or info['priority'] in priorities
        ]

        print(f'\nProcessing {len(datasets_to_process)} datasets...\n')

        for i, (code, info) in enumerate(datasets_to_process, 1):
            print(f'\n[{i}/{len(datasets_to_process)}] Processing {code}...')

            try:
                success = self.extract_dataset(code)

                if success:
                    results['success'].append(code)
                else:
                    results['failed'].append(code)

                # Rate limiting
                if i < len(datasets_to_process):
                    print('  Waiting 3 seconds before next request...')
                    time.sleep(3)

            except Exception as e:
                print(f'  Error processing {code}: {str(e)}')
                results['failed'].append(code)

        # Final summary
        print(f"\n{'='*80}")
        print('EXTRACTION COMPLETE')
        print('='*80)
        print(f"Successfully extracted: {len(results['success'])}/{len(datasets_to_process)}")
        print(f"Failed: {len(results['failed'])}")

        if results['success']:
            print(f"\nSuccessful extractions:")
            for code in results['success']:
                print(f"  [OK] {code}: {self.datasets[code]['description']}")

        if results['failed']:
            print(f"\nFailed extractions:")
            for code in results['failed']:
                print(f"  [FAIL] {code}: {self.datasets[code]['description']}")

        # Save extraction log
        log_data = {
            'extraction_date': datetime.now().isoformat(),
            'total_datasets': len(datasets_to_process),
            'successful': len(results['success']),
            'failed': len(results['failed']),
            'results': results,
            'priorities_filter': priorities
        }

        log_file = self.output_dir / 'extraction_log_macro.json'
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

        print(f"\nExtraction log saved: {log_file}")
        print(f"\nData saved in: {self.output_dir.absolute()}")
        print(f"  - JSON files: {self.output_dir / 'json'}")
        print(f"  - CSV files: {self.output_dir / 'csv'}")
        print(f"  - XLSX files: {self.output_dir / 'xlsx'}")
        print(f"  - Parquet files: {self.output_dir / 'parquet'} (RECOMMENDED)")


if __name__ == '__main__':
    print('Starting Eurostat Macroeconomic Data Extraction...')
    print('This will extract government finance, health expenditure, GDP, and wages data.\n')

    extractor = EurostatMacroExtractor(output_dir='eurostat_macro_data')

    # Extract Priority 1 datasets first (government finance + health expenditure)
    print('PHASE 1: Extracting Priority 1 datasets (government finance + health expenditure)')
    extractor.extract_all(priorities=[1])

    print('\n\nPHASE 2: Extracting Priority 2 and 3 datasets (GDP + wages)')
    extractor.extract_all(priorities=[2, 3])

    print('\nDone! Macroeconomic data extracted successfully.')
    print('Check the eurostat_macro_data/ directory for results.')
