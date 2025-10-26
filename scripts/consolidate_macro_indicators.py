"""
Macroeconomic Indicators Consolidation Script
==============================================

Extracts key macroeconomic indicators from Eurostat datasets and consolidates
them into a single time series dataset for analysis.

Key indicators:
- Government deficit/surplus (% GDP)
- Government debt (% GDP)
- Public health expenditure (% GDP)
- Total health expenditure (% GDP)
- GDP (million EUR)
- GDP per capita (EUR)

Output: Single CSV/XLSX/Parquet file with all indicators by year (1995-2024)

Author: Claude
Date: October 26, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

class MacroIndicatorConsolidator:
    """Consolidate key macroeconomic indicators from Eurostat datasets"""

    def __init__(self, eurostat_macro_dir: str = 'eurostat_macro_data'):
        self.data_dir = Path(eurostat_macro_dir) / 'parquet'
        self.output_dir = Path('macro_indicators_consolidated')
        self.output_dir.mkdir(exist_ok=True)

        # Dataset file paths
        self.datasets = {
            'deficit_debt': self.data_dir / 'gov_10dd_edpt1_government_deficit_debt.parquet',
            'health_financing': self.data_dir / 'hlth_sha11_hf_health_expenditure_by_financing.parquet',
            'health_function': self.data_dir / 'hlth_sha11_hc_health_expenditure_by_function.parquet',
            'gdp_components': self.data_dir / 'nama_10_gdp_gdp_main_components.parquet',
            'gdp_per_capita': self.data_dir / 'nama_10_pc_gdp_per_capita.parquet',
        }

    def extract_deficit_surplus(self) -> pd.DataFrame:
        """Extract government deficit/surplus as % of GDP"""
        df = pd.read_parquet(self.datasets['deficit_debt'])

        # Filter for net borrowing/lending (B9) as % of GDP
        deficit = df[
            (df['na_item'] == 'B9') &
            (df['unit'] == 'PC_GDP') &
            (df['sector'] == 'S13')  # General government
        ][['time', 'value']].copy()

        deficit.columns = ['year', 'deficit_surplus_pct_gdp']
        deficit['year'] = pd.to_numeric(deficit['year'], errors='coerce')

        print(f'  Deficit/surplus: {len(deficit)} records ({deficit["year"].min()}-{deficit["year"].max()})')

        return deficit.sort_values('year')

    def extract_government_debt(self) -> pd.DataFrame:
        """Extract government debt as % of GDP"""
        df = pd.read_parquet(self.datasets['deficit_debt'])

        # Filter for government consolidated gross debt (GD) as % of GDP
        debt = df[
            (df['na_item'] == 'GD') &
            (df['unit'] == 'PC_GDP') &
            (df['sector'] == 'S13')  # General government
        ][['time', 'value']].copy()

        debt.columns = ['year', 'government_debt_pct_gdp']
        debt['year'] = pd.to_numeric(debt['year'], errors='coerce')

        print(f'  Government debt: {len(debt)} records ({debt["year"].min()}-{debt["year"].max()})')

        return debt.sort_values('year')

    def extract_public_health_expenditure(self) -> pd.DataFrame:
        """Extract public health expenditure as % of GDP"""
        df = pd.read_parquet(self.datasets['health_financing'])

        # Filter for government schemes (HF1) as % of GDP
        public_health = df[
            (df['icha11_hf'] == 'HF1') &
            (df['unit'] == 'PC_GDP')
        ][['time', 'value']].copy()

        public_health.columns = ['year', 'public_health_exp_pct_gdp']
        public_health['year'] = pd.to_numeric(public_health['year'], errors='coerce')

        print(f'  Public health expenditure: {len(public_health)} records ({public_health["year"].min()}-{public_health["year"].max()})')

        return public_health.sort_values('year')

    def extract_total_health_expenditure(self) -> pd.DataFrame:
        """Extract total health expenditure as % of GDP"""
        df = pd.read_parquet(self.datasets['health_financing'])

        # Filter for all financing schemes (TOT_HF) as % of GDP
        total_health = df[
            (df['icha11_hf'] == 'TOT_HF') &
            (df['unit'] == 'PC_GDP')
        ][['time', 'value']].copy()

        total_health.columns = ['year', 'total_health_exp_pct_gdp']
        total_health['year'] = pd.to_numeric(total_health['year'], errors='coerce')

        print(f'  Total health expenditure: {len(total_health)} records ({total_health["year"].min()}-{total_health["year"].max()})')

        return total_health.sort_values('year')

    def extract_hospital_expenditure(self) -> pd.DataFrame:
        """Extract hospital care expenditure as % of GDP"""
        df = pd.read_parquet(self.datasets['health_function'])

        # Filter for curative and rehabilitative care (HC1) as % of GDP
        hospital = df[
            (df['icha11_hc'] == 'HC1') &
            (df['unit'] == 'PC_GDP')
        ][['time', 'value']].copy()

        hospital.columns = ['year', 'hospital_care_exp_pct_gdp']
        hospital['year'] = pd.to_numeric(hospital['year'], errors='coerce')

        print(f'  Hospital care expenditure: {len(hospital)} records ({hospital["year"].min()}-{hospital["year"].max()})')

        return hospital.sort_values('year')

    def extract_gdp(self) -> pd.DataFrame:
        """Extract GDP in million EUR (current prices)"""
        df = pd.read_parquet(self.datasets['gdp_components'])

        # Filter for GDP (B1GQ) in million EUR at current prices
        gdp = df[
            (df['na_item'] == 'B1GQ') &
            (df['unit'] == 'CP_MEUR')  # Current prices, million EUR
        ][['time', 'value']].copy()

        gdp.columns = ['year', 'gdp_million_eur']
        gdp['year'] = pd.to_numeric(gdp['year'], errors='coerce')

        print(f'  GDP: {len(gdp)} records ({gdp["year"].min()}-{gdp["year"].max()})')

        return gdp.sort_values('year')

    def extract_gdp_per_capita(self) -> pd.DataFrame:
        """Extract GDP per capita in EUR"""
        df = pd.read_parquet(self.datasets['gdp_per_capita'])

        # Filter for GDP per capita (B1GQ) in EUR at current prices
        gdp_pc = df[
            (df['na_item'] == 'B1GQ') &
            (df['unit'] == 'CP_EUR_HAB')  # Current prices, EUR per capita
        ][['time', 'value']].copy()

        gdp_pc.columns = ['year', 'gdp_per_capita_eur']
        gdp_pc['year'] = pd.to_numeric(gdp_pc['year'], errors='coerce')

        print(f'  GDP per capita: {len(gdp_pc)} records ({gdp_pc["year"].min()}-{gdp_pc["year"].max()})')

        return gdp_pc.sort_values('year')

    def consolidate_indicators(self) -> pd.DataFrame:
        """Consolidate all indicators into single DataFrame"""

        print('='*80)
        print('CONSOLIDATING MACROECONOMIC INDICATORS')
        print('='*80)

        print('\nExtracting indicators from Eurostat datasets...\n')

        # Extract all indicators
        deficit = self.extract_deficit_surplus()
        debt = self.extract_government_debt()
        public_health = self.extract_public_health_expenditure()
        total_health = self.extract_total_health_expenditure()
        hospital = self.extract_hospital_expenditure()
        gdp = self.extract_gdp()
        gdp_pc = self.extract_gdp_per_capita()

        print('\nMerging all indicators...')

        # Start with deficit (usually 1995-2024)
        consolidated = deficit

        # Merge all indicators on year
        for df_to_merge in [debt, public_health, total_health, hospital, gdp, gdp_pc]:
            consolidated = consolidated.merge(df_to_merge, on='year', how='outer')

        # Sort by year
        consolidated = consolidated.sort_values('year').reset_index(drop=True)

        # Calculate derived indicators
        print('\nCalculating derived indicators...')

        # Private health expenditure = Total - Public
        consolidated['private_health_exp_pct_gdp'] = (
            consolidated['total_health_exp_pct_gdp'] - consolidated['public_health_exp_pct_gdp']
        )

        # GDP growth rate (year-on-year %)
        consolidated['gdp_growth_rate_pct'] = consolidated['gdp_million_eur'].pct_change() * 100

        print(f'\nConsolidated dataset:')
        print(f'  Total records: {len(consolidated)}')
        print(f'  Year range: {consolidated["year"].min():.0f} - {consolidated["year"].max():.0f}')
        print(f'  Columns: {len(consolidated.columns)}')

        # Show data completeness
        print('\nData completeness by indicator:')
        for col in consolidated.columns:
            if col != 'year':
                non_null = consolidated[col].notna().sum()
                pct = 100 * non_null / len(consolidated)
                print(f'  {col}: {non_null}/{len(consolidated)} ({pct:.1f}%)')

        return consolidated

    def save_consolidated_data(self, df: pd.DataFrame):
        """Save consolidated data in multiple formats"""

        print(f'\n{"-"*80}')
        print('Saving consolidated data...')

        base_filename = 'macro_indicators_consolidated'

        # Save CSV (semicolon-delimited, Portuguese standard)
        csv_file = self.output_dir / f'{base_filename}.csv'
        df.to_csv(csv_file, index=False, sep=';', encoding='utf-8-sig', float_format='%.3f')
        print(f'  CSV: {csv_file.name} ({csv_file.stat().st_size // 1024} KB)')

        # Save XLSX
        xlsx_file = self.output_dir / f'{base_filename}.xlsx'
        df.to_excel(xlsx_file, index=False, engine='openpyxl', float_format='%.3f')
        print(f'  XLSX: {xlsx_file.name} ({xlsx_file.stat().st_size // 1024} KB)')

        # Save Parquet
        parquet_file = self.output_dir / f'{base_filename}.parquet'
        df.to_parquet(parquet_file, index=False, engine='pyarrow', compression='snappy')
        print(f'  Parquet: {parquet_file.name} ({parquet_file.stat().st_size // 1024} KB)')

        # Save JSON
        json_file = self.output_dir / f'{base_filename}.json'
        df.to_json(json_file, orient='records', indent=2, force_ascii=False)
        print(f'  JSON: {json_file.name} ({json_file.stat().st_size // 1024} KB)')

        # Save metadata
        metadata = {
            'creation_date': datetime.now().isoformat(),
            'description': 'Consolidated macroeconomic indicators for Portugal',
            'source': 'Eurostat (via eurostat_macro_extractor.py)',
            'total_records': len(df),
            'year_range': {
                'min': int(df['year'].min()),
                'max': int(df['year'].max())
            },
            'indicators': {
                'deficit_surplus_pct_gdp': 'Government deficit (-) or surplus (+) as % of GDP',
                'government_debt_pct_gdp': 'Government consolidated gross debt as % of GDP',
                'public_health_exp_pct_gdp': 'Public health expenditure as % of GDP',
                'total_health_exp_pct_gdp': 'Total health expenditure as % of GDP',
                'private_health_exp_pct_gdp': 'Private health expenditure as % of GDP (calculated)',
                'hospital_care_exp_pct_gdp': 'Hospital care expenditure as % of GDP',
                'gdp_million_eur': 'GDP in million EUR (current prices)',
                'gdp_per_capita_eur': 'GDP per capita in EUR (current prices)',
                'gdp_growth_rate_pct': 'GDP year-on-year growth rate % (calculated)'
            },
            'completeness': {
                col: {
                    'non_null': int(df[col].notna().sum()),
                    'total': len(df),
                    'percentage': float(100 * df[col].notna().sum() / len(df))
                }
                for col in df.columns if col != 'year'
            }
        }

        import json
        metadata_file = self.output_dir / f'{base_filename}_metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f'  Metadata: {metadata_file.name}')

        print(f'\nAll files saved to: {self.output_dir.absolute()}')

    def generate_summary_report(self, df: pd.DataFrame):
        """Generate summary statistics and report"""

        print(f'\n{"="*80}')
        print('SUMMARY STATISTICS')
        print('='*80)

        # Focus on 2015-2024 period (research period)
        df_recent = df[df['year'] >= 2015].copy()

        print(f'\nPeriod: 2015-2024 ({len(df_recent)} years)')
        print('-'*80)

        # Key statistics
        indicators = [
            ('deficit_surplus_pct_gdp', 'Deficit/Surplus (% GDP)'),
            ('government_debt_pct_gdp', 'Government Debt (% GDP)'),
            ('public_health_exp_pct_gdp', 'Public Health Exp (% GDP)'),
            ('gdp_growth_rate_pct', 'GDP Growth Rate (%)')
        ]

        for col, label in indicators:
            if col in df_recent.columns:
                data = df_recent[col].dropna()
                if len(data) > 0:
                    print(f'\n{label}:')
                    print(f'  Mean: {data.mean():.2f}')
                    print(f'  Median: {data.median():.2f}')
                    print(f'  Min: {data.min():.2f} (year {df_recent.loc[data.idxmin(), "year"]:.0f})')
                    print(f'  Max: {data.max():.2f} (year {df_recent.loc[data.idxmax(), "year"]:.0f})')
                    print(f'  Std Dev: {data.std():.2f}')

        # Show trends
        print(f'\n{"-"*80}')
        print('TRENDS (2015 vs 2024):')
        print('-'*80)

        if len(df_recent) > 0:
            year_2015 = df_recent[df_recent['year'] == 2015].iloc[0] if len(df_recent[df_recent['year'] == 2015]) > 0 else None
            year_2024 = df_recent[df_recent['year'] == 2024].iloc[0] if len(df_recent[df_recent['year'] == 2024]) > 0 else None

            if year_2015 is not None and year_2024 is not None:
                for col, label in indicators:
                    if col in df_recent.columns:
                        val_2015 = year_2015[col]
                        val_2024 = year_2024[col]
                        if pd.notna(val_2015) and pd.notna(val_2024):
                            change = val_2024 - val_2015
                            print(f'\n{label}:')
                            print(f'  2015: {val_2015:.2f}')
                            print(f'  2024: {val_2024:.2f}')
                            print(f'  Change: {change:+.2f}')

    def run(self):
        """Run full consolidation process"""

        print('\nMACROECONOMIC INDICATORS CONSOLIDATION')
        print('='*80)
        print('This script consolidates key macroeconomic indicators')
        print('from Eurostat datasets into a single time series file.\n')

        # Consolidate
        df = self.consolidate_indicators()

        # Save
        self.save_consolidated_data(df)

        # Generate summary
        self.generate_summary_report(df)

        print(f'\n{"="*80}')
        print('CONSOLIDATION COMPLETE')
        print('='*80)
        print(f'\nOutput: {self.output_dir.absolute()}')
        print(f'Files: CSV, XLSX, Parquet, JSON + metadata')
        print('\nReady for analysis!\n')


if __name__ == '__main__':
    consolidator = MacroIndicatorConsolidator(eurostat_macro_dir='eurostat_macro_data')
    consolidator.run()
