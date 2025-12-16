#!/usr/bin/env python3
"""
SNS Transparency Portal Data Downloader
========================================

Purpose: Automated download of Portuguese SNS datasets for financial distress research
Author: Research Assistant
Date: October 25, 2025

Features:
- Downloads 30+ datasets from SNS Transparency Portal
- Organized by research priority (P1, P2, P3)
- Error handling and retry logic
- Progress tracking and logging
- CSV and JSON format support
- Resumable downloads
"""

import requests
import pandas as pd
import os
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sns_download.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class Dataset:
    """Data structure for SNS dataset metadata"""
    dataset_id: str
    name: str
    url: str
    priority: int
    description: str
    importance: int  # 1-5 stars
    update_frequency: str
    phfsi_component: str


class SNSDataDownloader:
    """
    Downloads datasets from Portuguese SNS Transparency Portal
    """
    
    BASE_URL = "https://transparencia.sns.gov.pt/api/explore/v2.1"
    
    # Dataset catalog organized by priority
    DATASETS = [
        # PRIORITY 1: ESSENTIAL FINANCIAL DATA
        Dataset(
            dataset_id="divida-total-vencida-e-pagamentos",
            name="Dívida Total, Vencida e Pagamentos em Atraso",
            url="https://transparencia.sns.gov.pt/explore/dataset/divida-total-vencida-e-pagamentos",
            priority=1,
            description="Total debt, overdue debt, and late payments",
            importance=5,
            update_frequency="Monthly",
            phfsi_component="Stakeholder Pressure Index (SPI)"
        ),
        Dataset(
            dataset_id="agregados-economico-financeiros",
            name="Agregados Económico Financeiros",
            url="https://transparencia.sns.gov.pt/explore/dataset/agregados-economico-financeiros",
            priority=1,
            description="Economic-financial aggregates (revenues, expenses, assets)",
            importance=5,
            update_frequency="Monthly",
            phfsi_component="OSSR, TLR"
        ),
        Dataset(
            dataset_id="tempo-medio-de-pagamento-das-instituicoes-do-sns-a-fornecedores",
            name="Prazo Médio de Pagamento a Fornecedores",
            url="https://transparencia.sns.gov.pt/explore/dataset/tempo-medio-de-pagamento-das-instituicoes-do-sns-a-fornecedores",
            priority=1,
            description="Average payment period to suppliers",
            importance=5,
            update_frequency="Monthly",
            phfsi_component="SPI - Supplier Payment Days"
        ),
        Dataset(
            dataset_id="conta-do-servico-nacional-de-saude",
            name="Conta do Serviço Nacional de Saúde",
            url="https://transparencia.sns.gov.pt/explore/dataset/conta-do-servico-nacional-de-saude",
            priority=1,
            description="Comprehensive SNS financial accounts",
            importance=4,
            update_frequency="Annual",
            phfsi_component="Validation and benchmarking"
        ),
        
        # PRIORITY 2: OPERATIONAL & STAFFING DATA
        Dataset(
            dataset_id="trabalhadores-por-grupo-profissional",
            name="Trabalhadores por Grupo Profissional",
            url="https://transparencia.sns.gov.pt/explore/dataset/trabalhadores-por-grupo-profissional",
            priority=2,
            description="Monthly headcount by professional group",
            importance=4,
            update_frequency="Monthly",
            phfsi_component="SPI - Staff Turnover proxy"
        ),
        Dataset(
            dataset_id="trabalhadores-por-modalidade-de-vinculacao",
            name="Trabalhadores por Modalidade de Vinculação",
            url="https://transparencia.sns.gov.pt/explore/dataset/trabalhadores-por-modalidade-de-vinculacao",
            priority=2,
            description="Headcount by employment type",
            importance=3,
            update_frequency="Monthly",
            phfsi_component="SPI - precarious employment"
        ),
        Dataset(
            dataset_id="contagem-dos-dias-de-ausencia-ao-trabalho-segundo-o-motivo-de-ausencia",
            name="Ausência ao Trabalho por Tipologia",
            url="https://transparencia.sns.gov.pt/explore/dataset/contagem-dos-dias-de-ausencia-ao-trabalho-segundo-o-motivo-de-ausencia",
            priority=2,
            description="Absence days by reason",
            importance=3,
            update_frequency="Monthly",
            phfsi_component="SPI - workforce stress"
        ),
        Dataset(
            dataset_id="percentagem-de-gastos-com-te-e-suplementos-no-total-gastos-com-pessoal",
            name="Gastos com TE e Suplementos",
            url="https://transparencia.sns.gov.pt/explore/dataset/percentagem-de-gastos-com-te-e-suplementos-no-total-gastos-com-pessoal",
            priority=2,
            description="% overtime and supplements in personnel costs",
            importance=3,
            update_frequency="Monthly",
            phfsi_component="OSSR - cost structure"
        ),
        
        # PRIORITY 3: CLINICAL QUALITY & OUTCOMES
        Dataset(
            dataset_id="morbilidade-e-mortalidade-hospitalar",
            name="Morbilidade e Mortalidade Hospitalar",
            url="https://transparencia.sns.gov.pt/explore/dataset/morbilidade-e-mortalidade-hospitalar",
            priority=3,
            description="Inpatient admissions, days, and deaths",
            importance=4,
            update_frequency="Quarterly",
            phfsi_component="CQMI - mortality rate"
        ),
        Dataset(
            dataset_id="morbilidade-e-mortalidade-hospitalar-por-faixa-etaria",
            name="Morbilidade e Mortalidade por Faixa Etária",
            url="https://transparencia.sns.gov.pt/explore/dataset/morbilidade-e-mortalidade-hospitalar-por-faixa-etaria",
            priority=3,
            description="Inpatient data by age group",
            importance=4,
            update_frequency="Quarterly",
            phfsi_component="CQMI - age-adjusted mortality"
        ),
        Dataset(
            dataset_id="taxa-de-mortalidade-por-avc-isquemico-e-hemorragico",
            name="Mortalidade por AVC",
            url="https://transparencia.sns.gov.pt/explore/dataset/taxa-de-mortalidade-por-avc-isquemico-e-hemorragico",
            priority=3,
            description="Stroke mortality rates",
            importance=3,
            update_frequency="Annual",
            phfsi_component="CQMI - condition-specific"
        ),
        Dataset(
            dataset_id="fraturas-da-anca-cirurgias-nas-primeiras-48h",
            name="Fraturas da Anca (48h)",
            url="https://transparencia.sns.gov.pt/explore/dataset/fraturas-da-anca-cirurgias-nas-primeiras-48h",
            priority=3,
            description="Hip fracture surgeries within 48 hours",
            importance=4,
            update_frequency="Monthly",
            phfsi_component="CQMI - process quality"
        ),
        Dataset(
            dataset_id="notificacao-de-incidentes-de-seguranca-em-unidades-prestadoras-de-cuidados-de-sa",
            name="Incidentes de Segurança",
            url="https://transparencia.sns.gov.pt/explore/dataset/notificacao-de-incidentes-de-seguranca-em-unidades-prestadoras-de-cuidados-de-sa",
            priority=3,
            description="Safety incident notifications",
            importance=3,
            update_frequency="Monthly",
            phfsi_component="CQMI - safety"
        ),
    ]
    
    def __init__(self, output_dir: str = "sns_data"):
        """
        Initialize downloader
        
        Args:
            output_dir: Directory to save downloaded files
        """
        self.output_dir = Path(output_dir)
        self.create_directory_structure()
        self.download_log = self.output_dir / "download_log.json"
        self.load_download_log()
        
    def create_directory_structure(self):
        """Create organized directory structure for downloaded data"""
        directories = [
            self.output_dir / "priority_1_essential",
            self.output_dir / "priority_2_operational",
            self.output_dir / "priority_3_quality",
            self.output_dir / "metadata",
            self.output_dir / "logs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Created directory structure in {self.output_dir}")
    
    def load_download_log(self):
        """Load or create download log to track progress"""
        if self.download_log.exists():
            with open(self.download_log, 'r') as f:
                self.log = json.load(f)
            logger.info(f"Loaded existing download log with {len(self.log)} entries")
        else:
            self.log = {}
            logger.info("Created new download log")
    
    def save_download_log(self):
        """Save download log"""
        with open(self.download_log, 'w') as f:
            json.dump(self.log, f, indent=2)
    
    def get_priority_directory(self, priority: int) -> Path:
        """Get directory path for given priority"""
        priority_map = {
            1: "priority_1_essential",
            2: "priority_2_operational",
            3: "priority_3_quality"
        }
        return self.output_dir / priority_map.get(priority, "other")
    
    def download_dataset(self, dataset: Dataset, format: str = "csv", 
                        max_retries: int = 3, rows_per_request: int = 10000) -> bool:
        """
        Download a single dataset from SNS Portal
        
        Args:
            dataset: Dataset object with metadata
            format: Output format ('csv' or 'json')
            max_retries: Maximum number of retry attempts
            rows_per_request: Number of rows to fetch per API call
            
        Returns:
            bool: True if download successful, False otherwise
        """
        # Check if already downloaded
        output_file = self.get_priority_directory(dataset.priority) / f"{dataset.dataset_id}.{format}"
        
        if dataset.dataset_id in self.log and self.log[dataset.dataset_id].get('status') == 'completed':
            logger.info(f"✓ Already downloaded: {dataset.name}")
            return True
        
        logger.info(f"⬇ Downloading {dataset.priority} - {dataset.name}")
        logger.info(f"   Dataset ID: {dataset.dataset_id}")
        
        all_records = []
        offset = 0
        attempt = 0
        
        while attempt < max_retries:
            try:
                # Construct API URL for OpenDataSoft platform
                api_url = f"{self.BASE_URL}/catalog/datasets/{dataset.dataset_id}/exports/{format}"
                
                # Alternative: Use records endpoint for pagination
                records_url = f"{self.BASE_URL}/catalog/datasets/{dataset.dataset_id}/records"
                
                params = {
                    'limit': rows_per_request,
                    'offset': offset,
                    'timezone': 'UTC'
                }
                
                logger.info(f"   Fetching rows {offset} to {offset + rows_per_request}...")
                
                response = requests.get(records_url, params=params, timeout=60)
                response.raise_for_status()
                
                data = response.json()
                records = data.get('records', [])
                
                if not records:
                    logger.info(f"   No more records (total: {len(all_records)})")
                    break
                
                all_records.extend(records)
                offset += len(records)
                
                # Check if we've got all records
                total_count = data.get('total_count', 0)
                if offset >= total_count:
                    logger.info(f"   Retrieved all {len(all_records)} records")
                    break
                
                time.sleep(0.5)  # Rate limiting
                
            except requests.exceptions.RequestException as e:
                attempt += 1
                logger.warning(f"   Attempt {attempt}/{max_retries} failed: {str(e)}")
                
                if attempt < max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"   Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"✗ Failed to download {dataset.name} after {max_retries} attempts")
                    self.log[dataset.dataset_id] = {
                        'status': 'failed',
                        'timestamp': datetime.now().isoformat(),
                        'error': str(e)
                    }
                    self.save_download_log()
                    return False
        
        # Save data
        try:
            if format == 'csv':
                # Extract fields from records
                df = pd.json_normalize([r['fields'] for r in all_records])
                df.to_csv(output_file, index=False, encoding='utf-8')
                logger.info(f"   ✓ Saved {len(df)} rows to {output_file.name}")
                
            elif format == 'json':
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(all_records, f, indent=2, ensure_ascii=False)
                logger.info(f"   ✓ Saved {len(all_records)} records to {output_file.name}")
            
            # Save metadata
            metadata_file = self.output_dir / "metadata" / f"{dataset.dataset_id}_metadata.json"
            metadata = {
                'dataset_id': dataset.dataset_id,
                'name': dataset.name,
                'description': dataset.description,
                'priority': dataset.priority,
                'importance': dataset.importance,
                'update_frequency': dataset.update_frequency,
                'phfsi_component': dataset.phfsi_component,
                'download_timestamp': datetime.now().isoformat(),
                'record_count': len(all_records),
                'url': dataset.url
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            # Update log
            self.log[dataset.dataset_id] = {
                'status': 'completed',
                'timestamp': datetime.now().isoformat(),
                'record_count': len(all_records),
                'file': str(output_file)
            }
            self.save_download_log()
            
            return True
            
        except Exception as e:
            logger.error(f"✗ Error saving {dataset.name}: {str(e)}")
            self.log[dataset.dataset_id] = {
                'status': 'failed',
                'timestamp': datetime.now().isoformat(),
                'error': f"Save error: {str(e)}"
            }
            self.save_download_log()
            return False
    
    def download_all(self, priorities: List[int] = [1, 2, 3], format: str = "csv"):
        """
        Download all datasets for specified priorities
        
        Args:
            priorities: List of priority levels to download (default: all)
            format: Output format ('csv' or 'json')
        """
        logger.info("="*80)
        logger.info("SNS TRANSPARENCY PORTAL DATA DOWNLOAD")
        logger.info(f"Start time: {datetime.now()}")
        logger.info(f"Priorities: {priorities}")
        logger.info(f"Format: {format}")
        logger.info("="*80)
        
        datasets_to_download = [d for d in self.DATASETS if d.priority in priorities]
        
        total = len(datasets_to_download)
        successful = 0
        failed = 0
        skipped = 0
        
        for i, dataset in enumerate(datasets_to_download, 1):
            logger.info(f"\n[{i}/{total}] Priority {dataset.priority} - {dataset.name}")
            logger.info(f"{'⭐' * dataset.importance} ({dataset.importance}/5 importance)")
            
            if dataset.dataset_id in self.log and self.log[dataset.dataset_id].get('status') == 'completed':
                logger.info("Already completed - skipping")
                skipped += 1
                continue
            
            success = self.download_dataset(dataset, format=format)
            
            if success:
                successful += 1
            else:
                failed += 1
            
            # Rate limiting between datasets
            time.sleep(1)
        
        # Summary
        logger.info("\n" + "="*80)
        logger.info("DOWNLOAD SUMMARY")
        logger.info(f"Total datasets: {total}")
        logger.info(f"✓ Successful: {successful}")
        logger.info(f"⊘ Skipped (already downloaded): {skipped}")
        logger.info(f"✗ Failed: {failed}")
        logger.info(f"End time: {datetime.now()}")
        logger.info("="*80)
        
        # Generate download report
        self.generate_report()
    
    def generate_report(self):
        """Generate HTML report of downloaded datasets"""
        report_path = self.output_dir / "download_report.html"
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>SNS Data Download Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #2c3e50; }
                table { border-collapse: collapse; width: 100%; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #3498db; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
                .completed { color: green; font-weight: bold; }
                .failed { color: red; font-weight: bold; }
                .priority-1 { background-color: #e74c3c; color: white; }
                .priority-2 { background-color: #f39c12; color: white; }
                .priority-3 { background-color: #27ae60; color: white; }
            </style>
        </head>
        <body>
            <h1>SNS Transparency Portal Data Download Report</h1>
            <p>Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            
            <h2>Download Status</h2>
            <table>
                <tr>
                    <th>Priority</th>
                    <th>Dataset</th>
                    <th>Status</th>
                    <th>Records</th>
                    <th>Timestamp</th>
                    <th>PHFSI Component</th>
                </tr>
        """
        
        for dataset in sorted(self.DATASETS, key=lambda x: (x.priority, x.name)):
            status = self.log.get(dataset.dataset_id, {})
            status_text = status.get('status', 'not started')
            record_count = status.get('record_count', 0)
            timestamp = status.get('timestamp', '')
            
            status_class = 'completed' if status_text == 'completed' else 'failed'
            priority_class = f'priority-{dataset.priority}'
            
            html += f"""
                <tr>
                    <td class="{priority_class}">P{dataset.priority}</td>
                    <td>{dataset.name}</td>
                    <td class="{status_class}">{status_text}</td>
                    <td>{record_count:,}</td>
                    <td>{timestamp[:19] if timestamp else '-'}</td>
                    <td>{dataset.phfsi_component}</td>
                </tr>
            """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"\n📊 Download report generated: {report_path}")


def main():
    """Main execution function"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     SNS TRANSPARENCY PORTAL DATA DOWNLOADER                  ║
    ║     For Portuguese NHS Financial Distress Research           ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize downloader
    downloader = SNSDataDownloader(output_dir="sns_data")
    
    # Download Priority 1 datasets first (most critical)
    print("\n🎯 Phase 1: Downloading Priority 1 (Essential Financial Data)...")
    downloader.download_all(priorities=[1], format="csv")
    
    # Ask user if they want to continue
    response = input("\n✓ Priority 1 complete. Download Priority 2 & 3? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        print("\n🎯 Phase 2: Downloading Priority 2 (Operational Data)...")
        downloader.download_all(priorities=[2], format="csv")
        
        print("\n🎯 Phase 3: Downloading Priority 3 (Quality Data)...")
        downloader.download_all(priorities=[3], format="csv")
    
    print("\n✅ Download process complete!")
    print(f"📁 Data saved to: {downloader.output_dir.absolute()}")
    print(f"📊 View report: {downloader.output_dir.absolute()}/download_report.html")


if __name__ == "__main__":
    main()
