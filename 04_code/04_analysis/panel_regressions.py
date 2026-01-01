"""
Fixed Effects Panel Regressions for PHFSI Analysis

Implements three main models:
1. PHFSI Determinants (H1: Subsidy dependence → lower PHFSI)
2. Payment Delays & Subsidy Dependence (H2: Moral hazard effect)
3. Governance Proxy Analysis (Hospital characteristics → PHFSI)

Uses two-way fixed effects (hospital + year) with clustered standard errors.

Author: Research Team
Date: 2025-12-31
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Import econometric libraries
try:
    from linearmodels.panel import PanelOLS
    from linearmodels.panel import compare
except ImportError:
    print("ERROR: linearmodels not installed. Install with: pip install linearmodels")
    raise

try:
    import statsmodels.api as sm
    from statsmodels.iolib.summary2 import summary_col
except ImportError:
    print("ERROR: statsmodels not installed. Install with: pip install statsmodels")
    raise

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PROCESSED = PROJECT_ROOT / "03_data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "06_output" / "tables" / "main"
RESULTS_DIR = PROJECT_ROOT / "06_output" / "results" / "regressions"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class PanelRegressionAnalyzer:
    """
    Runs fixed effects panel regressions for PHFSI analysis.
    """

    def __init__(self):
        self.panel = None
        self.results = {}

    def load_data(self):
        """Load panel dataset with PHFSI scores."""
        logger.info("Loading panel data...")

        # Load panel
        panel_path = DATA_PROCESSED / "panel" / "hospital_year_panel.parquet"
        if not panel_path.exists():
            raise FileNotFoundError(f"Panel not found at {panel_path}")

        self.panel = pd.read_parquet(panel_path)

        # Load PHFSI scores
        phfsi_path = DATA_PROCESSED / "variables" / "phfsi_scores.parquet"
        if not phfsi_path.exists():
            raise FileNotFoundError(f"PHFSI scores not found at {phfsi_path}")

        phfsi_scores = pd.read_parquet(phfsi_path)

        # Merge PHFSI and components
        merge_cols = ['entidade', 'year', 'phfsi', 'phfsi_cluster']
        for col in ['ossr', 'spi', 'lrr', 'tlr', 'cqmi']:
            if col in phfsi_scores.columns:
                merge_cols.append(col)

        self.panel = self.panel.merge(
            phfsi_scores[merge_cols],
            on=['entidade', 'year'],
            how='left'
        )

        logger.info(f"Loaded panel: {len(self.panel)} rows, {self.panel['entidade'].nunique()} entities")

    def prepare_panel_data(self):
        """Prepare data for panel regression (create variables, set index)."""
        logger.info("Preparing panel data for regression...")

        df = self.panel.copy()

        # Filter to hospitals only
        hospital_keywords = [
            'Hospital', 'Hospitalar', 'Unidade Local de Saúde',
            'ULS', 'IPO', 'Instituto Português'
        ]
        hospital_mask = df['entidade'].str.contains(
            '|'.join(hospital_keywords),
            case=False,
            na=False
        )
        df = df[hospital_mask].copy()

        # Create key variables

        # 1. Subsidy dependence proxy: negative operating result ratio
        # (higher = more subsidies needed)
        df['subsidy_dependence'] = -df['resultados_operacionais'] / df['rendimentos_operacionais']
        df['subsidy_dependence'] = df['subsidy_dependence'].clip(lower=-1, upper=1)

        # 2. Size variables (log transform)
        df['log_revenue'] = np.log(df['rendimentos_operacionais'] + 1)
        df['log_debt'] = np.log(df['divida_total_fornecedores_externos'] + 1)

        # 3. Debt ratio
        df['debt_ratio'] = df['divida_total_fornecedores_externos'] / df['rendimentos_operacionais']
        df['debt_ratio'] = df['debt_ratio'].clip(upper=5)  # Cap outliers

        # 4. Overdue ratio
        df['overdue_ratio'] = (df['divida_vencida_fornecedores_externos'] /
                                df['divida_total_fornecedores_externos'])
        df['overdue_ratio'] = df['overdue_ratio'].clip(lower=0, upper=1)

        # 5. Past bailout indicator (lagged capital injection)
        # For now, create placeholder (would need actual bailout data)
        df['past_bailout'] = 0  # TODO: Add actual bailout data when available

        # 6. Governance proxies
        # University hospital indicator
        df['university_hospital'] = df['entidade'].str.contains(
            'Universitário', case=False, na=False
        ).astype(int)

        # Large hospital indicator (top quartile by revenue)
        revenue_75 = df['rendimentos_operacionais'].quantile(0.75)
        df['large_hospital'] = (df['rendimentos_operacionais'] > revenue_75).astype(int)

        # Set multi-index for panel data (entity, year)
        df = df.set_index(['entidade', 'year'])

        # Drop rows with missing PHFSI
        df = df[df['phfsi'].notna()].copy()

        logger.info(f"Prepared panel: {len(df)} observations, {df.index.get_level_values(0).nunique()} entities")
        logger.info(f"Years: {df.index.get_level_values(1).min()} to {df.index.get_level_values(1).max()}")

        self.panel = df

    def run_model1_phfsi_determinants(self):
        """
        Model 1: PHFSI Determinants

        DV: PHFSI
        IVs: Subsidy dependence, size (log revenue), debt ratio
        FE: Hospital + Year
        SE: Clustered at hospital level

        H1: Subsidy dependence → Lower PHFSI (β < 0)
        """
        logger.info("Running Model 1: PHFSI Determinants...")

        df = self.panel.copy()

        # Select variables (removed GDP - collinear with year FE)
        y = df['phfsi']
        X = df[['subsidy_dependence', 'log_revenue', 'debt_ratio']]

        # Drop missing values
        data = pd.concat([y, X], axis=1).dropna()

        # Extract y and X from cleaned data
        y = data['phfsi']
        X = data[['subsidy_dependence', 'log_revenue', 'debt_ratio']]

        # Run two-way fixed effects regression
        model = PanelOLS(y, X, entity_effects=True, time_effects=True)
        results = model.fit(cov_type='clustered', cluster_entity=True)

        logger.info(f"Model 1 R²: {results.rsquared:.4f}")
        logger.info(f"Model 1 Observations: {results.nobs}")

        # Store results
        self.results['model1'] = results

        return results

    def run_model2_payment_delays(self):
        """
        Model 2: Payment Delays & Subsidy Dependence

        DV: Payment delays (days)
        IVs: Subsidy dependence, debt ratio, overdue ratio
        FE: Hospital + Year
        SE: Clustered at hospital level

        H2: Subsidy dependence → Higher payment delays (β > 0)
        """
        logger.info("Running Model 2: Payment Delays & Subsidy Dependence...")

        df = self.panel.copy()

        # Select variables (removed past_bailout - no variation)
        y = df['pagamentos_em_atraso']
        X = df[['subsidy_dependence', 'debt_ratio', 'overdue_ratio']]

        # Drop missing values
        data = pd.concat([y, X], axis=1).dropna()

        # Extract y and X from cleaned data
        y = data['pagamentos_em_atraso']
        X = data[['subsidy_dependence', 'debt_ratio', 'overdue_ratio']]

        # Run two-way fixed effects regression
        model = PanelOLS(y, X, entity_effects=True, time_effects=True)
        results = model.fit(cov_type='clustered', cluster_entity=True)

        logger.info(f"Model 2 R²: {results.rsquared:.4f}")
        logger.info(f"Model 2 Observations: {results.nobs}")

        # Store results
        self.results['model2'] = results

        return results

    def run_model3_governance_proxies(self):
        """
        Model 3: Governance Proxies

        DV: PHFSI
        IVs: University hospital (time-invariant, absorbed by FE), overdue ratio, log debt
        FE: Hospital + Year
        SE: Clustered at hospital level

        H3: Better governance → Higher PHFSI

        Note: University_hospital is time-invariant and will be absorbed by hospital FE.
        """
        logger.info("Running Model 3: Governance Proxies...")

        df = self.panel.copy()

        # Select variables (removed covid_period - collinear with year FE)
        # University_hospital is time-invariant, will be absorbed by hospital FE
        y = df['phfsi']
        X = df[['overdue_ratio', 'log_debt', 'log_revenue']]

        # Drop missing values
        data = pd.concat([y, X], axis=1).dropna()

        # Extract y and X from cleaned data
        y = data['phfsi']
        X = data[['overdue_ratio', 'log_debt', 'log_revenue']]

        # Run two-way fixed effects regression
        model = PanelOLS(y, X, entity_effects=True, time_effects=True)
        results = model.fit(cov_type='clustered', cluster_entity=True)

        logger.info(f"Model 3 R²: {results.rsquared:.4f}")
        logger.info(f"Model 3 Observations: {results.nobs}")

        # Store results
        self.results['model3'] = results

        return results

    def generate_regression_table(self):
        """Generate formatted regression table for publication."""
        logger.info("Generating regression results table...")

        # Create comparison table
        results_list = [self.results['model1'], self.results['model2'], self.results['model3']]
        model_names = ['PHFSI Determinants', 'Payment Delays', 'Governance Proxies']

        # Save detailed results to CSV
        for model_name, result in zip(model_names, results_list):
            csv_path = RESULTS_DIR / f"{model_name.lower().replace(' ', '_')}_results.csv"

            # Extract coefficients, std errors, t-stats, p-values
            results_df = pd.DataFrame({
                'Variable': result.params.index,
                'Coefficient': result.params.values,
                'Std_Error': result.std_errors.values,
                'T_Stat': result.tstats.values,
                'P_Value': result.pvalues.values,
                'CI_Lower': result.conf_int().iloc[:, 0].values,
                'CI_Upper': result.conf_int().iloc[:, 1].values,
            })

            results_df.to_csv(csv_path, index=False)
            logger.info(f"Saved {model_name} results to: {csv_path}")

        # Generate LaTeX table
        self.generate_latex_table3()

    def generate_latex_table3(self):
        """Generate LaTeX formatted Table 3 for paper."""
        logger.info("Generating LaTeX Table 3...")

        latex_parts = []
        latex_parts.append("\\begin{table}[htbp]")
        latex_parts.append("\\centering")
        latex_parts.append("\\caption{Fixed Effects Panel Regression Results}")
        latex_parts.append("\\label{tab:panel_regressions}")
        latex_parts.append("\\begin{tabular}{lccc}")
        latex_parts.append("\\hline\\hline")
        latex_parts.append(" & (1) & (2) & (3) \\\\")
        latex_parts.append(" & PHFSI & Payment Delays & PHFSI \\\\")
        latex_parts.append(" & Determinants & & Governance \\\\")
        latex_parts.append("\\hline")

        # Extract key coefficients
        models = [self.results['model1'], self.results['model2'], self.results['model3']]

        # Common variables to display
        var_names = {
            'subsidy_dependence': 'Subsidy Dependence',
            'log_revenue': 'Log(Revenue)',
            'gdp_per_capita_eur': 'GDP per Capita',
            'covid_period': 'COVID Period',
            'past_bailout': 'Past Bailout',
            'debt_ratio': 'Debt Ratio',
            'university_hospital': 'University Hospital',
            'large_hospital': 'Large Hospital',
            'overdue_ratio': 'Overdue Ratio',
        }

        # Add coefficients
        for var_key, var_name in var_names.items():
            line = f"{var_name}"
            for model in models:
                if var_key in model.params.index:
                    coef = model.params[var_key]
                    se = model.std_errors[var_key]
                    pval = model.pvalues[var_key]

                    # Significance stars
                    stars = ''
                    if pval < 0.01:
                        stars = '***'
                    elif pval < 0.05:
                        stars = '**'
                    elif pval < 0.10:
                        stars = '*'

                    line += f" & {coef:.3f}{stars}"
                    line += f"\\\\ & ({se:.3f})"
                else:
                    line += " & "

            latex_parts.append(line + " \\\\")

        latex_parts.append("\\hline")

        # Add model statistics
        latex_parts.append(f"Observations & {models[0].nobs:.0f} & {models[1].nobs:.0f} & {models[2].nobs:.0f} \\\\")
        latex_parts.append(f"R-squared & {models[0].rsquared:.3f} & {models[1].rsquared:.3f} & {models[2].rsquared:.3f} \\\\")
        latex_parts.append("Hospital FE & Yes & Yes & Yes \\\\")
        latex_parts.append("Year FE & Yes & Yes & Yes \\\\")
        latex_parts.append("Clustered SE & Yes & Yes & Yes \\\\")

        latex_parts.append("\\hline\\hline")
        latex_parts.append("\\end{tabular}")
        latex_parts.append("\\begin{tablenotes}")
        latex_parts.append("\\small")
        latex_parts.append("\\item Notes: Two-way fixed effects panel regressions with hospital and year fixed effects. ")
        latex_parts.append("Standard errors clustered at hospital level in parentheses. ")
        latex_parts.append("*** p<0.01, ** p<0.05, * p<0.10.")
        latex_parts.append("\\end{tablenotes}")
        latex_parts.append("\\end{table}")

        # Save
        tex_path = OUTPUT_DIR / "table3_panel_regressions.tex"
        with open(tex_path, 'w') as f:
            f.write('\n'.join(latex_parts))

        logger.info(f"Table 3 saved to: {tex_path}")

    def run_diagnostics(self):
        """Run regression diagnostics."""
        logger.info("\n" + "="*60)
        logger.info("REGRESSION DIAGNOSTICS")
        logger.info("="*60)

        for model_name, result in self.results.items():
            logger.info(f"\n{model_name.upper()}:")
            logger.info(f"  Observations: {result.nobs}")
            logger.info(f"  R-squared: {result.rsquared:.4f}")
            logger.info(f"  Within R-squared: {result.rsquared_within:.4f}")
            logger.info(f"  Between R-squared: {result.rsquared_between:.4f}")
            logger.info(f"  F-statistic: {result.f_statistic.stat:.4f} (p={result.f_statistic.pval:.4f})")

        logger.info("\n" + "="*60)

    def run_pipeline(self):
        """Execute full panel regression pipeline."""
        logger.info("Starting panel regression analysis...")
        logger.info("="*60 + "\n")

        # Load and prepare data
        self.load_data()
        self.prepare_panel_data()

        # Run models
        self.run_model1_phfsi_determinants()
        self.run_model2_payment_delays()
        self.run_model3_governance_proxies()

        # Generate tables
        self.generate_regression_table()

        # Diagnostics
        self.run_diagnostics()

        logger.info("\n" + "="*60)
        logger.info("PANEL REGRESSION PIPELINE COMPLETE")
        logger.info("="*60)

        return self.results


def main():
    """Main execution function."""
    analyzer = PanelRegressionAnalyzer()
    results = analyzer.run_pipeline()

    print("\n" + "="*60)
    print("REGRESSION RESULTS SUMMARY")
    print("="*60)

    for model_name, result in results.items():
        print(f"\n{model_name.upper()}:")
        print(result.summary)


if __name__ == "__main__":
    main()
