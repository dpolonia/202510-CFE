"""
Descriptive Visualizations for PHFSI Analysis

Generates publication-quality figures for the paper:
- Figure 1: PHFSI Trends Over Time
- Figure 2: PHFSI Component Correlation Matrix
- Figure 3: Subsidy Dependence vs Payment Delays

Author: Research Team
Date: 2025-12-31
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for WSL
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set publication-quality plot settings
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PROCESSED = PROJECT_ROOT / "03_data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "06_output" / "figures" / "main"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class DescriptivePlotsGenerator:
    """
    Generates descriptive visualization plots for PHFSI analysis.
    """

    def __init__(self):
        self.panel = None
        self.phfsi_scores = None
        self.components = None

    def load_data(self):
        """Load panel dataset and PHFSI scores."""
        logger.info("Loading data...")

        # Load panel
        panel_path = DATA_PROCESSED / "panel" / "hospital_year_panel.parquet"
        if panel_path.exists():
            self.panel = pd.read_parquet(panel_path)
            logger.info(f"Loaded panel: {len(self.panel)} rows")
        else:
            raise FileNotFoundError(f"Panel not found at {panel_path}")

        # Load PHFSI scores
        phfsi_path = DATA_PROCESSED / "variables" / "phfsi_scores.parquet"
        if phfsi_path.exists():
            self.phfsi_scores = pd.read_parquet(phfsi_path)
            logger.info(f"Loaded PHFSI scores: {len(self.phfsi_scores)} rows")
        else:
            raise FileNotFoundError(f"PHFSI scores not found at {phfsi_path}")

        # Load components
        components_path = DATA_PROCESSED / "variables" / "phfsi_components.parquet"
        if components_path.exists():
            self.components = pd.read_parquet(components_path)
            logger.info(f"Loaded components: {len(self.components)} rows")
        else:
            raise FileNotFoundError(f"Components not found at {components_path}")

        # Merge PHFSI scores with panel
        merge_cols = ['entidade', 'year', 'phfsi', 'phfsi_cluster']
        for col in ['ossr', 'spi', 'lrr', 'tlr', 'cqmi']:
            if col in self.phfsi_scores.columns:
                merge_cols.append(col)

        self.panel = self.panel.merge(
            self.phfsi_scores[merge_cols],
            on=['entidade', 'year'],
            how='left'
        )

        # Filter to hospitals only
        hospital_keywords = [
            'Hospital', 'Hospitalar', 'Unidade Local de Saúde',
            'ULS', 'IPO', 'Instituto Português'
        ]
        hospital_mask = self.panel['entidade'].str.contains(
            '|'.join(hospital_keywords),
            case=False,
            na=False
        )
        self.panel['is_hospital'] = hospital_mask

    def generate_figure1_phfsi_trends(self):
        """
        Figure 1: PHFSI Trends Over Time

        Line plot showing:
        - Average PHFSI by year (with 95% CI)
        - Annotations for COVID period and ULS reform
        """
        logger.info("Generating Figure 1: PHFSI Trends Over Time...")

        # Filter to hospitals with PHFSI
        df = self.panel[
            (self.panel['is_hospital'] == True) &
            (self.panel['phfsi'].notna())
        ].copy()

        # Calculate annual statistics
        annual_stats = df.groupby('year')['phfsi'].agg([
            'mean',
            'std',
            'count',
            ('sem', lambda x: x.std() / np.sqrt(len(x)))
        ]).reset_index()

        # Calculate 95% CI
        annual_stats['ci_lower'] = annual_stats['mean'] - 1.96 * annual_stats['sem']
        annual_stats['ci_upper'] = annual_stats['mean'] + 1.96 * annual_stats['sem']

        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))

        # Main line plot
        ax.plot(annual_stats['year'], annual_stats['mean'],
                color='#2E86AB', linewidth=2, marker='o', markersize=6,
                label='Mean PHFSI')

        # 95% CI shaded area
        ax.fill_between(annual_stats['year'],
                        annual_stats['ci_lower'],
                        annual_stats['ci_upper'],
                        alpha=0.2, color='#2E86AB')

        # Add COVID period shading
        ax.axvspan(2020, 2021, alpha=0.1, color='red', label='COVID Period')

        # Add annotations
        ax.axvline(2024, linestyle='--', color='green', alpha=0.5, linewidth=1)
        ax.text(2024, ax.get_ylim()[1] * 0.95, 'ULS Reform',
                rotation=90, verticalalignment='top',
                fontsize=9, color='green')

        # Labels and title
        ax.set_xlabel('Year', fontweight='bold')
        ax.set_ylabel('PHFSI Score', fontweight='bold')
        ax.set_title('Public Hospital Financial Sustainability Index (PHFSI)\nTrends Over Time (2017-2024)',
                     fontweight='bold', pad=15)

        # Grid and legend
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(loc='best', framealpha=0.9)

        # Y-axis range
        ax.set_ylim(0, 0.8)

        # Add sample size note
        note_text = f"Note: Sample includes {annual_stats['count'].min():.0f}-{annual_stats['count'].max():.0f} hospitals per year with available PHFSI scores. "
        note_text += "Shaded area represents 95% confidence interval."
        fig.text(0.1, 0.02, note_text, fontsize=8, style='italic', wrap=True)

        # Save
        plt.tight_layout()
        output_path = OUTPUT_DIR / "figure1_phfsi_trends.pdf"
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.savefig(OUTPUT_DIR / "figure1_phfsi_trends.png", bbox_inches='tight', dpi=300)
        plt.close()

        logger.info(f"Figure 1 saved to: {output_path}")

    def generate_figure2_component_correlation(self):
        """
        Figure 2: PHFSI Component Correlation Matrix

        Heatmap showing correlations between 5 components.
        """
        logger.info("Generating Figure 2: Component Correlation Matrix...")

        # Filter to hospitals with data
        df = self.panel[
            (self.panel['is_hospital'] == True) &
            (self.panel['phfsi'].notna())
        ].copy()

        # Select components
        component_cols = ['ossr', 'spi', 'lrr', 'tlr']  # Exclude cqmi (all NaN)
        component_names = {
            'ossr': 'OSSR\n(Self-Sufficiency)',
            'spi': 'SPI\n(Pressure)',
            'lrr': 'LRR\n(Liquidity)',
            'tlr': 'TLR\n(Leverage)',
        }

        # Calculate correlation matrix
        corr_matrix = df[component_cols].corr()

        # Rename for plot
        corr_matrix = corr_matrix.rename(index=component_names, columns=component_names)

        # Create heatmap
        fig, ax = plt.subplots(figsize=(8, 6))

        sns.heatmap(corr_matrix,
                   annot=True,
                   fmt='.3f',
                   cmap='RdBu_r',
                   center=0,
                   vmin=-1,
                   vmax=1,
                   square=True,
                   linewidths=0.5,
                   cbar_kws={'label': 'Correlation Coefficient'},
                   ax=ax)

        ax.set_title('PHFSI Component Correlation Matrix',
                    fontweight='bold', pad=15)

        # Add note
        note_text = "Note: Correlations calculated from hospital-year observations with available component data. "
        note_text += "Low correlations indicate components measure distinct aspects of financial sustainability."
        fig.text(0.1, 0.02, note_text, fontsize=8, style='italic', wrap=True)

        # Save
        plt.tight_layout()
        output_path = OUTPUT_DIR / "figure2_component_correlation.pdf"
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.savefig(OUTPUT_DIR / "figure2_component_correlation.png", bbox_inches='tight', dpi=300)
        plt.close()

        logger.info(f"Figure 2 saved to: {output_path}")

    def generate_figure3_subsidy_delays(self):
        """
        Figure 3: Subsidy Dependence vs Payment Delays

        Scatter plot showing relationship between operating subsidies
        and payment delays, colored by PHFSI score.

        Note: This is a proxy since we don't have subsidy data separated.
        Using operating result as proxy for subsidy dependence.
        """
        logger.info("Generating Figure 3: Revenue Efficiency vs Payment Delays...")

        # Filter to hospitals with data
        df = self.panel[
            (self.panel['is_hospital'] == True) &
            (self.panel['phfsi'].notna()) &
            (self.panel['pagamentos_em_atraso'].notna()) &
            (self.panel['rendimentos_operacionais'].notna())
        ].copy()

        # Calculate revenue efficiency (proxy for subsidy dependence)
        # Lower efficiency = higher subsidy dependence
        df['revenue_efficiency'] = df['resultados_operacionais'] / df['rendimentos_operacionais']
        df['revenue_efficiency'] = df['revenue_efficiency'].clip(lower=-0.5, upper=0.5)

        # Convert to subsidy dependence (invert so higher = more subsidies needed)
        df['subsidy_dependence'] = -df['revenue_efficiency']

        # Create scatter plot
        fig, ax = plt.subplots(figsize=(10, 6))

        # Scatter plot colored by PHFSI
        scatter = ax.scatter(df['subsidy_dependence'],
                           df['pagamentos_em_atraso'],
                           c=df['phfsi'],
                           cmap='RdYlGn',
                           alpha=0.6,
                           s=50,
                           edgecolors='black',
                           linewidths=0.5)

        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('PHFSI Score', fontweight='bold')

        # Add trend line
        from scipy import stats
        mask = df[['subsidy_dependence', 'pagamentos_em_atraso']].notna().all(axis=1)
        if mask.sum() > 2:
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                df.loc[mask, 'subsidy_dependence'],
                df.loc[mask, 'pagamentos_em_atraso']
            )
            x_line = np.array([df['subsidy_dependence'].min(), df['subsidy_dependence'].max()])
            y_line = slope * x_line + intercept
            ax.plot(x_line, y_line, 'r--', linewidth=2, alpha=0.7,
                   label=f'Trend (R² = {r_value**2:.3f}, p = {p_value:.3f})')

        # Labels and title
        ax.set_xlabel('Subsidy Dependence (Proxy: -Operating Result / Revenue)',
                     fontweight='bold')
        ax.set_ylabel('Average Payment Delays (days)', fontweight='bold')
        ax.set_title('Relationship Between Subsidy Dependence and Payment Delays\n(Colored by PHFSI Score)',
                    fontweight='bold', pad=15)

        # Grid and legend
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(loc='best', framealpha=0.9)

        # Add note
        note_text = "Note: Subsidy dependence proxied by negative operating result ratio (higher = more subsidies needed). "
        note_text += "Each point represents a hospital-year observation. Color indicates PHFSI score (green = sustainable, red = distressed)."
        fig.text(0.1, 0.02, note_text, fontsize=8, style='italic', wrap=True)

        # Save
        plt.tight_layout()
        output_path = OUTPUT_DIR / "figure3_subsidy_delays.pdf"
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.savefig(OUTPUT_DIR / "figure3_subsidy_delays.png", bbox_inches='tight', dpi=300)
        plt.close()

        logger.info(f"Figure 3 saved to: {output_path}")

    def run_pipeline(self):
        """Execute full pipeline to generate all figures."""
        logger.info("Starting descriptive plots pipeline...")
        logger.info("="*60 + "\n")

        # Load data
        self.load_data()

        # Generate figures
        self.generate_figure1_phfsi_trends()
        self.generate_figure2_component_correlation()
        self.generate_figure3_subsidy_delays()

        logger.info("\n" + "="*60)
        logger.info("DESCRIPTIVE PLOTS PIPELINE COMPLETE")
        logger.info("="*60)
        logger.info("\nGenerated files:")
        logger.info(f"  - {OUTPUT_DIR / 'figure1_phfsi_trends.pdf'}")
        logger.info(f"  - {OUTPUT_DIR / 'figure1_phfsi_trends.png'}")
        logger.info(f"  - {OUTPUT_DIR / 'figure2_component_correlation.pdf'}")
        logger.info(f"  - {OUTPUT_DIR / 'figure2_component_correlation.png'}")
        logger.info(f"  - {OUTPUT_DIR / 'figure3_subsidy_delays.pdf'}")
        logger.info(f"  - {OUTPUT_DIR / 'figure3_subsidy_delays.png'}")


def main():
    """Main execution function."""
    generator = DescriptivePlotsGenerator()
    generator.run_pipeline()

    print("\n" + "="*60)
    print("All figures generated successfully!")
    print("Check 06_output/figures/main/ for PDF and PNG versions")
    print("="*60)


if __name__ == "__main__":
    main()
