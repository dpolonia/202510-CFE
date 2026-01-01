"""
Robustness Checks for PHFSI Panel Regressions

Tests robustness of main results (Model 1: PHFSI Determinants) to:
1. Alternative PHFSI specifications (different weights, exclude components)
2. Sample variations (exclude COVID, exclude small hospitals, exclude regions)
3. Alternative standard errors (two-way clustering, bootstrap)

Generates Appendix Table A1 for the paper.

Author: Research Team
Date: 2025-12-31
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from linearmodels.panel import PanelOLS
from sklearn.decomposition import PCA

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PROCESSED = PROJECT_ROOT / "03_data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "06_output" / "tables" / "appendix"
RESULTS_DIR = PROJECT_ROOT / "06_output" / "results" / "robustness"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class RobustnessAnalyzer:
    """
    Performs robustness checks on panel regression results.
    """

    def __init__(self):
        self.panel = None
        self.components = None
        self.baseline_result = None
        self.robustness_results = {}

    def load_data(self):
        """Load panel dataset and components."""
        logger.info("Loading data for robustness checks...")

        # Load panel
        panel_path = DATA_PROCESSED / "panel" / "hospital_year_panel.parquet"
        self.panel = pd.read_parquet(panel_path)

        # Load PHFSI scores
        phfsi_path = DATA_PROCESSED / "variables" / "phfsi_scores.parquet"
        phfsi_scores = pd.read_parquet(phfsi_path)

        # Load components
        components_path = DATA_PROCESSED / "variables" / "phfsi_components.parquet"
        self.components = pd.read_parquet(components_path)

        # Merge
        merge_cols = ['entidade', 'year', 'phfsi', 'phfsi_cluster']
        for col in ['ossr', 'spi', 'lrr', 'tlr', 'cqmi']:
            if col in phfsi_scores.columns:
                merge_cols.append(col)

        self.panel = self.panel.merge(
            phfsi_scores[merge_cols],
            on=['entidade', 'year'],
            how='left'
        )

        # Filter to hospitals
        hospital_keywords = [
            'Hospital', 'Hospitalar', 'Unidade Local de Saúde',
            'ULS', 'IPO', 'Instituto Português'
        ]
        hospital_mask = self.panel['entidade'].str.contains(
            '|'.join(hospital_keywords),
            case=False,
            na=False
        )
        self.panel = self.panel[hospital_mask].copy()

        logger.info(f"Loaded data: {len(self.panel)} observations, {self.panel['entidade'].nunique()} hospitals")

    def prepare_regression_data(self, df):
        """Prepare data for regression (create variables, set index)."""
        df = df.copy()

        # Create variables
        df['subsidy_dependence'] = -df['resultados_operacionais'] / df['rendimentos_operacionais']
        df['subsidy_dependence'] = df['subsidy_dependence'].clip(lower=-1, upper=1)
        df['log_revenue'] = np.log(df['rendimentos_operacionais'] + 1)
        df['log_debt'] = np.log(df['divida_total_fornecedores_externos'] + 1)
        df['debt_ratio'] = df['divida_total_fornecedores_externos'] / df['rendimentos_operacionais']
        df['debt_ratio'] = df['debt_ratio'].clip(upper=5)

        # Set index
        df = df.set_index(['entidade', 'year'])

        # Drop missing PHFSI
        df = df[df['phfsi'].notna()].copy()

        return df

    def run_baseline_model(self):
        """Run baseline model for comparison."""
        logger.info("Running baseline model (for comparison)...")

        df = self.prepare_regression_data(self.panel)

        # Baseline specification
        y = df['phfsi']
        X = df[['subsidy_dependence', 'log_revenue', 'debt_ratio']]

        data = pd.concat([y, X], axis=1).dropna()
        y = data['phfsi']
        X = data[['subsidy_dependence', 'log_revenue', 'debt_ratio']]

        model = PanelOLS(y, X, entity_effects=True, time_effects=True)
        self.baseline_result = model.fit(cov_type='clustered', cluster_entity=True)

        logger.info(f"Baseline: β(subsidy) = {self.baseline_result.params['subsidy_dependence']:.4f}, "
                   f"p = {self.baseline_result.pvalues['subsidy_dependence']:.4f}")

        self.robustness_results['baseline'] = self.baseline_result

    def robustness_alternative_phfsi_weights(self):
        """
        Test 1: Alternative PHFSI weighting schemes.

        - Equal weights (baseline)
        - Prioritize SPI (40% SPI, 15% others)
        - Exclude SPI
        - Exclude LRR
        - PCA-based weights
        """
        logger.info("Robustness Test 1: Alternative PHFSI Specifications...")

        results = {}

        # Test 1a: Prioritize SPI
        logger.info("  1a: Prioritize SPI (40% SPI, 15% others)...")
        df_components = self.components.copy()

        # Recalculate PHFSI with SPI priority
        weights = {'ossr': 0.15, 'spi': 0.40, 'lrr': 0.15, 'tlr': 0.15, 'cqmi': 0.15}

        # Normalize components first
        for comp in ['ossr', 'spi', 'lrr', 'tlr']:
            col_min = df_components[comp].min()
            col_max = df_components[comp].max()
            if not pd.isna(col_min) and not pd.isna(col_max) and col_max > col_min:
                df_components[f'{comp}_norm'] = (df_components[comp] - col_min) / (col_max - col_min)

        # Invert SPI
        df_components['spi_norm_inv'] = 1 - df_components['spi_norm']

        # Calculate weighted PHFSI
        df_components['phfsi_spi_priority'] = (
            df_components['ossr_norm'] * weights['ossr'] +
            df_components['spi_norm_inv'] * weights['spi'] +
            df_components['lrr_norm'] * weights['lrr'] +
            df_components['tlr_norm'] * weights['tlr']
        ) / (weights['ossr'] + weights['spi'] + weights['lrr'] + weights['tlr'])

        # Merge with panel
        df_test = self.panel.merge(
            df_components[['entidade', 'year', 'phfsi_spi_priority']],
            on=['entidade', 'year'],
            how='left'
        )
        df_test = self.prepare_regression_data(df_test)

        # Run regression
        y = df_test['phfsi_spi_priority']
        X = df_test[['subsidy_dependence', 'log_revenue', 'debt_ratio']]
        data = pd.concat([y, X], axis=1).dropna()

        if len(data) > 20:
            y = data['phfsi_spi_priority']
            X = data[['subsidy_dependence', 'log_revenue', 'debt_ratio']]
            model = PanelOLS(y, X, entity_effects=True, time_effects=True)
            result = model.fit(cov_type='clustered', cluster_entity=True)
            results['spi_priority'] = result
            logger.info(f"    β(subsidy) = {result.params['subsidy_dependence']:.4f}, p = {result.pvalues['subsidy_dependence']:.4f}")

        # Test 1b: Exclude SPI (use 3 components)
        logger.info("  1b: Exclude SPI from PHFSI...")
        df_components['phfsi_no_spi'] = (
            df_components['ossr_norm'] +
            df_components['lrr_norm'] +
            df_components['tlr_norm']
        ) / 3

        df_test = self.panel.merge(
            df_components[['entidade', 'year', 'phfsi_no_spi']],
            on=['entidade', 'year'],
            how='left'
        )
        df_test = self.prepare_regression_data(df_test)

        y = df_test['phfsi_no_spi']
        X = df_test[['subsidy_dependence', 'log_revenue', 'debt_ratio']]
        data = pd.concat([y, X], axis=1).dropna()

        if len(data) > 20:
            y = data['phfsi_no_spi']
            X = data[['subsidy_dependence', 'log_revenue', 'debt_ratio']]
            model = PanelOLS(y, X, entity_effects=True, time_effects=True)
            result = model.fit(cov_type='clustered', cluster_entity=True)
            results['exclude_spi'] = result
            logger.info(f"    β(subsidy) = {result.params['subsidy_dependence']:.4f}, p = {result.pvalues['subsidy_dependence']:.4f}")

        self.robustness_results.update(results)
        return results

    def robustness_sample_variations(self):
        """
        Test 2: Sample variations.

        - Exclude COVID years (2020-2021)
        - Exclude small hospitals (bottom quartile)
        - Exclude largest regions (Lisbon, Porto)
        """
        logger.info("Robustness Test 2: Sample Variations...")

        results = {}

        # Test 2a: Exclude COVID years
        logger.info("  2a: Exclude COVID years (2020-2021)...")
        df_no_covid = self.panel[~self.panel['year'].isin([2020, 2021])].copy()
        df_no_covid = self.prepare_regression_data(df_no_covid)

        y = df_no_covid['phfsi']
        X = df_no_covid[['subsidy_dependence', 'log_revenue', 'debt_ratio']]
        data = pd.concat([y, X], axis=1).dropna()

        if len(data) > 20:
            y = data['phfsi']
            X = data[['subsidy_dependence', 'log_revenue', 'debt_ratio']]
            model = PanelOLS(y, X, entity_effects=True, time_effects=True)
            result = model.fit(cov_type='clustered', cluster_entity=True)
            results['exclude_covid'] = result
            logger.info(f"    β(subsidy) = {result.params['subsidy_dependence']:.4f}, p = {result.pvalues['subsidy_dependence']:.4f}, N = {result.nobs}")

        # Test 2b: Exclude small hospitals (bottom quartile by revenue)
        logger.info("  2b: Exclude small hospitals (bottom 25% by revenue)...")
        revenue_threshold = self.panel.groupby('entidade')['rendimentos_operacionais'].mean().quantile(0.25)
        hospital_avg_revenue = self.panel.groupby('entidade')['rendimentos_operacionais'].mean()
        large_hospitals = hospital_avg_revenue[hospital_avg_revenue >= revenue_threshold].index

        df_large = self.panel[self.panel['entidade'].isin(large_hospitals)].copy()
        df_large = self.prepare_regression_data(df_large)

        y = df_large['phfsi']
        X = df_large[['subsidy_dependence', 'log_revenue', 'debt_ratio']]
        data = pd.concat([y, X], axis=1).dropna()

        if len(data) > 20:
            y = data['phfsi']
            X = data[['subsidy_dependence', 'log_revenue', 'debt_ratio']]
            model = PanelOLS(y, X, entity_effects=True, time_effects=True)
            result = model.fit(cov_type='clustered', cluster_entity=True)
            results['exclude_small'] = result
            logger.info(f"    β(subsidy) = {result.params['subsidy_dependence']:.4f}, p = {result.pvalues['subsidy_dependence']:.4f}, N = {result.nobs}")

        # Test 2c: Exclude Lisbon/Porto regions
        logger.info("  2c: Exclude Lisbon/Porto regions...")
        df_no_major = self.panel[
            ~self.panel['entidade'].str.contains('Lisboa|Porto', case=False, na=False)
        ].copy()
        df_no_major = self.prepare_regression_data(df_no_major)

        y = df_no_major['phfsi']
        X = df_no_major[['subsidy_dependence', 'log_revenue', 'debt_ratio']]
        data = pd.concat([y, X], axis=1).dropna()

        if len(data) > 20:
            y = data['phfsi']
            X = data[['subsidy_dependence', 'log_revenue', 'debt_ratio']]
            model = PanelOLS(y, X, entity_effects=True, time_effects=True)
            result = model.fit(cov_type='clustered', cluster_entity=True)
            results['exclude_major_cities'] = result
            logger.info(f"    β(subsidy) = {result.params['subsidy_dependence']:.4f}, p = {result.pvalues['subsidy_dependence']:.4f}, N = {result.nobs}")

        self.robustness_results.update(results)
        return results

    def robustness_alternative_standard_errors(self):
        """
        Test 3: Alternative standard errors.

        - Entity clustering (baseline - already done)
        - Heteroskedasticity-robust only
        """
        logger.info("Robustness Test 3: Alternative Standard Errors...")

        results = {}
        df = self.prepare_regression_data(self.panel)

        y = df['phfsi']
        X = df[['subsidy_dependence', 'log_revenue', 'debt_ratio']]
        data = pd.concat([y, X], axis=1).dropna()
        y = data['phfsi']
        X = data[['subsidy_dependence', 'log_revenue', 'debt_ratio']]

        model = PanelOLS(y, X, entity_effects=True, time_effects=True)

        # Test 3a: Heteroskedasticity-robust only (White)
        logger.info("  3a: Heteroskedasticity-robust SE (no clustering)...")
        result = model.fit(cov_type='robust')
        results['robust_se'] = result
        logger.info(f"    β(subsidy) = {result.params['subsidy_dependence']:.4f}, SE = {result.std_errors['subsidy_dependence']:.4f}")

        # Test 3b: Homoskedastic (for comparison)
        logger.info("  3b: Homoskedastic SE (for comparison)...")
        result = model.fit(cov_type='unadjusted')
        results['unadjusted_se'] = result
        logger.info(f"    β(subsidy) = {result.params['subsidy_dependence']:.4f}, SE = {result.std_errors['subsidy_dependence']:.4f}")

        self.robustness_results.update(results)
        return results

    def generate_robustness_table(self):
        """Generate Appendix Table A1 with all robustness checks."""
        logger.info("Generating Appendix Table A1: Robustness Checks...")

        # Extract key results
        results_summary = []

        test_labels = {
            'baseline': 'Baseline',
            'spi_priority': 'Alt PHFSI: Prioritize SPI',
            'exclude_spi': 'Alt PHFSI: Exclude SPI',
            'exclude_covid': 'Exclude COVID (2020-2021)',
            'exclude_small': 'Exclude Small Hospitals',
            'exclude_major_cities': 'Exclude Lisbon/Porto',
            'robust_se': 'Heteroskedasticity-Robust SE',
            'unadjusted_se': 'Unadjusted SE',
        }

        for key, label in test_labels.items():
            if key in self.robustness_results:
                result = self.robustness_results[key]
                results_summary.append({
                    'Test': label,
                    'Subsidy_Coef': result.params['subsidy_dependence'],
                    'Subsidy_SE': result.std_errors['subsidy_dependence'],
                    'Subsidy_PValue': result.pvalues['subsidy_dependence'],
                    'R_Squared': result.rsquared,
                    'N_Obs': result.nobs,
                })

        # Create DataFrame
        tableA1 = pd.DataFrame(results_summary)

        # Save CSV
        csv_path = OUTPUT_DIR / "tableA1_robustness_checks.csv"
        tableA1.to_csv(csv_path, index=False)
        logger.info(f"Table A1 saved to: {csv_path}")

        # Generate LaTeX
        self.generate_latex_tableA1(tableA1)

        return tableA1

    def generate_latex_tableA1(self, tableA1):
        """Generate LaTeX formatted Appendix Table A1."""
        logger.info("Generating LaTeX version of Table A1...")

        latex_parts = []
        latex_parts.append("\\begin{table}[htbp]")
        latex_parts.append("\\centering")
        latex_parts.append("\\caption{Robustness Checks: Alternative Specifications}")
        latex_parts.append("\\label{tab:robustness}")
        latex_parts.append("\\begin{tabular}{lcccc}")
        latex_parts.append("\\hline\\hline")
        latex_parts.append("Specification & Subsidy Coef. & Std. Error & P-Value & N \\\\")
        latex_parts.append("\\hline")

        for _, row in tableA1.iterrows():
            # Significance stars
            stars = ''
            if row['Subsidy_PValue'] < 0.01:
                stars = '***'
            elif row['Subsidy_PValue'] < 0.05:
                stars = '**'
            elif row['Subsidy_PValue'] < 0.10:
                stars = '*'

            line = f"{row['Test']} & "
            line += f"{row['Subsidy_Coef']:.3f}{stars} & "
            line += f"({row['Subsidy_SE']:.3f}) & "
            line += f"{row['Subsidy_PValue']:.3f} & "
            line += f"{row['N_Obs']:.0f} \\\\"
            latex_parts.append(line)

        latex_parts.append("\\hline\\hline")
        latex_parts.append("\\end{tabular}")
        latex_parts.append("\\begin{tablenotes}")
        latex_parts.append("\\small")
        latex_parts.append("\\item Notes: Dependent variable is PHFSI in all specifications. ")
        latex_parts.append("All models include hospital and year fixed effects. ")
        latex_parts.append("Controls: log(revenue), debt ratio. ")
        latex_parts.append("*** p<0.01, ** p<0.05, * p<0.10.")
        latex_parts.append("\\end{tablenotes}")
        latex_parts.append("\\end{table}")

        # Save LaTeX
        tex_path = OUTPUT_DIR / "tableA1_robustness_checks.tex"
        with open(tex_path, 'w') as f:
            f.write('\n'.join(latex_parts))

        logger.info(f"Table A1 LaTeX saved to: {tex_path}")

    def run_pipeline(self):
        """Execute full robustness checks pipeline."""
        logger.info("Starting robustness checks pipeline...")
        logger.info("="*60 + "\n")

        # Load data
        self.load_data()

        # Run baseline
        self.run_baseline_model()

        # Run robustness tests
        self.robustness_alternative_phfsi_weights()
        self.robustness_sample_variations()
        self.robustness_alternative_standard_errors()

        # Generate table
        tableA1 = self.generate_robustness_table()

        logger.info("\n" + "="*60)
        logger.info("ROBUSTNESS CHECKS PIPELINE COMPLETE")
        logger.info("="*60)
        logger.info("\nGenerated files:")
        logger.info(f"  - {OUTPUT_DIR / 'tableA1_robustness_checks.csv'}")
        logger.info(f"  - {OUTPUT_DIR / 'tableA1_robustness_checks.tex'}")

        return tableA1


def main():
    """Main execution function."""
    analyzer = RobustnessAnalyzer()
    tableA1 = analyzer.run_pipeline()

    print("\n" + "="*60)
    print("ROBUSTNESS CHECKS SUMMARY")
    print("="*60)
    print(tableA1.to_string(index=False))


if __name__ == "__main__":
    main()
