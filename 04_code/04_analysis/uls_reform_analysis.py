"""
ULS Reform Analysis (Month 4)

Given data constraints (no good control group for traditional DiD), this script performs:
1. Event study / before-after analysis of 2024 ULS integration
2. Mechanism tests: Which PHFSI components improved?
3. Heterogeneous effects: Did reform affect all hospitals equally?

Data limitation: Almost all hospitals converted to ULS in 2024 simultaneously,
leaving no "never-treated" control group. Full DiD would require 2025+ data
to identify late adopters as controls.

Pragmatic approach: Compare pre-reform (2017-2023) vs post-reform (2024) trends
for hospitals that integrated in 2024.

Author: Research Team
Date: 2025-12-31
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from linearmodels.panel import PanelOLS
from scipy import stats

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set plot style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PROCESSED = PROJECT_ROOT / "03_data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "06_output" / "tables" / "main"
FIGURES_DIR = PROJECT_ROOT / "06_output" / "figures" / "main"
RESULTS_DIR = PROJECT_ROOT / "06_output" / "results" / "uls_reform"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class ULSReformAnalyzer:
    """
    Analyzes the impact of 2024 ULS reform on hospital financial sustainability.
    """

    def __init__(self):
        self.panel = None
        self.components = None
        self.reform_hospitals = []

    def load_data(self):
        """Load panel data and identify reform hospitals."""
        logger.info("Loading data and identifying ULS reform hospitals...")

        # Load panel
        panel_path = DATA_PROCESSED / "panel" / "hospital_year_panel.parquet"
        self.panel = pd.read_parquet(panel_path)

        # Load PHFSI
        phfsi_path = DATA_PROCESSED / "variables" / "phfsi_scores.parquet"
        phfsi = pd.read_parquet(phfsi_path)

        # Load components
        comp_path = DATA_PROCESSED / "variables" / "phfsi_components.parquet"
        self.components = pd.read_parquet(comp_path)

        # Merge PHFSI and components
        self.panel = self.panel.merge(
            phfsi[['entidade', 'year', 'phfsi']],
            on=['entidade', 'year'],
            how='left'
        )

        # Merge components
        self.panel = self.panel.merge(
            self.components[['entidade', 'year', 'ossr', 'spi', 'lrr', 'tlr']],
            on=['entidade', 'year'],
            how='left'
        )

        # Identify Centro Hospitalar entities (pre-2024)
        ch_pre2024 = self.panel[
            (self.panel['year'] < 2024) &
            (self.panel['entidade'].str.contains('Centro Hospitalar', case=False, na=False))
        ]
        self.reform_hospitals = ch_pre2024['entidade'].unique().tolist()

        logger.info(f"Identified {len(self.reform_hospitals)} hospitals that underwent ULS reform in 2024")
        logger.info(f"Panel: {len(self.panel)} observations")

    def create_reform_indicator(self):
        """Create post-reform indicator."""
        # Post-reform period
        self.panel['post_reform'] = (self.panel['year'] >= 2024).astype(int)

        # Reform hospital indicator
        self.panel['reform_hospital'] = self.panel['entidade'].isin(self.reform_hospitals).astype(int)

        logger.info(f"Reform hospitals: {self.panel['reform_hospital'].sum()} observations")
        logger.info(f"Post-reform period: {self.panel['post_reform'].sum()} observations")

    def event_study_analysis(self):
        """
        Event study: PHFSI trends before and after 2024 reform.

        Compare 2017-2023 trend vs 2024 for reform hospitals.
        """
        logger.info("Running event study analysis...")

        # Filter to reform hospitals with PHFSI
        df = self.panel[
            (self.panel['reform_hospital'] == 1) &
            (self.panel['phfsi'].notna())
        ].copy()

        if len(df) == 0:
            logger.warning("No data for event study")
            return None

        # Calculate annual averages
        annual_phfsi = df.groupby('year').agg({
            'phfsi': ['mean', 'std', 'count'],
            'ossr': 'mean',
            'spi': 'mean',
            'lrr': 'mean',
            'tlr': 'mean'
        }).reset_index()

        annual_phfsi.columns = ['year', 'phfsi_mean', 'phfsi_std', 'phfsi_count',
                                'ossr_mean', 'spi_mean', 'lrr_mean', 'tlr_mean']

        # Calculate standard error
        annual_phfsi['phfsi_se'] = annual_phfsi['phfsi_std'] / np.sqrt(annual_phfsi['phfsi_count'])

        # Save
        csv_path = RESULTS_DIR / "event_study_annual_means.csv"
        annual_phfsi.to_csv(csv_path, index=False)
        logger.info(f"Event study results saved to: {csv_path}")

        # Test for break in 2024
        pre_2024 = annual_phfsi[annual_phfsi['year'] < 2024]
        post_2024 = annual_phfsi[annual_phfsi['year'] >= 2024]

        if len(pre_2024) > 0 and len(post_2024) > 0:
            pre_mean = pre_2024['phfsi_mean'].mean()
            post_mean = post_2024['phfsi_mean'].mean()
            change = post_mean - pre_mean

            logger.info(f"\nEvent Study Results:")
            logger.info(f"  Pre-2024 PHFSI:  {pre_mean:.3f}")
            logger.info(f"  Post-2024 PHFSI: {post_mean:.3f}")
            logger.info(f"  Change:          {change:.3f} ({change/pre_mean*100:.1f}%)")

        return annual_phfsi

    def before_after_ttest(self):
        """
        Simple t-test comparing pre-reform vs post-reform PHFSI.

        Note: This is descriptive only, not causal, due to lack of control group.
        """
        logger.info("Running before-after comparison (t-test)...")

        # Filter to reform hospitals
        df = self.panel[
            (self.panel['reform_hospital'] == 1) &
            (self.panel['phfsi'].notna())
        ].copy()

        if len(df) < 20:
            logger.warning("Insufficient data for before-after test")
            return None

        # Split pre/post
        pre_reform = df[df['post_reform'] == 0]['phfsi']
        post_reform = df[df['post_reform'] == 1]['phfsi']

        if len(pre_reform) == 0 or len(post_reform) == 0:
            logger.warning("No variation in pre/post periods")
            return None

        # T-test
        t_stat, p_value = stats.ttest_ind(post_reform, pre_reform)

        # Summary statistics
        pre_mean = pre_reform.mean()
        post_mean = post_reform.mean()
        change = post_mean - pre_mean
        pct_change = (change / pre_mean) * 100

        logger.info("\nBefore-After Comparison Results:")
        logger.info(f"  Pre-reform PHFSI:  {pre_mean:.4f} (N={len(pre_reform)})")
        logger.info(f"  Post-reform PHFSI: {post_mean:.4f} (N={len(post_reform)})")
        logger.info(f"  Change:            {change:.4f} ({pct_change:+.1f}%)")
        logger.info(f"  T-statistic:       {t_stat:.4f}")
        logger.info(f"  P-value:           {p_value:.4f}")

        # Save
        results_df = pd.DataFrame({
            'Metric': ['Pre-Reform Mean', 'Post-Reform Mean', 'Change', 'Pct Change (%)',
                      'T-Statistic', 'P-Value', 'N Pre', 'N Post'],
            'Value': [pre_mean, post_mean, change, pct_change,
                     t_stat, p_value, len(pre_reform), len(post_reform)]
        })
        csv_path = RESULTS_DIR / "before_after_comparison.csv"
        results_df.to_csv(csv_path, index=False)

        return results_df

    def mechanism_analysis(self):
        """
        Mechanism test: Which PHFSI components changed after reform?

        Run t-tests on each component separately to see which ones improved.

        Note: Descriptive only due to simultaneous treatment in 2024.
        """
        logger.info("Running mechanism analysis (component-level effects)...")

        # Filter to reform hospitals (components already merged in load_data)
        df = self.panel[
            (self.panel['reform_hospital'] == 1)
        ].copy()

        # Test each component
        components = ['ossr', 'spi', 'lrr', 'tlr', 'phfsi']
        results_list = []

        for comp in components:
            # Filter to non-missing data
            comp_df = df[[comp, 'post_reform']].dropna()

            if len(comp_df) < 20:
                logger.warning(f"Insufficient data for {comp}")
                continue

            # Split pre/post
            pre_reform = comp_df[comp_df['post_reform'] == 0][comp]
            post_reform = comp_df[comp_df['post_reform'] == 1][comp]

            if len(pre_reform) == 0 or len(post_reform) == 0:
                logger.warning(f"No variation in pre/post periods for {comp}")
                continue

            # Calculate change
            pre_mean = pre_reform.mean()
            post_mean = post_reform.mean()
            change = post_mean - pre_mean
            pct_change = (change / pre_mean) * 100 if pre_mean != 0 else 0

            # T-test
            t_stat, p_value = stats.ttest_ind(post_reform, pre_reform)

            results_list.append({
                'Component': comp.upper(),
                'Pre_Reform_Mean': pre_mean,
                'Post_Reform_Mean': post_mean,
                'Change': change,
                'Pct_Change': pct_change,
                'T_Statistic': t_stat,
                'P_Value': p_value,
                'N_Pre': len(pre_reform),
                'N_Post': len(post_reform)
            })

            logger.info(f"  {comp.upper()}: Δ = {change:.4f} ({pct_change:+.1f}%), p = {p_value:.4f}")

        # Save
        if len(results_list) > 0:
            results_df = pd.DataFrame(results_list)
            csv_path = RESULTS_DIR / "mechanism_component_effects.csv"
            results_df.to_csv(csv_path, index=False)
            logger.info(f"\nMechanism results saved to: {csv_path}")
            return results_df
        else:
            logger.warning("No mechanism results to save")
            return None

    def generate_event_study_figure(self, annual_data):
        """Generate event study figure (Figure 4 for paper)."""
        if annual_data is None or len(annual_data) == 0:
            logger.warning("No data for event study figure")
            return

        logger.info("Generating event study figure...")

        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot PHFSI trend
        ax.plot(annual_data['year'], annual_data['phfsi_mean'],
                color='#2E86AB', linewidth=2, marker='o', markersize=8,
                label='Mean PHFSI')

        # Add 95% CI
        if 'phfsi_se' in annual_data.columns:
            ci_lower = annual_data['phfsi_mean'] - 1.96 * annual_data['phfsi_se']
            ci_upper = annual_data['phfsi_mean'] + 1.96 * annual_data['phfsi_se']
            ax.fill_between(annual_data['year'], ci_lower, ci_upper,
                           alpha=0.2, color='#2E86AB')

        # Add vertical line at 2024 (reform)
        ax.axvline(2023.5, linestyle='--', color='red', linewidth=2, alpha=0.7,
                  label='ULS Reform (2024)')

        # Labels and formatting
        ax.set_xlabel('Year', fontweight='bold')
        ax.set_ylabel('PHFSI Score', fontweight='bold')
        ax.set_title('Event Study: PHFSI Before and After ULS Integration Reform',
                    fontweight='bold', pad=15)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(loc='best', framealpha=0.9)

        # Save
        plt.tight_layout()
        pdf_path = FIGURES_DIR / "figure4_uls_event_study.pdf"
        png_path = FIGURES_DIR / "figure4_uls_event_study.png"
        plt.savefig(pdf_path, bbox_inches='tight', dpi=300)
        plt.savefig(png_path, bbox_inches='tight', dpi=300)
        plt.close()

        logger.info(f"Event study figure saved to: {pdf_path}")

    def generate_summary_table(self):
        """Generate summary table for paper."""
        logger.info("Generating ULS reform summary table...")

        # This would be Table 4 or Appendix table
        # For now, create a placeholder noting data limitations

        summary = {
            'Analysis': [
                'Event Study (2017-2024)',
                'Before-After Regression',
                'Component Mechanisms',
            ],
            'Method': [
                'Annual means comparison',
                'FE regression with post-2024 dummy',
                'Component-level FE regressions',
            ],
            'Finding': [
                'Trend analysis pre/post reform',
                'Average reform effect',
                'Which components improved?',
            ],
            'Limitation': [
                'No control group (all hospitals treated 2024)',
                'Single post-period observation',
                'Cannot establish causality',
            ],
        }

        summary_df = pd.DataFrame(summary)
        csv_path = RESULTS_DIR / "uls_reform_summary.csv"
        summary_df.to_csv(csv_path, index=False)
        logger.info(f"Summary table saved to: {csv_path}")

        return summary_df

    def run_pipeline(self):
        """Execute ULS reform analysis pipeline."""
        logger.info("Starting ULS reform analysis...")
        logger.info("="*60 + "\n")

        # Load and prepare data
        self.load_data()
        self.create_reform_indicator()

        # Run analyses
        annual_data = self.event_study_analysis()
        before_after_result = self.before_after_ttest()
        mechanism_results = self.mechanism_analysis()

        # Generate outputs
        if annual_data is not None:
            self.generate_event_study_figure(annual_data)
        self.generate_summary_table()

        logger.info("\n" + "="*60)
        logger.info("ULS REFORM ANALYSIS COMPLETE")
        logger.info("="*60)
        logger.info("\nData Limitation Note:")
        logger.info("Traditional DiD not feasible: Almost all hospitals converted")
        logger.info("to ULS simultaneously in 2024, leaving no control group.")
        logger.info("Analysis provides descriptive evidence of reform timing,")
        logger.info("but cannot establish causal effects without controls.")
        logger.info("\nFor publication: Present as exploratory/descriptive analysis")
        logger.info("or note limitation and defer full DiD to future work.")

        return {
            'annual_data': annual_data,
            'before_after': before_after_result,
            'mechanisms': mechanism_results,
        }


def main():
    """Main execution function."""
    analyzer = ULSReformAnalyzer()
    results = analyzer.run_pipeline()

    print("\n" + "="*60)
    print("ULS REFORM ANALYSIS SUMMARY")
    print("="*60)

    if results['annual_data'] is not None:
        print("\nAnnual PHFSI Trends (Reform Hospitals):")
        print(results['annual_data'][['year', 'phfsi_mean', 'phfsi_count']].to_string(index=False))

    if results['mechanisms'] is not None:
        print("\nMechanism Analysis (Component Effects):")
        print(results['mechanisms'].to_string(index=False))


if __name__ == "__main__":
    main()
