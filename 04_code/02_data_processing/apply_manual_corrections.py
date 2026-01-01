"""
Apply Manual Corrections to Hospital→ULS Mapping

Updates the mapping with user-provided corrections for unmapped hospitals.

Corrections:
1. Hospital José Luciano de Castro - Anadia → REMOVED (no longer in SNS)
2. Hospital Dr. Francisco Zagalo - Ovar → ULS Entre Douro e Vouga
3. Hospital de Magalhães Lemos (psychiatric, Porto) → ULS Santo António
4. Hospital de Cascais (PPP) → EXCLUDED (private partnership)
5. Hospital Rovisco Pais (rehabilitation) → ULS Coimbra
6. Hospital Arcebispo João Crisóstomo - Cantanhede → ULS Coimbra

Author: Research Team
Date: 2025-12-31
"""

import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
CROSSWALK_DIR = PROJECT_ROOT / "03_data" / "processed" / "crosswalks"

# Manual corrections from user
MANUAL_CORRECTIONS = {
    'Hospital José Luciano de Castro - Anadia': {
        'parent_uls': None,
        'confidence': 'High',
        'matching_keywords': 'Removed from SNS',
        'mapping_method': 'Manual - Removed',
        'status': 'REMOVED'
    },
    'Hospital Dr. Francisco Zagalo - Ovar': {
        'parent_uls': 'ULS Entre Douro e Vouga',
        'confidence': 'High',
        'matching_keywords': 'Manual correction - Ovar geographic location',
        'mapping_method': 'Manual',
        'status': 'ACTIVE'
    },
    'Hospital Dr. Francisco Zagalo': {
        'parent_uls': 'ULS Entre Douro e Vouga',
        'confidence': 'High',
        'matching_keywords': 'Manual correction - Ovar',
        'mapping_method': 'Manual',
        'status': 'ACTIVE'
    },
    'Hospital de Magalhães Lemos, E. P. E.': {
        'parent_uls': 'ULS Santo António',
        'confidence': 'High',
        'matching_keywords': 'Manual correction - Porto psychiatric hospital',
        'mapping_method': 'Manual',
        'status': 'ACTIVE'
    },
    'Hospital de Magalhães Lemos, EPE': {
        'parent_uls': 'ULS Santo António',
        'confidence': 'High',
        'matching_keywords': 'Manual correction - Porto psychiatric hospital',
        'mapping_method': 'Manual',
        'status': 'ACTIVE'
    },
    'Hospital de Cascais, PPP': {
        'parent_uls': None,
        'confidence': 'High',
        'matching_keywords': 'Private Partnership - Not in SNS',
        'mapping_method': 'Manual - Excluded',
        'status': 'EXCLUDED_PPP'
    },
    'Hospital de Cascais Dr. José de Almeida': {
        'parent_uls': None,
        'confidence': 'High',
        'matching_keywords': 'Private Partnership - Not in SNS',
        'mapping_method': 'Manual - Excluded',
        'status': 'EXCLUDED_PPP'
    },
    'Hospital Rovisco Pais': {
        'parent_uls': 'ULS Coimbra',
        'confidence': 'High',
        'matching_keywords': 'Manual correction - Rehabilitation hospital in Coimbra area',
        'mapping_method': 'Manual',
        'status': 'ACTIVE'
    },
    'Hospital Arcebispo João Crisóstomo - Cantanhede': {
        'parent_uls': 'ULS Coimbra',
        'confidence': 'High',
        'matching_keywords': 'Manual correction - Cantanhede (Coimbra district)',
        'mapping_method': 'Manual',
        'status': 'ACTIVE'
    },
    'Hospital Arcebispo João Crisóstomo': {
        'parent_uls': 'ULS Coimbra',
        'confidence': 'High',
        'matching_keywords': 'Manual correction - Cantanhede',
        'mapping_method': 'Manual',
        'status': 'ACTIVE'
    },
    'Hospital da Senhora da Oliveira, Guimarães, EPE': {
        'parent_uls': 'ULS do Alto Ave',
        'confidence': 'High',
        'matching_keywords': 'Manual correction - Guimarães (Alto Ave region)',
        'mapping_method': 'Manual',
        'status': 'ACTIVE'
    },
    'Hospital da Senhora da Oliveira': {
        'parent_uls': 'ULS do Alto Ave',
        'confidence': 'High',
        'matching_keywords': 'Manual correction - Guimarães',
        'mapping_method': 'Manual',
        'status': 'ACTIVE'
    },
}


