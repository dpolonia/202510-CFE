"""
Construct Subsidy Dependence Variable
======================================

Calculate subsidy dependence from SNS financial data for use in IV analysis.

**Rationale**: Government subsidies cover operating deficits. When hospitals
have negative operating results, they require government transfers to continue
operations.

**Calculation**:
    Subsidy Dependence = |min(0, Operating Results)| / Operating Revenue

    Alternative formulation:
    Subsidy Dependence = (Operating Expenses - Operating Revenue) / Operating Revenue

**Output**: Hospital-year panel with subsidy dependence variable

Author: Claude Code + Daniel Polonia
Date: January 2026
"""

import logging
import numpy as np
import pandas as pd
from pathlib import Path
import sys

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "03_data"
OUTPUT_DIR = PROJECT_ROOT / "06_output"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(OUTPUT_DIR / "logs" / "subsidy_dependence.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ==============================================================================
# STEP 1: Load Financial Data
# ==============================================================================

def load_financial_data():
    """Load SNS financial aggregates data."""
    logger.info("=" * 80)
    logger.info("STEP 1: Loading Financial Data")
    logger.info("=" * 80)

    financial_path = DATA_DIR / "processed" / "financial" / "agregados-economico-financeiros.parquet"
    df = pd.read_parquet(financial_path)

    logger.info(f"✓ Loaded financial data: {df.shape[0]} observations")
    logger.info(f"  - Entities: {df['entidade'].nunique()}")
    logger.info(f"  - Date range: {df['tempo'].min()} to {df['tempo'].max()}")

    # Convert tempo to datetime
    df['tempo'] = pd.to_datetime(df['tempo'])
    df['year'] = df['tempo'].dt.year
    df['month'] = df['tempo'].dt.month

    logger.info(f"  - Years: {df['year'].min()}-{df['year'].max()}")

    return df

# ==============================================================================
# STEP 2: Calculate Subsidy Dependence
# ==============================================================================

def calculate_subsidy_dependence(df):
    """
    Calculate subsidy dependence at observation level.

    Logic:
    - If operating results < 0 → government must subsidize the deficit
    - Subsidy dependence = |negative operating results| / operating revenue
    - If operating results >= 0 → no subsidy needed (subsidy_dependence = 0)
    """
    logger.info("\n" + "=" * 80)
    logger.info("STEP 2: Calculating Subsidy Dependence")
    logger.info("=" * 80)

    # Calculate operating deficit (only when negative)
    df['operating_deficit'] = df['resultados_operacionais'].apply(lambda x: abs(min(0, x)))

    # Calculate subsidy dependence
    # Handle division by zero: if revenue = 0, set subsidy_dependence = NaN
    df['subsidy_dependence'] = np.where(
        df['rendimentos_operacionais'] > 0,
        df['operating_deficit'] / df['rendimentos_operacionais'],
        np.nan
    )

    # Alternative calculation for validation
    df['subsidy_dependence_alt'] = np.where(
        df['rendimentos_operacionais'] > 0,
        np.maximum(0, (df['gastos_operacionais'] - df['rendimentos_operacionais']) / df['rendimentos_operacionais']),
        np.nan
    )

    # Log summary statistics
    logger.info(f"  - Observations with negative operating results: {(df['resultados_operacionais'] < 0).sum()}/{len(df)} ({100*(df['resultados_operacionais'] < 0).sum()/len(df):.1f}%)")
    logger.info(f"  - Mean subsidy dependence (all obs): {df['subsidy_dependence'].mean():.3f}")
    logger.info(f"  - Mean subsidy dependence (deficit obs): {df[df['operating_deficit'] > 0]['subsidy_dependence'].mean():.3f}")

    # Validate consistency between two calculations
    diff = (df['subsidy_dependence'] - df['subsidy_dependence_alt']).abs()
    logger.info(f"  - Max difference between calculation methods: {diff.max():.6f}")

    # Check for outliers
    outliers = df[df['subsidy_dependence'] > 1.5]
    if len(outliers) > 0:
        logger.warning(f"⚠ {len(outliers)} observations with subsidy_dependence > 1.5 (extreme deficits)")
        logger.warning(f"  - Max: {df['subsidy_dependence'].max():.2f}")

    return df

# ==============================================================================
# STEP 3: Aggregate to Hospital-Year Level
# ==============================================================================

def aggregate_to_hospital_year(df):
    """
    Aggregate monthly data to hospital-year level.

    Aggregation method:
    - Sum revenues, expenses, deficits for the year
    - Recalculate subsidy dependence at annual level
    """
    logger.info("\n" + "=" * 80)
    logger.info("STEP 3: Aggregating to Hospital-Year Level")
    logger.info("=" * 80)

    # Group by entity and year
    agg_dict = {
        'rendimentos_operacionais': 'sum',
        'gastos_operacionais': 'sum',
        'resultados_operacionais': 'sum',
        'operating_deficit': 'sum',
        'resultado_liquido': 'sum',
        'ebitda': 'sum'
    }

    df_year = df.groupby(['entidade', 'year']).agg(agg_dict).reset_index()

    # Recalculate subsidy dependence at annual level
    df_year['subsidy_dependence'] = np.where(
        df_year['rendimentos_operacionais'] > 0,
        df_year['operating_deficit'] / df_year['rendimentos_operacionais'],
        np.nan
    )

    # Calculate additional metrics
    df_year['operating_margin'] = np.where(
        df_year['rendimentos_operacionais'] > 0,
        df_year['resultados_operacionais'] / df_year['rendimentos_operacionais'],
        np.nan
    )

    logger.info(f"✓ Aggregated to {len(df_year)} hospital-year observations")
    logger.info(f"  - Entities: {df_year['entidade'].nunique()}")
    logger.info(f"  - Years: {df_year['year'].min()}-{df_year['year'].max()}")
    logger.info(f"  - Mean subsidy dependence: {df_year['subsidy_dependence'].mean():.3f}")
    logger.info(f"  - Median subsidy dependence: {df_year['subsidy_dependence'].median():.3f}")

    # Distribution by year
    logger.info("\n  Subsidy dependence by year:")
    for year in sorted(df_year['year'].unique()):
        year_data = df_year[df_year['year'] == year]
        mean_sub = year_data['subsidy_dependence'].mean()
        n_deficit = (year_data['resultados_operacionais'] < 0).sum()
        logger.info(f"    {year}: Mean = {mean_sub:.3f}, Deficits = {n_deficit}/{len(year_data)} ({100*n_deficit/len(year_data):.1f}%)")

    return df_year

# ==============================================================================
# STEP 4: Create Lagged Variables for Historical Subsidy Instrument
# ==============================================================================

def create_lagged_subsidies(df):
    """
    Create lagged subsidy variables (3 and 4 years) for historical instrument.

    Rationale: Past subsidy allocations predict current allocations due to
    bureaucratic inertia, but 3-4 year lag ensures no reverse causality from
    current distress.
    """
    logger.info("\n" + "=" * 80)
    logger.info("STEP 4: Creating Lagged Subsidy Variables")
    logger.info("=" * 80)

    # Sort by entity and year
    df = df.sort_values(['entidade', 'year'])

    # Create lags
    df['subsidy_dependence_lag1'] = df.groupby('entidade')['subsidy_dependence'].shift(1)
    df['subsidy_dependence_lag2'] = df.groupby('entidade')['subsidy_dependence'].shift(2)
    df['subsidy_dependence_lag3'] = df.groupby('entidade')['subsidy_dependence'].shift(3)
    df['subsidy_dependence_lag4'] = df.groupby('entidade')['subsidy_dependence'].shift(4)

    # Create average of 3-4 year lags (main instrument)
    df['subsidy_dependence_historical'] = df[['subsidy_dependence_lag3', 'subsidy_dependence_lag4']].mean(axis=1)

    # Log coverage
    logger.info(f"  - Lag 1 coverage: {df['subsidy_dependence_lag1'].notna().sum()}/{len(df)} ({100*df['subsidy_dependence_lag1'].notna().sum()/len(df):.1f}%)")
    logger.info(f"  - Lag 2 coverage: {df['subsidy_dependence_lag2'].notna().sum()}/{len(df)} ({100*df['subsidy_dependence_lag2'].notna().sum()/len(df):.1f}%)")
    logger.info(f"  - Lag 3 coverage: {df['subsidy_dependence_lag3'].notna().sum()}/{len(df)} ({100*df['subsidy_dependence_lag3'].notna().sum()/len(df):.1f}%)")
    logger.info(f"  - Lag 4 coverage: {df['subsidy_dependence_lag4'].notna().sum()}/{len(df)} ({100*df['subsidy_dependence_lag4'].notna().sum()/len(df):.1f}%)")
    logger.info(f"  - Historical instrument (avg lag 3-4) coverage: {df['subsidy_dependence_historical'].notna().sum()}/{len(df)} ({100*df['subsidy_dependence_historical'].notna().sum()/len(df):.1f}%)")

    # Correlation between current and historical
    corr = df[['subsidy_dependence', 'subsidy_dependence_historical']].corr().iloc[0, 1]
    logger.info(f"\n  Correlation (current vs historical): r = {corr:.3f}")

    return df

# ==============================================================================
# STEP 5: Save Output
# ==============================================================================

def save_output(df):
    """Save subsidy dependence data."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 5: Saving Output")
    logger.info("=" * 80)

    # Save full panel
    output_path = DATA_DIR / "processed" / "variables" / "subsidy_dependence_panel.parquet"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    logger.info(f"✓ Saved subsidy dependence panel: {output_path}")
    logger.info(f"  - {len(df)} observations, {len(df.columns)} columns")

    # Save summary statistics
    summary = df.groupby('year').agg({
        'subsidy_dependence': ['mean', 'median', 'std', 'min', 'max'],
        'operating_margin': ['mean', 'median'],
        'entidade': 'nunique'
    }).round(3)

    summary_path = OUTPUT_DIR / "results" / "descriptive" / "subsidy_dependence_summary.csv"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(summary_path)
    logger.info(f"✓ Saved summary statistics: {summary_path}")

    return output_path

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("Subsidy Dependence Variable Construction")
    logger.info("=" * 80)
    logger.info(f"Project root: {PROJECT_ROOT}")
    logger.info(f"Data directory: {DATA_DIR}")
    logger.info(f"Output directory: {OUTPUT_DIR}\n")

    try:
        # Step 1: Load data
        df = load_financial_data()

        # Step 2: Calculate subsidy dependence
        df = calculate_subsidy_dependence(df)

        # Step 3: Aggregate to hospital-year
        df_year = aggregate_to_hospital_year(df)

        # Step 4: Create lagged variables
        df_year = create_lagged_subsidies(df_year)

        # Step 5: Save output
        output_path = save_output(df_year)

        logger.info("\n" + "=" * 80)
        logger.info("SUCCESS: Subsidy dependence variable constructed")
        logger.info("=" * 80)
        logger.info(f"\nOutput: {output_path}")
        logger.info(f"Ready for IV analysis merge")

        return 0

    except Exception as e:
        logger.error(f"\nERROR: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
