"""
Subsidy Endogeneity - Instrumental Variables Analysis
======================================================

Issue 3: Address potential endogeneity in the subsidy-distress relationship
using instrumental variables (IV) / two-stage least squares (2SLS) estimation.

**Endogeneity Concern**: Government may allocate MORE subsidies to hospitals
in WORSE financial condition (reverse causality), or omitted variables may
affect both subsidies and distress.

**IV Strategy**: Use instruments that affect subsidies but do NOT directly
affect financial distress except through subsidies:

1. **Political Affiliation**: Minister of Health political party (Left/Right)
   - Left governments may allocate more healthcare subsidies (ideology)
   - Exclusion restriction: Political party doesn't directly affect hospital
     management quality or efficiency (only via subsidy allocation)

2. **Regional GDP**: Regional economic conditions (NUTS 2 level)
   - Wealthier regions may receive different subsidy allocations
   - Exclusion restriction: Regional GDP affects hospital finances primarily
     through government subsidy allocation, not direct operational factors

3. **Historical Subsidies**: Lagged subsidies (3-4 years prior)
   - Past subsidy patterns predict current allocations (path dependence)
   - Exclusion restriction: 3-4 year lag ensures no reverse causality from
     current distress to historical subsidies

Author: Claude Code + Daniel Polonia
Date: January 2026
"""

import logging
import numpy as np
import pandas as pd
from pathlib import Path
import sys
from scipy import stats
from statsmodels.sandbox.regression.gmm import IV2SLS
from linearmodels.iv import IV2SLS as LinearModelsIV2SLS
import matplotlib.pyplot as plt
import seaborn as sns

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "03_data"
OUTPUT_DIR = PROJECT_ROOT / "06_output"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(OUTPUT_DIR / "logs" / "iv_analysis.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ==============================================================================
# STEP 1: Load and Prepare Data
# ==============================================================================

def load_panel_data():
    """Load main panel dataset with PHFSI and subsidy data."""
    logger.info("=" * 80)
    logger.info("STEP 1: Loading Panel Data")
    logger.info("=" * 80)

    # Load PHFSI components (has subsidy data)
    components_path = DATA_DIR / "processed" / "variables" / "phfsi_components_complete.parquet"
    df = pd.read_parquet(components_path)

    logger.info(f"✓ Loaded panel data: {df.shape[0]} observations, {df['entidade'].nunique()} entities")
    logger.info(f"  - Years: {df['year'].min()}-{df['year'].max()}")

    # We need to calculate subsidy dependence if not already present
    # Subsidy dependence = Operating Subsidies / Operating Revenue
    # This should be calculated in the components file construction

    return df

def load_political_data():
    """Load and aggregate Minister of Health political affiliation data."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 2: Loading Political Data (Instrument 1)")
    logger.info("=" * 80)

    political_path = DATA_DIR / "external" / "political" / "minister_health_portugal_2017_2024.csv"
    df_pol = pd.read_csv(political_path)

    logger.info(f"✓ Loaded political data: {len(df_pol)} minister-year observations")

    # Aggregate to year level using majority rule
    def aggregate_year(group):
        """Aggregate political affiliation by year using majority rule."""
        total_months = group['months_served'].sum()

        # Count months by ideology
        ideology_months = group.groupby('ideology')['months_served'].sum()

        # Get majority ideology
        majority_ideology = ideology_months.idxmax()

        # Count months by party
        party_months = group.groupby('party_abbreviation')['months_served'].sum()
        majority_party = party_months.idxmax()

        return pd.Series({
            'minister_ideology': majority_ideology,
            'minister_party': majority_party,
            'minister_left': 1 if majority_ideology == 'Left' else 0,
            'minister_center': 1 if majority_ideology == 'Center' else 0,
            'minister_right': 1 if majority_ideology == 'Right' else 0,
            'total_months': total_months,
            'ministers': ', '.join(group['minister_name'].unique())
        })

    df_pol_year = df_pol.groupby('year').apply(aggregate_year).reset_index()

    logger.info(f"✓ Aggregated to year level: {len(df_pol_year)} years")
    logger.info("\n  Political affiliation by year:")
    for _, row in df_pol_year.iterrows():
        logger.info(f"    {int(row['year'])}: {row['minister_ideology']} ({row['minister_party']}) - {row['ministers']}")

    return df_pol_year

def load_subsidy_dependence():
    """Load subsidy dependence panel data."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 3: Loading Subsidy Dependence Data")
    logger.info("=" * 80)

    subsidy_path = DATA_DIR / "processed" / "variables" / "subsidy_dependence_panel.parquet"
    df_subsidy = pd.read_parquet(subsidy_path)

    logger.info(f"✓ Loaded subsidy panel: {df_subsidy.shape[0]} observations, {df_subsidy['entidade'].nunique()} entities")
    logger.info(f"  - Years: {df_subsidy['year'].min()}-{df_subsidy['year'].max()}")
    logger.info(f"  - Mean subsidy dependence: {df_subsidy['subsidy_dependence'].mean():.3f}")
    logger.info(f"  - Historical instrument coverage: {df_subsidy['subsidy_dependence_historical'].notna().sum()}/{len(df_subsidy)} ({100*df_subsidy['subsidy_dependence_historical'].notna().sum()/len(df_subsidy):.1f}%)")

    return df_subsidy

