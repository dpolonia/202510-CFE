#!/usr/bin/env python3
"""
SNS Data Validator
==================

Validates downloaded SNS datasets for completeness and quality.
Run after downloading to check data integrity.

Usage: python validate_sns_data.py [data_directory]
"""

import pandas as pd
import sys
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class SNSDataValidator:
    """Validates SNS Portal datasets"""
    
    # Expected columns for key datasets
    EXPECTED_COLUMNS = {
        'divida-total-vencida-e-pagamentos': [
            'instituicao', 'data', 'divida_total', 'divida_vencida', 'pagamentos_atraso'
        ],
        'agregados-economico-financeiros': [
            'instituicao', 'data', 'receitas_totais', 'despesas_totais', 
            'ativo_total', 'passivo_total'
        ],
        'tempo-medio-de-pagamento': [
            'instituicao', 'data', 'prazo_medio_pagamento'
        ]
    }
    
    # Expected date ranges (adjust based on actual data availability)
    EXPECTED_START_YEAR = 2017
    EXPECTED_END_YEAR = 2024
    
    def __init__(self, data_dir: str):
        """Initialize validator"""
        self.data_dir = Path(data_dir)
        self.results = []
        
    def validate_file_exists(self, filepath: Path) -> dict:
        """Check if file exists and is readable"""
        result = {
            'file': filepath.name,
            'exists': filepath.exists(),
            'size_mb': 0,
            'readable': False,
            'error': None
        }
        
        if result['exists']:
            try:
                result['size_mb'] = round(filepath.stat().st_size / (1024 * 1024), 2)
                
                # Try to read first few rows
                df = pd.read_csv(filepath, nrows=5)
                result['readable'] = True
                result['columns'] = list(df.columns)
                
            except Exception as e:
                result['error'] = str(e)
        
        return result
    
    def validate_dataset(self, filepath: Path) -> dict:
        """Comprehensive validation of a dataset"""
        logger.info(f"\n📋 Validating: {filepath.name}")
        
        result = {
            'file': filepath.name,
            'status': 'PASS',
            'warnings': [],
            'errors': [],
            'stats': {}
        }
        
        try:
            # Read dataset
            df = pd.read_csv(filepath)
            
            # Basic stats
            result['stats']['rows'] = len(df)
            result['stats']['columns'] = len(df.columns)
            result['stats']['size_mb'] = round(filepath.stat().st_size / (1024 * 1024), 2)
            
            logger.info(f"   Rows: {result['stats']['rows']:,}")
            logger.info(f"   Columns: {result['stats']['columns']}")
            logger.info(f"   Size: {result['stats']['size_mb']} MB")
            
            # Check for empty dataset
            if len(df) == 0:
                result['errors'].append("Dataset is empty (0 rows)")
                result['status'] = 'FAIL'
                return result
            
            # Check for date column (most datasets have this)
            date_cols = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower()]
            
            if date_cols:
                date_col = date_cols[0]
                result['stats']['date_column'] = date_col
                
                try:
                    # Try to parse dates
                    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                    
                    valid_dates = df[date_col].dropna()
                    
                    if len(valid_dates) > 0:
                        min_date = valid_dates.min()
                        max_date = valid_dates.max()
                        
                        result['stats']['date_range'] = f"{min_date.strftime('%Y-%m')} to {max_date.strftime('%Y-%m')}"
                        result['stats']['min_year'] = min_date.year
                        result['stats']['max_year'] = max_date.year
                        
                        logger.info(f"   Date range: {result['stats']['date_range']}")
                        
                        # Check if date range is reasonable
                        if min_date.year < self.EXPECTED_START_YEAR:
                            result['warnings'].append(f"Data starts before {self.EXPECTED_START_YEAR}")
                        
                        if max_date.year < self.EXPECTED_END_YEAR - 1:
                            result['warnings'].append(f"Data may not include recent years (latest: {max_date.year})")
                    
                    else:
                        result['warnings'].append("No valid dates found in date column")
                        
                except Exception as e:
                    result['warnings'].append(f"Could not parse date column: {str(e)}")
            
            # Check for institution column
            inst_cols = [col for col in df.columns if 'instituicao' in col.lower() or 'institution' in col.lower()]
            
            if inst_cols:
                inst_col = inst_cols[0]
                unique_institutions = df[inst_col].nunique()
                result['stats']['institutions'] = unique_institutions
                logger.info(f"   Institutions: {unique_institutions}")
                
                if unique_institutions < 10:
                    result['warnings'].append(f"Only {unique_institutions} institutions (expected 100+)")
            
            # Check for missing values
            missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
            high_missing = missing_pct[missing_pct > 50]
            
            if len(high_missing) > 0:
                result['warnings'].append(f"{len(high_missing)} columns with >50% missing data")
                result['stats']['high_missing_cols'] = list(high_missing.index)
            
            # Check for duplicates
            if date_cols and inst_cols:
                key_cols = [date_cols[0], inst_cols[0]]
                duplicates = df.duplicated(subset=key_cols).sum()
                
                if duplicates > 0:
                    result['warnings'].append(f"{duplicates} duplicate rows found")
                    result['stats']['duplicates'] = duplicates
            
            # Determine overall status
            if result['errors']:
                result['status'] = 'FAIL'
            elif result['warnings']:
                result['status'] = 'WARNING'
            else:
                result['status'] = 'PASS'
            
            # Print status
            status_symbol = {
                'PASS': '✅',
                'WARNING': '⚠️',
                'FAIL': '❌'
            }
            logger.info(f"   Status: {status_symbol[result['status']]} {result['status']}")
            
            if result['warnings']:
                for warning in result['warnings']:
                    logger.info(f"   ⚠️  {warning}")
            
            if result['errors']:
                for error in result['errors']:
                    logger.info(f"   ❌ {error}")
        
        except Exception as e:
            result['status'] = 'ERROR'
            result['errors'].append(f"Validation error: {str(e)}")
            logger.error(f"   ❌ ERROR: {str(e)}")
        
        return result
    
    def validate_all(self) -> dict:
        """Validate all datasets in directory"""
        logger.info("="*70)
        logger.info("SNS DATA VALIDATION")
        logger.info(f"Directory: {self.data_dir.absolute()}")
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*70)
        
        # Find all CSV files
        csv_files = list(self.data_dir.rglob("*.csv"))
        
        if not csv_files:
            logger.error(f"\n❌ No CSV files found in {self.data_dir}")
            return {'total': 0, 'pass': 0, 'warning': 0, 'fail': 0, 'error': 0}
        
        logger.info(f"\nFound {len(csv_files)} CSV files\n")
        
        # Validate each file
        results = []
        for filepath in csv_files:
            result = self.validate_dataset(filepath)
            results.append(result)
        
        # Summary statistics
        summary = {
            'total': len(results),
            'pass': sum(1 for r in results if r['status'] == 'PASS'),
            'warning': sum(1 for r in results if r['status'] == 'WARNING'),
            'fail': sum(1 for r in results if r['status'] == 'FAIL'),
            'error': sum(1 for r in results if r['status'] == 'ERROR')
        }
        
        # Print summary
        logger.info("\n" + "="*70)
        logger.info("VALIDATION SUMMARY")
        logger.info("="*70)
        logger.info(f"Total files: {summary['total']}")
        logger.info(f"✅ Pass: {summary['pass']}")
        logger.info(f"⚠️  Warning: {summary['warning']}")
        logger.info(f"❌ Fail: {summary['fail']}")
        logger.info(f"🔥 Error: {summary['error']}")
        
        # List problematic files
        if summary['fail'] > 0 or summary['error'] > 0:
            logger.info("\n⚠️  Files needing attention:")
            for r in results:
                if r['status'] in ['FAIL', 'ERROR']:
                    logger.info(f"   - {r['file']}: {r['status']}")
                    for error in r.get('errors', []):
                        logger.info(f"     ❌ {error}")
        
        # Generate report
        self.generate_html_report(results, summary)
        
        return summary
    
    def generate_html_report(self, results: list, summary: dict):
        """Generate HTML validation report"""
        report_path = self.data_dir / "validation_report.html"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SNS Data Validation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2c3e50; }}
                .summary {{ 
                    background: #ecf0f1; 
                    padding: 20px; 
                    border-radius: 5px; 
                    margin: 20px 0; 
                }}
                .summary-item {{ 
                    display: inline-block; 
                    margin: 10px 20px; 
                    font-size: 18px; 
                }}
                table {{ 
                    border-collapse: collapse; 
                    width: 100%; 
                    margin-top: 20px; 
                }}
                th, td {{ 
                    border: 1px solid #ddd; 
                    padding: 12px; 
                    text-align: left; 
                }}
                th {{ 
                    background-color: #3498db; 
                    color: white; 
                }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .pass {{ color: green; font-weight: bold; }}
                .warning {{ color: orange; font-weight: bold; }}
                .fail {{ color: red; font-weight: bold; }}
                .error {{ color: darkred; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>SNS Data Validation Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <div class="summary">
                <h2>Summary</h2>
                <span class="summary-item">📊 Total: {summary['total']}</span>
                <span class="summary-item">✅ Pass: {summary['pass']}</span>
                <span class="summary-item">⚠️ Warning: {summary['warning']}</span>
                <span class="summary-item">❌ Fail: {summary['fail']}</span>
                <span class="summary-item">🔥 Error: {summary['error']}</span>
            </div>
            
            <h2>Detailed Results</h2>
            <table>
                <tr>
                    <th>File</th>
                    <th>Status</th>
                    <th>Rows</th>
                    <th>Columns</th>
                    <th>Size (MB)</th>
                    <th>Date Range</th>
                    <th>Institutions</th>
                    <th>Issues</th>
                </tr>
        """
        
        for r in results:
            status_class = r['status'].lower()
            stats = r.get('stats', {})
            
            issues = []
            if r.get('warnings'):
                issues.extend(r['warnings'])
            if r.get('errors'):
                issues.extend(r['errors'])
            
            issues_text = '<br>'.join(issues) if issues else '-'
            
            html += f"""
                <tr>
                    <td>{r['file']}</td>
                    <td class="{status_class}">{r['status']}</td>
                    <td>{stats.get('rows', 0):,}</td>
                    <td>{stats.get('columns', 0)}</td>
                    <td>{stats.get('size_mb', 0)}</td>
                    <td>{stats.get('date_range', '-')}</td>
                    <td>{stats.get('institutions', '-')}</td>
                    <td>{issues_text}</td>
                </tr>
            """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"\n📊 Validation report saved: {report_path}")


def main():
    """Main execution"""
    # Get data directory from command line or use default
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    else:
        data_dir = "sns_data"
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           SNS DATA VALIDATOR                                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    validator = SNSDataValidator(data_dir)
    summary = validator.validate_all()
    
    # Exit code based on results
    if summary['fail'] > 0 or summary['error'] > 0:
        print("\n⚠️  Validation completed with errors. Check validation_report.html for details.")
        sys.exit(1)
    elif summary['warning'] > 0:
        print("\n✅ Validation completed with warnings. Check validation_report.html for details.")
        sys.exit(0)
    else:
        print("\n✅ All datasets validated successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
