"""
PHFSI Composite Index Calculator

Calculates the composite Public Hospital Financial Sustainability Index (PHFSI)
from individual components.

Formula:
PHFSI = weighted_average(OSSR, 1-SPI, LRR, TLR, CQMI)

Where:
- OSSR: Operational Self-Sufficiency Ratio (higher = better)
- SPI: Stakeholder Pressure Index (INVERTED: higher pressure = lower score)
- LRR: Liquidity Realization Rate (higher = better)
- TLR: True Leverage Ratio (higher = better, already inverted in calculation)
- CQMI: Clinical Quality Maintenance Index (higher = better)

Range: 0 to 1 (higher = better financial sustainability)

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
DATA_PROCESSED = PROJECT_ROOT / "03_data" / "processed"
OUTPUT_DIR = DATA_PROCESSED / "variables"


class PHFSICalculator:
    """
    Calculates composite PHFSI index from individual components.
    """

    def __init__(self, component_weights=None):
        """
        Initialize calculator.

        Parameters:
        - component_weights: Dict with weights for each component
                           Default: Equal weights (0.20 each for 5 components)
                           If CQMI missing, automatically reweights to 0.25 each for 4 components
        """
        self.components = None
        self.phfsi_scores = None

        # Default equal weights
        if component_weights is None:
            self.component_weights = {
                'ossr': 0.20,
                'spi': 0.20,
                'lrr': 0.20,
                'tlr': 0.20,
                'cqmi': 0.20
            }
        else:
            self.component_weights = component_weights

    def load_components(self):
        """Load PHFSI components dataset."""
        logger.info("Loading PHFSI components...")

        components_path = OUTPUT_DIR / "phfsi_components.parquet"

        if not components_path.exists():
            raise FileNotFoundError(
                f"Components not found at {components_path}. "
                "Run phfsi_components.py first."
            )

        self.components = pd.read_parquet(components_path)
        logger.info(f"Loaded components: {len(self.components)} rows")

    def normalize_components(self):
        """
        Normalize all components to 0-1 scale.

        Note: Most components already normalized in component calculation,
        but this ensures consistency and handles any edge cases.
        """
        logger.info("Normalizing components to 0-1 scale...")

        df = self.components.copy()

        # Components to normalize
        component_cols = ['ossr', 'spi', 'lrr', 'tlr', 'cqmi']

        for col in component_cols:
            if col in df.columns:
                # Check if already normalized (min >= 0, max <= 1)
                col_min = df[col].min()
                col_max = df[col].max()

                if pd.isna(col_min) or pd.isna(col_max):
                    logger.warning(f"{col}: All values are NaN, skipping normalization")
                    continue

                if col_min < 0 or col_max > 1.1:  # Allow small tolerance
                    logger.info(f"{col}: Normalizing (current range: {col_min:.3f} to {col_max:.3f})")
                    df[f'{col}_normalized'] = (df[col] - col_min) / (col_max - col_min)
                else:
                    logger.info(f"{col}: Already normalized (range: {col_min:.3f} to {col_max:.3f})")
                    df[f'{col}_normalized'] = df[col]

        self.components = df
        return df

    def invert_spi(self):
        """
        Invert SPI so that higher values = better (consistent with other components).

        SPI measures pressure (higher = worse), so we invert it: (1 - SPI)
        """
        logger.info("Inverting SPI (higher pressure → lower score)...")

        if 'spi_normalized' in self.components.columns:
            self.components['spi_inverted'] = 1 - self.components['spi_normalized']
            logger.info(f"SPI inverted. New mean: {self.components['spi_inverted'].mean():.3f}")
        else:
            logger.warning("SPI normalized column not found")

    def calculate_composite_phfsi(self, method='weighted_average'):
        """
        Calculate composite PHFSI index.

        Parameters:
        - method: 'weighted_average' (default) or 'pca'

        Returns:
        - DataFrame with PHFSI scores
        """
        logger.info(f"Calculating composite PHFSI using method: {method}")

        df = self.components.copy()

        # Map component columns (using normalized and inverted versions)
        component_map = {
            'ossr': 'ossr_normalized',
            'spi': 'spi_inverted',  # Inverted version
            'lrr': 'lrr_normalized',
            'tlr': 'tlr_normalized',
            'cqmi': 'cqmi_normalized'
        }

        if method == 'weighted_average':
            # Calculate weighted average of available components
            df['phfsi_numerator'] = 0.0
            df['phfsi_denominator'] = 0.0

            for component, col_name in component_map.items():
                if col_name in df.columns:
                    weight = self.component_weights[component]

                    # Add to numerator where component is not NaN
                    df.loc[df[col_name].notna(), 'phfsi_numerator'] += (
                        df.loc[df[col_name].notna(), col_name] * weight
                    )

                    # Add weight to denominator where component is not NaN
                    df.loc[df[col_name].notna(), 'phfsi_denominator'] += weight

            # Calculate PHFSI (rescale to use full 0-1 range)
            df['phfsi'] = df['phfsi_numerator'] / df['phfsi_denominator']

            # Handle edge case: no components available
            df.loc[df['phfsi_denominator'] == 0, 'phfsi'] = np.nan

            # Count how many components contributed to each observation
            df['phfsi_n_components'] = 0
            for component, col_name in component_map.items():
                if col_name in df.columns:
                    df['phfsi_n_components'] += df[col_name].notna().astype(int)

        elif method == 'pca':
            logger.warning("PCA method not implemented yet. Using weighted_average.")
            return self.calculate_composite_phfsi(method='weighted_average')

        else:
            raise ValueError(f"Unknown method: {method}")

        logger.info(f"PHFSI calculated. Mean: {df['phfsi'].mean():.3f}, Median: {df['phfsi'].median():.3f}")

        self.phfsi_scores = df
        return df

    def create_phfsi_clusters(self, cutoffs=None):
        """
        Create PHFSI clusters: Distressed, Stable, Self-Sustaining.

        Parameters:
        - cutoffs: Dict with 'distressed' and 'self_sustaining' cutoffs
                  Default: distressed < 0.4, stable 0.4-0.7, self-sustaining > 0.7
        """
        logger.info("Creating PHFSI clusters...")

        if cutoffs is None:
            cutoffs = {
                'distressed': 0.4,
                'self_sustaining': 0.7
            }

        df = self.phfsi_scores.copy()

        # Create cluster categories
        df['phfsi_cluster'] = 'Stable'  # Default
        df.loc[df['phfsi'] < cutoffs['distressed'], 'phfsi_cluster'] = 'Distressed'
        df.loc[df['phfsi'] >= cutoffs['self_sustaining'], 'phfsi_cluster'] = 'Self-Sustaining'
        df.loc[df['phfsi'].isna(), 'phfsi_cluster'] = 'Missing Data'

        # Log distribution
        logger.info("\nPHFSI Cluster Distribution:")
        for cluster in ['Distressed', 'Stable', 'Self-Sustaining', 'Missing Data']:
            count = (df['phfsi_cluster'] == cluster).sum()
            pct = count / len(df) * 100
            logger.info(f"  {cluster}: {count} ({pct:.1f}%)")

        self.phfsi_scores = df
        return df

    def validate_phfsi(self):
        """Validate PHFSI scores and flag potential issues."""
        logger.info("\n" + "="*60)
        logger.info("PHFSI VALIDATION REPORT")
        logger.info("="*60)

        df = self.phfsi_scores

        # Basic statistics
        logger.info(f"\nPHFSI Statistics:")
        logger.info(f"  Mean: {df['phfsi'].mean():.3f}")
        logger.info(f"  Median: {df['phfsi'].median():.3f}")
        logger.info(f"  Std Dev: {df['phfsi'].std():.3f}")
        logger.info(f"  Min: {df['phfsi'].min():.3f}")
        logger.info(f"  Max: {df['phfsi'].max():.3f}")
        logger.info(f"  Missing: {df['phfsi'].isna().sum()} ({df['phfsi'].isna().sum()/len(df)*100:.1f}%)")

        # Component availability
        logger.info(f"\nComponent Availability:")
        logger.info(f"  All 5 components: {(df['phfsi_n_components'] == 5).sum()} observations")
        logger.info(f"  4 components: {(df['phfsi_n_components'] == 4).sum()} observations")
        logger.info(f"  3 components: {(df['phfsi_n_components'] == 3).sum()} observations")
        logger.info(f"  2 components: {(df['phfsi_n_components'] == 2).sum()} observations")
        logger.info(f"  1 component: {(df['phfsi_n_components'] == 1).sum()} observations")
        logger.info(f"  0 components: {(df['phfsi_n_components'] == 0).sum()} observations")

        # Outliers
        mean = df['phfsi'].mean()
        std = df['phfsi'].std()
        outliers = ((df['phfsi'] < mean - 3*std) | (df['phfsi'] > mean + 3*std)).sum()
        logger.info(f"\nOutliers (>3 std dev): {outliers}")

        # Correlation with components
        logger.info(f"\nPHFSI Correlation with Components:")
        for col in ['ossr', 'spi', 'lrr', 'tlr', 'cqmi']:
            if f'{col}_normalized' in df.columns:
                corr = df['phfsi'].corr(df[f'{col}_normalized'])
                if not pd.isna(corr):
                    logger.info(f"  {col}: {corr:.3f}")

        logger.info("\n" + "="*60)

    def save_phfsi_scores(self, filename='phfsi_scores.parquet'):
        """Save PHFSI scores to file."""
        if self.phfsi_scores is None:
            logger.error("PHFSI not calculated yet.")
            return

        # Select key columns to save
        cols_to_save = ['entidade', 'year', 'phfsi', 'phfsi_n_components', 'phfsi_cluster']

        # Add individual components if available
        for col in ['ossr', 'spi', 'lrr', 'tlr', 'cqmi']:
            if col in self.phfsi_scores.columns:
                cols_to_save.append(col)

        output_df = self.phfsi_scores[cols_to_save].copy()

        output_path = OUTPUT_DIR / filename
        output_df.to_parquet(output_path, index=False)
        logger.info(f"\nPHFSI scores saved to: {output_path}")
        logger.info(f"File size: {output_path.stat().st_size / 1024:.1f} KB")

    def run_pipeline(self, method='weighted_average'):
        """Execute full pipeline to calculate and validate PHFSI."""
        logger.info("Starting PHFSI calculation pipeline...")
        logger.info("="*60 + "\n")

        # Load components
        self.load_components()

        # Normalize components
        self.normalize_components()

        # Invert SPI
        self.invert_spi()

        # Calculate composite PHFSI
        self.calculate_composite_phfsi(method=method)

        # Create clusters
        self.create_phfsi_clusters()

        # Validate
        self.validate_phfsi()

        # Save
        self.save_phfsi_scores()

        logger.info("\nPipeline completed successfully!")

        return self.phfsi_scores


def main():
    """Main execution function."""
    calculator = PHFSICalculator()
    phfsi_scores = calculator.run_pipeline()

    print("\n" + "="*60)
    print("PHFSI SCORES PREVIEW")
    print("="*60)
    print(phfsi_scores[['entidade', 'year', 'phfsi', 'phfsi_cluster', 'phfsi_n_components']].head(20))

    print("\n" + "="*60)
    print("SUMMARY BY CLUSTER")
    print("="*60)
    summary = phfsi_scores.groupby('phfsi_cluster').agg({
        'phfsi': ['count', 'mean', 'median', 'std'],
        'ossr': 'mean',
        'spi': 'mean',
        'lrr': 'mean',
        'tlr': 'mean'
    }).round(3)
    print(summary)


if __name__ == "__main__":
    main()
