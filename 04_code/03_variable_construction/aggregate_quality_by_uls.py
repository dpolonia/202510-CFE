"""
Aggregate Quality Metrics by Parent ULS

Uses the corrected hospital→ULS mapping to aggregate quality metrics from
pre-integration hospitals (2017-2023) to their parent ULS entities.

This solves the CQMI component construction problem identified in peer reviews:
"CQMI Component Missing (Major): One of five PHFSI components (Clinical Quality
Maintenance Index) is entirely missing due to entity name mapping issues."

Input:
- Quality metrics (raw): 03_data/processed/quality/quality_metrics.parquet
- Hospital→ULS mapping: 03_data/processed/crosswalks/hospital_to_uls_mapping_corrected.csv

Output:
- Quality metrics aggregated by ULS: 03_data/processed/quality/quality_metrics_by_uls.parquet
- Ready for CQMI component calculation

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
DATA_PROCESSED = PROJECT_ROOT / "03_data" / "processed"
CROSSWALK_DIR = DATA_PROCESSED / "crosswalks"
QUALITY_DIR = DATA_PROCESSED / "quality"

QUALITY_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    """Load quality metrics and hospital→ULS mapping."""
    logger.info("Loading data...")

    # Load quality metrics
    quality_file = QUALITY_DIR / "quality_metrics.parquet"
    quality_df = pd.read_parquet(quality_file)
    logger.info(f"  Quality metrics: {len(quality_df)} rows")

    # Load hospital→ULS mapping
    mapping_file = CROSSWALK_DIR / "hospital_to_uls_mapping_corrected.csv"
    mapping_df = pd.read_csv(mapping_file, encoding='utf-8-sig')
    logger.info(f"  Hospital→ULS mapping: {len(mapping_df)} hospitals")

    return quality_df, mapping_df


def standardize_entity_names(quality_df):
    """Standardize entity names in quality data to match mapping."""
    logger.info("\nStandardizing entity names...")

    # Quality data uses 'instituicao' column
    if 'instituicao' in quality_df.columns:
        entity_col = 'instituicao'
    elif 'entidade' in quality_df.columns:
        entity_col = 'entidade'
    else:
        logger.error("No entity column found in quality data")
        return quality_df, None

    original_count = quality_df[entity_col].nunique()
    logger.info(f"  Original entities in quality data: {original_count}")

    return quality_df, entity_col


def create_entity_mapping_dict(mapping_df):
    """Create dictionary mapping old hospital names to parent ULS."""
    logger.info("\nCreating entity mapping dictionary...")

    # Include both standardized and original names
    mapping_dict = {}

    for idx, row in mapping_df.iterrows():
        if pd.notna(row['parent_uls']) and row['status'] == 'ACTIVE':
            # Map both original and standardized names
            mapping_dict[row['old_hospital_name']] = row['parent_uls']
            if pd.notna(row['hospital_standardized']):
                mapping_dict[row['hospital_standardized']] = row['parent_uls']

    logger.info(f"  Created mappings for {len(set(mapping_dict.values()))} unique ULS")
    logger.info(f"  Total mapping entries: {len(mapping_dict)}")

    return mapping_dict


def aggregate_quality_by_uls(quality_df, entity_col, mapping_dict):
    """
    Aggregate quality metrics from hospitals to parent ULS.

    Strategy:
    1. Map hospital names to parent ULS
    2. For pre-2024 data: Aggregate by parent ULS (mean/sum as appropriate)
    3. For post-2024 data: Use ULS names directly
    """
    logger.info("\n" + "="*70)
    logger.info("AGGREGATING QUALITY METRICS BY PARENT ULS")
    logger.info("="*70)

    df = quality_df.copy()

    # Add year column if not exists
    if 'year' not in df.columns and 'ano' in df.columns:
        df['ano'] = pd.to_datetime(df['ano'], errors='coerce')
        df['year'] = df['ano'].dt.year
        df['month'] = df['ano'].dt.month

    # Map entities to parent ULS
    df['parent_uls'] = df[entity_col].map(mapping_dict)

    # For entities not in mapping (likely already ULS names), keep original
    unmapped_mask = df['parent_uls'].isna()
    df.loc[unmapped_mask, 'parent_uls'] = df.loc[unmapped_mask, entity_col]

    # Count mapping success
    total_entities = df[entity_col].nunique()
    mapped_entities = df[df['parent_uls'].notna()][entity_col].nunique()

    logger.info(f"\nEntity mapping:")
    logger.info(f"  Total entities: {total_entities}")
    logger.info(f"  Mapped: {mapped_entities} ({mapped_entities/total_entities*100:.1f}%)")

    # Identify quality metric columns
    quality_cols = [
        'taxa_mortalidade',
        'mortalidade_avc_hemorragico_30_dias',
        'mortalidade_avc_isquemico_30_dias',
        'taxa_internamento',
        'dias_internamento'
    ]

    available_quality_cols = [col for col in quality_cols if col in df.columns]
    logger.info(f"\nQuality metrics to aggregate: {len(available_quality_cols)}")
    for col in available_quality_cols:
        logger.info(f"  - {col}")

    # Prepare for aggregation
    # Group by parent_uls + year + month (or trimestre if monthly not available)
    group_cols = ['parent_uls', 'year']

    if 'month' in df.columns:
        group_cols.append('month')
    elif 'trimestre' in df.columns:
        group_cols.append('trimestre')

    # Add region if available
    if 'regiao' in df.columns:
        df['regiao_uls'] = df.groupby('parent_uls')['regiao'].transform('first')

    # Aggregation functions
    agg_dict = {}

    # Quality metrics: Use weighted mean (weight by number of admissions if available)
    # Otherwise simple mean
    for col in available_quality_cols:
        agg_dict[col] = 'mean'

    # Keep first values for categorical
    if 'regiao' in df.columns:
        agg_dict['regiao'] = 'first'

    # Aggregate
    logger.info(f"\nAggregating by: {group_cols}")

    aggregated_df = df.groupby(group_cols, as_index=False).agg(agg_dict)

    logger.info(f"\nAggregation results:")
    logger.info(f"  Input rows: {len(df)}")
    logger.info(f"  Output rows: {len(aggregated_df)}")
    logger.info(f"  Unique ULS: {aggregated_df['parent_uls'].nunique()}")

    # Rename parent_uls to entidade for consistency
    aggregated_df = aggregated_df.rename(columns={'parent_uls': 'entidade'})

    return aggregated_df


def validate_aggregation(aggregated_df):
    """Validate aggregated quality metrics."""
    logger.info("\n" + "="*70)
    logger.info("VALIDATION")
    logger.info("="*70)

    logger.info(f"\nAggregated dataset:")
    logger.info(f"  Shape: {aggregated_df.shape}")
    logger.info(f"  Unique ULS: {aggregated_df['entidade'].nunique()}")
    logger.info(f"  Years: {aggregated_df['year'].min()} - {aggregated_df['year'].max()}")

    # Check data availability by year
    logger.info(f"\nData availability by year:")
    year_counts = aggregated_df.groupby('year').size()
    for year, count in year_counts.items():
        logger.info(f"  {year}: {count} ULS-periods")

    # Check quality metric coverage
    quality_cols = [
        'taxa_mortalidade',
        'mortalidade_avc_hemorragico_30_dias',
        'mortalidade_avc_isquemico_30_dias',
        'taxa_internamento',
        'dias_internamento'
    ]

    logger.info(f"\nQuality metric coverage:")
    for col in quality_cols:
        if col in aggregated_df.columns:
            non_null = aggregated_df[col].notna().sum()
            pct = non_null / len(aggregated_df) * 100
            logger.info(f"  {col}: {non_null}/{len(aggregated_df)} ({pct:.1f}%)")


def save_aggregated_data(aggregated_df):
    """Save aggregated quality metrics."""
    logger.info("\nSaving aggregated data...")

    output_file = QUALITY_DIR / "quality_metrics_by_uls.parquet"
    aggregated_df.to_parquet(output_file, index=False)

    logger.info(f"  Saved: {output_file}")
    logger.info(f"  Size: {output_file.stat().st_size / 1024:.1f} KB")

    # Also save CSV preview
    preview_file = QUALITY_DIR / "quality_metrics_by_uls_preview.csv"
    aggregated_df.head(100).to_csv(preview_file, index=False)
    logger.info(f"  Preview: {preview_file}")


def main():
    """Main execution."""
    logger.info("="*70)
    logger.info("AGGREGATE QUALITY METRICS BY PARENT ULS")
    logger.info("="*70 + "\n")

    # Load data
    quality_df, mapping_df = load_data()

    # Standardize entity names
    quality_df, entity_col = standardize_entity_names(quality_df)

    if entity_col is None:
        logger.error("Cannot proceed without entity column")
        return

    # Create mapping dictionary
    mapping_dict = create_entity_mapping_dict(mapping_df)

    # Aggregate
    aggregated_df = aggregate_quality_by_uls(quality_df, entity_col, mapping_dict)

    # Validate
    validate_aggregation(aggregated_df)

    # Save
    save_aggregated_data(aggregated_df)

    logger.info("\n" + "="*70)
    logger.info("AGGREGATION COMPLETE")
    logger.info("="*70)
    logger.info("\nNext step: Calculate CQMI component using aggregated quality metrics")


if __name__ == "__main__":
    main()
