#!/usr/bin/env python3
"""
SNS Multi-Format Data Downloader
=================================
Downloads data in CSV, XLSX, and JSON formats
Organizes files by format in separate directories
"""

import requests
import pandas as pd
import os
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
import sys
import io

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sns_multiformat_download.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class Dataset:
    dataset_id: str
    name: str
    url: str
    priority: int
    description: str
    importance: int
    update_frequency: str
    phfsi_component: str


class SNSMultiFormatDownloader:
    """Downloads datasets in multiple formats"""

    BASE_URL = "https://transparencia.sns.gov.pt/api/explore/v2.1"

    # Supported formats
    FORMATS = ['csv', 'xlsx', 'json', 'parquet']

    DATASETS = [
        # PRIORITY 1
        Dataset("divida-total-vencida-e-pagamentos", "Divida Total, Vencida e Pagamentos",
                "https://transparencia.sns.gov.pt/explore/dataset/divida-total-vencida-e-pagamentos",
                1, "Total debt, overdue debt, late payments", 5, "Monthly", "SPI"),
        Dataset("agregados-economico-financeiros", "Agregados Economico Financeiros",
                "https://transparencia.sns.gov.pt/explore/dataset/agregados-economico-financeiros",
                1, "Economic-financial aggregates", 5, "Monthly", "OSSR, TLR"),
        Dataset("tempo-medio-de-pagamento-das-instituicoes-do-sns-a-fornecedores", "Prazo Medio de Pagamento",
                "https://transparencia.sns.gov.pt/explore/dataset/tempo-medio-de-pagamento-das-instituicoes-do-sns-a-fornecedores",
                1, "Average payment period to suppliers", 5, "Monthly", "SPI"),
        Dataset("conta-do-servico-nacional-de-saude", "Conta do SNS",
                "https://transparencia.sns.gov.pt/explore/dataset/conta-do-servico-nacional-de-saude",
                1, "Comprehensive SNS financial accounts", 4, "Annual", "Validation"),

        # PRIORITY 2
        Dataset("trabalhadores-por-grupo-profissional", "Trabalhadores por Grupo",
                "https://transparencia.sns.gov.pt/explore/dataset/trabalhadores-por-grupo-profissional",
                2, "Headcount by professional group", 4, "Monthly", "SPI"),
        Dataset("trabalhadores-por-modalidade-de-vinculacao", "Trabalhadores por Modalidade",
                "https://transparencia.sns.gov.pt/explore/dataset/trabalhadores-por-modalidade-de-vinculacao",
                2, "Headcount by employment type", 3, "Monthly", "SPI"),
        Dataset("contagem-dos-dias-de-ausencia-ao-trabalho-segundo-o-motivo-de-ausencia", "Ausencia ao Trabalho",
                "https://transparencia.sns.gov.pt/explore/dataset/contagem-dos-dias-de-ausencia-ao-trabalho-segundo-o-motivo-de-ausencia",
                2, "Absence days by reason", 3, "Monthly", "SPI"),
        Dataset("percentagem-de-gastos-com-te-e-suplementos-no-total-gastos-com-pessoal", "Gastos com TE",
                "https://transparencia.sns.gov.pt/explore/dataset/percentagem-de-gastos-com-te-e-suplementos-no-total-gastos-com-pessoal",
                2, "Overtime percentage", 3, "Monthly", "OSSR"),

        # PRIORITY 3
        Dataset("morbilidade-e-mortalidade-hospitalar", "Morbilidade e Mortalidade",
                "https://transparencia.sns.gov.pt/explore/dataset/morbilidade-e-mortalidade-hospitalar",
                3, "Inpatient admissions, deaths", 4, "Quarterly", "CQMI"),
        Dataset("morbilidade-e-mortalidade-hospitalar-por-faixa-etaria", "Morbilidade por Faixa Etaria",
                "https://transparencia.sns.gov.pt/explore/dataset/morbilidade-e-mortalidade-hospitalar-por-faixa-etaria",
                3, "Inpatient data by age", 4, "Quarterly", "CQMI"),
        Dataset("taxa-de-mortalidade-por-avc-isquemico-e-hemorragico", "Mortalidade por AVC",
                "https://transparencia.sns.gov.pt/explore/dataset/taxa-de-mortalidade-por-avc-isquemico-e-hemorragico",
                3, "Stroke mortality rates", 3, "Annual", "CQMI"),
        Dataset("fraturas-da-anca-cirurgias-nas-primeiras-48h", "Fraturas da Anca",
                "https://transparencia.sns.gov.pt/explore/dataset/fraturas-da-anca-cirurgias-nas-primeiras-48h",
                3, "Hip fracture surgeries <48h", 4, "Monthly", "CQMI"),
        Dataset("notificacao-de-incidentes-de-seguranca-em-unidades-prestadoras-de-cuidados-de-sa", "Incidentes",
                "https://transparencia.sns.gov.pt/explore/dataset/notificacao-de-incidentes-de-seguranca-em-unidades-prestadoras-de-cuidados-de-sa",
                3, "Safety incidents", 3, "Monthly", "CQMI"),
    ]

    def __init__(self, output_dir: str = "sns_data_multiformat"):
        self.output_dir = Path(output_dir)
        self.create_directory_structure()
        self.download_log = self.output_dir / "download_log.json"
        self.load_download_log()

    def create_directory_structure(self):
        """Create directories organized by format and priority"""
        for fmt in self.FORMATS:
            for priority in [1, 2, 3]:
                dir_path = self.output_dir / fmt / f"priority_{priority}"
                dir_path.mkdir(parents=True, exist_ok=True)

        (self.output_dir / "metadata").mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory structure in {self.output_dir}")

    def load_download_log(self):
        if self.download_log.exists():
            with open(self.download_log, 'r') as f:
                self.log = json.load(f)
        else:
            self.log = {}

    def save_download_log(self):
        with open(self.download_log, 'w') as f:
            json.dump(self.log, f, indent=2)

    def download_single_format(self, dataset: Dataset, fmt: str, max_retries: int = 3) -> bool:
        """Download a single dataset in specific format"""

        # Create log key
        log_key = f"{dataset.dataset_id}_{fmt}"

        # Get output path
        output_dir = self.output_dir / fmt / f"priority_{dataset.priority}"
        output_file = output_dir / f"{dataset.dataset_id}.{fmt}"

        # Check if already downloaded
        if log_key in self.log and self.log[log_key].get('status') == 'completed':
            logger.info(f"  {fmt.upper():5} - Already downloaded")
            return True

        # Download
        export_url = f"{self.BASE_URL}/catalog/datasets/{dataset.dataset_id}/exports/{fmt}"
        params = {'limit': -1, 'timezone': 'UTC'}

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"  {fmt.upper():5} - Downloading (attempt {attempt}/{max_retries})...")
                response = requests.get(export_url, params=params, timeout=120)
                response.raise_for_status()

                # Save file
                output_file.write_bytes(response.content)
                size_kb = len(response.content) / 1024

                # Count records
                record_count = 0
                if fmt == 'csv':
                    df = pd.read_csv(io.BytesIO(response.content), sep=';', encoding='utf-8-sig')
                    record_count = len(df)
                elif fmt == 'xlsx':
                    df = pd.read_excel(io.BytesIO(response.content))
                    record_count = len(df)
                elif fmt == 'json':
                    data = json.loads(response.content)
                    record_count = len(data) if isinstance(data, list) else len(data.get('records', []))
                elif fmt == 'parquet':
                    # Parquet record counting would require pyarrow
                    # For now, just mark as downloaded
                    record_count = 0  # Will be counted later if needed

                logger.info(f"  {fmt.upper():5} - OK! {record_count:,} records, {size_kb:.1f} KB")

                # Update log
                self.log[log_key] = {
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat(),
                    'record_count': record_count,
                    'file_size_bytes': len(response.content),
                    'file': str(output_file)
                }
                self.save_download_log()
                return True

            except Exception as e:
                if attempt < max_retries:
                    logger.warning(f"  {fmt.upper():5} - Attempt {attempt} failed, retrying...")
                    time.sleep(2 ** attempt)
                else:
                    logger.error(f"  {fmt.upper():5} - FAILED after {max_retries} attempts: {str(e)[:50]}")
                    self.log[log_key] = {
                        'status': 'failed',
                        'timestamp': datetime.now().isoformat(),
                        'error': str(e)
                    }
                    self.save_download_log()
                    return False
        return False

    def download_dataset_all_formats(self, dataset: Dataset) -> Dict[str, bool]:
        """Download dataset in all available formats"""
        logger.info(f"[P{dataset.priority}] {dataset.name}")

        results = {}
        for fmt in self.FORMATS:
            success = self.download_single_format(dataset, fmt)
            results[fmt] = success
            time.sleep(0.5)  # Small delay between formats

        return results

    def download_all(self, priorities: List[int] = [1, 2, 3]):
        """Download all datasets in all formats"""
        logger.info("="*80)
        logger.info("SNS MULTI-FORMAT DATA DOWNLOAD")
        logger.info(f"Formats: {', '.join(self.FORMATS)}")
        logger.info(f"Priorities: {priorities}")
        logger.info("="*80)

        datasets = [d for d in self.DATASETS if d.priority in priorities]

        stats = {fmt: {'success': 0, 'failed': 0, 'skipped': 0} for fmt in self.FORMATS}

        for i, dataset in enumerate(datasets, 1):
            logger.info(f"\n[{i}/{len(datasets)}] Starting download...")
            results = self.download_dataset_all_formats(dataset)

            for fmt, success in results.items():
                if success:
                    log_key = f"{dataset.dataset_id}_{fmt}"
                    if self.log[log_key]['status'] == 'completed':
                        if self.log[log_key].get('record_count', 0) > 0:
                            stats[fmt]['success'] += 1
                        else:
                            stats[fmt]['skipped'] += 1
                else:
                    stats[fmt]['failed'] += 1

            time.sleep(1)  # Delay between datasets

        # Summary
        logger.info("\n" + "="*80)
        logger.info("DOWNLOAD SUMMARY")
        for fmt in self.FORMATS:
            logger.info(f"{fmt.upper():5} - Success: {stats[fmt]['success']}, Skipped: {stats[fmt]['skipped']}, Failed: {stats[fmt]['failed']}")
        logger.info("="*80)

        self.generate_report()

    def generate_report(self):
        """Generate HTML report"""
        report_path = self.output_dir / "download_report.html"

        html = f"""<!DOCTYPE html>
<html>
<head>
<title>SNS Multi-Format Download Report</title>
<style>
body {{ font-family: Arial; margin: 20px; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background-color: #3498db; color: white; }}
.ok {{ color: green; font-weight: bold; }}
.fail {{ color: red; }}
</style>
</head>
<body>
<h1>SNS Multi-Format Download Report</h1>
<p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
<table>
<tr><th>Dataset</th><th>CSV</th><th>XLSX</th><th>JSON</th><th>Parquet</th></tr>
"""
        for ds in sorted(self.DATASETS, key=lambda x: (x.priority, x.name)):
            html += f"<tr><td>{ds.name}</td>"
            for fmt in self.FORMATS:
                log_key = f"{ds.dataset_id}_{fmt}"
                status = self.log.get(log_key, {})
                if status.get('status') == 'completed':
                    count = status.get('record_count', 0)
                    html += f'<td class="ok">OK ({count:,})</td>'
                else:
                    html += f'<td class="fail">Failed</td>'
            html += "</tr>\n"

        html += "</table></body></html>"

        with open(report_path, 'w') as f:
            f.write(html)
        logger.info(f"\nReport: {report_path}")


def main():
    print("\n" + "="*70)
    print("SNS MULTI-FORMAT DATA DOWNLOADER")
    print("Downloads: CSV, XLSX, JSON")
    print("="*70 + "\n")

    downloader = SNSMultiFormatDownloader()
    downloader.download_all(priorities=[1, 2, 3])

    print(f"\nData saved to: {downloader.output_dir.absolute()}")


if __name__ == "__main__":
    main()
