"""
Create Monthly Panel Dataset for Granger Causality Analysis

This script creates a hospital-month panel dataset to enable temporal analysis
of the sequential transfer mechanism (payment delays → staff turnover → quality decline).

Addresses peer review critique: "The sequential transfer mechanism untested -
The mechanism tests (Section 4.3) just show cross-sectional correlations between
subsidy dependence and various distress symptoms, not their temporal ordering."

Inputs:
- SNS monthly datasets (financial, debt, operational, quality)
- Eurostat macro indicators

Output:
- Hospital-month panel: 03_data/processed/panel/hospital_month_panel.parquet
- Enables Granger causality tests with monthly frequency

Author: Research Team
Date: 2025-12-31
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

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


class MonthlyPanelBuilder:
    """
    Builds hospital-month panel dataset preserving temporal structure.

    Key difference from annual panel: NO aggregation to yearly level.
    Keeps month-level granularity for time-series analysis.
    """

    def __init__(self):
        self.sns_financial = None
        self.sns_debt = None
        self.sns_activity = None
        self.sns_quality = None
        self.macro_data = None
        self.monthly_panel = None

    def load_sns_datasets(self):
        """Load SNS parquet datasets and preserve monthly structure."""
        logger.info("Loading SNS datasets (monthly granularity)...")

        # Financial aggregates
        financial_path = DATA_PROCESSED / "financial" / "agregados-economico-financeiros.parquet"
        if financial_path.exists():
            self.sns_financial = pd.read_parquet(financial_path)
            logger.info(f"Loaded financial data: {len(self.sns_financial)} rows")
        else:
            logger.warning(f"Financial data not found at {financial_path}")

        # Debt and payment delays (CRITICAL for Granger causality)
        debt_path = DATA_PROCESSED / "divida-total-vencida-e-pagamentos.parquet"
        if debt_path.exists():
            self.sns_debt = pd.read_parquet(debt_path)
            logger.info(f"Loaded debt/payment data: {len(self.sns_debt)} rows")
        else:
            logger.warning(f"Debt data not found at {debt_path}")

        # Hospital activity (for staffing metrics)
        activity_path = DATA_PROCESSED / "operational" / "atividade-de-internamento-hospitalar.parquet"
        if activity_path.exists():
            self.sns_activity = pd.read_parquet(activity_path)
            logger.info(f"Loaded activity data: {len(self.sns_activity)} rows")
        else:
            logger.warning(f"Activity data not found at {activity_path}")

        # Quality metrics (mortality, readmissions)
        quality_path = DATA_PROCESSED / "quality" / "quality_metrics.parquet"
        if quality_path.exists():
            self.sns_quality = pd.read_parquet(quality_path)
            logger.info(f"Loaded quality data: {len(self.sns_quality)} rows")
        else:
            logger.warning(f"Quality data not found at {quality_path}")

    def standardize_dates(self, df, date_col='data_referencia'):
        """
        Standardize date column and create year-month identifier.

        CRITICAL: Keep full date precision, extract both year and month.
        """
        if date_col not in df.columns:
            # Try alternative date column names
            alt_cols = ['data', 'date', 'periodo', 'ano_mes', 'tempo']
            date_col = next((col for col in alt_cols if col in df.columns), None)

            if date_col is None:
                logger.warning(f"No date column found. Columns: {df.columns.tolist()}")
                return df

        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['year_month'] = df[date_col].dt.to_period('M')  # 'YYYY-MM' format

        return df

    def prepare_payment_delays(self):
        """
        Prepare monthly payment delay metrics (LEADING indicator in sequential transfer).

        Expected temporal pattern:
        Payment_Delays(t) → Staff_Turnover(t+1) → Quality_Decline(t+2) → Bailout(t+3)
        """
        if self.sns_debt is None:
            logger.warning("Debt data not available. Cannot create payment delay metrics.")
            return None

        logger.info("Preparing monthly payment delay metrics...")

        df = self.standardize_dates(self.sns_debt)

        # Filter to analysis period (2017-2024)
        df = df[(df['year'] >= 2017) & (df['year'] <= 2024)]

        # Identify entity column
        entity_col = 'entidade' if 'entidade' in df.columns else 'hospital'

        # Key payment delay metrics (search for relevant columns)
        payment_cols = [col for col in df.columns if any(
            keyword in col.lower() for keyword in
            ['pagamento', 'divida', 'vencid', 'prazo', 'delay', 'overdue']
        )]

        logger.info(f"Identified payment-related columns: {payment_cols}")

        # Select key columns
        keep_cols = [entity_col, 'year', 'month', 'year_month'] + payment_cols
        keep_cols = [col for col in keep_cols if col in df.columns]

        monthly_delays = df[keep_cols].copy()

        # Remove duplicates (keep last observation per hospital-month)
        monthly_delays = monthly_delays.drop_duplicates(
            subset=[entity_col, 'year_month'],
            keep='last'
        )

        logger.info(f"Payment delays panel: {len(monthly_delays)} hospital-months")

        return monthly_delays

    def prepare_staffing_metrics(self):
        """
        Prepare monthly staffing metrics (INTERMEDIATE indicator in sequential transfer).

        Metrics:
        - Staff count changes (proxy for turnover)
        - Temporary staff ratio
        - Wage bill per FTE
        """
        if self.sns_activity is None:
            logger.warning("Activity data not available. Cannot create staffing metrics.")
            return None

        logger.info("Preparing monthly staffing metrics...")

        df = self.standardize_dates(self.sns_activity)
        df = df[(df['year'] >= 2017) & (df['year'] <= 2024)]

        entity_col = 'entidade' if 'entidade' in df.columns else 'hospital'

        # Search for staffing-related columns
        staff_cols = [col for col in df.columns if any(
            keyword in col.lower() for keyword in
            ['trabalhador', 'pessoal', 'funcionario', 'staff', 'employee', 'medico', 'enfermeiro']
        )]

        logger.info(f"Identified staffing columns: {staff_cols}")

        if not staff_cols:
            logger.warning("No staffing columns found in activity data")
            return None

        keep_cols = [entity_col, 'year', 'month', 'year_month'] + staff_cols
        keep_cols = [col for col in keep_cols if col in df.columns]

        monthly_staff = df[keep_cols].copy()
        monthly_staff = monthly_staff.drop_duplicates(
            subset=[entity_col, 'year_month'],
            keep='last'
        )

        logger.info(f"Staffing metrics panel: {len(monthly_staff)} hospital-months")

        return monthly_staff

    def prepare_quality_metrics(self):
        """
        Prepare monthly quality metrics (LAGGING indicator in sequential transfer).

        Metrics:
        - Mortality rates (taxa_mortalidade)
        - Stroke mortality (30-day rates)
        - Length of stay (dias_internamento)
        - Admission rates (taxa_internamento)
        """
        if self.sns_quality is None:
            logger.warning("Quality data not available. Cannot create quality metrics.")
            return None

        logger.info("Preparing monthly quality metrics...")

        df = self.standardize_dates(self.sns_quality, date_col='ano')

        # Filter to analysis period
        if 'year' in df.columns:
            df = df[(df['year'] >= 2017) & (df['year'] <= 2024)]

        # Quality data uses 'instituicao' as entity column
        if 'instituicao' in df.columns:
            entity_col = 'instituicao'
            df = df.rename(columns={'instituicao': 'entidade'})
        elif 'entidade' in df.columns:
            entity_col = 'entidade'
        else:
            entity_col = 'hospital'

        # Key quality metrics
        quality_cols = [col for col in df.columns if any(
            keyword in col.lower() for keyword in
            ['mortalidade', 'mortality', 'internamento', 'dias_', 'taxa_']
        )]

        logger.info(f"Identified quality columns: {quality_cols}")

        if not quality_cols:
            logger.warning("No quality columns found")
            return None

        # Select and aggregate
        keep_cols = ['entidade', 'year', 'month', 'year_month'] + quality_cols
        keep_cols = [col for col in keep_cols if col in df.columns]

        monthly_quality = df[keep_cols].copy()

        # Remove duplicates - aggregate by institution-month if multiple records
        if 'year_month' in monthly_quality.columns:
            # Calculate mean for numeric quality metrics per hospital-month
            agg_dict = {col: 'mean' for col in quality_cols if col in monthly_quality.columns}
            agg_dict['year'] = 'first'
            agg_dict['month'] = 'first'

            monthly_quality = monthly_quality.groupby(['entidade', 'year_month'], as_index=False).agg(agg_dict)

        logger.info(f"Quality metrics panel: {len(monthly_quality)} hospital-months")

        return monthly_quality

    def prepare_financial_metrics(self):
        """
        Prepare monthly financial metrics (for controls).
        """
        if self.sns_financial is None:
            logger.warning("Financial data not available.")
            return None

        logger.info("Preparing monthly financial metrics...")

        df = self.standardize_dates(self.sns_financial)
        df = df[(df['year'] >= 2017) & (df['year'] <= 2024)]

        entity_col = 'entidade' if 'entidade' in df.columns else 'hospital'

        # Key financial columns for controls
        financial_cols = [col for col in df.columns if any(
            keyword in col.lower() for keyword in
            ['receita', 'revenue', 'despesa', 'expense', 'subsid', 'subsidy',
             'resultado', 'result', 'ativo', 'asset', 'passivo', 'liability']
        )]

        logger.info(f"Identified financial columns: {financial_cols}")

        keep_cols = [entity_col, 'year', 'month', 'year_month'] + financial_cols
        keep_cols = [col for col in keep_cols if col in df.columns]

        monthly_financial = df[keep_cols].copy()
        monthly_financial = monthly_financial.drop_duplicates(
            subset=[entity_col, 'year_month'],
            keep='last'
        )

        logger.info(f"Financial metrics panel: {len(monthly_financial)} hospital-months")

        return monthly_financial

    def create_dummy_variables(self, df):
        """Create time-based dummy variables."""
        logger.info("Creating monthly dummy variables...")

        df = df.copy()

        # COVID period (March 2020 - December 2021)
        df['covid_period'] = (
            ((df['year'] == 2020) & (df['month'] >= 3)) |
            (df['year'] == 2021)
        ).astype(int)

        # Election months (October 2019, October 2024)
        df['election_month'] = (
            ((df['year'] == 2019) & (df['month'] == 10)) |
            ((df['year'] == 2024) & (df['month'] == 10))
        ).astype(int)

        # ULS integration (post-2024)
        df['uls_integrated'] = (df['year'] >= 2024).astype(int)

        # Month fixed effects (seasonality)
        for m in range(1, 13):
            df[f'month_{m}'] = (df['month'] == m).astype(int)

        return df

    def merge_monthly_datasets(self):
        """
        Merge all monthly datasets into master monthly panel.

        Merge strategy: OUTER join to preserve all observations.
        Missing values will be handled in Granger causality analysis.
        """
        logger.info("Merging monthly datasets...")

        # Prepare component datasets
        payment_delays = self.prepare_payment_delays()
        staffing = self.prepare_staffing_metrics()
        quality = self.prepare_quality_metrics()
        financial = self.prepare_financial_metrics()

        # Identify which datasets exist
        datasets = {
            'payment_delays': payment_delays,
            'staffing': staffing,
            'quality': quality,
            'financial': financial
        }

        available = {k: v for k, v in datasets.items() if v is not None}

        if not available:
            logger.error("No datasets available for monthly panel creation")
            return None

        logger.info(f"Available datasets: {list(available.keys())}")

        # Start with first available dataset
        first_key = list(available.keys())[0]
        panel = available[first_key]

        entity_col = 'entidade' if 'entidade' in panel.columns else 'hospital'

        # Merge remaining datasets
        for key in list(available.keys())[1:]:
            df = available[key]
            panel = panel.merge(
                df,
                on=[entity_col, 'year', 'month', 'year_month'],
                how='outer',
                suffixes=('', f'_{key}')
            )
            logger.info(f"Merged {key}. Panel size: {len(panel)} hospital-months")

        # Add dummy variables
        panel = self.create_dummy_variables(panel)

        # Sort by entity and time
        panel = panel.sort_values([entity_col, 'year', 'month']).reset_index(drop=True)

        self.monthly_panel = panel
        return panel

    def validate_monthly_panel(self):
        """
        Validate monthly panel for Granger causality requirements.

        Requirements:
        1. Balanced panel (or document missingness)
        2. Sufficient time periods (>24 months recommended)
        3. Key variables present (payment delays, quality metrics)
        4. No large temporal gaps
        """
        if self.monthly_panel is None:
            logger.error("Monthly panel not created yet")
            return

        logger.info("\n" + "="*70)
        logger.info("MONTHLY PANEL VALIDATION FOR GRANGER CAUSALITY")
        logger.info("="*70)

        entity_col = 'entidade' if 'entidade' in self.monthly_panel.columns else 'hospital'

        # 1. Panel structure
        n_hospitals = self.monthly_panel[entity_col].nunique()
        n_months = self.monthly_panel['year_month'].nunique()
        total_obs = len(self.monthly_panel)
        theoretical_max = n_hospitals * n_months

        logger.info(f"\n1. PANEL STRUCTURE")
        logger.info(f"   Number of hospitals: {n_hospitals}")
        logger.info(f"   Number of months: {n_months}")
        logger.info(f"   Date range: {self.monthly_panel['year_month'].min()} to {self.monthly_panel['year_month'].max()}")
        logger.info(f"   Total observations: {total_obs}")
        logger.info(f"   Theoretical maximum: {theoretical_max}")
        logger.info(f"   Missingness: {(theoretical_max - total_obs) / theoretical_max * 100:.1f}%")

        # 2. Time coverage per hospital
        months_per_hospital = self.monthly_panel.groupby(entity_col)['year_month'].nunique()
        logger.info(f"\n2. TIME COVERAGE PER HOSPITAL")
        logger.info(f"   Mean months: {months_per_hospital.mean():.1f}")
        logger.info(f"   Min months: {months_per_hospital.min()}")
        logger.info(f"   Max months: {months_per_hospital.max()}")
        logger.info(f"   Hospitals with >24 months (Granger causality viable): {(months_per_hospital > 24).sum()}")

        # 3. Key variable coverage
        logger.info(f"\n3. KEY VARIABLE COVERAGE")
        key_patterns = {
            'Payment Delays': ['pagamento', 'divida', 'vencid', 'delay'],
            'Staffing': ['trabalhador', 'pessoal', 'staff'],
            'Quality': ['mortalidade', 'mortality', 'readmiss', 'complicacao']
        }

        for category, patterns in key_patterns.items():
            cols = [c for c in self.monthly_panel.columns if any(p in c.lower() for p in patterns)]
            if cols:
                logger.info(f"   {category}: {len(cols)} variables")
                # Check data availability
                non_null_counts = self.monthly_panel[cols].notna().sum()
                logger.info(f"      Variables: {cols[:3]}...")  # Show first 3
                logger.info(f"      Non-null obs: {non_null_counts.mean():.0f} avg ({non_null_counts.mean()/total_obs*100:.1f}%)")
            else:
                logger.info(f"   {category}: NO VARIABLES FOUND")

        # 4. Temporal gaps
        logger.info(f"\n4. TEMPORAL GAPS (Missing months)")
        for entity in self.monthly_panel[entity_col].unique()[:5]:  # Check first 5 hospitals
            entity_data = self.monthly_panel[self.monthly_panel[entity_col] == entity]
            dates = pd.to_datetime(entity_data['year_month'].astype(str))
            gaps = dates.diff().dt.days
            large_gaps = (gaps > 40).sum()  # More than ~1 month
            if large_gaps > 0:
                logger.info(f"   {entity}: {large_gaps} gaps detected")

        # 5. Missing values by variable
        logger.info(f"\n5. MISSING VALUES (top 10 variables)")
        missing = self.monthly_panel.isnull().sum()
        missing_pct = (missing / total_obs * 100).round(1)
        missing_df = pd.DataFrame({
            'Missing': missing[missing > 0],
            'Percent': missing_pct[missing > 0]
        }).sort_values('Missing', ascending=False).head(10)

        logger.info(f"\n{missing_df}")

        logger.info("\n" + "="*70)

        # 6. Granger causality feasibility assessment
        logger.info(f"\nGRANGER CAUSALITY FEASIBILITY:")
        feasible = (months_per_hospital > 24).sum()
        total = len(months_per_hospital)
        logger.info(f"   Hospitals with sufficient data: {feasible}/{total} ({feasible/total*100:.0f}%)")

        if feasible / total > 0.5:
            logger.info("   ✓ GRANGER CAUSALITY ANALYSIS FEASIBLE")
        else:
            logger.warning("   ⚠ LIMITED GRANGER CAUSALITY - Consider imputation or subset analysis")

    def save_monthly_panel(self, filename='hospital_month_panel.parquet'):
        """Save monthly panel to parquet."""
        if self.monthly_panel is None:
            logger.error("Monthly panel not created yet")
            return

        output_path = OUTPUT_DIR / filename
        self.monthly_panel.to_parquet(output_path, index=False)
        logger.info(f"\nMonthly panel saved to: {output_path}")
        logger.info(f"File size: {output_path.stat().st_size / (1024*1024):.2f} MB")

    def run_pipeline(self):
        """Execute full pipeline for monthly panel creation."""
        logger.info("="*70)
        logger.info("MONTHLY PANEL CREATION FOR GRANGER CAUSALITY ANALYSIS")
        logger.info("="*70 + "\n")

        # Load data
        self.load_sns_datasets()

        # Merge to monthly panel
        panel = self.merge_monthly_datasets()

        if panel is None:
            logger.error("Pipeline failed: Could not create monthly panel")
            return None

        # Validate
        self.validate_monthly_panel()

        # Save
        self.save_monthly_panel()

        logger.info("\n✓ Monthly panel creation completed successfully!")
        return self.monthly_panel


def main():
    """Main execution."""
    builder = MonthlyPanelBuilder()
    panel = builder.run_pipeline()

    if panel is not None:
        print("\n" + "="*70)
        print("MONTHLY PANEL PREVIEW")
        print("="*70)
        print(f"\nShape: {panel.shape}")
        print(f"\nFirst 10 rows:")
        print(panel.head(10))
        print(f"\nColumns ({len(panel.columns)}):")
        print(panel.columns.tolist())


if __name__ == "__main__":
    main()
