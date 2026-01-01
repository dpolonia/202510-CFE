"""
CQMI Integration and Complete 5-Component PHFSI Calculation
=============================================================

Issue 6: Integrate CQMI component into main PHFSI components file and
recalculate complete 5-component PHFSI.

**Challenge**: Entity name mismatch
- Main components file: Pre-reform hospital names (149 entities, 2017-2024)
- CQMI file: Post-reform ULS names (43 entities, 2019-2024)
- Solution: Use hospital-to-ULS crosswalk for mapping

**Approach**:
1. Load all three datasets (components, CQMI, crosswalk)
2. Create reverse mapping (ULS → hospitals) from crosswalk
3. Expand CQMI from ULS-level to hospital-level using crosswalk
4. Merge CQMI into main components file
5. Recalculate complete 5-component PHFSI
6. Compare 4-component vs 5-component versions

Author: Claude Code + Daniel Polonia
Date: January 2026
"""

import logging
import numpy as np
import pandas as pd
from pathlib import Path
import sys

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Fixed: parents[2] not parents[3]
DATA_DIR = PROJECT_ROOT / "03_data"
OUTPUT_DIR = PROJECT_ROOT / "06_output"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(OUTPUT_DIR / "logs" / "cqmi_integration.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ==============================================================================
# STEP 1: Load All Data Sources
# ==============================================================================

def load_data():
    """Load main components, CQMI scores, and entity crosswalk."""
    logger.info("=" * 80)
    logger.info("STEP 1: Loading Data")
    logger.info("=" * 80)

    # 1a. Load main components file
    components_path = DATA_DIR / "processed" / "variables" / "phfsi_components.parquet"
    df_components = pd.read_parquet(components_path)
    logger.info(f"✓ Main components: {df_components.shape[0]} observations, {df_components['entidade'].nunique()} entities, years {df_components['year'].min()}-{df_components['year'].max()}")
    logger.info(f"  - CQMI missing: {df_components['cqmi'].isna().sum()}/{len(df_components)} ({100*df_components['cqmi'].isna().sum()/len(df_components):.1f}%)")

    # 1b. Load CQMI scores
    cqmi_path = DATA_DIR / "processed" / "variables" / "cqmi_component_scores.parquet"
    df_cqmi = pd.read_parquet(cqmi_path)
    logger.info(f"✓ CQMI scores: {df_cqmi.shape[0]} observations, {df_cqmi['entidade'].nunique()} ULS entities, years {int(df_cqmi['year'].min())}-{int(df_cqmi['year'].max())}")

    # 1c. Load entity crosswalk
    crosswalk_path = DATA_DIR / "processed" / "crosswalks" / "hospital_to_uls_mapping_corrected.csv"
    df_crosswalk = pd.read_csv(crosswalk_path)
    logger.info(f"✓ Entity crosswalk: {len(df_crosswalk)} hospital → {df_crosswalk['parent_uls'].nunique()} ULS mappings")

    # Check overlap
    components_entities = set(df_components['entidade'].unique())
    cqmi_entities = set(df_cqmi['entidade'].unique())
    overlap = components_entities & cqmi_entities
    logger.info(f"\n  Entity overlap BEFORE crosswalk: {len(overlap)}/43 (expected 0 due to name changes)")

    return df_components, df_cqmi, df_crosswalk

# ==============================================================================
# STEP 2: Create ULS-to-Hospitals Reverse Mapping
# ==============================================================================

def create_reverse_mapping(df_crosswalk):
    """Create reverse mapping: ULS → list of hospitals."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 2: Creating ULS → Hospitals Reverse Mapping")
    logger.info("=" * 80)

    # Group hospitals by parent ULS
    uls_to_hospitals = df_crosswalk.groupby('parent_uls')['old_hospital_name'].apply(list).to_dict()

    logger.info(f"✓ Created reverse mapping for {len(uls_to_hospitals)} ULS entities")
    logger.info(f"  Example: {list(uls_to_hospitals.items())[0][0]} ← {len(list(uls_to_hospitals.items())[0][1])} hospitals")

    return uls_to_hospitals

# ==============================================================================
# STEP 3: Normalize Entity Names for Matching
# ==============================================================================

def normalize_entity_name(name):
    """Normalize entity names for robust matching."""
    if pd.isna(name):
        return ""

    # Convert to lowercase
    name = str(name).lower()

    # Replace full "Unidade Local de Saúde" with "ULS" abbreviation (CRITICAL for matching)
    name = name.replace('unidade local de saúde', 'uls')
    name = name.replace('unidade local de saude', 'uls')  # without accent

    # Remove common abbreviations and punctuation
    replacements = {
        'e.p.e.': '',
        'epe': '',
        'e. p. e.': '',
        'e.p.e': '',
        ', e.p.e.': '',
        ' epe': '',
        ',': '',
        '.': '',
        '  ': ' ',  # double spaces
    }

    for old, new in replacements.items():
        name = name.replace(old, new)

    return name.strip()

# ==============================================================================
# STEP 4: Two-Stage CQMI Matching Strategy
# ==============================================================================

def expand_cqmi_with_twostage_matching(df_cqmi, df_components, uls_to_hospitals):
    """
    Two-stage CQMI matching strategy:

    Stage 1: Direct entity name matching (ULS-to-ULS)
        - Handles post-2024 reform data where both files use ULS names
        - Main components file uses "E. P. E.", CQMI uses "E.P.E."
        - Just need robust normalization

    Stage 2: Crosswalk expansion (ULS-to-hospitals)
        - Handles pre-2024 data where components file uses old hospital names
        - Expands each ULS CQMI score to ALL hospitals that compose that ULS

    This two-stage approach maximizes coverage across both pre/post reform periods.
    """
    logger.info("\n" + "=" * 80)
    logger.info("STEP 3: Two-Stage CQMI Matching")
    logger.info("=" * 80)

    # Normalize entity names in both files
    df_cqmi['entity_normalized'] = df_cqmi['entidade'].apply(normalize_entity_name)

    components_entities_normalized = {
        normalize_entity_name(e): e
        for e in df_components['entidade'].unique()
    }

    # STAGE 1: Direct entity name matching (ULS-to-ULS)
    logger.info("\n--- Stage 1: Direct Entity Name Matching (ULS-to-ULS) ---")

    matched_rows_direct = []
    matched_direct = 0
    unmatched_for_stage2 = []

    for _, row in df_cqmi.iterrows():
        entity_norm = row['entity_normalized']

        # Check if this normalized name exists in components file
        if entity_norm in components_entities_normalized:
            matched_direct += 1
            matched_row = row.copy()
            matched_row['entidade'] = components_entities_normalized[entity_norm]  # Use original name from components
            matched_row['matching_method'] = 'direct'
            matched_rows_direct.append(matched_row)
        else:
            # Not matched in Stage 1, try Stage 2
            unmatched_for_stage2.append(row)

    logger.info(f"✓ Stage 1: {matched_direct}/{df_cqmi['entidade'].nunique()} ULS entities matched directly")
    logger.info(f"  → {len(matched_rows_direct)} CQMI observations matched")

    # STAGE 2: Crosswalk expansion (ULS-to-hospitals)
    logger.info("\n--- Stage 2: Crosswalk Expansion (ULS-to-hospitals) ---")

    # Normalize ULS names in reverse mapping
    uls_normalized_mapping = {}
    for uls_name, hospitals in uls_to_hospitals.items():
        uls_normalized_mapping[normalize_entity_name(uls_name)] = hospitals

    matched_rows_crosswalk = []
    matched_crosswalk = 0
    unmatched_final = []

    for row in unmatched_for_stage2:
        uls_norm = row['entity_normalized']

        # Find matching hospitals
        if uls_norm in uls_normalized_mapping:
            matched_crosswalk += 1
            hospitals = uls_normalized_mapping[uls_norm]

            # Create one row for each hospital
            for hospital_name in hospitals:
                expanded_row = row.copy()
                expanded_row['entidade'] = hospital_name  # Replace ULS name with hospital name
                expanded_row['matching_method'] = 'crosswalk'
                expanded_row['source_uls'] = row['entidade']
                matched_rows_crosswalk.append(expanded_row)
        else:
            unmatched_final.append(row['entidade'])

    logger.info(f"✓ Stage 2: {matched_crosswalk}/{len(unmatched_for_stage2)} remaining ULS entities matched via crosswalk")
    logger.info(f"  → {len(matched_rows_crosswalk)} CQMI observations matched")

    # COMBINE BOTH STAGES
    logger.info("\n--- Combined Results ---")

    all_matched_rows = matched_rows_direct + matched_rows_crosswalk

    if len(all_matched_rows) == 0:
        logger.error("❌ CRITICAL: No ULS entities matched in either stage! Cannot proceed with empty dataset.")
        logger.error("   This indicates entity name mismatch between CQMI and components files.")
        raise ValueError("Entity matching failed - 0 ULS entities matched")

    df_cqmi_expanded = pd.DataFrame(all_matched_rows)

    total_matched_uls = matched_direct + matched_crosswalk
    logger.info(f"✓ Total matched: {total_matched_uls}/{df_cqmi['entidade'].nunique()} ULS entities")
    logger.info(f"  - Stage 1 (direct): {matched_direct} ULS → {len(matched_rows_direct)} observations")
    logger.info(f"  - Stage 2 (crosswalk): {matched_crosswalk} ULS → {len(matched_rows_crosswalk)} observations")
    logger.info(f"✓ Total CQMI observations: {len(df_cqmi_expanded)}")

    if len(unmatched_final) > 0:
        unique_unmatched = list(set(unmatched_final))
        logger.warning(f"\n⚠ Unmatched ULS entities ({len(unique_unmatched)}):")
        for uls in unique_unmatched[:5]:
            logger.warning(f"    - {uls}")
        if len(unique_unmatched) > 5:
            logger.warning(f"    ... and {len(unique_unmatched) - 5} more")

    # Keep only necessary columns
    cols_to_keep = [col for col in ['entidade', 'year', 'CQMI', 'mortality_quality_index', 'efficiency_index', 'matching_method', 'source_uls'] if col in df_cqmi_expanded.columns]
    df_cqmi_expanded = df_cqmi_expanded[cols_to_keep]

    return df_cqmi_expanded

# ==============================================================================
# STEP 5: Merge CQMI into Main Components File
# ==============================================================================

def merge_cqmi_into_components(df_components, df_cqmi_expanded):
    """Merge expanded CQMI scores into main components file."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 4: Merging CQMI into Main Components File")
    logger.info("=" * 80)

    # Before merge
    logger.info(f"Before merge:")
    logger.info(f"  - Components file: {len(df_components)} observations")
    logger.info(f"  - CQMI missing: {df_components['cqmi'].isna().sum()} ({100*df_components['cqmi'].isna().sum()/len(df_components):.1f}%)")

    # Normalize entity names for matching
    df_components['entidade_normalized'] = df_components['entidade'].apply(normalize_entity_name)
    df_cqmi_expanded['entidade_normalized'] = df_cqmi_expanded['entidade'].apply(normalize_entity_name)

    # Convert year to int for matching
    df_cqmi_expanded['year'] = df_cqmi_expanded['year'].astype(int)

    # Merge on normalized entity name + year
    df_merged = df_components.merge(
        df_cqmi_expanded[['entidade_normalized', 'year', 'CQMI', 'mortality_quality_index', 'efficiency_index']],
        on=['entidade_normalized', 'year'],
        how='left',
        suffixes=('_old', '_new')
    )

    # Update CQMI columns (replace NaN with new values)
    df_merged['cqmi'] = df_merged['CQMI'].combine_first(df_merged['cqmi'])
    df_merged['cqmi_mortality'] = df_merged['mortality_quality_index'].combine_first(df_merged['cqmi_mortality'])

    # Drop temporary columns
    df_merged = df_merged.drop(columns=['entidade_normalized', 'CQMI', 'mortality_quality_index', 'efficiency_index'], errors='ignore')

    # After merge
    logger.info(f"\nAfter merge:")
    logger.info(f"  - Total observations: {len(df_merged)}")
    logger.info(f"  - CQMI available: {df_merged['cqmi'].notna().sum()} ({100*df_merged['cqmi'].notna().sum()/len(df_merged):.1f}%)")
    logger.info(f"  - CQMI still missing: {df_merged['cqmi'].isna().sum()} ({100*df_merged['cqmi'].isna().sum()/len(df_merged):.1f}%)")

    # Year breakdown
    cqmi_by_year = df_merged.groupby('year')['cqmi'].apply(lambda x: x.notna().sum())
    logger.info(f"\n  CQMI coverage by year:")
    for year, count in cqmi_by_year.items():
        total = len(df_merged[df_merged['year'] == year])
        logger.info(f"    {year}: {count}/{total} ({100*count/total:.1f}%)")

    return df_merged

