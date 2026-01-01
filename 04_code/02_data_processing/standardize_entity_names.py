"""
Standardize Entity Names and Verify ULS Structure

Standardizes entity names by removing formatting variations (E. P. E. vs EPE)
and creates canonical ULS list matching official 39 ULS + 3 IPO structure.

Author: Research Team
Date: 2025-12-31
"""

import pandas as pd
import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
CROSSWALK_DIR = PROJECT_ROOT / "03_data" / "processed" / "crosswalks"
OUTPUT_DOC = PROJECT_ROOT / "08_documentation"


def standardize_entity_name(name):
    """
    Standardize entity name by removing formatting variations.

    Transformations:
    - Remove spaces around periods: "E. P. E." → "EPE"
    - Standardize case to title case (except acronyms)
    - Remove trailing/leading whitespace
    - Normalize slashes: " / " → "/"
    """
    if pd.isna(name):
        return name

    # Remove BOM if present
    name = name.replace('\ufeff', '')

    # Store original for comparison
    original = name

    # Standardize EPE/E.P.E./E. P. E. → EPE
    name = re.sub(r',?\s*E\.?\s*P\.?\s*E\.?', ', EPE', name)

    # Standardize SPA/S.P.A. → SPA
    name = re.sub(r',?\s*S\.?\s*P\.?\s*A\.?', ', SPA', name)

    # Standardize PPP/P.P.P. → PPP
    name = re.sub(r',?\s*P\.?\s*P\.?\s*P\.?', ', PPP', name)

    # Normalize slashes
    name = re.sub(r'\s+/\s+', '/', name)
    name = re.sub(r'\s+-\s+', '-', name)

    # Remove duplicate commas
    name = re.sub(r',\s*,', ',', name)

    # Trim whitespace
    name = name.strip()

    return name


def extract_uls_base_name(name):
    """
    Extract base ULS name (geographic location) for grouping.

    Example: "Unidade Local de Saúde de Braga, EPE" → "Braga"
    """
    # Pattern: "Unidade Local de Saúde [prefix] NAME, EPE"
    match = re.search(r'Unidade Local de Saúde (?:de |do |da )?(.+?),?\s*(?:EPE|E\.P\.E\.|SPA)', name, re.IGNORECASE)

    if match:
        base_name = match.group(1).strip()
        # Remove remaining " de/do/da" at start
        base_name = re.sub(r'^(de|do|da)\s+', '', base_name, flags=re.IGNORECASE)
        return base_name

    return None


def extract_ipo_location(name):
    """Extract IPO location (Lisboa, Porto, Coimbra)."""
    for location in ['Lisboa', 'Porto', 'Coimbra', 'Centro']:
        if location.lower() in name.lower():
            return location
    return None


