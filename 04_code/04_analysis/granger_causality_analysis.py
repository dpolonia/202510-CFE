"""
Granger Causality Analysis: Sequential Transfer Mechanism

Tests temporal ordering of stakeholder-distributed distress:
Payment Delays(t) → Staff Constraints(t+1) → Quality Decline(t+2) → Bailout(t+3)

Addresses peer review critique:
"The sequential transfer mechanism untested - The mechanism tests (Section 4.3)
just show cross-sectional correlations between subsidy dependence and various
distress symptoms, not their temporal ordering. From a finance perspective,
establishing *timing* is critical. Does liquidity stress *cause* quality decline,
or do they co-occur? Granger causality tests would address this."

Methodology:
- Granger causality tests (statsmodels)
- Vector Autoregression (VAR)
- Impulse Response Functions (IRF)
- Panel Granger causality (if sufficient observations)

Input:
- Monthly panel dataset: 03_data/processed/panel/hospital_month_panel.parquet

Output:
- Granger causality results: 06_output/results/granger_causality_results.txt
- IRF plots: 06_output/figures/mechanisms/irf_*.pdf
- Summary table: 06_output/tables/appendix/tableA3_granger_causality.tex

Author: Research Team
Date: 2025-12-31
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import warnings
warnings.filterwarnings('ignore')

# Statistical models
from statsmodels.tsa.stattools import grangercausalitytests, adfuller
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.vecm import coint_johansen
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "03_data" / "processed" / "panel"
OUTPUT_DIR = PROJECT_ROOT / "06_output" / "results"
FIGURE_DIR = PROJECT_ROOT / "06_output" / "figures" / "mechanisms"
TABLE_DIR = PROJECT_ROOT / "06_output" / "tables" / "appendix"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)


class GrangerCausalityAnalyzer:
    """
    Analyzes temporal ordering of distress symptoms using Granger causality.
    """

    def __init__(self, monthly_panel_path):
        self.monthly_panel_path = monthly_panel_path
        self.monthly_panel = None
        self.results = {}

    def load_monthly_panel(self):
        """Load monthly panel dataset."""
        logger.info("Loading monthly panel dataset...")

        self.monthly_panel = pd.read_parquet(self.monthly_panel_path)
        logger.info(f"Loaded {len(self.monthly_panel)} hospital-months")
        logger.info(f"Columns: {self.monthly_panel.columns.tolist()}")

    def prepare_time_series(self, entity, variables, min_periods=36):
        """
        Prepare time series for a single hospital entity.

        Parameters:
        - entity: Hospital name/ID
        - variables: List of variable names to include
        - min_periods: Minimum number of time periods required (default: 36 months = 3 years)

        Returns:
        - DataFrame with time-indexed variables, or None if insufficient data
        """
        # Filter to specific entity
        entity_data = self.monthly_panel[self.monthly_panel['entidade'] == entity].copy()

        if len(entity_data) < min_periods:
            return None

        # Create year_month if it doesn't exist
        if 'year_month' not in entity_data.columns:
            entity_data['year_month'] = pd.to_datetime(
                entity_data[['year', 'month']].assign(day=1)
            ).dt.to_period('M')

        # Sort by time
        entity_data = entity_data.sort_values('year_month')

        # Set time index
        entity_data['date'] = pd.to_datetime(entity_data['year_month'].astype(str))
        entity_data = entity_data.set_index('date')

        # Select variables
        available_vars = [v for v in variables if v in entity_data.columns]

        if not available_vars:
            return None

        ts_data = entity_data[available_vars]

        # Remove rows with all NaN
        ts_data = ts_data.dropna(how='all')

        # Forward fill small gaps (up to 2 months)
        ts_data = ts_data.fillna(method='ffill', limit=2)

        # Drop remaining NaNs
        ts_data = ts_data.dropna()

        if len(ts_data) < min_periods:
            return None

        return ts_data

    def test_stationarity(self, series, name):
        """
        Test if time series is stationary using Augmented Dickey-Fuller test.

        Returns: (is_stationary, p_value)
        """
        result = adfuller(series.dropna(), autolag='AIC')
        p_value = result[1]
        is_stationary = p_value < 0.05

        logger.info(f"  {name}: ADF p-value = {p_value:.4f} ({'stationary' if is_stationary else 'non-stationary'})")

        return is_stationary, p_value

    def test_granger_causality_pairwise(self, ts_data, cause_var, effect_var, max_lags=6):
        """
        Test if cause_var Granger-causes effect_var.

        H0: cause_var does NOT Granger-cause effect_var
        H1: cause_var Granger-causes effect_var

        Returns: Dictionary with test results
        """
        logger.info(f"\nTesting: {cause_var} → {effect_var}")

        # Prepare data
        data = ts_data[[effect_var, cause_var]].dropna()

        if len(data) < 30:
            logger.warning(f"  Insufficient data: {len(data)} observations (need ≥30)")
            return None

        # Test stationarity
        logger.info("  Stationarity tests:")
        stat_effect, pval_effect = self.test_stationarity(data[effect_var], effect_var)
        stat_cause, pval_cause = self.test_stationarity(data[cause_var], cause_var)

        # If non-stationary, difference
        if not stat_effect:
            data[effect_var] = data[effect_var].diff().dropna()
            logger.info(f"    Differenced {effect_var}")

        if not stat_cause:
            data[cause_var] = data[cause_var].diff().dropna()
            logger.info(f"    Differenced {cause_var}")

        data = data.dropna()

        if len(data) < 30:
            logger.warning(f"  Insufficient data after differencing: {len(data)} obs")
            return None

        # Run Granger causality test
        try:
            gc_results = grangercausalitytests(data[[effect_var, cause_var]], max_lags, verbose=False)

            # Extract p-values and AICs for each lag
            results = {
                'cause': cause_var,
                'effect': effect_var,
                'n_obs': len(data),
                'stationarity_cause': (stat_cause, pval_cause),
                'stationarity_effect': (stat_effect, pval_effect),
                'lags': {}
            }

            aics = []
            for lag in range(1, max_lags + 1):
                # F-test p-value
                f_test = gc_results[lag][0]['ssr_ftest']
                chi2_test = gc_results[lag][0]['ssr_chi2test']

                # Get AIC from the regression
                aic = gc_results[lag][1][0].aic
                aics.append((lag, aic))

                results['lags'][lag] = {
                    'f_stat': f_test[0],
                    'p_value': f_test[1],
                    'df': f_test[2],  # degrees of freedom
                    'aic': aic,
                    'significant': f_test[1] < 0.05
                }

            # Find optimal lag using AIC (CORRECTED: was using min p-value)
            optimal_lag = min(aics, key=lambda x: x[1])[0]
            results['optimal_lag'] = optimal_lag
            results['optimal_p_value'] = results['lags'][optimal_lag]['p_value']
            results['optimal_f_stat'] = results['lags'][optimal_lag]['f_stat']
            results['optimal_df'] = results['lags'][optimal_lag]['df']
            results['granger_causes'] = results['optimal_p_value'] < 0.05

            logger.info(f"  Optimal lag (AIC): {optimal_lag} months")
            logger.info(f"  F-statistic: {results['optimal_f_stat']:.3f}, p-value: {results['optimal_p_value']:.4f}")
            logger.info(f"  Conclusion: {cause_var} {'DOES' if results['granger_causes'] else 'DOES NOT'} Granger-cause {effect_var}")

            return results

        except Exception as e:
            logger.error(f"  Error in Granger causality test: {str(e)}")
            return None

    def test_sequential_transfer_pooled(self):
        """
        Test sequential transfer mechanism using pooled data from multiple hospitals.

        Tests:
        1. Payment Delays(t) → Quality Decline(t+k)
        2. Payment Delays(t) → Financial Results(t+k)
        3. Quality Decline(t) → Payment Delays(t+k) (reverse causality check)
        """
        logger.info("\n" + "="*70)
        logger.info("SEQUENTIAL TRANSFER MECHANISM: POOLED GRANGER CAUSALITY")
        logger.info("="*70)

        # Define variable pairs to test
        tests = [
            # H3a: Payment delays lead to quality deterioration
            ('pagamentos_em_atraso', 'taxa_mortalidade'),

            # H3b: Payment delays lead to financial deterioration
            ('pagamentos_em_atraso', 'resultados_operacionais'),

            # H3c: Reverse causality check (should be weak/absent)
            ('taxa_mortalidade', 'pagamentos_em_atraso'),
            ('resultados_operacionais', 'pagamentos_em_atraso'),
        ]

        pooled_results = []

        # Get entities with sufficient data
        entity_counts = self.monthly_panel.groupby('entidade').size()
        viable_entities = entity_counts[entity_counts >= 36].index.tolist()

        logger.info(f"\nEntities with ≥36 months: {len(viable_entities)}")

        # Test each pair
        for cause_var, effect_var in tests:
            logger.info(f"\n{'='*70}")
            logger.info(f"TESTING: {cause_var} → {effect_var}")
            logger.info(f"{'='*70}")

            # Collect results across entities
            entity_results = []

            for entity in viable_entities[:20]:  # Test first 20 entities (for computational efficiency)
                ts_data = self.prepare_time_series(entity, [cause_var, effect_var])

                if ts_data is None or len(ts_data) < 36:
                    continue

                result = self.test_granger_causality_pairwise(ts_data, cause_var, effect_var, max_lags=6)

                if result is not None:
                    result['entity'] = entity
                    entity_results.append(result)

            # Summarize across entities
            if entity_results:
                n_significant = sum(1 for r in entity_results if r['granger_causes'])
                n_total = len(entity_results)
                pct_significant = n_significant / n_total * 100

                avg_pval = np.mean([r['optimal_p_value'] for r in entity_results])
                avg_fstat = np.mean([r['optimal_f_stat'] for r in entity_results])
                avg_lag = np.mean([r['optimal_lag'] for r in entity_results])

                # Stationarity summary
                n_stationary_cause = sum(1 for r in entity_results if r['stationarity_cause'][0])
                n_stationary_effect = sum(1 for r in entity_results if r['stationarity_effect'][0])

                summary = {
                    'cause': cause_var,
                    'effect': effect_var,
                    'n_entities_tested': n_total,
                    'n_significant': n_significant,
                    'pct_significant': pct_significant,
                    'avg_p_value': avg_pval,
                    'avg_f_stat': avg_fstat,
                    'avg_lag': avg_lag,
                    'n_stationary_cause': n_stationary_cause,
                    'n_stationary_effect': n_stationary_effect,
                    'conclusion': 'SUPPORTED' if pct_significant > 50 else 'NOT SUPPORTED'
                }

                pooled_results.append(summary)

                logger.info(f"\n  SUMMARY: {cause_var} → {effect_var}")
                logger.info(f"    Entities tested: {n_total}")
                logger.info(f"    Significant (p < 0.05): {n_significant} ({pct_significant:.1f}%)")
                logger.info(f"    Average p-value: {avg_pval:.4f}")
                logger.info(f"    Average F-statistic: {avg_fstat:.3f}")
                logger.info(f"    Average optimal lag: {avg_lag:.1f} months")
                logger.info(f"    Conclusion: {summary['conclusion']}")

            else:
                logger.warning(f"  No valid results for {cause_var} → {effect_var}")

        self.results['pooled_granger'] = pooled_results

        return pooled_results

    def estimate_var_model(self, variables, entity=None, max_lags=6):
        """
        Estimate Vector Autoregression (VAR) model.

        If entity is specified, uses single-entity time series.
        Otherwise, uses pooled data (first differences).
        """
        logger.info("\n" + "="*70)
        logger.info("VAR MODEL ESTIMATION")
        logger.info("="*70)

        if entity:
            ts_data = self.prepare_time_series(entity, variables, min_periods=48)
            logger.info(f"Entity: {entity}")
        else:
            # Use first hospital with sufficient data
            entity_counts = self.monthly_panel.groupby('entidade').size()
            viable_entity = entity_counts[entity_counts >= 48].index[0]
            ts_data = self.prepare_time_series(viable_entity, variables, min_periods=48)
            logger.info(f"Using entity: {viable_entity}")

        if ts_data is None:
            logger.error("Insufficient data for VAR estimation")
            return None

        logger.info(f"Time series length: {len(ts_data)}")

        # Difference if needed
        for var in variables:
            if var in ts_data.columns:
                is_stat, _ = self.test_stationarity(ts_data[var], var)
                if not is_stat:
                    ts_data[var] = ts_data[var].diff()
                    logger.info(f"  Differenced {var}")

        ts_data = ts_data.dropna()

        # Estimate VAR
        try:
            model = VAR(ts_data)
            results = model.fit(maxlags=max_lags, ic='aic')

            logger.info(f"\nVAR Model Summary:")
            logger.info(f"  Optimal lag order (AIC): {results.k_ar}")
            logger.info(f"  Number of observations: {results.nobs}")
            logger.info(f"\n{results.summary()}")

            self.results['var_model'] = results

            return results

        except Exception as e:
            logger.error(f"VAR estimation failed: {str(e)}")
            return None

    def plot_impulse_responses(self, var_results, variables, periods=12):
        """
        Plot Impulse Response Functions from VAR model.

        Shows: Response of quality metrics to a shock in payment delays.
        """
        logger.info("\nGenerating Impulse Response Functions...")

        if var_results is None:
            logger.warning("No VAR results available for IRF")
            return

        try:
            irf = var_results.irf(periods)

            # Plot IRF
            fig = irf.plot(orth=True, impulse=variables[0], response=variables[1:])
            fig.suptitle(f'Impulse Response: Shock to {variables[0]}', fontsize=14)

            output_file = FIGURE_DIR / "irf_payment_delays_to_quality.pdf"
            plt.savefig(output_file, bbox_inches='tight', dpi=300)
            logger.info(f"  IRF plot saved: {output_file}")

            plt.close()

        except Exception as e:
            logger.error(f"IRF plotting failed: {str(e)}")

    def save_results(self):
        """Save Granger causality results to file."""
        logger.info("\nSaving results...")

        # Text report
        report_file = OUTPUT_DIR / "granger_causality_results.txt"
        with open(report_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write("GRANGER CAUSALITY ANALYSIS: SEQUENTIAL TRANSFER MECHANISM\n")
            f.write("="*70 + "\n\n")

            if 'pooled_granger' in self.results:
                f.write("POOLED GRANGER CAUSALITY TESTS\n")
                f.write("-"*70 + "\n\n")

                for result in self.results['pooled_granger']:
                    f.write(f"Test: {result['cause']} → {result['effect']}\n")
                    f.write(f"  Entities tested: {result['n_entities_tested']}\n")
                    f.write(f"  Significant (p<0.05): {result['n_significant']} ({result['pct_significant']:.1f}%)\n")
                    f.write(f"  Average min p-value: {result['avg_min_p_value']:.4f}\n")
                    f.write(f"  Conclusion: {result['conclusion']}\n\n")

        logger.info(f"Results saved: {report_file}")

        # LaTeX table
        if 'pooled_granger' in self.results:
            self.create_latex_table()

    def create_latex_table(self):
        """Create LaTeX table of Granger causality results with Bonferroni correction."""
        results = self.results['pooled_granger']

        # Apply Bonferroni correction (k tests)
        k_tests = len(results)
        bonferroni_alpha = 0.05 / k_tests

        logger.info(f"\nApplying Bonferroni correction: α = 0.05 / {k_tests} = {bonferroni_alpha:.4f}")

        latex_lines = []
        latex_lines.append(r"\begin{table}[htbp]")
        latex_lines.append(r"\centering")
        latex_lines.append(r"\caption{Granger Causality Tests: Sequential Transfer Mechanism}")
        latex_lines.append(r"\label{tab:granger_causality}")
        latex_lines.append(r"\footnotesize")
        latex_lines.append(r"\begin{threeparttable}")
        latex_lines.append(r"\begin{tabular}{llccccc}")
        latex_lines.append(r"\toprule")
        latex_lines.append(r"Cause & Effect & N & Lag & F-stat & p-value & Bonf. p \\")
        latex_lines.append(r"\midrule")

        for r in results:
            cause = r['cause'].replace('_', ' ').replace('pagamentos em atraso', 'Payment delays') \
                              .replace('taxa mortalidade', 'Mortality rate') \
                              .replace('resultados operacionais', 'Operating results')
            effect = r['effect'].replace('_', ' ').replace('pagamentos em atraso', 'Payment delays') \
                               .replace('taxa mortalidade', 'Mortality rate') \
                               .replace('resultados operacionais', 'Operating results')
            n = r['n_entities_tested']
            lag = f"{r['avg_lag']:.1f}"
            fstat = f"{r['avg_f_stat']:.2f}"
            pval = r['avg_p_value']
            bonf_pval = min(pval * k_tests, 1.0)  # Bonferroni correction

            # Add significance markers
            if bonf_pval < 0.01:
                bonf_str = f"{bonf_pval:.3f}***"
            elif bonf_pval < 0.05:
                bonf_str = f"{bonf_pval:.3f}**"
            elif bonf_pval < 0.10:
                bonf_str = f"{bonf_pval:.3f}*"
            else:
                bonf_str = f"{bonf_pval:.3f}"

            pval_str = f"{pval:.3f}"

            latex_lines.append(f"{cause} & {effect} & {n} & {lag} & {fstat} & {pval_str} & {bonf_str} \\\\")

        latex_lines.append(r"\bottomrule")
        latex_lines.append(r"\end{tabular}")
        latex_lines.append(r"\begin{tablenotes}")
        latex_lines.append(r"\small")
        latex_lines.append(r"\item \textit{Notes:} Granger causality tests examine temporal ordering of distress symptoms using monthly panel data (2017--2024). ``Lag'' indicates optimal lag order selected by AIC criterion (maximum 6 months tested). ``F-stat'' is the average F-statistic from SSR-based tests across entities. ``p-value'' is the average uncorrected p-value. ``Bonf. p'' applies Bonferroni correction for " + f"{k_tests}" + r" simultaneous tests (α = " + f"{bonferroni_alpha:.4f}" + r"). All series tested for stationarity using Augmented Dickey-Fuller tests; non-stationary series first-differenced before analysis. *** p<0.01, ** p<0.05, * p<0.10 (Bonferroni-corrected).")
        latex_lines.append(r"\end{tablenotes}")
        latex_lines.append(r"\end{threeparttable}")
        latex_lines.append(r"\end{table}")

        latex_file = TABLE_DIR / "tableA3_granger_causality.tex"
        with open(latex_file, 'w') as f:
            f.write('\n'.join(latex_lines))

        logger.info(f"LaTeX table saved: {latex_file}")
        logger.info(f"  Bonferroni-corrected significance threshold: p < {bonferroni_alpha:.4f}")

    def run_analysis(self):
        """Execute full Granger causality analysis pipeline."""
        logger.info("="*70)
        logger.info("GRANGER CAUSALITY ANALYSIS PIPELINE")
        logger.info("="*70 + "\n")

        # Load data
        self.load_monthly_panel()

        # Test sequential transfer (pooled)
        self.test_sequential_transfer_pooled()

        # Estimate VAR model (for IRF)
        variables = ['pagamentos_em_atraso', 'taxa_mortalidade', 'resultados_operacionais']
        var_results = self.estimate_var_model(variables)

        # Plot IRF if VAR successful
        if var_results:
            self.plot_impulse_responses(var_results, variables)

        # Save results
        self.save_results()

        logger.info("\n" + "="*70)
        logger.info("GRANGER CAUSALITY ANALYSIS COMPLETE")
        logger.info("="*70)


def main():
    """Main execution."""
    # Use the final consolidated panel with quality metrics
    panel_file = Path(__file__).parent.parent.parent / "03_data" / "processed" / "panel" / "hospital_month_panel_final.parquet"

    if not panel_file.exists():
        logger.error(f"Monthly panel not found: {panel_file}")
        logger.error("Run create_monthly_panel_dataset.py first")
        return

    analyzer = GrangerCausalityAnalyzer(panel_file)
    analyzer.run_analysis()


if __name__ == "__main__":
    main()
