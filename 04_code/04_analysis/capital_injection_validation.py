"""
October 2025 Capital Injection Validation Analysis

Validates PHFSI predictive power using actual capital allocation data
from Despacho 12497/2025 (October 24, 2025).

Data: 42 hospital entities (39 ULS + 3 IPO) receiving €500M total
to liquidate overdue supplier payments >90 days.

Analysis:
1. Correlation: PHFSI vs allocation magnitude
2. Comparison with top 10 recipients
3. Validation that higher distress → larger allocations

Author: Research Team
Date: 2026-01-01
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import spearmanr, pearsonr

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
sns.set_palette("husl")

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_EXTERNAL = PROJECT_ROOT / "03_data" / "external" / "interventions"
DATA_PROCESSED = PROJECT_ROOT / "03_data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "06_output" / "tables" / "main"
FIGURES_DIR = PROJECT_ROOT / "06_output" / "figures" / "main"
RESULTS_DIR = PROJECT_ROOT / "06_output" / "results" / "validation"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class CapitalInjectionValidator:
    """
    Validates PHFSI against actual October 2025 capital injections.
    """

    def __init__(self):
        self.allocations = None
        self.phfsi_data = None
        self.validation_data = None

    def load_data(self):
        """Load capital allocation and PHFSI data."""
        logger.info("Loading October 2025 capital allocation data...")

        # Load allocation data
        alloc_path = DATA_EXTERNAL / "capital_injections_hospital_level.csv"
        if not alloc_path.exists():
            alloc_path = DATA_EXTERNAL / "dr_allocations_found.csv"

        self.allocations = pd.read_csv(alloc_path)

        # Filter to October 2025 capital injections (Despacho 12497/2025)
        # This excludes infrastructure projects (Portarias)
        self.allocations = self.allocations[
            self.allocations['dr_number'] == 'Despacho 12497/2025'
        ].copy()

        logger.info(f"Loaded {len(self.allocations)} allocation records from October 2025")

        # Load PHFSI data
        phfsi_path = DATA_PROCESSED / "variables" / "phfsi_scores.parquet"
        phfsi_df = pd.read_parquet(phfsi_path)

        # Get 2024 PHFSI scores (most recent before Oct 2025 allocation)
        self.phfsi_data = phfsi_df[phfsi_df['year'] == 2024].copy()

        logger.info(f"Loaded PHFSI data: {len(self.phfsi_data)} hospital-years")

    def prepare_validation_dataset(self):
        """Match allocations to PHFSI scores."""
        logger.info("Preparing validation dataset...")

        # Normalize entity names for matching
        self.allocations['entity_normalized'] = (
            self.allocations['entity']
            .str.upper()
            .str.replace('ULS', '')
            .str.replace('IPO', '')
            .str.strip()
        )

        self.phfsi_data['entity_normalized'] = (
            self.phfsi_data['entidade']
            .str.upper()
            .str.replace('UNIDADE LOCAL DE SAÚDE', '')
            .str.replace('ULS', '')
            .str.replace('IPO', '')
            .str.replace('INSTITUTO PORTUGUÊS DE ONCOLOGIA', '')
            .str.strip()
        )

        # Merge
        validation = self.allocations.merge(
            self.phfsi_data[['entity_normalized', 'phfsi']],
            on='entity_normalized',
            how='left'
        )

        # Convert amount to millions
        validation['allocation_millions'] = validation['amount_eur'] / 1_000_000

        # Flag matched vs unmatched
        validation['matched'] = ~validation['phfsi'].isna()

        self.validation_data = validation

        matched_count = validation['matched'].sum()
        total_allocation_matched = validation[validation['matched']]['allocation_millions'].sum()

        logger.info(f"Matched {matched_count} of {len(validation)} entities")
        logger.info(f"Matched allocation: €{total_allocation_matched:.1f}M")

        # Save for inspection
        validation[['entity', 'allocation_millions', 'phfsi', 'matched']].to_csv(
            RESULTS_DIR / "validation_matching.csv", index=False
        )

    def analyze_correlation(self):
        """Analyze correlation between PHFSI and allocation."""
        logger.info("Analyzing PHFSI-allocation correlation...")

        # Filter to matched entities
        data = self.validation_data[self.validation_data['matched']].copy()

        if len(data) < 5:
            logger.warning(f"Only {len(data)} matched entities. Analysis may be underpowered.")
            return None

        # Correlation
        pearson_r, pearson_p = pearsonr(data['phfsi'], data['allocation_millions'])
        spearman_r, spearman_p = spearmanr(data['phfsi'], data['allocation_millions'])

        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            data['phfsi'], data['allocation_millions']
        )

        results = {
            'n': len(data),
            'pearson_r': pearson_r,
            'pearson_p': pearson_p,
            'spearman_r': spearman_r,
            'spearman_p': spearman_p,
            'r_squared': r_value**2,
            'slope': slope,
            'intercept': intercept,
            'regression_p': p_value
        }

        logger.info(f"Pearson r: {pearson_r:.3f} (p={pearson_p:.4f})")
        logger.info(f"Spearman ρ: {spearman_r:.3f} (p={spearman_p:.4f})")
        logger.info(f"R²: {results['r_squared']:.3f}")

        # Save results
        with open(RESULTS_DIR / "correlation_results.txt", 'w') as f:
            f.write("OCTOBER 2025 CAPITAL INJECTION VALIDATION\n")
            f.write("="*60 + "\n\n")
            f.write(f"Sample size: {results['n']} matched entities\n")
            f.write(f"Pearson correlation: r = {pearson_r:.3f}, p = {pearson_p:.4f}\n")
            f.write(f"Spearman correlation: ρ = {spearman_r:.3f}, p = {spearman_p:.4f}\n")
            f.write(f"R-squared: {results['r_squared']:.3f}\n")
            f.write(f"Regression slope: {slope:.2f}M€ per PHFSI unit\n")
            f.write(f"Regression p-value: {p_value:.4f}\n\n")

            if pearson_r < 0:
                f.write("✓ VALIDATED: Lower PHFSI (higher distress) → Larger allocations\n")
            else:
                f.write("✗ UNEXPECTED: Higher PHFSI → Larger allocations\n")

        return results

    def create_validation_figure(self):
        """Create scatter plot of PHFSI vs allocation."""
        logger.info("Creating validation figure...")

        data = self.validation_data[self.validation_data['matched']].copy()

        if len(data) < 5:
            logger.warning("Insufficient data for visualization")
            return

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))

        # Scatter plot
        scatter = ax.scatter(
            data['phfsi'],
            data['allocation_millions'],
            s=100,
            alpha=0.6,
            c=data['phfsi'],
            cmap='RdYlGn',
            edgecolors='black',
            linewidth=0.5
        )

        # Add regression line
        z = np.polyfit(data['phfsi'], data['allocation_millions'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(data['phfsi'].min(), data['phfsi'].max(), 100)
        ax.plot(x_line, p(x_line), 'r--', alpha=0.8, linewidth=2, label='Linear fit')

        # Labels
        ax.set_xlabel('PHFSI (2024)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Capital Allocation (€ millions)', fontsize=12, fontweight='bold')
        ax.set_title(
            'October 2025 Capital Injection Validation\n'
            'PHFSI vs. Allocation Magnitude',
            fontsize=14, fontweight='bold'
        )

        # Add correlation info
        pearson_r, pearson_p = pearsonr(data['phfsi'], data['allocation_millions'])
        ax.text(
            0.05, 0.95,
            f'Pearson r = {pearson_r:.3f}\np = {pearson_p:.4f}\nn = {len(data)}',
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )

        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('PHFSI Score', fontsize=10)

        # Grid
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=10)

        plt.tight_layout()

        # Save
        output_path = FIGURES_DIR / "figure5_capital_injection_validation.pdf"
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Figure saved: {output_path}")

        plt.close()

    def create_summary_table(self):
        """Create summary table of top recipients."""
        logger.info("Creating summary table...")

        data = self.validation_data[self.validation_data['matched']].copy()

        # Sort by allocation amount
        top10 = data.nlargest(10, 'allocation_millions')[
            ['entity', 'allocation_millions', 'phfsi']
        ].copy()

        top10['rank'] = range(1, len(top10) + 1)
        top10 = top10[['rank', 'entity', 'allocation_millions', 'phfsi']]

        # Save CSV
        top10.to_csv(RESULTS_DIR / "top10_recipients.csv", index=False)

        # Create LaTeX table
        latex_lines = []
        latex_lines.append(r"\begin{tabular}{rlcc}")
        latex_lines.append(r"\toprule")
        latex_lines.append(r"Rank & Hospital/IPO & Allocation (€M) & PHFSI (2024) \\")
        latex_lines.append(r"\midrule")

        for _, row in top10.iterrows():
            entity_short = row['entity'].replace('ULS ', '').replace('IPO ', '')[:30]
            latex_lines.append(
                f"{int(row['rank'])} & {entity_short} & "
                f"{row['allocation_millions']:.1f} & {row['phfsi']:.3f} \\\\"
            )

        latex_lines.append(r"\bottomrule")
        latex_lines.append(r"\end{tabular}")

        latex_table = "\n".join(latex_lines)

        # Save
        output_path = OUTPUT_DIR / "table6_capital_injection_top10.tex"
        with open(output_path, 'w') as f:
            f.write(latex_table)

        logger.info(f"LaTeX table saved: {output_path}")

    def run_all(self):
        """Run complete validation analysis."""
        logger.info("Starting Capital Injection Validation Analysis...")

        self.load_data()
        self.prepare_validation_dataset()
        results = self.analyze_correlation()

        if results is not None:
            self.create_validation_figure()
            self.create_summary_table()

        logger.info("Capital Injection Validation Complete!")


if __name__ == "__main__":
    validator = CapitalInjectionValidator()
    validator.run_all()