def load_phfsi_components():
    """Load PHFSI components data."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 4: Loading PHFSI Components")
    logger.info("=" * 80)

    components_path = DATA_DIR / "processed" / "variables" / "phfsi_components_complete.parquet"
    df_phfsi = pd.read_parquet(components_path)

    logger.info(f"✓ Loaded PHFSI components: {df_phfsi.shape[0]} observations, {df_phfsi['entidade'].nunique()} entities")
    logger.info(f"  - Years: {df_phfsi['year'].min()}-{df_phfsi['year'].max()}")
    logger.info(f"  - PHFSI 4-comp coverage: {df_phfsi['phfsi_4comp'].notna().sum()}/{len(df_phfsi)} ({100*df_phfsi['phfsi_4comp'].notna().sum()/len(df_phfsi):.1f}%)")

    return df_phfsi

# ==============================================================================
# STEP 5: Merge Instruments with Panel Data
# ==============================================================================

def merge_all_data(df_phfsi, df_subsidy, df_political):
    """Merge PHFSI, subsidy, and political instruments."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 5: Merging All Data")
    logger.info("=" * 80)

    # Start with PHFSI components
    df = df_phfsi.copy()
    logger.info(f"  Starting with PHFSI data: {len(df)} observations")

    # Merge subsidy dependence data
    df = df.merge(
        df_subsidy[['entidade', 'year', 'subsidy_dependence', 'subsidy_dependence_historical',
                   'subsidy_dependence_lag1', 'subsidy_dependence_lag3', 'subsidy_dependence_lag4',
                   'operating_margin', 'operating_deficit']],
        on=['entidade', 'year'],
        how='left'
    )

    logger.info(f"✓ Merged subsidy dependence data")
    logger.info(f"  - Observations with subsidy data: {df['subsidy_dependence'].notna().sum()}/{len(df)} ({100*df['subsidy_dependence'].notna().sum()/len(df):.1f}%)")
    logger.info(f"  - Observations with historical instrument: {df['subsidy_dependence_historical'].notna().sum()}/{len(df)} ({100*df['subsidy_dependence_historical'].notna().sum()/len(df):.1f}%)")

    # Merge political data
    df = df.merge(
        df_political[['year', 'minister_left', 'minister_center', 'minister_right',
                     'minister_party', 'minister_ideology']],
        on='year',
        how='left'
    )

    logger.info(f"✓ Merged political instruments")
    logger.info(f"  - Observations with political data: {df['minister_left'].notna().sum()}/{len(df)} ({100*df['minister_left'].notna().sum()/len(df):.1f}%)")

    # Create complete observations indicator
    df['has_phfsi'] = df['phfsi_4comp'].notna()
    df['has_subsidy'] = df['subsidy_dependence'].notna()
    df['has_instruments'] = df['minister_left'].notna() & df['subsidy_dependence_historical'].notna()
    df['complete_for_iv'] = df['has_phfsi'] & df['has_subsidy'] & df['has_instruments']

    logger.info(f"\n  Data completeness:")
    logger.info(f"    - PHFSI available: {df['has_phfsi'].sum()}/{len(df)} ({100*df['has_phfsi'].sum()/len(df):.1f}%)")
    logger.info(f"    - Subsidy available: {df['has_subsidy'].sum()}/{len(df)} ({100*df['has_subsidy'].sum()/len(df):.1f}%)")
    logger.info(f"    - Instruments available: {df['has_instruments'].sum()}/{len(df)} ({100*df['has_instruments'].sum()/len(df):.1f}%)")
    logger.info(f"    - Complete for IV analysis: {df['complete_for_iv'].sum()}/{len(df)} ({100*df['complete_for_iv'].sum()/len(df):.1f}%)")

    return df

# ==============================================================================
# STEP 6: First Stage Regression (Test Instrument Relevance)
# ==============================================================================