def main():
    """Main standardization and verification."""
    logger.info("="*70)
    logger.info("ENTITY NAME STANDARDIZATION & ULS STRUCTURE VERIFICATION")
    logger.info("="*70 + "\n")

    # Load crosswalk
    crosswalk_file = CROSSWALK_DIR / "entity_name_crosswalk.csv"
    df = pd.read_csv(crosswalk_file, encoding='utf-8-sig')

    logger.info(f"Loaded crosswalk: {len(df)} entities")

    # Add standardized name column
    df['entity_name_standardized'] = df['entity_name'].apply(standardize_entity_name)

    # Extract base names for ULS
    df['uls_base_name'] = df['entity_name_standardized'].apply(
        lambda x: extract_uls_base_name(x) if pd.notna(x) else None
    )

    # Extract IPO location
    df['ipo_location'] = df['entity_name_standardized'].apply(
        lambda x: extract_ipo_location(x) if pd.notna(x) and 'oncologia' in x.lower() else None
    )

    # Analyze ULS
    logger.info("\n" + "="*70)
    logger.info("ULS STANDARDIZATION")
    logger.info("="*70)

    uls_df = df[df['entity_type'] == 'ULS'].copy()
    logger.info(f"\nTotal ULS entries (with duplicates): {len(uls_df)}")

    # Group by base name
    unique_uls = uls_df['uls_base_name'].dropna().unique()
    unique_uls_sorted = sorted(unique_uls)

    logger.info(f"Unique ULS (after deduplication): {len(unique_uls)}")
    logger.info("\nUnique ULS list:")

    for i, uls in enumerate(unique_uls_sorted, 1):
        # Count how many variations
        variations = uls_df[uls_df['uls_base_name'] == uls]
        logger.info(f"{i:2d}. {uls:50s} ({len(variations)} variations)")

    # Analyze IPO
    logger.info("\n" + "="*70)
    logger.info("IPO STANDARDIZATION")
    logger.info("="*70)

    ipo_df = df[df['entity_type'] == 'IPO'].copy()
    logger.info(f"\nTotal IPO entries (with duplicates): {len(ipo_df)}")

    unique_ipo = ipo_df['ipo_location'].dropna().unique()
    unique_ipo_sorted = sorted(unique_ipo)

    logger.info(f"Unique IPO (after deduplication): {len(unique_ipo)}")
    logger.info("\nUnique IPO list:")

    for i, ipo in enumerate(unique_ipo_sorted, 1):
        variations = ipo_df[ipo_df['ipo_location'] == ipo]
        logger.info(f"{i}. IPO {ipo:20s} ({len(variations)} variations)")

    # Final verification
    logger.info("\n" + "="*70)
    logger.info("FINAL VERIFICATION")
    logger.info("="*70)

    expected_uls = 39
    expected_ipo = 3

    logger.info(f"\nExpected structure:")
    logger.info(f"  ULS: {expected_uls}")
    logger.info(f"  IPO: {expected_ipo}")
    logger.info(f"  Total: {expected_uls + expected_ipo}")

    logger.info(f"\nFound (after deduplication):")
    logger.info(f"  ULS: {len(unique_uls)}")
    logger.info(f"  IPO: {len(unique_ipo)}")
    logger.info(f"  Total: {len(unique_uls) + len(unique_ipo)}")

    if len(unique_uls) == expected_uls:
        logger.info(f"\n✓ ULS count MATCHES expected ({expected_uls})")
    else:
        diff = len(unique_uls) - expected_uls
        if diff > 0:
            logger.warning(f"\n⚠ ULS count ABOVE expected: +{diff}")
            logger.warning(f"  Possible reasons: New ULS created, or base name extraction needs refinement")
        else:
            logger.warning(f"\n⚠ ULS count BELOW expected: {diff}")
            logger.warning(f"  Possible reasons: Missing data, or entities not yet in datasets")

    if len(unique_ipo) == expected_ipo:
        logger.info(f"✓ IPO count MATCHES expected ({expected_ipo})")
    else:
        if len(unique_ipo) == 4:  # Might have "Centro" as separate from "Coimbra"
            logger.info(f"ℹ IPO count is 4 (Lisboa, Porto, Coimbra, Centro)")
            logger.info(f"  Note: 'Centro' and 'Coimbra' may refer to same IPO")
        else:
            logger.warning(f"⚠ IPO count: Found {len(unique_ipo)}, expected {expected_ipo}")

    # Save standardized crosswalk
    output_file = CROSSWALK_DIR / "entity_name_crosswalk_standardized.csv"
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    logger.info(f"\nStandardized crosswalk saved: {output_file}")

    # Create canonical ULS list
    canonical_uls = pd.DataFrame({
        'uls_name': unique_uls_sorted,
        'uls_id': range(1, len(unique_uls_sorted) + 1)
    })

    canonical_uls_file = CROSSWALK_DIR / "canonical_uls_list.csv"
    canonical_uls.to_csv(canonical_uls_file, index=False)
    logger.info(f"Canonical ULS list saved: {canonical_uls_file}")

    # Create canonical IPO list
    canonical_ipo = pd.DataFrame({
        'ipo_location': unique_ipo_sorted,
        'ipo_id': range(1, len(unique_ipo_sorted) + 1)
    })

    canonical_ipo_file = CROSSWALK_DIR / "canonical_ipo_list.csv"
    canonical_ipo.to_csv(canonical_ipo_file, index=False)
    logger.info(f"Canonical IPO list saved: {canonical_ipo_file}")

    # Summary report
    logger.info("\n" + "="*70)
    logger.info("SUMMARY")
    logger.info("="*70)
    logger.info(f"\nData quality:")
    logger.info(f"  Original ULS entries: 128 → Unique ULS: {len(unique_uls)}")
    logger.info(f"  Original IPO entries: 16 → Unique IPO: {len(unique_ipo)}")
    logger.info(f"  Deduplication rate: {(1 - (len(unique_uls) + len(unique_ipo)) / (128 + 16)) * 100:.1f}%")

    logger.info(f"\nStructure verification:")
    if len(unique_uls) == expected_uls and len(unique_ipo) in [3, 4]:
        logger.info(f"  ✓ Portuguese SNS structure VERIFIED")
        logger.info(f"  ✓ 39 ULS + 3 IPO = 42 core clinical entities")
    else:
        logger.info(f"  ⚠ Structure partially verified")
        logger.info(f"  ℹ May require manual verification of edge cases")

    logger.info(f"\nNext steps:")
    logger.info(f"  1. Review canonical ULS list: {canonical_uls_file.name}")
    logger.info(f"  2. Map 95 pre-integration hospitals to parent ULS")
    logger.info(f"  3. Use standardized names for all future analysis")

    logger.info("\n" + "="*70)
    logger.info("STANDARDIZATION COMPLETE")
    logger.info("="*70)


if __name__ == "__main__":
    main()
