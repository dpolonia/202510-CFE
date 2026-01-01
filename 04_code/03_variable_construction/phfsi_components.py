"""
PHFSI Component Calculations

Implements the 5 components of the Public Hospital Financial Sustainability Index (PHFSI):
1. OSSR - Operational Self-Sufficiency Ratio
2. SPI - Stakeholder Pressure Index
3. LRR - Liquidity Realization Rate
4. TLR - True Leverage Ratio
5. CQMI - Clinical Quality Maintenance Index

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
DATA_RAW = PROJECT_ROOT / "03_data" / "raw" / "sns" / "combined" / "parquet"
DATA_PROCESSED = PROJECT_ROOT / "03_data" / "processed"
OUTPUT_DIR = DATA_PROCESSED / "variables"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class PHFSIComponentCalculator:
    """
    Calculates individual components of the PHFSI index.
    """

    def __init__(self):
        self.panel = None
        self.payment_time_data = None
        self.mortality_data = None
        self.hip_fracture_data = None

    def load_panel_dataset(self):
        """Load master panel dataset."""
        logger.info("Loading panel dataset...")
        panel_path = DATA_PROCESSED / "panel" / "hospital_year_panel.parquet"

        if not panel_path.exists():
            raise FileNotFoundError(
                f"Panel dataset not found at {panel_path}. "
                "Run create_panel_dataset.py first."
            )

        self.panel = pd.read_parquet(panel_path)
        logger.info(f"Loaded panel: {len(self.panel)} rows, {len(self.panel.columns)} columns")

    def load_supplementary_data(self):
        """Load additional datasets needed for PHFSI components."""
        logger.info("Loading supplementary datasets...")

        # Payment time data for SPI
        payment_path = DATA_RAW / "priority_1" / "tempo-medio-de-pagamento-das-instituicoes-do-sns-a-fornecedores.parquet"
        if payment_path.exists():
            df = pd.read_parquet(payment_path)
            # Standardize column names and aggregate to annual
            df['tempo'] = pd.to_datetime(df['tempo'])
            df['year'] = df['tempo'].dt.year
            # Rename instituicao to entidade for merging
            df = df.rename(columns={'instituicao': 'entidade'})
            # Aggregate to annual average
            self.payment_time_data = df.groupby(['entidade', 'year'], as_index=False).agg({
                'prazo_medio_de_pagamento': 'mean'
            })
            logger.info(f"Loaded payment time data: {len(self.payment_time_data)} rows")
        else:
            logger.warning(f"Payment time data not found at {payment_path}")

        # Mortality data for CQMI
        mortality_path = DATA_RAW / "priority_3" / "morbilidade-e-mortalidade-hospitalar.parquet"
        if mortality_path.exists():
            df = pd.read_parquet(mortality_path)
            df['ano'] = pd.to_datetime(df['ano'])
            df['year'] = df['ano'].dt.year
            # Rename instituicao to entidade
            df = df.rename(columns={'instituicao': 'entidade'})
            # Aggregate to annual average across all diagnoses
            self.mortality_data = df.groupby(['entidade', 'year'], as_index=False).agg({
                'taxa_mortalidade': 'mean',
                'taxa_internamento': 'sum',
                'dias_internamento': 'sum'
            })
            logger.info(f"Loaded mortality data: {len(self.mortality_data)} rows")
        else:
            logger.warning(f"Mortality data not found at {mortality_path}")

        # Hip fracture quality indicator for CQMI
        hip_path = DATA_RAW / "priority_3" / "fraturas-da-anca-cirurgias-nas-primeiras-48h.parquet"
        if hip_path.exists():
            df = pd.read_parquet(hip_path)
            df['tempo'] = pd.to_datetime(df['tempo'])
            df['year'] = df['tempo'].dt.year
            # Rename instituicao to entidade
            df = df.rename(columns={'instituicao': 'entidade'})
            # Aggregate to annual average
            self.hip_fracture_data = df.groupby(['entidade', 'year'], as_index=False).agg({
                'fraturas_anca_com_cirurgia_realizada_nas_primeiras_48_horas': 'mean'
            })
            logger.info(f"Loaded hip fracture data: {len(self.hip_fracture_data)} rows")
        else:
            logger.warning(f"Hip fracture data not found at {hip_path}")

    def calculate_ossr(self):
        """
        Component 1: Operational Self-Sufficiency Ratio (OSSR)

        Formula: OSSR = Operating_Revenue / Operating_Expenses
        Range: 0 to 1+ (higher = more self-sufficient)

        Note: Ideally would exclude subsidies from revenue, but subsidy data not
        separately available in current dataset.
        """
        logger.info("Calculating OSSR (Operational Self-Sufficiency Ratio)...")

        df = self.panel.copy()

        # Calculate OSSR
        df['ossr_raw'] = df['rendimentos_operacionais'] / df['gastos_operacionais']

        # Handle edge cases
        df['ossr_raw'] = df['ossr_raw'].replace([np.inf, -np.inf], np.nan)

        # Cap outliers at reasonable range (0 to 2)
        df['ossr'] = df['ossr_raw'].clip(lower=0, upper=2)

        # Flag potential data issues
        issues = (df['gastos_operacionais'] <= 0) | (df['rendimentos_operacionais'] < 0)
        if issues.sum() > 0:
            logger.warning(f"OSSR: {issues.sum()} observations with negative/zero values")

        logger.info(f"OSSR calculated. Mean: {df['ossr'].mean():.3f}, Median: {df['ossr'].median():.3f}")

        return df[['entidade', 'year', 'ossr', 'ossr_raw']]

    def calculate_spi(self):
        """
        Component 2: Stakeholder Pressure Index (SPI)

        Formula (simplified for 6-month version):
        SPI = (Payment_Days / 90) + (Overdue_Liabilities / Total_Liabilities)

        Range: 0 to 2+ (higher = more pressure)

        Full version would include: + Staff_Turnover + (Complaints / 1000)
        but these data not available in current dataset.
        """
        logger.info("Calculating SPI (Stakeholder Pressure Index)...")

        df = self.panel.copy()

        # Merge payment time data
        if self.payment_time_data is not None:
            df = df.merge(
                self.payment_time_data,
                on=['entidade', 'year'],
                how='left'
            )
        else:
            df['prazo_medio_de_pagamento'] = np.nan

        # Subcomponent 1: Payment delay ratio (normalized to 90 days)
        df['spi_payment_delay'] = df['prazo_medio_de_pagamento'] / 90
        df['spi_payment_delay'] = df['spi_payment_delay'].clip(lower=0, upper=5)  # Cap at 5x benchmark

        # Subcomponent 2: Overdue debt ratio
        df['spi_overdue_ratio'] = (
            df['divida_vencida_fornecedores_externos'] /
            df['divida_total_fornecedores_externos']
        )
        df['spi_overdue_ratio'] = df['spi_overdue_ratio'].replace([np.inf, -np.inf], np.nan)
        df['spi_overdue_ratio'] = df['spi_overdue_ratio'].clip(lower=0, upper=1)

        # Calculate SPI (average of available subcomponents)
        df['spi'] = (df['spi_payment_delay'] + df['spi_overdue_ratio']) / 2

        logger.info(f"SPI calculated. Mean: {df['spi'].mean():.3f}, Median: {df['spi'].median():.3f}")

        return df[['entidade', 'year', 'spi', 'spi_payment_delay', 'spi_overdue_ratio']]

    def calculate_lrr(self):
        """
        Component 3: Liquidity Realization Rate (LRR)

        Simplified proxy (cash flow data not available):
        LRR = Revenue_Efficiency = Operating_Result / Operating_Revenue

        Range: -1 to 1 (higher = better liquidity)

        Note: This is a proxy. Ideally would use: Cash_Collections_t / Accrued_Revenue_t-1
        """
        logger.info("Calculating LRR (Liquidity Realization Rate - proxy)...")

        df = self.panel.copy()

        # Use operating result / revenue as proxy for cash realization
        df['lrr_raw'] = df['resultados_operacionais'] / df['rendimentos_operacionais']
        df['lrr_raw'] = df['lrr_raw'].replace([np.inf, -np.inf], np.nan)

        # Normalize to 0-1 range (shift and scale from typical -1 to 1 range)
        df['lrr'] = (df['lrr_raw'] + 1) / 2
        df['lrr'] = df['lrr'].clip(lower=0, upper=1)

        logger.info(f"LRR calculated. Mean: {df['lrr'].mean():.3f}, Median: {df['lrr'].median():.3f}")

        return df[['entidade', 'year', 'lrr', 'lrr_raw']]

    def calculate_tlr(self):
        """
        Component 4: True Leverage Ratio (TLR)

        Simplified proxy (balance sheet data not available):
        TLR = Total_Supplier_Debt / Operating_Revenue

        Range: 0 to infinity (higher = worse leverage, will be normalized)

        Note: Ideally would use: (Total_Liabilities + NPV_Subsidies) / Retained_Earnings
        """
        logger.info("Calculating TLR (True Leverage Ratio - proxy)...")

        df = self.panel.copy()

        # Use supplier debt / revenue as proxy for leverage
        df['tlr_raw'] = df['divida_total_fornecedores_externos'] / df['rendimentos_operacionais']
        df['tlr_raw'] = df['tlr_raw'].replace([np.inf, -np.inf], np.nan)

        # Cap at reasonable range and invert so higher = better (for consistency with other components)
        # Normalize: if ratio > 1 (debt > annual revenue), that's very high leverage
        df['tlr_capped'] = df['tlr_raw'].clip(lower=0, upper=2)

        # Invert and normalize to 0-1 (so high debt = low score)
        df['tlr'] = 1 - (df['tlr_capped'] / 2)
        df['tlr'] = df['tlr'].clip(lower=0, upper=1)

        logger.info(f"TLR calculated. Mean: {df['tlr'].mean():.3f}, Median: {df['tlr'].median():.3f}")

        return df[['entidade', 'year', 'tlr', 'tlr_raw', 'tlr_capped']]

    def calculate_cqmi(self):
        """
        Component 5: Clinical Quality Maintenance Index (CQMI)

        Formula (simplified):
        CQMI = (1 - Normalized_Mortality_Rate) * 0.5 + Hip_Fracture_48h_Rate * 0.5

        Range: 0 to 1 (higher = better quality)

        Uses:
        - Mortality rate (lower is better, so we invert)
        - Hip fracture surgery within 48h (higher is better - quality indicator)
        """
        logger.info("Calculating CQMI (Clinical Quality Maintenance Index)...")

        df = self.panel.copy()

        # Merge mortality data
        if self.mortality_data is not None:
            df = df.merge(
                self.mortality_data,
                on=['entidade', 'year'],
                how='left'
            )
        else:
            df['taxa_mortalidade'] = np.nan

        # Merge hip fracture quality data
        if self.hip_fracture_data is not None:
            df = df.merge(
                self.hip_fracture_data,
                on=['entidade', 'year'],
                how='left'
            )
        else:
            df['fraturas_anca_com_cirurgia_realizada_nas_primeiras_48_horas'] = np.nan

        # Subcomponent 1: Mortality (invert so lower mortality = higher score)
        # Normalize mortality rate to 0-1 range (typical range 0-20%)
        df['cqmi_mortality'] = 1 - (df['taxa_mortalidade'] / 20).clip(lower=0, upper=1)

        # Subcomponent 2: Hip fracture 48h surgery rate (already in %, normalize to 0-1)
        df['cqmi_hip_fracture'] = (df['fraturas_anca_com_cirurgia_realizada_nas_primeiras_48_horas'] / 100).clip(lower=0, upper=1)

        # Calculate CQMI (weighted average of available subcomponents)
        # Use equal weights for now
        df['cqmi'] = (df['cqmi_mortality'] + df['cqmi_hip_fracture']) / 2

        logger.info(f"CQMI calculated. Mean: {df['cqmi'].mean():.3f}, Median: {df['cqmi'].median():.3f}")

        return df[['entidade', 'year', 'cqmi', 'cqmi_mortality', 'cqmi_hip_fracture']]

    def merge_all_components(self):
        """Merge all PHFSI components into single dataset."""
        logger.info("Merging all PHFSI components...")

        # Calculate each component
        ossr_df = self.calculate_ossr()
        spi_df = self.calculate_spi()
        lrr_df = self.calculate_lrr()
        tlr_df = self.calculate_tlr()
        cqmi_df = self.calculate_cqmi()

        # Merge all components
        components = self.panel[['entidade', 'year']].copy()

        for df in [ossr_df, spi_df, lrr_df, tlr_df, cqmi_df]:
            components = components.merge(df, on=['entidade', 'year'], how='left')

        logger.info(f"All components merged. Shape: {components.shape}")

        return components

    def run_pipeline(self):
        """Execute full pipeline to calculate all PHFSI components."""
        logger.info("Starting PHFSI component calculation pipeline...")
        logger.info("="*60 + "\n")

        # Load data
        self.load_panel_dataset()
        self.load_supplementary_data()

        # Calculate and merge components
        components = self.merge_all_components()

        # Validation
        logger.info("\n" + "="*60)
        logger.info("COMPONENT VALIDATION")
        logger.info("="*60)

        component_cols = ['ossr', 'spi', 'lrr', 'tlr', 'cqmi']
        for col in component_cols:
            if col in components.columns:
                logger.info(f"\n{col.upper()}:")
                logger.info(f"  Mean: {components[col].mean():.3f}")
                logger.info(f"  Median: {components[col].median():.3f}")
                logger.info(f"  Std: {components[col].std():.3f}")
                logger.info(f"  Min: {components[col].min():.3f}")
                logger.info(f"  Max: {components[col].max():.3f}")
                logger.info(f"  Missing: {components[col].isna().sum()} ({components[col].isna().sum()/len(components)*100:.1f}%)")

        # Save components
        output_path = OUTPUT_DIR / "phfsi_components.parquet"
        components.to_parquet(output_path, index=False)
        logger.info(f"\nComponents saved to: {output_path}")
        logger.info(f"File size: {output_path.stat().st_size / 1024:.1f} KB")

        logger.info("\nPipeline completed successfully!")

        return components


def main():
    """Main execution function."""
    calculator = PHFSIComponentCalculator()
    components = calculator.run_pipeline()

    print("\n" + "="*60)
    print("PHFSI COMPONENTS PREVIEW")
    print("="*60)
    print(components.head(10))
    print("\nColumns:", components.columns.tolist())


if __name__ == "__main__":
    main()
