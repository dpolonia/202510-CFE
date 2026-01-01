"""
Subsidy Dependence and PHFSI - Panel Regression Analysis
=========================================================

Since IV approach faces weak instrument problem (F=2.26 < 10), we use
OLS panel regressions with robustness checks:

1. Fixed effects (entity + year) to control for unobserved heterogeneity
2. Lagged subsidy as control for reverse causality concerns
3. Cluster-robust standard errors

**Research Question**: Does higher subsidy dependence → lower PHFSI?

**H1 (Moral Hazard)**: Higher subsidy dependence → lower financial sustainability

Author: Claude Code + Daniel Polonia
Date: January 2026
"""

import logging
import numpy as np
import pandas as pd
from pathlib import Path
import sys
from statsmodels.api import OLS, add_constant
from linearmodels.panel import PanelOLS
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
        logging.FileHandler(OUTPUT_DIR / "logs" / "panel_regressions.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ==============================================================================
# STEP 1: Load Data
# ==============================================================================

def load_panel_data():
    """Load panel data with instruments."""
    logger.info("=" * 80)
    logger.info("Loading Panel Data for Regression Analysis")
    logger.info("=" * 80)

    panel_path = DATA_DIR / "processed" / "panel" / "panel_with_instruments.parquet"
    df = pd.read_parquet(panel_path)

    logger.info(f"✓ Loaded panel data: {df.shape[0]} observations")
    logger.info(f"  - Entities: {df['entidade'].nunique()}")
    logger.info(f"  - Years: {df['year'].min()}-{df['year'].max()}")

    return df

# ==============================================================================
# STEP 2: Prepare Regression Sample
# ==============================================================================

def prepare_regression_sample(df):
    """Prepare regression sample with required variables."""
    logger.info("\n" + "=" * 80)
    logger.info("Preparing Regression Sample")
    logger.info("=" * 80)

    # Filter to observations with PHFSI and subsidy data
    df_reg = df[(df['phfsi_4comp'].notna()) & (df['subsidy_dependence'].notna())].copy()

    logger.info(f"  Regression sample: {len(df_reg)} observations")
    logger.info(f"    - Entities: {df_reg['entidade'].nunique()}")
    logger.info(f"    - Years: {df_reg['year'].min()}-{df_reg['year'].max()}")

    # Create COVID indicator
    df_reg['covid'] = ((df_reg['year'] == 2020) | (df_reg['year'] == 2021)).astype(int)

    # Create time trend
    df_reg['time_trend'] = df_reg['year'] - df_reg['year'].min()

    # Log summary statistics
    logger.info("\n  Variable summary:")
    logger.info(f"    - PHFSI 4-comp: Mean={df_reg['phfsi_4comp'].mean():.3f}, SD={df_reg['phfsi_4comp'].std():.3f}")
    logger.info(f"    - Subsidy dependence: Mean={df_reg['subsidy_dependence'].mean():.3f}, SD={df_reg['subsidy_dependence'].std():.3f}")
    logger.info(f"    - COVID observations: {df_reg['covid'].sum()}/{len(df_reg)} ({100*df_reg['covid'].sum()/len(df_reg):.1f}%)")

    # Check for lagged subsidy availability
    has_lag = df_reg['subsidy_dependence_lag1'].notna().sum()
    logger.info(f"    - Lagged subsidy (t-1) available: {has_lag}/{len(df_reg)} ({100*has_lag/len(df_reg):.1f}%)")

    return df_reg

# ==============================================================================
# STEP 3: OLS Baseline (Pooled)
# ==============================================================================

def run_pooled_ols(df):
    """Run pooled OLS as baseline."""
    logger.info("\n" + "=" * 80)
    logger.info("Model 1: Pooled OLS (Baseline)")
    logger.info("=" * 80)

    # Simple model: PHFSI ~ Subsidy + COVID
    X = df[['subsidy_dependence', 'covid']].copy()
    X = add_constant(X)
    y = df['phfsi_4comp']

    model = OLS(y, X).fit(cov_type='HC3')  # Heteroskedasticity-robust SEs

    logger.info("\n  Results:")
    logger.info(f"    R²: {model.rsquared:.4f}")
    logger.info(f"    Adjusted R²: {model.rsquared_adj:.4f}")
    logger.info(f"    N: {int(model.nobs)}")

    logger.info("\n  Coefficients:")
    logger.info("    " + "-" * 60)
    logger.info(f"    {'Variable':<30} {'Coef':>10} {'SE':>10} {'p-value':>10}")
    logger.info("    " + "-" * 60)
    for var in ['subsidy_dependence', 'covid']:
        coef = model.params[var]
        se = model.bse[var]
        pval = model.pvalues[var]
        sig = '***' if pval < 0.01 else ('**' if pval < 0.05 else ('*' if pval < 0.1 else ''))
        logger.info(f"    {var:<30} {coef:>10.4f} {se:>10.4f} {pval:>10.4f} {sig}")

    return model

# ==============================================================================
# STEP 4: Fixed Effects Panel Regression
# ==============================================================================

def run_fixed_effects(df):
    """Run entity and year fixed effects panel regression."""
    logger.info("\n" + "=" * 80)
    logger.info("Model 2: Fixed Effects (Entity + Year)")
    logger.info("=" * 80)

    # Prepare panel data
    df_panel = df.set_index(['entidade', 'year'])

    # Model: PHFSI ~ Subsidy
    # Fixed effects absorb entity-specific and year-specific effects
    # NOTE: COVID variable absorbed by year FE, so excluded
    from linearmodels.panel import PanelOLS

    # Define dependent and independent variables
    dependent = df_panel[['phfsi_4comp']]
    exog = df_panel[['subsidy_dependence']]

    # Estimate with two-way fixed effects
    model = PanelOLS(dependent, exog, entity_effects=True, time_effects=True).fit(
        cov_type='clustered',
        cluster_entity=True
    )

    logger.info("\n  Results:")
    logger.info(f"    R² (within): {model.rsquared:.4f}")
    logger.info(f"    R² (overall): {model.rsquared_overall:.4f}")
    logger.info(f"    R² (between): {model.rsquared_between:.4f}")
    logger.info(f"    N: {int(model.nobs)}")
    logger.info(f"    Entities: {model.entity_info['total']}")

    logger.info("\n  Coefficients (cluster-robust SEs):")
    logger.info("    " + "-" * 60)
    logger.info(f"    {'Variable':<30} {'Coef':>10} {'SE':>10} {'p-value':>10}")
    logger.info("    " + "-" * 60)
    for var in ['subsidy_dependence']:
        coef = model.params[var]
        se = model.std_errors[var]
        pval = model.pvalues[var]
        sig = '***' if pval < 0.01 else ('**' if pval < 0.05 else ('*' if pval < 0.1 else ''))
        logger.info(f"    {var:<30} {coef:>10.4f} {se:>10.4f} {pval:>10.4f} {sig}")

    logger.info("\n  Note: COVID absorbed by year fixed effects")

    return model

# ==============================================================================
# STEP 5: Robustness - Add Lagged Subsidy
# ==============================================================================

def run_lagged_control(df):
    """Add lagged subsidy to control for persistence/reverse causality."""
    logger.info("\n" + "=" * 80)
    logger.info("Model 3: Fixed Effects + Lagged Subsidy Control")
    logger.info("=" * 80)

    # Filter to observations with lagged subsidy
    df_lag = df[df['subsidy_dependence_lag1'].notna()].copy()
    logger.info(f"  Sample with lagged subsidy: {len(df_lag)} observations")

    # Prepare panel
    df_panel = df_lag.set_index(['entidade', 'year'])

    # Model: PHFSI ~ Subsidy(t) + Subsidy(t-1)
    dependent = df_panel[['phfsi_4comp']]
    exog = df_panel[['subsidy_dependence', 'subsidy_dependence_lag1']]

    from linearmodels.panel import PanelOLS
    model = PanelOLS(dependent, exog, entity_effects=True, time_effects=True).fit(
        cov_type='clustered',
        cluster_entity=True
    )

    logger.info("\n  Results:")
    logger.info(f"    R² (within): {model.rsquared:.4f}")
    logger.info(f"    N: {int(model.nobs)}")

    logger.info("\n  Coefficients:")
    logger.info("    " + "-" * 60)
    logger.info(f"    {'Variable':<30} {'Coef':>10} {'SE':>10} {'p-value':>10}")
    logger.info("    " + "-" * 60)
    for var in ['subsidy_dependence', 'subsidy_dependence_lag1']:
        coef = model.params[var]
        se = model.std_errors[var]
        pval = model.pvalues[var]
        sig = '***' if pval < 0.01 else ('**' if pval < 0.05 else ('*' if pval < 0.1 else ''))
        logger.info(f"    {var:<30} {coef:>10.4f} {se:>10.4f} {pval:>10.4f} {sig}")

    logger.info("\n  Note: COVID absorbed by year fixed effects")

    return model

# ==============================================================================
# STEP 6: Generate Regression Table
# ==============================================================================

def generate_regression_table(models, output_path):
    """Generate publication-ready regression table."""
    logger.info("\n" + "=" * 80)
    logger.info("Generating Regression Table")
    logger.info("=" * 80)

    # Extract results from all models
    # TODO: Format as LaTeX table

    logger.info(f"✓ Table saved: {output_path}")

    return output_path

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("Subsidy Dependence and PHFSI - Panel Regression Analysis")
    logger.info("=" * 80)
    logger.info(f"Project root: {PROJECT_ROOT}\n")

    try:
        # Step 1: Load data
        df = load_panel_data()

        # Step 2: Prepare regression sample
        df_reg = prepare_regression_sample(df)

        # Step 3: Pooled OLS baseline
        model1 = run_pooled_ols(df_reg)

        # Step 4: Fixed effects
        model2 = run_fixed_effects(df_reg)

        # Step 5: Lagged subsidy control
        model3 = run_lagged_control(df_reg)

        # Step 6: Generate table
        # table_path = OUTPUT_DIR / "tables" / "main" / "table_subsidy_phfsi.tex"
        # generate_regression_table([model1, model2, model3], table_path)

        logger.info("\n" + "=" * 80)
        logger.info("SUCCESS: Panel regression analysis completed")
        logger.info("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"\nERROR: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