# ==============================================================================
# STEP 6: Calculate Complete 5-Component PHFSI
# ==============================================================================

def calculate_complete_phfsi(df):
    """
    Calculate complete 5-component PHFSI including CQMI.

    PHFSI = (1/5) * [OSSR + (1 - SPI) + LRR + (1 - TLR) + CQMI]

    All components normalized to [0, 1] where higher = better sustainability.
    """
    logger.info("\n" + "=" * 80)
    logger.info("STEP 5: Calculating Complete 5-Component PHFSI")
    logger.info("=" * 80)

    # Check which components are available
    df['has_ossr'] = df['ossr'].notna()
    df['has_spi'] = df['spi'].notna()
    df['has_lrr'] = df['lrr'].notna()
    df['has_tlr'] = df['tlr'].notna()
    df['has_cqmi'] = df['cqmi'].notna()

    # Count available components
    df['n_components'] = (
        df['has_ossr'].astype(int) +
        df['has_spi'].astype(int) +
        df['has_lrr'].astype(int) +
        df['has_tlr'].astype(int) +
        df['has_cqmi'].astype(int)
    )

    logger.info(f"Component availability:")
    logger.info(f"  - OSSR: {df['has_ossr'].sum()} ({100*df['has_ossr'].sum()/len(df):.1f}%)")
    logger.info(f"  - SPI: {df['has_spi'].sum()} ({100*df['has_spi'].sum()/len(df):.1f}%)")
    logger.info(f"  - LRR: {df['has_lrr'].sum()} ({100*df['has_lrr'].sum()/len(df):.1f}%)")
    logger.info(f"  - TLR: {df['has_tlr'].sum()} ({100*df['has_tlr'].sum()/len(df):.1f}%)")
    logger.info(f"  - CQMI: {df['has_cqmi'].sum()} ({100*df['has_cqmi'].sum()/len(df):.1f}%)")

    logger.info(f"\nComplete case distribution:")
    for n in range(6):
        count = (df['n_components'] == n).sum()
        logger.info(f"  - {n} components: {count} observations ({100*count/len(df):.1f}%)")

    # Calculate 5-component PHFSI (only when ALL 5 components available)
    df['phfsi_5comp'] = np.nan

    mask_complete = df['n_components'] == 5
    n_complete = mask_complete.sum()

    if n_complete > 0:
        df.loc[mask_complete, 'phfsi_5comp'] = (
            df.loc[mask_complete, 'ossr'] +
            (1 - df.loc[mask_complete, 'spi']) +
            df.loc[mask_complete, 'lrr'] +
            (1 - df.loc[mask_complete, 'tlr']) +
            df.loc[mask_complete, 'cqmi']
        ) / 5

        logger.info(f"\n✓ Calculated 5-component PHFSI for {n_complete} complete observations")
        logger.info(f"  - Mean: {df.loc[mask_complete, 'phfsi_5comp'].mean():.3f}")
        logger.info(f"  - SD: {df.loc[mask_complete, 'phfsi_5comp'].std():.3f}")
        logger.info(f"  - Range: [{df.loc[mask_complete, 'phfsi_5comp'].min():.3f}, {df.loc[mask_complete, 'phfsi_5comp'].max():.3f}]")
    else:
        logger.warning(f"⚠ No complete observations with all 5 components!")

    # Calculate 4-component PHFSI (without CQMI) for comparison
    df['phfsi_4comp'] = np.nan

    mask_4comp = (df['has_ossr'] & df['has_spi'] & df['has_lrr'] & df['has_tlr'])
    n_4comp = mask_4comp.sum()

    if n_4comp > 0:
        df.loc[mask_4comp, 'phfsi_4comp'] = (
            df.loc[mask_4comp, 'ossr'] +
            (1 - df.loc[mask_4comp, 'spi']) +
            df.loc[mask_4comp, 'lrr'] +
            (1 - df.loc[mask_4comp, 'tlr'])
        ) / 4

        logger.info(f"\n✓ Calculated 4-component PHFSI for {n_4comp} observations (for comparison)")
        logger.info(f"  - Mean: {df.loc[mask_4comp, 'phfsi_4comp'].mean():.3f}")
        logger.info(f"  - SD: {df.loc[mask_4comp, 'phfsi_4comp'].std():.3f}")

    return df