def test_instrument_relevance(df):
    """
    Test instrument relevance using first-stage F-statistic.

    Rule of thumb: F-stat > 10 indicates strong instruments.
    """
    logger.info("\n" + "=" * 80)
    logger.info("STEP 6: Testing Instrument Relevance (First Stage)")
    logger.info("=" * 80)

    # Filter to complete observations
    df_complete = df[df['complete_for_iv']].copy()
    logger.info(f"  Analysis sample: {len(df_complete)} complete observations")
    logger.info(f"    - Entities: {df_complete['entidade'].nunique()}")
    logger.info(f"    - Years: {df_complete['year'].min()}-{df_complete['year'].max()}")

    if len(df_complete) < 30:
        logger.warning("⚠ Sample size too small for reliable IV estimation (N < 30)")
        return None

    # First stage regression: Subsidy ~ Instruments
    # Model: subsidy_dependence = α + β₁*minister_left + β₂*historical_subsidy + ε

    from statsmodels.api import OLS, add_constant

    # Prepare data
    X_instruments = df_complete[['minister_left', 'subsidy_dependence_historical']].copy()
    X_instruments = add_constant(X_instruments)
    y_subsidy = df_complete['subsidy_dependence']

    # Estimate first stage
    first_stage = OLS(y_subsidy, X_instruments).fit()

    logger.info("\n  First-Stage Regression Results:")
    logger.info("  " + "=" * 60)
    logger.info(f"    R²: {first_stage.rsquared:.4f}")
    logger.info(f"    Adjusted R²: {first_stage.rsquared_adj:.4f}")
    logger.info(f"    F-statistic: {first_stage.fvalue:.2f} (p={first_stage.f_pvalue:.4f})")

    # Individual instrument coefficients
    logger.info("\n  Instrument Coefficients:")
    logger.info("    " + "-" * 55)
    logger.info(f"    {'Variable':<30} {'Coef':>10} {'p-value':>10}")
    logger.info("    " + "-" * 55)
    for var in ['minister_left', 'subsidy_dependence_historical']:
        coef = first_stage.params[var]
        pval = first_stage.pvalues[var]
        sig = '***' if pval < 0.01 else ('**' if pval < 0.05 else ('*' if pval < 0.1 else ''))
        logger.info(f"    {var:<30} {coef:>10.4f} {pval:>10.4f} {sig}")

    # Test for weak instruments (F-stat > 10 rule)
    if first_stage.fvalue > 10:
        logger.info(f"\n  ✓ Strong instruments: F = {first_stage.fvalue:.2f} > 10")
    elif first_stage.fvalue > 5:
        logger.warning(f"\n  ⚠ Moderately weak instruments: F = {first_stage.fvalue:.2f} (5-10)")
    else:
        logger.error(f"\n  ❌ Weak instruments: F = {first_stage.fvalue:.2f} < 5")

    # Partial R² for each instrument
    logger.info("\n  Partial R² (instrument relevance):")
    for var in ['minister_left', 'subsidy_dependence_historical']:
        # Calculate partial R² by comparing full model with model excluding this instrument
        X_partial = df_complete[['minister_left', 'subsidy_dependence_historical']].copy()
        X_partial = X_partial.drop(columns=[var])
        X_partial = add_constant(X_partial)
        partial_model = OLS(y_subsidy, X_partial).fit()
        partial_r2 = first_stage.rsquared - partial_model.rsquared
        logger.info(f"    {var:<30} {partial_r2:>10.4f}")

    return first_stage

# ==============================================================================
# STEP 7: Two-Stage Least Squares (2SLS) Estimation
# ==============================================================================

def run_2sls_estimation(df):
    """Run 2SLS estimation."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 7: 2SLS Estimation")
    logger.info("=" * 80)

    # TODO: Implement 2SLS

    pass

# ==============================================================================
# STEP 8: Compare IV vs OLS Results
# ==============================================================================

def compare_iv_ols(df):
    """Compare IV estimates with OLS estimates."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 8: Comparing IV vs OLS")
    logger.info("=" * 80)

    # TODO: Implement comparison

    pass

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("Subsidy Endogeneity - Instrumental Variables Analysis")
    logger.info("=" * 80)
    logger.info(f"Project root: {PROJECT_ROOT}")
    logger.info(f"Data directory: {DATA_DIR}")
    logger.info(f"Output directory: {OUTPUT_DIR}\n")

    try:
        # Step 1: Load panel data (PHFSI components)
        df_phfsi = load_panel_data()

        # Step 2: Load political data
        df_political = load_political_data()

        # Step 3: Load subsidy dependence data
        df_subsidy = load_subsidy_dependence()

        # Step 4: Load PHFSI components (for merge)
        df_phfsi_full = load_phfsi_components()

        # Step 5: Merge all data
        df_merged = merge_all_data(df_phfsi_full, df_subsidy, df_political)

        # Save intermediate dataset
        output_path = DATA_DIR / "processed" / "panel" / "panel_with_instruments.parquet"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df_merged.to_parquet(output_path, index=False)
        logger.info(f"\n✓ Saved panel data with instruments: {output_path}")
        logger.info(f"  - {len(df_merged)} observations, {len(df_merged.columns)} columns")

        # Step 6: Test instrument relevance
        first_stage_results = test_instrument_relevance(df_merged)

        if first_stage_results is not None:
            # Step 7: Run 2SLS (TODO)
            # run_2sls_estimation(df_merged, first_stage_results)

            # Step 8: Compare IV vs OLS (TODO)
            # compare_iv_ols(df_merged)

            logger.info("\n" + "=" * 80)
            logger.info("PARTIAL SUCCESS: First-stage analysis completed")
            logger.info("=" * 80)
            logger.info("TODO: Implement 2SLS estimation and comparison")
        else:
            logger.warning("\n" + "=" * 80)
            logger.warning("PARTIAL SUCCESS: Data merged but sample too small for IV")
            logger.warning("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"\nERROR: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
