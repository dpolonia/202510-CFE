#!/usr/bin/env python3
"""
SNS Data Downloader - Simple Version
====================================

Simplified backup script using direct CSV export URLs.
Use this if the main API-based downloader encounters issues.

Usage: python sns_data_downloader_simple.py
"""

import requests
import time
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


# Priority 1: Essential Financial Data (Download These First)
PRIORITY_1 = [
    {
        'name': 'Divida_Total_Vencida_Pagamentos',
        'url': 'https://transparencia.sns.gov.pt/api/explore/v2.1/catalog/datasets/divida-total-vencida-e-pagamentos/exports/csv',
        'description': 'Total debt, overdue debt, late payments'
    },
    {
        'name': 'Agregados_Economico_Financeiros',
        'url': 'https://transparencia.sns.gov.pt/api/explore/v2.1/catalog/datasets/agregados-economico-financeiros/exports/csv',
        'description': 'Revenues, expenses, assets, liabilities'
    },
    {
        'name': 'Prazo_Medio_Pagamento',
        'url': 'https://transparencia.sns.gov.pt/api/explore/v2.1/catalog/datasets/tempo-medio-de-pagamento-das-instituicoes-do-sns-a-fornecedores/exports/csv',
        'description': 'Average payment days to suppliers'
    },
    {
        'name': 'Conta_SNS',
        'url': 'https://transparencia.sns.gov.pt/api/explore/v2.1/catalog/datasets/conta-do-servico-nacional-de-saude/exports/csv',
        'description': 'SNS financial accounts'
    }
]

# Priority 2: Operational Data
PRIORITY_2 = [
    {
        'name': 'Trabalhadores_Grupo_Profissional',
        'url': 'https://transparencia.sns.gov.pt/api/explore/v2.1/catalog/datasets/trabalhadores-por-grupo-profissional/exports/csv',
        'description': 'Headcount by professional group'
    },
    {
        'name': 'Trabalhadores_Modalidade_Vinculacao',
        'url': 'https://transparencia.sns.gov.pt/api/explore/v2.1/catalog/datasets/trabalhadores-por-modalidade-de-vinculacao/exports/csv',
        'description': 'Headcount by employment type'
    },
    {
        'name': 'Ausencia_Trabalho',
        'url': 'https://transparencia.sns.gov.pt/api/explore/v2.1/catalog/datasets/contagem-dos-dias-de-ausencia-ao-trabalho-segundo-o-motivo-de-ausencia/exports/csv',
        'description': 'Absence days by reason'
    },
    {
        'name': 'Gastos_TE_Suplementos',
        'url': 'https://transparencia.sns.gov.pt/api/explore/v2.1/catalog/datasets/percentagem-de-gastos-com-te-e-suplementos-no-total-gastos-com-pessoal/exports/csv',
        'description': 'Overtime costs percentage'
    }
]

# Priority 3: Clinical Quality Data
PRIORITY_3 = [
    {
        'name': 'Morbilidade_Mortalidade_Hospitalar',
        'url': 'https://transparencia.sns.gov.pt/api/explore/v2.1/catalog/datasets/morbilidade-e-mortalidade-hospitalar/exports/csv',
        'description': 'Admissions, days, deaths'
    },
    {
        'name': 'Morbilidade_Faixa_Etaria',
        'url': 'https://transparencia.sns.gov.pt/api/explore/v2.1/catalog/datasets/morbilidade-e-mortalidade-hospitalar-por-faixa-etaria/exports/csv',
        'description': 'Inpatient data by age'
    },
    {
        'name': 'Mortalidade_AVC',
        'url': 'https://transparencia.sns.gov.pt/api/explore/v2.1/catalog/datasets/taxa-de-mortalidade-por-avc-isquemico-e-hemorragico/exports/csv',
        'description': 'Stroke mortality rates'
    },
    {
        'name': 'Fraturas_Anca_48h',
        'url': 'https://transparencia.sns.gov.pt/api/explore/v2.1/catalog/datasets/fraturas-da-anca-cirurgias-nas-primeiras-48h/exports/csv',
        'description': 'Hip fractures surgery timing'
    }
]


def download_file(name, url, output_dir, max_retries=3):
    """Download a single file with retry logic"""
    output_path = output_dir / f"{name}.csv"
    
    if output_path.exists():
        logger.info(f"✓ Already exists: {name}")
        return True
    
    logger.info(f"⬇ Downloading: {name}")
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=120, stream=True)
            response.raise_for_status()
            
            # Save file
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = output_path.stat().st_size / (1024 * 1024)  # MB
            logger.info(f"  ✓ Saved {name}.csv ({file_size:.2f} MB)")
            return True
            
        except Exception as e:
            attempt += 1
            logger.warning(f"  Attempt {attempt}/{max_retries} failed: {str(e)}")
            
            if attempt < max_retries:
                wait_time = 2 ** attempt
                logger.info(f"  Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error(f"  ✗ Failed after {max_retries} attempts")
                return False


def download_priority(datasets, priority_num, base_dir):
    """Download all datasets for a given priority"""
    logger.info(f"\n{'='*70}")
    logger.info(f"PRIORITY {priority_num} DATASETS")
    logger.info(f"{'='*70}")
    
    output_dir = base_dir / f"priority_{priority_num}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    total = len(datasets)
    successful = 0
    
    for i, dataset in enumerate(datasets, 1):
        logger.info(f"\n[{i}/{total}] {dataset['description']}")
        
        if download_file(dataset['name'], dataset['url'], output_dir):
            successful += 1
        
        time.sleep(2)  # Rate limiting
    
    logger.info(f"\n✓ Priority {priority_num}: {successful}/{total} successful")
    return successful


def main():
    """Main execution"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   SNS DATA DOWNLOADER - SIMPLE VERSION                      ║
    ║   Direct CSV Export Downloads                                ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    base_dir = Path("sns_data_simple")
    base_dir.mkdir(exist_ok=True)
    
    start_time = datetime.now()
    logger.info(f"Start time: {start_time}")
    logger.info(f"Output directory: {base_dir.absolute()}\n")
    
    # Download Priority 1 (Essential)
    p1_success = download_priority(PRIORITY_1, 1, base_dir)
    
    # Ask before continuing
    if p1_success > 0:
        response = input("\n✓ Priority 1 complete. Continue with Priority 2 & 3? (y/n): ")
        
        if response.lower() in ['y', 'yes']:
            # Download Priority 2 (Operational)
            p2_success = download_priority(PRIORITY_2, 2, base_dir)
            
            # Download Priority 3 (Quality)
            p3_success = download_priority(PRIORITY_3, 3, base_dir)
            
            total_success = p1_success + p2_success + p3_success
            total_datasets = len(PRIORITY_1) + len(PRIORITY_2) + len(PRIORITY_3)
        else:
            total_success = p1_success
            total_datasets = len(PRIORITY_1)
    else:
        logger.error("No Priority 1 datasets downloaded successfully. Stopping.")
        return
    
    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() / 60
    
    logger.info(f"\n{'='*70}")
    logger.info("DOWNLOAD COMPLETE")
    logger.info(f"{'='*70}")
    logger.info(f"Total successful: {total_success}/{total_datasets}")
    logger.info(f"Duration: {duration:.1f} minutes")
    logger.info(f"Output: {base_dir.absolute()}")
    logger.info(f"End time: {end_time}")
    
    print(f"\n✅ Download complete! Data saved to: {base_dir.absolute()}")


if __name__ == "__main__":
    main()
