"""
Merge Quality Metrics with Monthly Panel for Granger Causality Analysis

This script addresses the data structure issue identified in the initial Granger
causality analysis: quality metrics (aggregated by ULS) and payment delays
(monthly panel) exist in separate datasets.

Solution:
1. Load monthly panel (hospital-month observations)
2. Load ULS-aggregated quality metrics
3. Use hospital→ULS crosswalk to map panel entities to parent ULS
4. Merge datasets on parent_uls + year + month
5. Create unified panel for temporal analysis

This enables proper Granger causality testing of:
- Payment Delays(t) → Quality Decline(t+k)
- Financial Results(t) → Quality Decline(t+k)

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
PANEL_DIR = DATA_PROCESSED / "panel"
QUALITY_DIR = DATA_PROCESSED / "quality"
CROSSWALK_DIR = DATA_PROCESSED / "crosswalks"

PANEL_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    """Load all required datasets."""
    logger.info("Loading datasets...")

    # 1. Monthly panel
    panel_file = PANEL_DIR / "hospital_month_panel.parquet"
    panel_df = pd.read_parquet(panel_file)
    logger.info(f"  Monthly panel: {len(panel_df)} rows, {panel_df['entidade'].nunique()} entities")

    # 2. Quality metrics (aggregated by ULS)
    quality_file = QUALITY_DIR / "quality_metrics_by_uls.parquet"
    quality_df = pd.read_parquet(quality_file)
    logger.info(f"  Quality metrics: {len(quality_df)} rows, {quality_df['entidade'].nunique()} ULS")

    # 3. Hospital→ULS crosswalk
    crosswalk_file = CROSSWALK_DIR / "hospital_to_uls_mapping_corrected.csv"
    crosswalk_df = pd.read_csv(crosswalk_file, encoding='utf-8-sig')
    logger.info(f"  Crosswalk: {len(crosswalk_df)} hospital mappings")

    return panel_df, quality_df, crosswalk_df


def create_mapping_dict(crosswalk_df):
    """Create dictionary mapping hospital names to parent ULS."""
    logger.info("\nCreating hospital→ULS mapping dictionary...")

    mapping_dict = {}

    for idx, row in crosswalk_df.iterrows():
        if pd.notna(row['parent_uls']) and row['status'] == 'ACTIVE':
            # Map both old hospital name and standardized name
            mapping_dict[row['old_hospital_name']] = row['parent_uls']
            if pd.notna(row['hospital_standardized']):
                mapping_dict[row['hospital_standardized']] = row['parent_uls']

    logger.info(f"  Created {len(mapping_dict)} mapping entries")
    logger.info(f"  Covering {len(set(mapping_dict.values()))} unique ULS")

    return mapping_dict


def map_panel_to_uls(panel_df, mapping_dict):
    """Map monthly panel entities to their parent ULS."""
    logger.info("\n" + "="*70)
    logger.info("MAPPING MONTHLY PANEL TO PARENT ULS")
    logger.info("="*70)

    df = panel_df.copy()

    # Map to parent ULS
    df['parent_uls'] = df['entidade'].map(mapping_dict)

    # For unmapped (likely already ULS names), keep original
    unmapped_mask = df['parent_uls'].isna()
    df.loc[unmapped_mask, 'parent_uls'] = df.loc[unmapped_mask, 'entidade']

    # Mapping statistics
    logger.info(f"\nMapping results:")
    logger.info(f"  Total entities: {df['entidade'].nunique()}")
    logger.info(f"  Mapped to ULS: {df[~unmapped_mask]['entidade'].nunique()}")
    logger.info(f"  Already ULS: {df[unmapped_mask]['entidade'].nunique()}")
    logger.info(f"  Unique parent ULS: {df['parent_uls'].nunique()}")

    return df


def merge_quality_metrics(panel_df, quality_df):
    """Merge quality metrics into monthly panel."""
    logger.info("\n" + "="*70)
    logger.info("MERGING QUALITY METRICS WITH MONTHLY PANEL")
    logger.info("="*70)

    # Ensure consistent datetime types
    if 'year_month' not in panel_df.columns:
        panel_df['year_month'] = pd.to_datetime(
            panel_df[['year', 'month']].assign(day=1)
        ).dt.to_period('M')

    if 'year_month' not in quality_df.columns:
        quality_df['year_month'] = pd.to_datetime(
            quality_df[['year', 'month']].assign(day=1)
        ).dt.to_period('M')

    logger.info(f"\nBefore merge:")
    logger.info(f"  Panel: {len(panel_df)} rows")
    logger.info(f"  Quality: {len(quality_df)} rows")

    # Merge on parent_uls + year + month
    merged_df = panel_df.merge(
        quality_df[['entidade', 'year', 'month', 'taxa_mortalidade',
                    'taxa_internamento', 'dias_internamento']],
        left_on=['parent_uls', 'year', 'month'],
        right_on=['entidade', 'year', 'month'],
        how='left',
        suffixes=('', '_quality')
    )

    # Drop duplicate entidade column from quality
    if 'entidade_quality' in merged_df.columns:
        merged_df = merged_df.drop(columns=['entidade_quality'])

    logger.info(f"\nAfter merge:")
    logger.info(f"  Merged: {len(merged_df)} rows")
    logger.info(f"  Entities: {merged_df['entidade'].nunique()}")

    # Check quality metric coverage
    quality_cols = ['taxa_mortalidade', 'taxa_internamento', 'dias_internamento']
    logger.info(f"\nQuality metric coverage in merged panel:")
    for col in quality_cols:
        if col in merged_df.columns:
            non_null = merged_df[col].notna().sum()
            pct = non_null / len(merged_df) * 100
            logger.info(f"  {col}: {non_null}/{len(merged_df)} ({pct:.1f}%)")

    return merged_df


def validate_merged_panel(merged_df):
    """Validate the merged panel dataset."""
    logger.info("\n" + "="*70)
    logger.info("VALIDATION OF MERGED PANEL")
    logger.info("="*70)

    # Overall statistics
    logger.info(f"\nDataset dimensions:")
    logger.info(f"  Rows: {len(merged_df)}")
    logger.info(f"  Columns: {len(merged_df.columns)}")
    logger.info(f"  Entities: {merged_df['parent_uls'].nunique()}")
    logger.info(f"  Time range: {merged_df['year'].min()}-{merged_df['year'].max()}")

    # Check temporal overlap of key variables
    logger.info(f"\nTemporal overlap for Granger causality:")

    # Entities with both payment delays AND quality metrics
    has_payments = merged_df['pagamentos_em_atraso'].notna()
    has_mortality = merged_df['taxa_mortalidade'].notna()

    overlap_entities = merged_df[has_payments & has_mortality]['parent_uls'].unique()
    logger.info(f"  Entities with BOTH payment delays AND quality data: {len(overlap_entities)}")

    # Count observations per entity with overlap
    overlap_df = merged_df[has_payments & has_mortality]
    entity_counts = overlap_df.groupby('parent_uls').size().sort_values(ascending=False)

    logger.info(f"\nTop 10 entities by overlapping observations:")
    for entity, count in entity_counts.head(10).items():
        logger.info(f"  {entity}: {count} months")

    # Minimum 36 months for Granger (3 years)
    sufficient_data = entity_counts[entity_counts >= 36]
    logger.info(f"\nEntities with ≥36 overlapping months: {len(sufficient_data)}")

    if len(sufficient_data) == 0:
        logger.warning("  WARNING: No entities have sufficient overlapping data for Granger causality!")
        logger.warning("  This indicates quality metrics and payment delays still don't overlap temporally")

        # Diagnose the issue
        logger.info(f"\nDiagnosing temporal mismatch:")
        logger.info(f"  Payment delays coverage: {merged_df['pagamentos_em_atraso'].notna().sum()} rows")
        logger.info(f"  Quality metrics coverage: {merged_df['taxa_mortalidade'].notna().sum()} rows")

        # Show year distribution
        payment_years = merged_df[has_payments]['year'].value_counts().sort_index()
        quality_years = merged_df[has_mortality]['year'].value_counts().sort_index()

        logger.info(f"\n  Payment delays by year:")
        for year, count in payment_years.items():
            logger.info(f"    {int(year)}: {count} observations")

        logger.info(f"\n  Quality metrics by year:")
        for year, count in quality_years.items():
            logger.info(f"    {int(year)}: {count} observations")
    else:
        logger.info(f"  ✓ Sufficient data for Granger causality analysis")

    return merged_df


def save_merged_panel(merged_df):
    """Save the merged panel dataset."""
    logger.info("\nSaving merged panel...")

    output_file = PANEL_DIR / "hospital_month_panel_with_quality.parquet"
    merged_df.to_parquet(output_file, index=False)

    logger.info(f"  Saved: {output_file}")
    logger.info(f"  Size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")

    # Also save preview CSV
    preview_file = PANEL_DIR / "hospital_month_panel_with_quality_preview.csv"
    merged_df.head(100).to_csv(preview_file, index=False)
    logger.info(f"  Preview: {preview_file}")


def main():
    """Main execution."""
    logger.info("="*70)
    logger.info("MERGE QUALITY METRICS WITH MONTHLY PANEL")
    logger.info("="*70 + "\n")

    # Load data
    panel_df, quality_df, crosswalk_df = load_data()

    # Create mapping
    mapping_dict = create_mapping_dict(crosswalk_df)

    # Map panel to ULS
    panel_with_uls = map_panel_to_uls(panel_df, mapping_dict)

    # Merge quality metrics
    merged_df = merge_quality_metrics(panel_with_uls, quality_df)

    # Validate
    merged_df = validate_merged_panel(merged_df)

    # Save
    save_merged_panel(merged_df)

    logger.info("\n" + "="*70)
    logger.info("MERGE COMPLETE")
    logger.info("="*70)
    logger.info("\nNext step: Re-run Granger causality analysis with merged panel")


if __name__ == "__main__":
    main()
