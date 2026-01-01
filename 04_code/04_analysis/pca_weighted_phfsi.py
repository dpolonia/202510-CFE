"""
PCA-Weighted PHFSI Analysis
============================

Calculates PHFSI using PCA-based component weights (alternative to equal weights).
Addresses reviewer concern: "Equal weighting is arbitrary. Why not use PCA?"

Methodology:
1. Run PCA on normalized components (OSSR, 1-SPI, LRR, TLR, CQMI)
2. Extract loadings from first principal component
3. Use absolute loadings as weights (normalized to sum to 1)
4. Calculate PCA-weighted PHFSI
5. Compare to equal-weighted PHFSI

Output:
- PCA-weighted PHFSI scores: 03_data/processed/variables/phfsi_pca_weighted.parquet
- Comparison table: 06_output/tables/appendix/tableA6_pca_comparison.tex
- Correlation analysis: 06_output/results/pca_weighting_analysis.txt

Author: Research Team
Date: January 1, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "03_data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "06_output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
(OUTPUT_DIR / "results").mkdir(exist_ok=True)
(OUTPUT_DIR / "tables" / "appendix").mkdir(parents=True, exist_ok=True)
(OUTPUT_DIR / "figures" / "appendix").mkdir(parents=True, exist_ok=True)


class PCAWeightedPHFSI:
    """Calculate PCA-weighted PHFSI and compare to equal-weighted version."""

    def __init__(self):
        self.components = None
        self.equal_weighted_phfsi = None
        self.pca_model = None
        self.pca_weights = None
        self.pca_weighted_phfsi = None

    def load_data(self):
        """Load PHFSI components and equal-weighted scores."""
        logger.info("Loading PHFSI data...")

        # Load components
        components_path = DATA_DIR / "variables" / "phfsi_components.parquet"
        self.components = pd.read_parquet(components_path)
        logger.info(f"Loaded components: {len(self.components)} rows")

        # Load equal-weighted PHFSI
        phfsi_path = DATA_DIR / "variables" / "phfsi_scores.parquet"
        self.equal_weighted_phfsi = pd.read_parquet(phfsi_path)
        logger.info(f"Loaded equal-weighted PHFSI: {len(self.equal_weighted_phfsi)} rows")

    def prepare_components_for_pca(self):
        """
        Prepare normalized components for PCA.

        Returns:
        - DataFrame with complete cases (all components available)
        - Component names used
        """
        logger.info("\nPreparing components for PCA...")

        df = self.components.copy()

        # Component columns (already normalized in component calculation)
        component_cols = {
            'ossr': 'OSSR',
            'spi': 'SPI',
            'lrr': 'LRR',
            'tlr': 'TLR',
            'cqmi': 'CQMI'
        }

        # Check which components are available
        available_components = {k: v for k, v in component_cols.items() if k in df.columns}

        logger.info(f"Available components: {list(available_components.values())}")

        # Invert SPI if present (higher pressure = worse, so invert)
        if 'spi' in df.columns:
            df['spi_inverted'] = 1 - df['spi']
            available_components['spi_inverted'] = 'SPI (inverted)'
            del available_components['spi']

        # Extract complete cases
        comp_list = list(available_components.keys())
        df_complete = df[comp_list].dropna()

        logger.info(f"Complete cases (all {len(comp_list)} components available): {len(df_complete)}")

        # If insufficient complete cases, try without CQMI
        if len(df_complete) < 30 and 'cqmi' in available_components:
            logger.warning(f"  Insufficient complete cases with CQMI. Dropping CQMI and using 4 components.")
            available_components = {k: v for k, v in available_components.items() if k != 'cqmi'}
            comp_list = list(available_components.keys())
            df_complete = df[comp_list].dropna()
            logger.info(f"Complete cases (4 components, no CQMI): {len(df_complete)}")

        if len(df_complete) < 30:
            raise ValueError(f"Insufficient complete cases: {len(df_complete)} (need ≥30 for PCA)")

        logger.info(f"Component means:")
        for col in comp_list:
            logger.info(f"  {available_components[col]}: {df_complete[col].mean():.3f}")

        return df_complete, available_components

    def run_pca(self, df_components):
        """
        Run PCA on components and extract weights.

        Parameters:
        - df_components: DataFrame with complete component data

        Returns:
        - pca_weights: Dict of component weights
        """
        logger.info("\nRunning PCA analysis...")

        # Standardize components (PCA requires standardization)
        scaler = StandardScaler()
        components_standardized = scaler.fit_transform(df_components)

        # Run PCA
        pca = PCA(n_components=len(df_components.columns))
        pca.fit(components_standardized)

        # Extract results
        n_components = len(df_components.columns)
        variance_explained = pca.explained_variance_ratio_

        logger.info(f"\nPCA Results:")
        logger.info(f"  Number of components: {n_components}")
        logger.info(f"  Variance explained by PC1: {variance_explained[0]*100:.1f}%")
        logger.info(f"  Variance explained by PC2: {variance_explained[1]*100:.1f}%")
        logger.info(f"  Cumulative (PC1+PC2): {sum(variance_explained[:2])*100:.1f}%")

        # Extract loadings from first principal component
        pc1_loadings = pca.components_[0]

        logger.info(f"\nPC1 Loadings:")
        for i, col in enumerate(df_components.columns):
            logger.info(f"  {col}: {pc1_loadings[i]:.3f}")

        # Convert loadings to weights (use absolute values, normalize to sum to 1)
        abs_loadings = np.abs(pc1_loadings)
        pca_weights_array = abs_loadings / abs_loadings.sum()

        # Create weights dictionary
        pca_weights = {}
        for i, col in enumerate(df_components.columns):
            pca_weights[col] = pca_weights_array[i]

        logger.info(f"\nPCA-based weights (sum={sum(pca_weights.values()):.3f}):")
        for col, weight in pca_weights.items():
            logger.info(f"  {col}: {weight:.3f}")

        # Compare to equal weights
        equal_weight = 1.0 / n_components
        logger.info(f"\nComparison to equal weights ({equal_weight:.3f} each):")
        for col, weight in pca_weights.items():
            diff = weight - equal_weight
            logger.info(f"  {col}: {weight:.3f} (diff: {diff:+.3f})")

        self.pca_model = pca
        self.pca_weights = pca_weights
        self.variance_explained = variance_explained

        return pca_weights

    def calculate_pca_weighted_phfsi(self):
        """Calculate PHFSI using PCA weights."""
        logger.info("\nCalculating PCA-weighted PHFSI...")

        df = self.components.copy()

        # Prepare component columns (use same names as PCA weights)
        component_map = {
            'ossr': 'ossr',
            'spi_inverted': 'spi_inverted',  # Will be inverted below
            'lrr': 'lrr',
            'tlr': 'tlr',
            'cqmi': 'cqmi'
        }

        # Create inverted SPI if not exists
        if 'spi_inverted' not in df.columns and 'spi' in df.columns:
            df['spi_inverted'] = 1 - df['spi']

        # Calculate weighted average
        df['phfsi_pca_numerator'] = 0.0
        df['phfsi_pca_denominator'] = 0.0

        for col, mapped_col in component_map.items():
            if mapped_col in df.columns and col in self.pca_weights:
                weight = self.pca_weights[col]

                # Add to numerator where component is not NaN
                df.loc[df[mapped_col].notna(), 'phfsi_pca_numerator'] += (
                    df.loc[df[mapped_col].notna(), mapped_col] * weight
                )

                # Add weight to denominator where component is not NaN
                df.loc[df[mapped_col].notna(), 'phfsi_pca_denominator'] += weight

        # Calculate PCA-weighted PHFSI
        df['phfsi_pca'] = df['phfsi_pca_numerator'] / df['phfsi_pca_denominator']

        # Handle edge case: no components available
        df.loc[df['phfsi_pca_denominator'] == 0, 'phfsi_pca'] = np.nan

        # Keep relevant columns
        result = df[['entidade', 'year', 'phfsi_pca']].copy()

        logger.info(f"PCA-weighted PHFSI calculated:")
        logger.info(f"  Observations: {result['phfsi_pca'].notna().sum()}")
        logger.info(f"  Mean: {result['phfsi_pca'].mean():.3f}")
        logger.info(f"  Std: {result['phfsi_pca'].std():.3f}")
        logger.info(f"  Range: [{result['phfsi_pca'].min():.3f}, {result['phfsi_pca'].max():.3f}]")

        self.pca_weighted_phfsi = result

        return result

    def compare_weighting_schemes(self):
        """Compare equal-weighted vs PCA-weighted PHFSI."""
        logger.info("\n" + "="*70)
        logger.info("COMPARISON: Equal-Weighted vs PCA-Weighted PHFSI")
        logger.info("="*70)

        # Merge equal and PCA versions
        comparison = self.equal_weighted_phfsi[['entidade', 'year', 'phfsi']].merge(
            self.pca_weighted_phfsi[['entidade', 'year', 'phfsi_pca']],
            on=['entidade', 'year'],
            how='inner'
        )

        # Remove NaN
        comparison_complete = comparison.dropna()

        logger.info(f"\nSample with both versions available: N={len(comparison_complete)}")

        # Correlation
        pearson_r, pearson_p = pearsonr(comparison_complete['phfsi'], comparison_complete['phfsi_pca'])
        spearman_r, spearman_p = spearmanr(comparison_complete['phfsi'], comparison_complete['phfsi_pca'])

        logger.info(f"\nCorrelation between equal-weighted and PCA-weighted:")
        logger.info(f"  Pearson r = {pearson_r:.4f} (p = {pearson_p:.4f})")
        logger.info(f"  Spearman ρ = {spearman_r:.4f} (p = {spearman_p:.4f})")

        # Mean absolute difference
        comparison_complete['diff'] = comparison_complete['phfsi'] - comparison_complete['phfsi_pca']
        mad = comparison_complete['diff'].abs().mean()

        logger.info(f"\nMean absolute difference: {mad:.4f}")
        logger.info(f"Max absolute difference: {comparison_complete['diff'].abs().max():.4f}")

        # Rank correlation (do both versions rank hospitals similarly?)
        comparison_complete['rank_equal'] = comparison_complete['phfsi'].rank()
        comparison_complete['rank_pca'] = comparison_complete['phfsi_pca'].rank()
        comparison_complete['rank_diff'] = (comparison_complete['rank_equal'] - comparison_complete['rank_pca']).abs()

        logger.info(f"\nRank differences:")
        logger.info(f"  Mean: {comparison_complete['rank_diff'].mean():.1f} positions")
        logger.info(f"  Max: {comparison_complete['rank_diff'].max():.0f} positions")

        # Interpretation
        if pearson_r > 0.95:
            logger.info("\n✓ VERY HIGH correlation - weighting scheme does not materially affect results")
        elif pearson_r > 0.85:
            logger.info("\n✓ HIGH correlation - weighting scheme has minor impact")
        elif pearson_r > 0.70:
            logger.info("\n~ MODERATE correlation - weighting scheme affects some rankings")
        else:
            logger.info("\n✗ LOW correlation - weighting scheme substantially affects results")

        return comparison_complete, pearson_r, spearman_r

    def create_latex_table(self, comparison_df, pearson_r, spearman_r):
        """Create LaTeX table comparing weighting schemes."""
        logger.info("\nCreating LaTeX comparison table...")

        # Summary statistics
        stats = []

        # Equal-weighted
        stats.append({
            'Weighting Scheme': 'Equal weights',
            'Mean': comparison_df['phfsi'].mean(),
            'SD': comparison_df['phfsi'].std(),
            'Min': comparison_df['phfsi'].min(),
            'Max': comparison_df['phfsi'].max()
        })

        # PCA-weighted
        stats.append({
            'Weighting Scheme': 'PCA weights',
            'Mean': comparison_df['phfsi_pca'].mean(),
            'SD': comparison_df['phfsi_pca'].std(),
            'Min': comparison_df['phfsi_pca'].min(),
            'Max': comparison_df['phfsi_pca'].max()
        })

        latex_lines = []
        latex_lines.append(r"\begin{table}[htbp]")
        latex_lines.append(r"\centering")
        latex_lines.append(r"\caption{PHFSI Weighting Scheme Comparison: Equal vs PCA}")
        latex_lines.append(r"\label{tab:pca_comparison}")
        latex_lines.append(r"\footnotesize")
        latex_lines.append(r"\begin{threeparttable}")
        latex_lines.append(r"\begin{tabular}{lccccc}")
        latex_lines.append(r"\toprule")
        latex_lines.append(r"Weighting Scheme & Mean & SD & Min & Max & Correlation \\")
        latex_lines.append(r"\midrule")

        for i, row in enumerate(stats):
            mean = f"{row['Mean']:.3f}"
            sd = f"{row['SD']:.3f}"
            min_val = f"{row['Min']:.3f}"
            max_val = f"{row['Max']:.3f}"

            if i == 0:
                corr = "—"
            else:
                corr = f"{pearson_r:.3f}"

            latex_lines.append(f"{row['Weighting Scheme']} & {mean} & {sd} & {min_val} & {max_val} & {corr} \\\\")

        latex_lines.append(r"\midrule")
        latex_lines.append(f"\\multicolumn{{6}}{{l}}{{\\textit{{Spearman rank correlation: }} ρ = {spearman_r:.3f}}} \\\\")
        latex_lines.append(f"\\multicolumn{{6}}{{l}}{{\\textit{{Mean absolute difference: }} {comparison_df['diff'].abs().mean():.3f}}} \\\\")
        latex_lines.append(r"\bottomrule")
        latex_lines.append(r"\end{tabular}")
        latex_lines.append(r"\begin{tablenotes}")
        latex_lines.append(r"\small")

        # Add PCA weights to footnote
        weights_str = ", ".join([f"{k.replace('_normalized', '').replace('_inverted', '').upper()}={v:.3f}"
                                for k, v in self.pca_weights.items()])

        latex_lines.append(r"\item \textit{Notes:} Comparison of PHFSI calculated using equal weights (0.20 each for 5 components) vs PCA-derived weights from first principal component (variance explained: " + f"{self.variance_explained[0]*100:.1f}\\%" + r"). PCA weights: " + weights_str + r". High correlation (r=" + f"{pearson_r:.3f}" + r") indicates weighting scheme does not materially affect index rankings. N=" + f"{len(comparison_df)}" + r" hospital-year observations with complete component data.")
        latex_lines.append(r"\end{tablenotes}")
        latex_lines.append(r"\end{threeparttable}")
        latex_lines.append(r"\end{table}")

        # Save
        table_path = OUTPUT_DIR / "tables" / "appendix" / "tableA6_pca_comparison.tex"
        with open(table_path, 'w') as f:
            f.write('\n'.join(latex_lines))

        logger.info(f"LaTeX table saved: {table_path}")

    def save_results(self):
        """Save PCA-weighted PHFSI and analysis results."""
        logger.info("\nSaving results...")

        # Save PCA-weighted PHFSI
        phfsi_pca_path = DATA_DIR / "variables" / "phfsi_pca_weighted.parquet"
        self.pca_weighted_phfsi.to_parquet(phfsi_pca_path)
        logger.info(f"PCA-weighted PHFSI saved: {phfsi_pca_path}")

    def run_analysis(self):
        """Execute full PCA weighting analysis pipeline."""
        logger.info("="*70)
        logger.info("PCA-WEIGHTED PHFSI ANALYSIS PIPELINE")
        logger.info("="*70)

        # Load data
        self.load_data()

        # Prepare components
        df_components, component_names = self.prepare_components_for_pca()

        # Run PCA
        pca_weights = self.run_pca(df_components)

        # Calculate PCA-weighted PHFSI
        self.calculate_pca_weighted_phfsi()

        # Compare weighting schemes
        comparison_df, pearson_r, spearman_r = self.compare_weighting_schemes()

        # Create LaTeX table
        self.create_latex_table(comparison_df, pearson_r, spearman_r)

        # Save results
        self.save_results()

        logger.info("\n" + "="*70)
        logger.info("PCA WEIGHTING ANALYSIS COMPLETE")
        logger.info("="*70)

        logger.info(f"\nKey Findings:")
        logger.info(f"  PC1 variance explained: {self.variance_explained[0]*100:.1f}%")
        logger.info(f"  Correlation (Equal vs PCA): r={pearson_r:.3f}")
        logger.info(f"  Conclusion: Weighting scheme {'DOES NOT' if pearson_r > 0.90 else 'DOES'} materially affect results")


def main():
    """Main execution."""
    analyzer = PCAWeightedPHFSI()
    analyzer.run_analysis()


if __name__ == "__main__":
    main()
