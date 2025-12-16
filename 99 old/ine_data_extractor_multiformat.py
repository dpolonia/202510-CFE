#!/usr/bin/env python3
"""
INE (Statistics Portugal) Multi-Format Data Extractor
======================================================
Extracts demographic and economic indicators in multiple formats:
- JSON (original API response)
- CSV (semicolon-delimited, UTF-8)
- XLSX (Excel format)
- Parquet (columnar format)
"""

import requests
import json
import pandas as pd
from pathlib import Path
import time
from datetime import datetime

class INEMultiFormatExtractor:
    """
    Extracts data from INE API and saves in multiple formats
    """

    BASE_URL = "https://www.ine.pt/ine/json_indicador/pindica.jsp"

    # Relevant indicators for healthcare research - CORRECTED CODES
    INDICATORS = {
        # Population and Demographics - VERIFIED CORRECT
        '0008273': {
            'name': 'Population by region, sex and age group',
            'category': 'Demographics',
            'use_case': 'Case-mix adjustment, demand forecasting'
        },
        '0008274': {
            'name': 'Fertility index',
            'category': 'Demographics',
            'use_case': 'Birth rate trends'
        },
        '0008275': {
            'name': 'Adolescent fertility rate',
            'category': 'Demographics',
            'use_case': 'Maternal health services demand'
        },

        # Aging and Dependency Indices - CORRECTED CODES
        '0008258': {
            'name': 'Aging index by region (Indice de envelhecimento)',
            'category': 'Demographics',
            'use_case': 'Elderly population trends'
        },
        '0008259': {
            'name': 'Elderly dependency index',
            'category': 'Demographics',
            'use_case': 'Healthcare demand from aging population'
        },
        '0008261': {
            'name': 'Total dependency ratio',
            'category': 'Demographics',
            'use_case': 'Healthcare demand pressure'
        },

        # Economic Indicators - CORRECTED CODES
        '0012136': {
            'name': 'Unemployment rate by region',
            'category': 'Economics',
            'use_case': 'Economic distress indicator'
        },
        '0010683': {
            'name': 'Employment statistics',
            'category': 'Economics',
            'use_case': 'Regional employment context'
        },

        # Healthcare-Related Indicators - BONUS
        '0008277': {
            'name': 'Nurses per 1000 inhabitants',
            'category': 'Healthcare',
            'use_case': 'Healthcare workforce availability'
        },
        '0001228': {
            'name': 'Life expectancy at 65 years',
            'category': 'Demographics',
            'use_case': 'Population health outcomes'
        },
    }

    FORMATS = ['json', 'csv', 'xlsx', 'parquet']

    def __init__(self, output_dir: str = "ine_data_multiformat"):
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

    def get_indicator(self, code: str, lang: str = "PT"):
        """
        Fetch a single indicator from INE API

        Args:
            code: Indicator code
            lang: Language (PT or EN)

        Returns:
            dict: Indicator data (original JSON response)
        """
        url = f"{self.BASE_URL}?op=2&varcd={code}&lang={lang}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            if isinstance(data, list) and len(data) > 0:
                return data[0]
            else:
                return None

        except Exception as e:
            print(f"Error fetching indicator {code}: {str(e)}")
            return None

    def extract_indicator_multiformat(self, code: str):
        """
        Extract and save indicator data in all formats

        Args:
            code: Indicator code

        Returns:
            bool: Success status
        """
        info = self.INDICATORS.get(code, {})
        print(f"\nExtracting {code}: {info.get('name', 'Unknown')}")

        # Fetch data from API
        data = self.get_indicator(code)

        if data is None:
            print(f"  Failed to retrieve data")
            self.log.append({
                'code': code,
                'status': 'failed',
                'timestamp': datetime.now().isoformat()
            })
            return False

        # Extract metadata
        metadata = {
            'indicator_code': code,
            'indicator_name': data.get('IndicadorDsg', ''),
            'last_update': data.get('DataUltimoAtualizacao', ''),
            'last_period': data.get('UltimoPref', ''),
            'metadata_url': data.get('MetaInfUrl', ''),
            'extraction_date': datetime.now().isoformat(),
            'category': info.get('category', ''),
            'use_case': info.get('use_case', '')
        }

        print(f"  Name: {metadata['indicator_name'][:80]}")
        print(f"  Last update: {metadata['last_update']}")
        print(f"  Last period: {metadata['last_period']}")

        # Extract data points
        dados = data.get('Dados', {})

        if not dados:
            print(f"  No data points available")
            return False

        # Convert to DataFrame
        all_records = []
        for period, records in dados.items():
            for record in records:
                record['periodo'] = period
                all_records.append(record)

        if not all_records:
            print(f"  No records to save")
            return False

        df = pd.DataFrame(all_records)
        record_count = len(df)

        print(f"  Processing {record_count} records...")

        # Save in all formats
        formats_saved = []

        # 1. Save original JSON
        try:
            json_file = self.output_dir / 'json' / f'ind_{code}.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            formats_saved.append('JSON')
        except Exception as e:
            print(f"  Warning: Failed to save JSON - {str(e)}")

        # 2. Save CSV
        try:
            csv_file = self.output_dir / 'csv' / f'ind_{code}.csv'
            df.to_csv(csv_file, index=False, encoding='utf-8-sig', sep=';')
            formats_saved.append('CSV')
        except Exception as e:
            print(f"  Warning: Failed to save CSV - {str(e)}")

        # 3. Save XLSX
        try:
            xlsx_file = self.output_dir / 'xlsx' / f'ind_{code}.xlsx'
            df.to_excel(xlsx_file, index=False, engine='openpyxl')
            formats_saved.append('XLSX')
        except Exception as e:
            print(f"  Warning: Failed to save XLSX - {str(e)}")

        # 4. Save Parquet
        try:
            parquet_file = self.output_dir / 'parquet' / f'ind_{code}.parquet'
            df.to_parquet(parquet_file, index=False, engine='pyarrow')
            formats_saved.append('Parquet')
        except Exception as e:
            print(f"  Warning: Failed to save Parquet - {str(e)}")

        # Save metadata
        metadata_file = self.output_dir / 'metadata' / f'ind_{code}_metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"  Saved {record_count} records in {len(formats_saved)} formats: {', '.join(formats_saved)}")

        self.log.append({
            'code': code,
            'status': 'success',
            'records': record_count,
            'formats': formats_saved,
            'timestamp': datetime.now().isoformat()
        })

        return True

    def extract_all(self):
        """Extract all indicators in all formats"""
        print("="*70)
        print("INE MULTI-FORMAT DATA EXTRACTION")
        print(f"Indicators to extract: {len(self.INDICATORS)}")
        print(f"Formats: {', '.join(self.FORMATS)}")
        print("="*70)

        success_count = 0
        for code in self.INDICATORS.keys():
            success = self.extract_indicator_multiformat(code)
            if success:
                success_count += 1
            time.sleep(1)  # Rate limiting

        print(f"\n{'='*70}")
        print(f"EXTRACTION COMPLETE")
        print(f"Success: {success_count}/{len(self.INDICATORS)}")
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
                info = self.INDICATORS.get(code, {})
                summary.append({
                    'code': code,
                    'name': info.get('name', 'Unknown'),
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
        report_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>INE Multi-Format Data Extraction Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #003366; }}
        h2 {{ color: #0066cc; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #0066cc; color: white; }}
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
    <h1>INE Multi-Format Data Extraction Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

    <h2>Summary Statistics</h2>
    <div class="stat-box">
        <strong>Total Indicators:</strong> {len(self.INDICATORS)}
    </div>
    <div class="stat-box">
        <strong>Successfully Extracted:</strong> {sum(1 for e in self.log if e['status'] == 'success')}
    </div>
    <div class="stat-box">
        <strong>Total Records:</strong> {sum(e.get('records', 0) for e in self.log if e['status'] == 'success')}
    </div>
    <div class="stat-box">
        <strong>Formats:</strong> {len(self.FORMATS)}
    </div>

    <h2>Extraction Details</h2>
    <table>
        <tr>
            <th>Code</th>
            <th>Indicator Name</th>
            <th>Category</th>
            <th>Records</th>
            <th>Formats</th>
            <th>Status</th>
        </tr>
"""

        for entry in self.log:
            code = entry['code']
            info = self.INDICATORS.get(code, {})
            status_class = 'success' if entry['status'] == 'success' else 'failed'
            status_text = 'SUCCESS' if entry['status'] == 'success' else 'FAILED'

            report_html += f"""
        <tr>
            <td>{code}</td>
            <td>{info.get('name', 'Unknown')}</td>
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
ine_data_multiformat/
├── json/          (Original API responses)
├── csv/           (Semicolon-delimited, UTF-8)
├── xlsx/          (Excel format)
├── parquet/       (Columnar format)
└── metadata/      (Indicator metadata)
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
    print("INE MULTI-FORMAT DATA EXTRACTOR FOR HEALTHCARE RESEARCH")
    print("="*70 + "\n")

    extractor = INEMultiFormatExtractor(output_dir="ine_data_multiformat")
    extractor.extract_all()
    summary = extractor.generate_summary()

    if summary is not None:
        print("\n" + "="*70)
        print("DATA SUMMARY")
        print("="*70)
        print(summary.to_string(index=False))

    extractor.generate_report()

    print("\n" + "="*70)
    print("Files saved to: ine_data_multiformat/")
    print("Formats: JSON, CSV, XLSX, Parquet")
    print("="*70)


if __name__ == "__main__":
    main()
