#!/usr/bin/env python3
"""
INE (Statistics Portugal) Data Extractor
=========================================
Extracts demographic and economic indicators useful for healthcare research
"""

import requests
import json
import pandas as pd
from pathlib import Path
import time
from datetime import datetime

class INEDataExtractor:
    """
    Extracts data from INE (Instituto Nacional de Estatística) API
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

    def __init__(self, output_dir: str = "ine_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log = []

    def get_indicator(self, code: str, lang: str = "PT"):
        """
        Fetch a single indicator from INE API

        Args:
            code: Indicator code
            lang: Language (PT or EN)

        Returns:
            dict: Indicator data
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

    def extract_indicator_data(self, code: str):
        """
        Extract and save indicator data

        Args:
            code: Indicator code

        Returns:
            bool: Success status
        """
        info = self.INDICATORS.get(code, {})
        print(f"\nExtracting {code}: {info.get('name', 'Unknown')}")

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

        if all_records:
            df = pd.DataFrame(all_records)

            # Save data
            csv_file = self.output_dir / f"ind_{code}.csv"
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')

            # Save metadata
            json_file = self.output_dir / f"ind_{code}_metadata.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            print(f"  Saved {len(df)} records to {csv_file.name}")

            self.log.append({
                'code': code,
                'status': 'success',
                'records': len(df),
                'file': str(csv_file),
                'timestamp': datetime.now().isoformat()
            })

            return True
        else:
            print(f"  No records to save")
            return False

    def extract_all(self):
        """Extract all indicators"""
        print("="*70)
        print("INE DATA EXTRACTION")
        print(f"Indicators to extract: {len(self.INDICATORS)}")
        print("="*70)

        success_count = 0
        for code in self.INDICATORS.keys():
            success = self.extract_indicator_data(code)
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
                    'file': entry.get('file', '')
                })

        if summary:
            df = pd.DataFrame(summary)
            summary_file = self.output_dir / "data_summary.csv"
            df.to_csv(summary_file, index=False)
            print(f"\nSummary saved to: {summary_file}")

            return df

        return None


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("INE DATA EXTRACTOR FOR HEALTHCARE RESEARCH")
    print("="*70 + "\n")

    extractor = INEDataExtractor(output_dir="ine_data")
    extractor.extract_all()
    summary = extractor.generate_summary()

    if summary is not None:
        print("\n" + "="*70)
        print("DATA SUMMARY")
        print("="*70)
        print(summary.to_string(index=False))

    print("\n" + "="*70)
    print("Files saved to: ine_data/")
    print("="*70)


if __name__ == "__main__":
    main()
