"""
Standardize ULS Names for Merging Quality Metrics with Panel Data

The issue: Quality data uses full official names (e.g., "Unidade Local de Saúde
de Coimbra, E.P.E.") while the panel data uses shortened names (e.g., "ULS Coimbra").

Solution: Create standardization function that converts all variations to common format.

Author: Research Team
Date: 2025-12-31
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PROCESSED = PROJECT_ROOT / "03_data" / "processed"
PANEL_DIR = DATA_PROCESSED / "panel"
QUALITY_DIR = DATA_PROCESSED / "quality"
CROSSWALK_DIR = DATA_PROCESSED / "crosswalks"


def standardize_uls_name(name):
    """
    Standardize ULS names to a common format for merging.

    Converts both:
    - "Unidade Local de Saúde de Coimbra, E.P.E."
    - "ULS Coimbra"
    - "ULS do Alto Ave"

    To: "ULS Coimbra" / "ULS Alto Ave" (Title Case for consistency)
    """
    if pd.isna(name):
        return name

    name = str(name).strip()

    # Convert "Unidade Local de Saúde de X, E.P.E." → "ULS X"
    name = re.sub(r'Unidade Local de Saúde (de |da |do )', 'ULS ', name, flags=re.IGNORECASE)

    # Remove E.P.E./EPE variations
    name = re.sub(r',?\s*E\.?\s*P\.?\s*E\.?', '', name, flags=re.IGNORECASE)

    # Convert "Instituto Português Oncologia F. Gentil - X" → "IPO X"
    name = re.sub(r'Instituto Português Oncologia\s+F\.\s*Gentil\s*-\s*', 'IPO ', name, flags=re.IGNORECASE)
    name = re.sub(r'Instituto Português de Oncologia (de |do )', 'IPO ', name, flags=re.IGNORECASE)

    # Handle "ULS do/da/de X" → "ULS X"
    name = re.sub(r'^ULS (do |da |de )', 'ULS ', name, flags=re.IGNORECASE)

    # Clean up extra spaces and commas
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r',\s*,', ',', name)
    name = name.strip(' ,')

    # Convert to title case for consistency (handles "ULS GUARDA" vs "ULS Guarda")
    name = name.title()

    return name


def test_standardization():
    """Test standardization function with known examples."""
    logger.info("Testing ULS name standardization...\n")

    test_cases = [
        ("Unidade Local de Saúde de Coimbra, E.P.E.", "Uls Coimbra"),
        ("ULS Coimbra", "Uls Coimbra"),
        ("Unidade Local de Saúde do Alto Minho, E.P.E.", "Uls Alto Minho"),
        ("ULS do Alto Ave", "Uls Alto Ave"),
        ("Instituto Português Oncologia  F. Gentil - Lisboa, E.P.E.", "Ipo Lisboa"),
        ("Instituto Português de Oncologia de Porto, E. P. E.", "Ipo Porto"),
    ]

    all_passed = True
    for original, expected in test_cases:
        result = standardize_uls_name(original)
        passed = result == expected
        all_passed = all_passed and passed

        status = "✓" if passed else "✗"
        logger.info(f"{status} {original}")
        logger.info(f"  Expected: {expected}")
        logger.info(f"  Got:      {result}\n")

    if all_passed:
        logger.info("All tests PASSED!\n")
    else:
        logger.warning("Some tests FAILED - check standardization logic\n")

    return all_passed


def load_and_standardize_data():
    """Load data and apply standardization."""
    logger.info("="*70)
    logger.info("STANDARDIZE ULS NAMES FOR MERGING")
    logger.info("="*70 + "\n")

    # Load monthly panel
    panel_file = PANEL_DIR / "hospital_month_panel_with_quality.parquet"
    panel_df = pd.read_parquet(panel_file)
    logger.info(f"Loaded monthly panel: {len(panel_df)} rows")

    # Load quality metrics
    quality_file = QUALITY_DIR / "quality_metrics_by_uls.parquet"
    quality_df = pd.read_parquet(quality_file)
    logger.info(f"Loaded quality metrics: {len(quality_df)} rows")

    logger.info(f"\nStandardizing ULS names...")

    # Standardize panel parent_uls
    panel_df['parent_uls_std'] = panel_df['parent_uls'].apply(standardize_uls_name)

    # Standardize quality entidade
    quality_df['entidade_std'] = quality_df['entidade'].apply(standardize_uls_name)

    logger.info(f"  Panel unique standardized ULS: {panel_df['parent_uls_std'].nunique()}")
    logger.info(f"  Quality unique standardized ULS: {quality_df['entidade_std'].nunique()}")

    return panel_df, quality_df


def merge_with_standardized_names(panel_df, quality_df):
    """Merge using standardized ULS names."""
    logger.info("\n" + "="*70)
    logger.info("MERGING WITH STANDARDIZED NAMES")
    logger.info("="*70)

    # Ensure year_month exists
    if 'year_month' not in panel_df.columns:
        panel_df['year_month'] = pd.to_datetime(
            panel_df[['year', 'month']].assign(day=1)
        ).dt.to_period('M')

    if 'year_month' not in quality_df.columns:
        quality_df['year_month'] = pd.to_datetime(
            quality_df[['year', 'month']].assign(day=1)
        ).dt.to_period('M')

    logger.info(f"\nBefore consolidation:")
    logger.info(f"  Panel: {len(panel_df)} rows")

    # CRITICAL: Consolidate duplicate rows (same ULS/year/month, different entity name variations)
    # Group by standardized ULS + year + month and aggregate
    logger.info(f"\nConsolidating duplicate entity variations...")

    # Identify numeric columns for aggregation
    numeric_cols = panel_df.select_dtypes(include=[np.number]).columns.tolist()
    # Remove year, month from aggregation list (they're grouping keys)
    numeric_cols = [col for col in numeric_cols if col not in ['year', 'month']]

    # Aggregation: use mean for numeric, first for others
    agg_dict = {col: 'mean' for col in numeric_cols}
    agg_dict['entidade'] = 'first'  # Keep first entity name
    agg_dict['parent_uls'] = 'first'

    # Group and aggregate
    panel_consolidated = panel_df.groupby(['parent_uls_std', 'year', 'month'], as_index=False).agg(agg_dict)

    logger.info(f"  Before: {len(panel_df)} rows")
    logger.info(f"  After: {len(panel_consolidated)} rows")
    logger.info(f"  Removed {len(panel_df) - len(panel_consolidated)} duplicate rows")

    logger.info(f"\nBefore merge:")
    logger.info(f"  Panel (consolidated): {len(panel_consolidated)} rows")
    logger.info(f"  Quality: {len(quality_df)} rows")

    # Drop old quality columns if they exist
    quality_cols_to_drop = [col for col in panel_consolidated.columns if col.endswith('_quality')]
    if quality_cols_to_drop:
        panel_consolidated = panel_consolidated.drop(columns=quality_cols_to_drop)
        logger.info(f"  Dropped {len(quality_cols_to_drop)} old quality columns")

    # Merge on standardized ULS name + year + month
    merged_df = panel_consolidated.merge(
        quality_df[['entidade_std', 'year', 'month', 'taxa_mortalidade',
                    'taxa_internamento', 'dias_internamento']],
        left_on=['parent_uls_std', 'year', 'month'],
        right_on=['entidade_std', 'year', 'month'],
        how='left',
        suffixes=('', '_dup')
    )

    # Drop duplicate columns
    dup_cols = [col for col in merged_df.columns if col.endswith('_dup')]
    if dup_cols:
        merged_df = merged_df.drop(columns=dup_cols)

    logger.info(f"\nAfter merge:")
    logger.info(f"  Merged: {len(merged_df)} rows")
    logger.info(f"  Entities: {merged_df['entidade'].nunique()}")

    # Check quality metric coverage
    quality_cols = ['taxa_mortalidade', 'taxa_internamento', 'dias_internamento']
    logger.info(f"\nQuality metric coverage:")
    for col in quality_cols:
        if col in merged_df.columns:
            non_null = merged_df[col].notna().sum()
            pct = non_null / len(merged_df) * 100
            logger.info(f"  {col}: {non_null}/{len(merged_df)} ({pct:.1f}%)")

    return merged_df


def validate_overlap(merged_df):
    """Validate temporal overlap for Granger causality."""
    logger.info("\n" + "="*70)
    logger.info("TEMPORAL OVERLAP VALIDATION")
    logger.info("="*70)

    # Check overlap
    has_payments = merged_df['pagamentos_em_atraso'].notna()
    has_mortality = merged_df['taxa_mortalidade'].notna()

    overlap_df = merged_df[has_payments & has_mortality]
    overlap_entities = overlap_df['parent_uls_std'].unique()

    logger.info(f"\nEntities with BOTH payment delays AND quality data: {len(overlap_entities)}")

    if len(overlap_entities) > 0:
        # Count observations per entity
        entity_counts = overlap_df.groupby('parent_uls_std').size().sort_values(ascending=False)

        logger.info(f"\nTop 10 entities by overlapping observations:")
        for entity, count in entity_counts.head(10).items():
            logger.info(f"  {entity}: {count} months")

        # Minimum 36 months for Granger
        sufficient_data = entity_counts[entity_counts >= 36]
        logger.info(f"\nEntities with ≥36 overlapping months: {len(sufficient_data)}")

        if len(sufficient_data) > 0:
            logger.info(f"  ✓ SUFFICIENT DATA for Granger causality analysis!")
            logger.info(f"\nEntities ready for Granger testing:")
            for entity, count in sufficient_data.items():
                logger.info(f"  {entity}: {count} months")
        else:
            logger.warning(f"  ✗ No entities with sufficient temporal overlap")
    else:
        logger.warning("  ✗ NO OVERLAP found between payment delays and quality metrics")

    return merged_df


def save_final_panel(merged_df):
    """Save final merged panel."""
    logger.info("\nSaving final merged panel...")

    output_file = PANEL_DIR / "hospital_month_panel_final.parquet"
    merged_df.to_parquet(output_file, index=False)

    logger.info(f"  Saved: {output_file}")
    logger.info(f"  Size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")

    # Preview
    preview_file = PANEL_DIR / "hospital_month_panel_final_preview.csv"
    merged_df.head(200).to_csv(preview_file, index=False)
    logger.info(f"  Preview: {preview_file}")


def main():
    """Main execution."""
    # Test standardization first
    if not test_standardization():
        logger.error("Standardization tests failed - aborting")
        return

    # Load and standardize
    panel_df, quality_df = load_and_standardize_data()

    # Merge
    merged_df = merge_with_standardized_names(panel_df, quality_df)

    # Validate
    merged_df = validate_overlap(merged_df)

    # Save
    save_final_panel(merged_df)

    logger.info("\n" + "="*70)
    logger.info("STANDARDIZATION AND MERGE COMPLETE")
    logger.info("="*70)
    logger.info("\nNext step: Re-run Granger causality with final merged panel")


if __name__ == "__main__":
    main()
