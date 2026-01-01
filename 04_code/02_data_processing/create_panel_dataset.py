"""
Create Master Panel Dataset for PHFSI Analysis

This script consolidates all data sources into a hospital-year panel structure for analysis.

Inputs:
- SNS datasets (financial, debt, operational)
- Eurostat macro indicators
- INE demographic data

Output:
- Hospital-year panel dataset: 03_data/processed/panel/hospital_year_panel.parquet

Author: Research Team
Date: 2025-12-31
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_RAW = PROJECT_ROOT / "03_data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "03_data" / "processed"
OUTPUT_DIR = DATA_PROCESSED / "panel"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class PanelDatasetBuilder:
    """
    Builds master hospital-year panel dataset from multiple sources.
    """

    def __init__(self):
        self.sns_financial = None
        self.sns_debt = None
        self.sns_accounts = None
        self.sns_activity = None
        self.macro_data = None
        self.panel = None

    def load_sns_datasets(self):
        """Load SNS parquet datasets from processed directory."""
        logger.info("Loading SNS datasets...")

        # Financial aggregates
        financial_path = DATA_PROCESSED / "financial" / "agregados-economico-financeiros.parquet"
        if financial_path.exists():
            self.sns_financial = pd.read_parquet(financial_path)
            logger.info(f"Loaded financial data: {len(self.sns_financial)} rows")
        else:
            logger.warning(f"Financial data not found at {financial_path}")

        # Debt and payments
        debt_path = DATA_PROCESSED / "divida-total-vencida-e-pagamentos.parquet"
        if debt_path.exists():
            self.sns_debt = pd.read_parquet(debt_path)
            logger.info(f"Loaded debt data: {len(self.sns_debt)} rows")
        else:
            logger.warning(f"Debt data not found at {debt_path}")

        # National health service accounts
        accounts_path = DATA_PROCESSED / "financial" / "conta-do-servico-nacional-de-saude.parquet"
        if accounts_path.exists():
            self.sns_accounts = pd.read_parquet(accounts_path)
            logger.info(f"Loaded accounts data: {len(self.sns_accounts)} rows")
        else:
            logger.warning(f"Accounts data not found at {accounts_path}")

        # Hospital activity/operational
        activity_path = DATA_PROCESSED / "operational" / "atividade-de-internamento-hospitalar.parquet"
        if activity_path.exists():
            self.sns_activity = pd.read_parquet(activity_path)
            logger.info(f"Loaded activity data: {len(self.sns_activity)} rows")
        else:
            logger.warning(f"Activity data not found at {activity_path}")

    def load_macro_data(self):
        """Load consolidated macro indicators from Eurostat."""
        logger.info("Loading macro indicators...")

        macro_path = DATA_PROCESSED / "consolidated" / "macro_indicators_consolidated" / "macro_indicators_consolidated.parquet"
        if macro_path.exists():
            self.macro_data = pd.read_parquet(macro_path)
            logger.info(f"Loaded macro data: {len(self.macro_data)} rows")
        else:
            logger.warning(f"Macro data not found at {macro_path}")

    def standardize_dates(self, df, date_col='data_referencia'):
        """
        Standardize date column to datetime and extract year.

        Parameters:
        - df: DataFrame with date column
        - date_col: Name of date column (default: 'data_referencia')

        Returns:
        - DataFrame with 'year' column
        """
        if date_col not in df.columns:
            # Try alternative date column names
            alt_cols = ['data', 'date', 'periodo', 'ano', 'tempo']
            date_col = next((col for col in alt_cols if col in df.columns), None)

            if date_col is None:
                logger.warning(f"No date column found in DataFrame. Columns: {df.columns.tolist()}")
                return df

        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month

        return df

    def aggregate_to_annual(self, df, group_cols, agg_dict):
        """
        Aggregate monthly data to annual level.

        Parameters:
        - df: DataFrame with monthly data
        - group_cols: Columns to group by (e.g., ['entidade', 'year'])
        - agg_dict: Dictionary of column: aggregation function

        Returns:
        - Annual aggregated DataFrame
        """
        return df.groupby(group_cols, as_index=False).agg(agg_dict)

    def create_financial_panel(self):
        """Create annual financial metrics from SNS financial data."""
        if self.sns_financial is None:
            logger.warning("SNS financial data not loaded. Skipping financial panel.")
            return None

        logger.info("Creating financial panel...")

        # Standardize dates
        df = self.standardize_dates(self.sns_financial)

        # Filter to analysis period (2017-2024)
        df = df[(df['year'] >= 2017) & (df['year'] <= 2024)]

        # Identify relevant columns (will vary by actual data structure)
        # This is a template - adjust based on actual column names
        financial_cols = {
            'year': 'first',
            # Add actual financial columns here based on data exploration
        }

        # Aggregate to hospital-year
        if 'entidade' in df.columns:
            entity_col = 'entidade'
        elif 'hospital' in df.columns:
            entity_col = 'hospital'
        else:
            logger.warning("No entity identifier found in financial data")
            return None

        # Calculate annual aggregates
        annual_df = df.groupby([entity_col, 'year'], as_index=False).agg({
            col: 'sum' if df[col].dtype in ['int64', 'float64'] else 'first'
            for col in df.columns if col not in [entity_col, 'year', 'month']
        })

        return annual_df

    def create_debt_panel(self):
        """Create annual debt metrics from SNS debt data."""
        if self.sns_debt is None:
            logger.warning("SNS debt data not loaded. Skipping debt panel.")
            return None

        logger.info("Creating debt panel...")

        # Standardize dates
        df = self.standardize_dates(self.sns_debt)

        # Filter to analysis period
        df = df[(df['year'] >= 2017) & (df['year'] <= 2024)]

        # Identify entity column
        entity_col = 'entidade' if 'entidade' in df.columns else 'hospital'

        # Calculate annual averages for debt metrics
        annual_df = df.groupby([entity_col, 'year'], as_index=False).agg({
            col: 'mean' if df[col].dtype in ['int64', 'float64'] else 'first'
            for col in df.columns if col not in [entity_col, 'year', 'month']
        })

        return annual_df

    def create_dummy_variables(self, df):
        """
        Create dummy variables for COVID period, ULS integration, elections.

        Parameters:
        - df: Panel DataFrame with 'year' column

        Returns:
        - DataFrame with dummy variables added
        """
        logger.info("Creating dummy variables...")

        df = df.copy()

        # COVID period (2020-2021)
        df['covid_period'] = ((df['year'] == 2020) | (df['year'] == 2021)).astype(int)

        # Election years in Portugal (2019, 2024)
        df['election_year'] = ((df['year'] == 2019) | (df['year'] == 2024)).astype(int)

        # ULS integration status
        # TODO: Add actual ULS integration dates from ACSS data
        # For now, create placeholder (all hospitals integrated post-2024)
        df['uls_integrated'] = (df['year'] >= 2024).astype(int)

        logger.info(f"Added dummy variables: covid_period, election_year, uls_integrated")

        return df

    def merge_all_datasets(self):
        """Merge all datasets into master panel."""
        logger.info("Merging all datasets into master panel...")

        # Start with financial data as base
        financial_panel = self.create_financial_panel()
        debt_panel = self.create_debt_panel()

        if financial_panel is None and debt_panel is None:
            logger.error("No base data available for panel creation")
            return None

        # Use whichever exists as base
        if financial_panel is not None:
            panel = financial_panel
            entity_col = 'entidade' if 'entidade' in panel.columns else 'hospital'
        else:
            panel = debt_panel
            entity_col = 'entidade' if 'entidade' in panel.columns else 'hospital'

        # Merge debt data if available
        if debt_panel is not None and financial_panel is not None:
            panel = panel.merge(
                debt_panel,
                on=[entity_col, 'year'],
                how='outer',
                suffixes=('', '_debt')
            )
            logger.info(f"Merged debt data. Panel size: {len(panel)}")

        # Merge macro data if available
        if self.macro_data is not None:
            # Rename 'year' to match if needed
            macro_df = self.macro_data.copy()
            if 'year' not in macro_df.columns and 'Year' in macro_df.columns:
                macro_df = macro_df.rename(columns={'Year': 'year'})

            panel = panel.merge(
                macro_df,
                on='year',
                how='left'
            )
            logger.info(f"Merged macro data. Panel size: {len(panel)}")

        # Add dummy variables
        panel = self.create_dummy_variables(panel)

        # Sort by entity and year
        panel = panel.sort_values([entity_col, 'year']).reset_index(drop=True)

        self.panel = panel
        return panel

    def validate_panel(self):
        """Validate the created panel dataset."""
        if self.panel is None:
            logger.error("Panel not created yet. Run merge_all_datasets() first.")
            return

        logger.info("\n" + "="*60)
        logger.info("PANEL VALIDATION REPORT")
        logger.info("="*60)

        # Basic shape
        logger.info(f"\nPanel shape: {self.panel.shape}")
        logger.info(f"Number of hospitals: {self.panel['entidade'].nunique() if 'entidade' in self.panel.columns else 'N/A'}")
        logger.info(f"Years covered: {self.panel['year'].min()} - {self.panel['year'].max()}")
        logger.info(f"Total hospital-years: {len(self.panel)}")

        # Missing values
        logger.info("\nMissing values by column:")
        missing = self.panel.isnull().sum()
        missing_pct = (missing / len(self.panel) * 100).round(2)
        missing_df = pd.DataFrame({
            'Missing': missing[missing > 0],
            'Percent': missing_pct[missing > 0]
        }).sort_values('Missing', ascending=False)

        if len(missing_df) > 0:
            logger.info(f"\n{missing_df.head(20)}")
        else:
            logger.info("No missing values found!")

        # Duplicates
        entity_col = 'entidade' if 'entidade' in self.panel.columns else 'hospital'
        duplicates = self.panel.duplicated(subset=[entity_col, 'year']).sum()
        logger.info(f"\nDuplicate hospital-years: {duplicates}")

        # Outliers (simple check for numeric columns)
        logger.info("\nOutlier detection (values beyond 3 std dev):")
        numeric_cols = self.panel.select_dtypes(include=[np.number]).columns
        for col in numeric_cols[:10]:  # Check first 10 numeric columns
            mean = self.panel[col].mean()
            std = self.panel[col].std()
            outliers = ((self.panel[col] < mean - 3*std) | (self.panel[col] > mean + 3*std)).sum()
            if outliers > 0:
                logger.info(f"  {col}: {outliers} outliers")

        logger.info("\n" + "="*60)

    def save_panel(self, filename='hospital_year_panel.parquet'):
        """Save panel dataset to parquet."""
        if self.panel is None:
            logger.error("Panel not created yet.")
            return

        output_path = OUTPUT_DIR / filename
        self.panel.to_parquet(output_path, index=False)
        logger.info(f"\nPanel saved to: {output_path}")
        logger.info(f"File size: {output_path.stat().st_size / 1024:.1f} KB")

    def run_pipeline(self):
        """Execute full pipeline to create panel dataset."""
        logger.info("Starting panel dataset creation pipeline...")
        logger.info("="*60 + "\n")

        # Step 1: Load data
        self.load_sns_datasets()
        self.load_macro_data()

        # Step 2: Merge
        panel = self.merge_all_datasets()

        if panel is None:
            logger.error("Pipeline failed: Could not create panel")
            return None

        # Step 3: Validate
        self.validate_panel()

        # Step 4: Save
        self.save_panel()

        logger.info("\nPipeline completed successfully!")
        return self.panel


def main():
    """Main execution function."""
    builder = PanelDatasetBuilder()
    panel = builder.run_pipeline()

    if panel is not None:
        print("\n" + "="*60)
        print("PANEL DATASET PREVIEW")
        print("="*60)
        print(panel.head(10))
        print("\nColumns:", panel.columns.tolist())


if __name__ == "__main__":
    main()
