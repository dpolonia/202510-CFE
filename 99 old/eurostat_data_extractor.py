#!/usr/bin/env python3
"""
Eurostat Data Extractor for Healthcare Research
================================================
Extracts health, demographic, and economic data from Eurostat API
Saves in multiple formats: JSON, CSV, XLSX, Parquet
"""

import requests
import json
import pandas as pd
from pathlib import Path
import time
from datetime import datetime

class EurostatExtractor:
    """
    Extracts data from Eurostat API (JSON-stat format)
    """

    BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"

    # Relevant datasets for healthcare research
    DATASETS = {
        # Regional GDP and Economics
        'nama_10r_3gdp': {
            'name': 'regional_gdp_by_nuts',
            'description': 'Gross domestic product (GDP) at current market prices by NUTS 3 regions',
            'category': 'Economics',
            'use_case': 'Regional economic context for hospital analysis',
            'params': {'unit': 'MIO_EUR'}  # Remove geo filter to get all Portuguese NUTS regions
        },

        # Healthcare Resources
        'hlth_rs_bdsrg2': {
            'name': 'hospital_beds_by_region',
            'description': 'Available beds in hospitals by NUTS 2 regions',
            'category': 'Healthcare',
            'use_case': 'Hospital capacity and infrastructure',
            'params': {}  # Get all regions, filter Portugal later
        },
        'hlth_rs_physreg': {
            'name': 'physicians_by_region',
            'description': 'Practising physicians by NUTS 2 regions',
            'category': 'Healthcare',
            'use_case': 'Healthcare workforce availability',
            'params': {}  # Get all regions, filter Portugal later
        },

        # Health Outcomes
        'hlth_cd_asdr2': {
            'name': 'mortality_rate_by_region',
            'description': 'Causes of death - standardised death rate by NUTS 2 region',
            'category': 'Health Outcomes',
            'use_case': 'Population health status',
            'params': {}  # Get all regions, filter Portugal later
        },
        'demo_mlexpec': {
            'name': 'life_expectancy',
            'description': 'Life expectancy by age and sex',
            'category': 'Demographics',
            'use_case': 'Population health outcomes',
            'params': {}  # Get all countries, filter Portugal later
        },

        # Demographics
        'demo_r_pjangrp3': {
            'name': 'population_by_age_sex_region',
            'description': 'Population on 1 January by age group, sex and NUTS 3 region',
            'category': 'Demographics',
            'use_case': 'Case-mix adjustment and demand forecasting',
            'params': {}  # Get all NUTS 3, filter Portugal later
        },
        'demo_r_find3': {
            'name': 'fertility_indicators_regional',
            'description': 'Fertility indicators by NUTS 3 region',
            'category': 'Demographics',
            'use_case': 'Birth trends and maternity services demand',
            'params': {}  # Get all NUTS 3, filter Portugal later
        },

        # Economics and Employment
        'nama_10r_3empers': {
            'name': 'employment_by_region',
            'description': 'Employment by sex, age and NUTS 3 region',
            'category': 'Economics',
            'use_case': 'Regional employment context',
            'params': {}  # Get all NUTS 3, filter Portugal later
        },
        'lfst_r_lfu3rt': {
            'name': 'unemployment_rate_regional',
            'description': 'Unemployment rate by NUTS 3 regions',
            'category': 'Economics',
            'use_case': 'Economic distress indicator',
            'params': {}  # Get all NUTS 3, filter Portugal later
        },
    }

    FORMATS = ['json', 'csv', 'xlsx', 'parquet']

    def __init__(self, output_dir: str = "eurostat_data_multiformat"):
        self.output_dir = Path(output_dir)
        self.create_directory_structure()
        self.log = []

    def create_directory_structure(self):
        """Create directory structure for all formats"""
        for fmt in self.FORMATS:
            fmt_dir = self.output_dir / fmt
            fmt_dir.mkdir(parents=True, exist_ok=True)

        # Metadata directory
        metadata_dir = self.output_dir / 'metadata'
        metadata_dir.mkdir(parents=True, exist_ok=True)

    def get_dataset(self, dataset_code: str, params: dict = None):
        """
        Fetch a dataset from Eurostat API

        Args:
            dataset_code: Dataset code (e.g., 'nama_10r_3gdp')
            params: Additional query parameters

        Returns:
            dict: Dataset in JSON-stat format
        """
        url = f"{self.BASE_URL}/{dataset_code}"

        # Default parameters
        query_params = {
            'format': 'JSON',
            'lang': 'en'
        }

        # Add custom parameters
        if params:
            query_params.update(params)

        try:
            print(f"    Fetching from: {url}")
            print(f"    Parameters: {query_params}")

            response = requests.get(url, params=query_params, timeout=120)
            response.raise_for_status()

            data = response.json()
            return data

        except Exception as e:
            print(f"    Error fetching dataset {dataset_code}: {str(e)}")
            return None

    def jsonstat_to_dataframe(self, jsonstat_data):
        """
        Convert JSON-stat format to pandas DataFrame

        Args:
            jsonstat_data: JSON-stat formatted data

        Returns:
            DataFrame or None
        """
        try:
            # JSON-stat structure: dimension and value
            if 'dimension' not in jsonstat_data or 'value' not in jsonstat_data:
                print("    Warning: Not a valid JSON-stat format")
                return None

            dimensions = jsonstat_data['dimension']
            values = jsonstat_data['value']

            # Get dimension IDs and their categories
            dim_ids = list(jsonstat_data['id'])
            dim_sizes = [dimensions[dim_id]['category']['index'] for dim_id in dim_ids]

            # Create all combinations
            records = []

            # Get size of each dimension
            sizes = [len(dimensions[dim_id]['category']['index']) for dim_id in dim_ids]

            # Create index for all combinations
            total_records = 1
            for size in sizes:
                total_records *= size

            for i in range(total_records):
                record = {}
                temp_i = i

                for j, dim_id in enumerate(dim_ids):
                    categories = list(dimensions[dim_id]['category']['index'].keys())
                    idx = temp_i % sizes[j]
                    temp_i = temp_i // sizes[j]

                    # Get category code and label
                    cat_code = categories[idx]
                    cat_label = dimensions[dim_id]['category']['label'].get(cat_code, cat_code)

                    record[f'{dim_id}'] = cat_code
                    record[f'{dim_id}_label'] = cat_label

                # Add value
                record['value'] = values.get(str(i))

                records.append(record)

            df = pd.DataFrame(records)
            return df

        except Exception as e:
            print(f"    Error converting JSON-stat to DataFrame: {str(e)}")
            return None

    def extract_dataset_multiformat(self, dataset_code: str):
        """
        Extract and save dataset in all formats

        Args:
            dataset_code: Dataset code

        Returns:
            bool: Success status
        """
        info = self.DATASETS.get(dataset_code, {})
        name = info.get('name', dataset_code)
        desc = info.get('description', 'Unknown')

        print(f"\nExtracting {dataset_code}: {name}")
        print(f"  Description: {desc[:80]}")

        # Fetch data from API
        params = info.get('params', {})
        data = self.get_dataset(dataset_code, params)

        if data is None:
            print(f"  Failed to retrieve data")
            self.log.append({
                'code': dataset_code,
                'name': name,
                'status': 'failed',
                'timestamp': datetime.now().isoformat()
            })
            return False

        # Extract metadata
        metadata = {
            'dataset_code': dataset_code,
            'dataset_name': name,
            'description': desc,
            'label': data.get('label', ''),
            'source': data.get('source', 'Eurostat'),
            'updated': data.get('updated', ''),
            'extraction_date': datetime.now().isoformat(),
            'category': info.get('category', ''),
            'use_case': info.get('use_case', '')
        }

        print(f"  Label: {metadata['label'][:80]}")
        print(f"  Updated: {metadata['updated']}")

        # Convert to DataFrame
        df = self.jsonstat_to_dataframe(data)

        if df is None or len(df) == 0:
            print(f"  No records to save")
            return False

        # Remove rows where value is None
        df = df.dropna(subset=['value'])

        # Filter for Portugal only (keep PT, PTxx, PTxxx codes)
        if 'geo' in df.columns:
            before_filter = len(df)
            df = df[df['geo'].str.startswith('PT', na=False)]
            after_filter = len(df)
            if before_filter > after_filter:
                print(f"  Filtered to Portugal: {before_filter:,} -> {after_filter:,} records")

        record_count = len(df)

        if record_count == 0:
            print(f"  No records after filtering for Portugal")
            return False

        print(f"  Processing {record_count} records...")

        # Save in all formats
        formats_saved = []

        # 1. Save original JSON
        try:
            json_file = self.output_dir / 'json' / f'{dataset_code}_{name}.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            formats_saved.append('JSON')
        except Exception as e:
            print(f"  Warning: Failed to save JSON - {str(e)}")

        # 2. Save CSV
        try:
            csv_file = self.output_dir / 'csv' / f'{dataset_code}_{name}.csv'
            df.to_csv(csv_file, index=False, encoding='utf-8-sig', sep=';')
            formats_saved.append('CSV')
        except Exception as e:
            print(f"  Warning: Failed to save CSV - {str(e)}")

        # 3. Save XLSX
        try:
            xlsx_file = self.output_dir / 'xlsx' / f'{dataset_code}_{name}.xlsx'
            df.to_excel(xlsx_file, index=False, engine='openpyxl')
            formats_saved.append('XLSX')
        except Exception as e:
            print(f"  Warning: Failed to save XLSX - {str(e)}")

        # 4. Save Parquet
        try:
            parquet_file = self.output_dir / 'parquet' / f'{dataset_code}_{name}.parquet'
            df.to_parquet(parquet_file, index=False, engine='pyarrow')
            formats_saved.append('Parquet')
        except Exception as e:
            print(f"  Warning: Failed to save Parquet - {str(e)}")

        # Save metadata
        metadata_file = self.output_dir / 'metadata' / f'{dataset_code}_{name}_metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"  Saved {record_count} records in {len(formats_saved)} formats: {', '.join(formats_saved)}")

        self.log.append({
            'code': dataset_code,
            'name': name,
            'status': 'success',
            'records': record_count,
            'formats': formats_saved,
            'timestamp': datetime.now().isoformat()
        })

        return True

    def extract_all(self):
        """Extract all datasets in all formats"""
        print("="*70)
        print("EUROSTAT MULTI-FORMAT DATA EXTRACTION")
        print(f"Datasets to extract: {len(self.DATASETS)}")
        print(f"Formats: {', '.join(self.FORMATS)}")
        print("="*70)

        success_count = 0
        for dataset_code in self.DATASETS.keys():
            success = self.extract_dataset_multiformat(dataset_code)
            if success:
                success_count += 1
            time.sleep(2)  # Rate limiting

        print(f"\n{'='*70}")
        print(f"EXTRACTION COMPLETE")
        print(f"Success: {success_count}/{len(self.DATASETS)}")
        print("="*70)

        # Save log
        log_file = self.output_dir / "extraction_log.json"
        with open(log_file, 'w') as f:
            json.dump(self.log, f, indent=2)

        print(f"\nLog saved to: {log_file}")

        return self.log

    def generate_summary(self):
        """Generate summary of extracted data"""
        summary = []

        for entry in self.log:
            if entry['status'] == 'success':
                code = entry['code']
                info = self.DATASETS.get(code, {})
                summary.append({
                    'code': code,
                    'name': entry['name'],
                    'description': info.get('description', ''),
                    'category': info.get('category', 'Unknown'),
                    'use_case': info.get('use_case', ''),
                    'records': entry.get('records', 0),
                    'formats': ', '.join(entry.get('formats', []))
                })

        if summary:
            df = pd.DataFrame(summary)
            summary_file = self.output_dir / "data_summary.csv"
            df.to_csv(summary_file, index=False, encoding='utf-8-sig')
            print(f"\nSummary saved to: {summary_file}")

            return df

        return None

    def generate_report(self):
        """Generate HTML report"""
        success_count = sum(1 for e in self.log if e['status'] == 'success')
        total_records = sum(e.get('records', 0) for e in self.log if e['status'] == 'success')

        report_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Eurostat Multi-Format Data Extraction Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #003399; }}
        h2 {{ color: #0066cc; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #003399; color: white; }}
        .success {{ color: green; }}
        .failed {{ color: red; }}
        .stat-box {{
            display: inline-block;
            padding: 15px;
            margin: 10px;
            background: #f0f0f0;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <h1>Eurostat Multi-Format Data Extraction Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

    <h2>Summary Statistics</h2>
    <div class="stat-box">
        <strong>Total Datasets:</strong> {len(self.DATASETS)}
    </div>
    <div class="stat-box">
        <strong>Successfully Extracted:</strong> {success_count}
    </div>
    <div class="stat-box">
        <strong>Total Records:</strong> {total_records:,}
    </div>
    <div class="stat-box">
        <strong>Formats:</strong> {len(self.FORMATS)}
    </div>

    <h2>Extraction Details</h2>
    <table>
        <tr>
            <th>Code</th>
            <th>Dataset Name</th>
            <th>Category</th>
            <th>Records</th>
            <th>Formats</th>
            <th>Status</th>
        </tr>
"""

        for entry in self.log:
            code = entry['code']
            info = self.DATASETS.get(code, {})
            status_class = 'success' if entry['status'] == 'success' else 'failed'
            status_text = 'SUCCESS' if entry['status'] == 'success' else 'FAILED'

            report_html += f"""
        <tr>
            <td>{code}</td>
            <td>{entry.get('name', 'Unknown')}</td>
            <td>{info.get('category', 'Unknown')}</td>
            <td>{entry.get('records', 0):,}</td>
            <td>{', '.join(entry.get('formats', []))}</td>
            <td class="{status_class}">{status_text}</td>
        </tr>
"""

        report_html += """
    </table>

    <h2>File Organization</h2>
    <pre>
eurostat_data_multiformat/
├── json/          (JSON-stat format)
├── csv/           (Semicolon-delimited, UTF-8)
├── xlsx/          (Excel format)
├── parquet/       (Columnar format)
└── metadata/      (Dataset metadata)
    </pre>

</body>
</html>
"""

        report_file = self.output_dir / "extraction_report.html"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_html)

        print(f"HTML report saved to: {report_file}")


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("EUROSTAT MULTI-FORMAT DATA EXTRACTOR FOR HEALTHCARE RESEARCH")
    print("="*70 + "\n")

    extractor = EurostatExtractor(output_dir="eurostat_data_multiformat")
    extractor.extract_all()
    summary = extractor.generate_summary()

    if summary is not None:
        print("\n" + "="*70)
        print("DATA SUMMARY")
        print("="*70)
        print(summary.to_string(index=False))

    extractor.generate_report()

    print("\n" + "="*70)
    print("Files saved to: eurostat_data_multiformat/")
    print("Formats: JSON, CSV, XLSX, Parquet")
    print("="*70)


if __name__ == "__main__":
    main()
