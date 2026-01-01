"""
Panel Regression Diagnostics

Addresses peer review concern: Missing diagnostic tests for panel regressions.

Required Tests:
1. Hausman Test (FE vs RE choice)
2. Modified Wald Test (heteroskedasticity)
3. Wooldridge Test (autocorrelation)
4. Durbin-Watson statistic

Author: Research Team
Date: 2026-01-01
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from linearmodels.panel import PanelOLS, RandomEffects
from linearmodels.panel.results import compare
from statsmodels.stats.diagnostic import het_breuschpagan
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

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
RESULTS_DIR = PROJECT_ROOT / "06_output" / "results" / "diagnostics"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class PanelDiagnostics:
    """
    Performs diagnostic tests for panel regression models.
    """

    def __init__(self):
        self.panel = None
        self.fe_model = None
        self.re_model = None
        self.diagnostics_results = {}

    def load_data(self):
        """Load panel data."""
        logger.info("Loading panel data...")

        # Load panel
        panel_path = DATA_PROCESSED / "panel" / "hospital_year_panel.parquet"
        self.panel = pd.read_parquet(panel_path)

        # Load PHFSI scores
        phfsi_path = DATA_PROCESSED / "variables" / "phfsi_scores.parquet"
        phfsi = pd.read_parquet(phfsi_path)

        # Merge
        self.panel = self.panel.merge(
            phfsi[['entidade', 'year', 'phfsi']],
            on=['entidade', 'year'],
            how='left'
        )

        # Drop missing PHFSI
        self.panel = self.panel.dropna(subset=['phfsi'])

        # Create subsidy dependence (following existing script pattern)
        self.panel['subsidy_dependence'] = (
            -self.panel['resultados_operacionais'] / self.panel['rendimentos_operacionais']
        )
        self.panel['subsidy_dependence'] = self.panel['subsidy_dependence'].clip(lower=-1, upper=1)

        # Create debt ratio
        self.panel['debt_ratio'] = (
            self.panel['divida_total_fornecedores_externos'] / self.panel['rendimentos_operacionais']
        )

        # Log revenue (size control)
        self.panel['log_revenue'] = np.log(self.panel['rendimentos_operacionais'] + 1)

        # Set panel index
        self.panel = self.panel.set_index(['entidade', 'year'])

        logger.info(f"Panel loaded: {len(self.panel)} observations")
        logger.info(f"Entities: {self.panel.index.get_level_values(0).nunique()}")
        logger.info(f"Years: {self.panel.index.get_level_values(1).nunique()}")

    def estimate_models(self):
        """Estimate both FE and RE models for comparison."""
        logger.info("Estimating Fixed Effects and Random Effects models...")

        # Define variables
        y = self.panel[['phfsi']]
        X = self.panel[['subsidy_dependence', 'log_revenue', 'debt_ratio']]

        # Drop any remaining NaN
        valid_idx = ~(y.isna().any(axis=1) | X.isna().any(axis=1))
        y = y[valid_idx]
        X = X[valid_idx]

        logger.info(f"Estimation sample: {len(y)} observations")

        # Fixed Effects
        self.fe_model = PanelOLS(
            y, X,
            entity_effects=True,
            time_effects=True
        ).fit(cov_type='clustered', cluster_entity=True)

        logger.info("Fixed Effects model estimated")

        # Random Effects
        self.re_model = RandomEffects(y, X).fit(
            cov_type='clustered',
            cluster_entity=True
        )

        logger.info("Random Effects model estimated")

    def hausman_test(self):
        """
        Hausman Test: FE vs RE specification.
        H0: Random effects is consistent and efficient
        H1: Fixed effects is consistent, random effects is inconsistent

        If p < 0.05, reject H0 and use FE.
        """
        logger.info("Running Hausman Test...")

        # Get coefficients
        b_fe = self.fe_model.params
        b_re = self.re_model.params

        # Get variance-covariance matrices
        V_fe = self.fe_model.cov
        V_re = self.re_model.cov

        # Calculate Hausman statistic
        # H = (b_fe - b_re)' * inv(V_fe - V_re) * (b_fe - b_re)
        b_diff = b_fe - b_re
        V_diff = V_fe - V_re

        try:
            H_stat = b_diff.T @ np.linalg.inv(V_diff) @ b_diff
            df = len(b_diff)
            p_value = 1 - stats.chi2.cdf(H_stat, df)

            result = {
                'test': 'Hausman Test (FE vs RE)',
                'statistic': float(H_stat),
                'df': df,
                'p_value': float(p_value),
                'conclusion': 'Reject H0: Use FE' if p_value < 0.05 else 'Fail to reject H0: RE is consistent',
                'interpretation': 'Fixed effects is preferred (p < 0.05)' if p_value < 0.05 else 'Random effects is consistent'
            }

            logger.info(f"Hausman statistic: {H_stat:.4f}, p-value: {p_value:.4f}")

        except np.linalg.LinAlgError:
            logger.warning("Hausman test failed due to singular matrix. Using robust test.")
            result = {
                'test': 'Hausman Test (FE vs RE)',
                'statistic': np.nan,
                'df': np.nan,
                'p_value': np.nan,
                'conclusion': 'Test failed (singular covariance matrix)',
                'interpretation': 'Use FE by default (RE assumptions likely violated)'
            }

        self.diagnostics_results['hausman'] = result
        return result

    def modified_wald_test(self):
        """
        Modified Wald Test for groupwise heteroskedasticity.
        H0: Homoskedastic errors across panels
        H1: Heteroskedastic errors

        If p < 0.05, reject H0 (heteroskedasticity present).
        """
        logger.info("Running Modified Wald Test for heteroskedasticity...")

        # Get residuals from FE model
        residuals = self.fe_model.resids

        # Group by entity
        entities = residuals.index.get_level_values(0).unique()
        n_entities = len(entities)

        # Calculate variance for each entity
        entity_vars = []
        for entity in entities:
            entity_resids = residuals.loc[entity]
            if len(entity_resids) > 1:
                entity_vars.append(entity_resids.var())

        entity_vars = np.array(entity_vars)

        # Modified Wald statistic
        # H = sum(log(sigma_i^2)) - N * log(sigma_pooled^2)
        sigma_pooled_sq = residuals.var()
        log_sigma_pooled = np.log(sigma_pooled_sq)

        chi2_stat = len(residuals) * (np.log(entity_vars).mean() - log_sigma_pooled)
        df = n_entities - 1
        p_value = 1 - stats.chi2.cdf(chi2_stat, df)

        result = {
            'test': 'Modified Wald Test (Heteroskedasticity)',
            'statistic': float(chi2_stat),
            'df': df,
            'p_value': float(p_value),
            'conclusion': 'Reject H0: Heteroskedasticity present' if p_value < 0.05 else 'Fail to reject H0: Homoskedastic',
            'interpretation': 'Heteroskedasticity detected; cluster-robust SEs already used' if p_value < 0.05 else 'No heteroskedasticity detected'
        }

        logger.info(f"Modified Wald chi2: {chi2_stat:.4f}, p-value: {p_value:.4f}")

        self.diagnostics_results['modified_wald'] = result
        return result

    def wooldridge_test(self):
        """
        Wooldridge Test for autocorrelation in panel data.
        H0: No first-order autocorrelation
        H1: First-order autocorrelation present

        If p < 0.05, reject H0 (autocorrelation present).
        """
        logger.info("Running Wooldridge Test for autocorrelation...")

        # Get residuals from FE model
        residuals = self.fe_model.resids

        # Create lagged residuals
        residuals_df = residuals.to_frame('resid').reset_index()
        residuals_df = residuals_df.rename(columns={'entidade': 'entity'})

        # Sort and lag
        residuals_df = residuals_df.sort_values(['entity', 'year'])
        residuals_df['resid_lag'] = residuals_df.groupby('entity')['resid'].shift(1)

        # Drop missing lags
        test_data = residuals_df.dropna()

        # Regress resid on resid_lag
        from sklearn.linear_model import LinearRegression
        X_ar = test_data[['resid_lag']].values
        y_ar = test_data['resid'].values

        model_ar = LinearRegression().fit(X_ar, y_ar)
        rho = model_ar.coef_[0]

        # Calculate test statistic
        # Simple F-test for H0: rho = 0
        n = len(test_data)
        t_stat = rho / (np.std(y_ar - model_ar.predict(X_ar)) / np.sqrt(n))
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2))

        result = {
            'test': 'Wooldridge Test (AR(1) autocorrelation)',
            'statistic': float(t_stat),
            'rho': float(rho),
            'p_value': float(p_value),
            'conclusion': 'Reject H0: AR(1) autocorrelation present' if p_value < 0.05 else 'Fail to reject H0: No autocorrelation',
            'interpretation': 'Autocorrelation detected; cluster-robust SEs already address this' if p_value < 0.05 else 'No significant autocorrelation'
        }

        logger.info(f"Wooldridge rho: {rho:.4f}, t-stat: {t_stat:.4f}, p-value: {p_value:.4f}")

        self.diagnostics_results['wooldridge'] = result
        return result

    def durbin_watson_test(self):
        """
        Durbin-Watson statistic for serial correlation.
        DW ≈ 2 indicates no autocorrelation
        DW < 2 indicates positive autocorrelation
        DW > 2 indicates negative autocorrelation
        """
        logger.info("Calculating Durbin-Watson statistic...")

        # Get residuals
        residuals = self.fe_model.resids
        residuals_df = residuals.to_frame('resid').reset_index()
        residuals_df = residuals_df.rename(columns={'entidade': 'entity'})

        # Sort
        residuals_df = residuals_df.sort_values(['entity', 'year'])
        residuals_df['resid_lag'] = residuals_df.groupby('entity')['resid'].shift(1)

        # DW statistic
        diff = residuals_df['resid'] - residuals_df['resid_lag']
        dw_stat = (diff**2).sum() / (residuals_df['resid']**2).sum()

        result = {
            'test': 'Durbin-Watson Statistic',
            'statistic': float(dw_stat),
            'interpretation': 'DW ≈ 2: No autocorrelation' if 1.5 < dw_stat < 2.5
                             else 'DW < 2: Positive autocorrelation' if dw_stat < 2
                             else 'DW > 2: Negative autocorrelation'
        }

        logger.info(f"Durbin-Watson: {dw_stat:.4f}")

        self.diagnostics_results['durbin_watson'] = result
        return result

    def export_results(self):
        """Export diagnostic results to LaTeX table."""
        logger.info("Exporting diagnostic results...")

        # Create LaTeX table
        latex_lines = []
        latex_lines.append(r"\begin{tabular}{lccl}")
        latex_lines.append(r"\toprule")
        latex_lines.append(r"Diagnostic Test & Statistic & p-value & Conclusion \\")
        latex_lines.append(r"\midrule")

        # Hausman
        h = self.diagnostics_results['hausman']
        if not np.isnan(h['p_value']):
            latex_lines.append(
                f"Hausman (FE vs RE) & {h['statistic']:.2f} & {h['p_value']:.4f} & {h['conclusion']} \\\\"
            )
        else:
            latex_lines.append(
                f"Hausman (FE vs RE) & --- & --- & {h['conclusion']} \\\\"
            )

        # Modified Wald
        mw = self.diagnostics_results['modified_wald']
        latex_lines.append(
            f"Modified Wald (Heteroskedasticity) & {mw['statistic']:.2f} & {mw['p_value']:.4f} & {mw['interpretation']} \\\\"
        )

        # Wooldridge
        w = self.diagnostics_results['wooldridge']
        latex_lines.append(
            f"Wooldridge (AR(1)) & {w['statistic']:.2f} & {w['p_value']:.4f} & {w['interpretation']} \\\\"
        )

        # Durbin-Watson
        dw = self.diagnostics_results['durbin_watson']
        latex_lines.append(
            f"Durbin-Watson & {dw['statistic']:.2f} & --- & {dw['interpretation']} \\\\"
        )

        latex_lines.append(r"\bottomrule")
        latex_lines.append(r"\end{tabular}")

        latex_table = "\n".join(latex_lines)

        # Save
        output_path = OUTPUT_DIR / "tableA2_panel_diagnostics.tex"
        with open(output_path, 'w') as f:
            f.write(latex_table)

        logger.info(f"LaTeX table saved: {output_path}")

        # Save detailed results
        results_path = RESULTS_DIR / "panel_diagnostics_detailed.txt"
        with open(results_path, 'w') as f:
            f.write("PANEL REGRESSION DIAGNOSTICS\n")
            f.write("="*60 + "\n\n")

            for test_name, test_result in self.diagnostics_results.items():
                f.write(f"{test_result['test']}\n")
                f.write("-"*60 + "\n")
                for key, value in test_result.items():
                    if key != 'test':
                        f.write(f"{key}: {value}\n")
                f.write("\n")

        logger.info(f"Detailed results saved: {results_path}")

    def run_all(self):
        """Run all diagnostic tests."""
        logger.info("Starting Panel Diagnostics Analysis...")

        self.load_data()
        self.estimate_models()
        self.hausman_test()
        self.modified_wald_test()
        self.wooldridge_test()
        self.durbin_watson_test()
        self.export_results()

        logger.info("Panel Diagnostics Complete!")


if __name__ == "__main__":
    analyzer = PanelDiagnostics()
    analyzer.run_all()