def apply_manual_corrections():
    """Apply manual corrections to hospital→ULS mapping."""
    logger.info("="*70)
    logger.info("APPLYING MANUAL CORRECTIONS TO HOSPITAL→ULS MAPPING")
    logger.info("="*70 + "\n")

    # Load mapping
    mapping_file = CROSSWALK_DIR / "hospital_to_uls_mapping.csv"
    df = pd.read_csv(mapping_file, encoding='utf-8-sig')

    logger.info(f"Loaded mapping: {len(df)} hospitals")

    # Count before corrections
    before_high = len(df[df['confidence'] == 'High'])
    before_unmapped = len(df[df['parent_uls'].isna()])

    logger.info(f"\nBefore corrections:")
    logger.info(f"  High confidence: {before_high} ({before_high/len(df)*100:.1f}%)")
    logger.info(f"  Unmapped: {before_unmapped} ({before_unmapped/len(df)*100:.1f}%)")

    # Apply corrections
    corrections_applied = 0

    for hospital_name, correction in MANUAL_CORRECTIONS.items():
        # Find matching rows (partial match to handle variations)
        mask = df['old_hospital_name'].str.contains(hospital_name, case=False, na=False)

        if mask.any():
            for col, value in correction.items():
                df.loc[mask, col] = value

            corrections_applied += mask.sum()
            logger.info(f"\n✓ Corrected: {hospital_name}")
            logger.info(f"    → {correction['parent_uls']}")
            logger.info(f"    Status: {correction['status']}")

    # Add status column if not exists
    if 'status' not in df.columns:
        df['status'] = 'ACTIVE'

    # Count after corrections
    after_high = len(df[df['confidence'] == 'High'])
    after_unmapped = len(df[(df['parent_uls'].isna()) & (df['status'] == 'ACTIVE')])

    logger.info(f"\n" + "="*70)
    logger.info("CORRECTION SUMMARY")
    logger.info("="*70)

    logger.info(f"\nAfter corrections:")
    logger.info(f"  High confidence: {after_high} ({after_high/len(df)*100:.1f}%)")
    logger.info(f"  Unmapped (active): {after_unmapped} ({after_unmapped/len(df)*100:.1f}%)")
    logger.info(f"  Removed from SNS: {len(df[df['status'] == 'REMOVED'])}")
    logger.info(f"  Excluded (PPP): {len(df[df['status'] == 'EXCLUDED_PPP'])}")

    logger.info(f"\nImprovements:")
    logger.info(f"  High confidence: {before_high} → {after_high} (+{after_high - before_high})")
    logger.info(f"  Unmapped: {before_unmapped} → {after_unmapped} (-{before_unmapped - after_unmapped})")

    # Save corrected mapping
    output_file = CROSSWALK_DIR / "hospital_to_uls_mapping_corrected.csv"
    df.to_csv(output_file, index=False, encoding='utf-8-sig')

    logger.info(f"\nCorrected mapping saved: {output_file}")

    # Remaining unmapped (active only)
    remaining_unmapped = df[(df['parent_uls'].isna()) & (df['status'] == 'ACTIVE')]

    if len(remaining_unmapped) > 0:
        logger.info(f"\n" + "="*70)
        logger.info(f"REMAINING UNMAPPED HOSPITALS ({len(remaining_unmapped)})")
        logger.info("="*70)

        for idx, row in remaining_unmapped.iterrows():
            logger.info(f"\n  {row['old_hospital_name']}")
            logger.info(f"    Confidence: {row['confidence']}")
            logger.info(f"    Keywords: {row['matching_keywords']}")
    else:
        logger.info(f"\n✅ ALL ACTIVE HOSPITALS MAPPED!")

    # Generate updated statistics
    generate_final_statistics(df)

    return df


def generate_final_statistics(df):
    """Generate final mapping statistics."""
    logger.info("\n" + "="*70)
    logger.info("FINAL MAPPING STATISTICS")
    logger.info("="*70)

    total = len(df)
    active = len(df[df['status'] == 'ACTIVE'])
    removed = len(df[df['status'] == 'REMOVED'])
    excluded = len(df[df['status'] == 'EXCLUDED_PPP'])

    logger.info(f"\nTotal hospital entities: {total}")
    logger.info(f"  Active in SNS: {active} ({active/total*100:.1f}%)")
    logger.info(f"  Removed from SNS: {removed} ({removed/total*100:.1f}%)")
    logger.info(f"  Excluded (PPP): {excluded} ({excluded/total*100:.1f}%)")

    # Active hospitals only
    active_df = df[df['status'] == 'ACTIVE']

    if len(active_df) > 0:
        mapped = len(active_df[active_df['parent_uls'].notna()])
        high_conf = len(active_df[active_df['confidence'] == 'High'])

        logger.info(f"\nActive hospitals mapping:")
        logger.info(f"  Mapped to ULS: {mapped}/{len(active_df)} ({mapped/len(active_df)*100:.1f}%)")
        logger.info(f"  High confidence: {high_conf}/{len(active_df)} ({high_conf/len(active_df)*100:.1f}%)")

        # Count by parent ULS
        logger.info(f"\nHospitals per ULS (active only):")
        uls_counts = active_df[active_df['parent_uls'].notna()]['parent_uls'].value_counts()

        for uls, count in uls_counts.head(10).items():
            logger.info(f"  {uls}: {count} hospitals")

        logger.info(f"\n  ... and {len(uls_counts) - 10} more ULS")


def main():
    """Main execution."""
    df = apply_manual_corrections()

    logger.info("\n" + "="*70)
    logger.info("MANUAL CORRECTIONS COMPLETE")
    logger.info("="*70)

    logger.info("\nOutputs:")
    logger.info("  1. Updated mapping: hospital_to_uls_mapping_corrected.csv")
    logger.info("\nNext steps:")
    logger.info("  1. Use corrected mapping for quality metric aggregation")
    logger.info("  2. Recalculate PHFSI with complete 5-component index")
    logger.info("  3. Proceed with Granger causality analysis")


if __name__ == "__main__":
    main()
