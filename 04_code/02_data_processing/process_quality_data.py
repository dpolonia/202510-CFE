"""
Process Quality Data for PHFSI Analysis

Extract and process hospital quality metrics (mortality, readmissions, complications)
to support CQMI component and Granger causality tests.

Input:
- Raw SNS quality data from priority_3 folder

Output:
- Processed quality metrics: 03_data/processed/quality/quality_metrics.parquet

Author: Research Team
Date: 2025-12-31
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_RAW = PROJECT_ROOT / "03_data" / "raw" / "sns" / "combined" / "parquet" / "priority_3"
OUTPUT_DIR = PROJECT_ROOT / "03_data" / "processed" / "quality"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def process_mortality_data():
    """Process hospital morbidity and mortality data."""
    logger.info("Processing mortality data...")

    mortality_file = DATA_RAW / "morbilidade-e-mortalidade-hospitalar.parquet"

    if not mortality_file.exists():
        logger.warning(f"Mortality file not found: {mortality_file}")
        return None

    df = pd.read_parquet(mortality_file)
    logger.info(f"Loaded mortality data: {len(df)} rows, {len(df.columns)} columns")

    # Display column names to understand structure
    logger.info(f"Columns: {df.columns.tolist()}")

    # Standardize dates
    date_cols = [c for c in df.columns if any(x in c.lower() for x in ['data', 'date', 'periodo', 'ano', 'tempo'])]
    if date_cols:
        date_col = date_cols[0]
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['year_month'] = df[date_col].dt.to_period('M')

    # Filter to 2017-2024
    if 'year' in df.columns:
        df = df[(df['year'] >= 2017) & (df['year'] <= 2024)]
        logger.info(f"Filtered to 2017-2024: {len(df)} rows")

    return df


def process_stroke_mortality():
    """Process stroke mortality rates."""
    logger.info("Processing stroke mortality data...")

    stroke_file = DATA_RAW / "taxa-de-mortalidade-por-avc-isquemico-e-hemorragico.parquet"

    if not stroke_file.exists():
        logger.warning(f"Stroke mortality file not found: {stroke_file}")
        return None

    df = pd.read_parquet(stroke_file)
    logger.info(f"Loaded stroke mortality data: {len(df)} rows, {len(df.columns)} columns")
    logger.info(f"Columns: {df.columns.tolist()}")

    # Standardize dates
    date_cols = [c for c in df.columns if any(x in c.lower() for x in ['data', 'date', 'periodo', 'ano'])]
    if date_cols:
        date_col = date_cols[0]
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['year_month'] = df[date_col].dt.to_period('M')

    if 'year' in df.columns:
        df = df[(df['year'] >= 2017) & (df['year'] <= 2024)]

    return df


def consolidate_quality_metrics():
    """Consolidate all quality metrics into single dataset."""
    logger.info("Consolidating quality metrics...")

    mortality = process_mortality_data()
    stroke = process_stroke_mortality()

    datasets = []

    if mortality is not None:
        datasets.append(mortality)

    if stroke is not None:
        datasets.append(stroke)

    if not datasets:
        logger.error("No quality data available")
        return None

    # If multiple datasets, merge on common keys
    if len(datasets) == 1:
        quality_df = datasets[0]
    else:
        # Find common entity column
        entity_cols = ['entidade', 'hospital', 'estabelecimento']
        entity_col = None
        for col in entity_cols:
            if col in datasets[0].columns:
                entity_col = col
                break

        if entity_col and 'year_month' in datasets[0].columns:
            quality_df = datasets[0]
            for df in datasets[1:]:
                quality_df = quality_df.merge(
                    df,
                    on=[entity_col, 'year_month'],
                    how='outer',
                    suffixes=('', '_stroke')
                )
        else:
            # Just concatenate if can't merge
            quality_df = pd.concat(datasets, ignore_index=True)

    logger.info(f"Consolidated quality data: {len(quality_df)} rows")

    return quality_df


def save_quality_data(df):
    """Save processed quality data."""
    if df is None:
        logger.error("No data to save")
        return

    output_file = OUTPUT_DIR / "quality_metrics.parquet"
    df.to_parquet(output_file, index=False)

    logger.info(f"Quality data saved to: {output_file}")
    logger.info(f"File size: {output_file.stat().st_size / 1024:.1f} KB")

    # Save preview
    preview_file = OUTPUT_DIR / "quality_metrics_preview.csv"
    df.head(100).to_csv(preview_file, index=False)
    logger.info(f"Preview saved to: {preview_file}")


def main():
    """Main execution."""
    logger.info("="*70)
    logger.info("QUALITY DATA PROCESSING")
    logger.info("="*70 + "\n")

    quality_df = consolidate_quality_metrics()

    if quality_df is not None:
        save_quality_data(quality_df)

        print("\n" + "="*70)
        print("QUALITY DATA PREVIEW")
        print("="*70)
        print(f"\nShape: {quality_df.shape}")
        print(f"\nColumns: {quality_df.columns.tolist()}")
        print(f"\nFirst 5 rows:")
        print(quality_df.head())
    else:
        logger.error("Quality data processing failed")


if __name__ == "__main__":
    main()