# ==============================================================================
# STEP 7: Compare 4-Component vs 5-Component PHFSI
# ==============================================================================

def compare_4comp_vs_5comp(df):
    """Compare 4-component (no CQMI) vs 5-component (with CQMI) PHFSI."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 6: Comparing 4-Component vs 5-Component PHFSI")
    logger.info("=" * 80)

    # Find observations with both versions
    df_both = df[(df['phfsi_4comp'].notna()) & (df['phfsi_5comp'].notna())].copy()

    if len(df_both) == 0:
        logger.warning("⚠ No observations with both 4-comp and 5-comp PHFSI for comparison")
        return None

    logger.info(f"✓ {len(df_both)} observations with both 4-comp and 5-comp PHFSI")

    # Correlation
    from scipy.stats import pearsonr, spearmanr

    r_pearson, p_pearson = pearsonr(df_both['phfsi_4comp'], df_both['phfsi_5comp'])
    r_spearman, p_spearman = spearmanr(df_both['phfsi_4comp'], df_both['phfsi_5comp'])

    logger.info(f"\nCorrelation between 4-comp and 5-comp:")
    logger.info(f"  - Pearson r = {r_pearson:.4f} (p = {p_pearson:.4e})")
    logger.info(f"  - Spearman ρ = {r_spearman:.4f} (p = {p_spearman:.4e})")

    # Descriptive differences
    df_both['diff'] = df_both['phfsi_5comp'] - df_both['phfsi_4comp']
    df_both['abs_diff'] = df_both['diff'].abs()

    logger.info(f"\nDifferences (5-comp minus 4-comp):")
    logger.info(f"  - Mean difference: {df_both['diff'].mean():.4f}")
    logger.info(f"  - SD of difference: {df_both['diff'].std():.4f}")
    logger.info(f"  - Mean absolute difference: {df_both['abs_diff'].mean():.4f}")
    logger.info(f"  - Max absolute difference: {df_both['abs_diff'].max():.4f}")

    # Rank correlation
    df_both['rank_4comp'] = df_both['phfsi_4comp'].rank()
    df_both['rank_5comp'] = df_both['phfsi_5comp'].rank()
    df_both['rank_diff'] = (df_both['rank_5comp'] - df_both['rank_4comp']).abs()

    logger.info(f"\nRank differences:")
    logger.info(f"  - Mean rank difference: {df_both['rank_diff'].mean():.1f} positions")
    logger.info(f"  - Max rank difference: {df_both['rank_diff'].max():.0f} positions")

    # Interpretation
    if r_pearson >= 0.90:
        conclusion = "VERY HIGH correlation - versions are nearly identical"
    elif r_pearson >= 0.75:
        conclusion = "HIGH correlation - versions are similar"
    elif r_pearson >= 0.50:
        conclusion = "MODERATE correlation - versions differ meaningfully"
    else:
        conclusion = "LOW correlation - versions differ substantially"

    logger.info(f"\n{'=' * 80}")
    logger.info(f"CONCLUSION: {conclusion}")
    logger.info(f"{'=' * 80}")

    return df_both

# ==============================================================================
# STEP 8: Save Results
# ==============================================================================

def save_results(df):
    """Save integrated components with complete 5-component PHFSI."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 7: Saving Results")
    logger.info("=" * 80)

    # Save updated components file
    output_path = DATA_DIR / "processed" / "variables" / "phfsi_components_complete.parquet"
    df.to_parquet(output_path, index=False)
    logger.info(f"✓ Saved complete components file: {output_path}")
    logger.info(f"  - {len(df)} observations")
    logger.info(f"  - {df.shape[1]} columns")

    # Save summary statistics
    summary_path = OUTPUT_DIR / "results" / "descriptive" / "phfsi_5comp_summary.csv"
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    summary_stats = df[['phfsi_4comp', 'phfsi_5comp']].describe()
    summary_stats.to_csv(summary_path)
    logger.info(f"✓ Saved summary statistics: {summary_path}")

    # Save observations with complete 5-component PHFSI
    df_complete = df[df['phfsi_5comp'].notna()].copy()
    complete_path = DATA_DIR / "processed" / "variables" / "phfsi_5comp_complete_observations.parquet"
    df_complete.to_parquet(complete_path, index=False)
    logger.info(f"✓ Saved complete 5-comp observations: {complete_path}")
    logger.info(f"  - {len(df_complete)} observations with all 5 components")

    logger.info(f"\n{'=' * 80}")
    logger.info(f"INTEGRATION COMPLETE")
    logger.info(f"{'=' * 80}")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("CQMI Integration and Complete 5-Component PHFSI Calculation")
    logger.info("=" * 80)
    logger.info(f"Project root: {PROJECT_ROOT}")
    logger.info(f"Data directory: {DATA_DIR}")
    logger.info(f"Output directory: {OUTPUT_DIR}")
    logger.info("")

    try:
        # Step 1: Load data
        df_components, df_cqmi, df_crosswalk = load_data()

        # Step 2: Create reverse mapping
        uls_to_hospitals = create_reverse_mapping(df_crosswalk)

        # Step 3: Two-stage matching (direct + crosswalk)
        df_cqmi_expanded = expand_cqmi_with_twostage_matching(df_cqmi, df_components, uls_to_hospitals)

        # Step 4: Merge CQMI into components
        df_merged = merge_cqmi_into_components(df_components, df_cqmi_expanded)

        # Step 5: Calculate complete 5-component PHFSI
        df_final = calculate_complete_phfsi(df_merged)

        # Step 6: Compare 4-comp vs 5-comp
        df_comparison = compare_4comp_vs_5comp(df_final)

        # Step 7: Save results
        save_results(df_final)

        logger.info("\n" + "=" * 80)
        logger.info("SUCCESS: CQMI integration completed successfully")
        logger.info("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"\nERROR: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
