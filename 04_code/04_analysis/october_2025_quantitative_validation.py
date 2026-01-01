#!/usr/bin/env python3
"""
October 2025 Capital Injection - Quantitative Validation
========================================================

This script performs quantitative validation of the PHFSI framework using
October 2025 capital injection data (€500M to 42 entities).

Objective:
- Match October 2025 allocations to 2024 PHFSI scores
- Calculate correlation between PHFSI and allocation amounts
- Generate ROC curve for PHFSI predicting allocation receipt
- Compare to baseline (random/Z-score if available)

Key Challenge: Entity renaming during 2024 ULS integration
Solution: Use entity name matching with fuzzy matching algorithms

Author: Claude Code
Date: January 1, 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import roc_curve, auc, roc_auc_score
from difflib import SequenceMatcher
import re

# Set paths
BASE_DIR = Path("/home/dpolonia/202512-CFE")
DATA_DIR = BASE_DIR / "03_data"
OUTPUT_DIR = BASE_DIR / "06_output"

class October2025Validator:
    """Validate PHFSI using October 2025 capital injection data"""

    def __init__(self):
        self.allocations = None
        self.phfsi_scores = None
        self.matched_data = None

    def load_data(self):
        """Load allocation data and PHFSI scores"""
        print("Loading data...")

        # Load October 2025 allocations
        allocations_file = DATA_DIR / "external" / "interventions" / "capital_injections.csv"
        df_alloc = pd.read_csv(allocations_file)

        # Filter to October 2025 only
        self.allocations = df_alloc[
            df_alloc['dr_number'] == 'Despacho 12497/2025'
        ].copy()

        print(f"October 2025 allocations: {len(self.allocations)} entities")
        print(f"Total amount: €{self.allocations['amount_eur_millions'].sum():.1f}M")

        # Load PHFSI scores - try multiple locations
        phfsi_files = [
            DATA_DIR / "processed" / "variables" / "phfsi_scores.parquet",
            DATA_DIR / "processed" / "panel" / "hospital_year_panel.parquet",
            OUTPUT_DIR / "results" / "phfsi_scores_all_years.csv"
        ]

        for phfsi_file in phfsi_files:
            if phfsi_file.exists():
                if phfsi_file.suffix == '.parquet':
                    self.phfsi_scores = pd.read_parquet(phfsi_file)
                else:
                    self.phfsi_scores = pd.read_csv(phfsi_file)

                # Filter to 2024 only
                if 'year' in self.phfsi_scores.columns:
                    self.phfsi_scores = self.phfsi_scores[
                        self.phfsi_scores['year'] == 2024
                    ].copy()

                print(f"Loaded PHFSI scores from: {phfsi_file.name}")
                print(f"2024 PHFSI scores: {len(self.phfsi_scores)} entities")
                break

        if self.phfsi_scores is None:
            raise FileNotFoundError("Could not find PHFSI scores file")

    def normalize_entity_name(self, name):
        """Normalize entity names for matching"""
        if pd.isna(name):
            return ""

        # Convert to uppercase
        name = str(name).upper()

        # Remove common abbreviations and punctuation
        replacements = {
            'E.P.E.': '',
            'EPE': '',
            'E. P. E.': '',
            'E.P.E': '',
            ',': '',
            '.': '',
            '  ': ' ',
        }

        for old, new in replacements.items():
            name = name.replace(old, new)

        # Standardize ULS naming
        name = name.replace('UNIDADE LOCAL DE SAUDE', 'ULS')
        name = name.replace('UNIDADE LOCAL DE SAÚDE', 'ULS')

        # Standardize hospital naming
        name = name.replace('CENTRO HOSPITALAR', 'CH')
        name = name.replace('HOSPITAL', 'H')

        # Remove extra whitespace
        name = ' '.join(name.split())

        return name.strip()

    def fuzzy_match_score(self, s1, s2):
        """Calculate fuzzy match score between two strings"""
        return SequenceMatcher(None, s1, s2).ratio()

    def match_entities(self, threshold=0.7):
        """Match allocation entities to PHFSI entities"""
        print(f"\nMatching entities (threshold={threshold})...")

        # Normalize names in both datasets
        self.allocations['entity_normalized'] = self.allocations['entity'].apply(
            self.normalize_entity_name
        )

        # Get entity column name from PHFSI (could be 'entidade', 'entity', 'entity_name')
        entity_col = None
        for col in ['entidade', 'entity', 'entity_name', 'hospital']:
            if col in self.phfsi_scores.columns:
                entity_col = col
                break

        if entity_col is None:
            raise ValueError("Could not find entity column in PHFSI data")

        self.phfsi_scores['entity_normalized'] = self.phfsi_scores[entity_col].apply(
            self.normalize_entity_name
        )

        # Try exact matching first
        matches = []
        for idx, alloc_row in self.allocations.iterrows():
            alloc_name = alloc_row['entity_normalized']

            # Try exact match
            exact_match = self.phfsi_scores[
                self.phfsi_scores['entity_normalized'] == alloc_name
            ]

            if len(exact_match) > 0:
                matches.append({
                    'allocation_entity': alloc_row['entity'],
                    'phfsi_entity': exact_match.iloc[0][entity_col],
                    'match_score': 1.0,
                    'match_type': 'exact',
                    'allocation_amount': alloc_row['amount_eur_millions'],
                    'phfsi_score': exact_match.iloc[0].get('phfsi', None)
                })
            else:
                # Try fuzzy matching
                best_score = 0
                best_match = None

                for _, phfsi_row in self.phfsi_scores.iterrows():
                    score = self.fuzzy_match_score(
                        alloc_name,
                        phfsi_row['entity_normalized']
                    )

                    if score > best_score and score >= threshold:
                        best_score = score
                        best_match = phfsi_row

                if best_match is not None:
                    matches.append({
                        'allocation_entity': alloc_row['entity'],
                        'phfsi_entity': best_match[entity_col],
                        'match_score': best_score,
                        'match_type': 'fuzzy',
                        'allocation_amount': alloc_row['amount_eur_millions'],
                        'phfsi_score': best_match.get('phfsi', None)
                    })

        self.matched_data = pd.DataFrame(matches)

        print(f"\nMatching results:")
        print(f"  Exact matches: {len(self.matched_data[self.matched_data['match_type']=='exact'])}")
        print(f"  Fuzzy matches: {len(self.matched_data[self.matched_data['match_type']=='fuzzy'])}")
        print(f"  Total matched: {len(self.matched_data)} of {len(self.allocations)} allocations")
        print(f"  Match rate: {len(self.matched_data)/len(self.allocations)*100:.1f}%")

        if len(self.matched_data) > 0:
            print(f"\nSample matches:")
            print(self.matched_data[['allocation_entity', 'phfsi_entity', 'match_score']].head(10))

        return self.matched_data

    def calculate_correlation(self):
        """Calculate correlation between PHFSI and allocation amounts"""
        if len(self.matched_data) < 10:
            print(f"\nWarning: Only {len(self.matched_data)} matched entities - correlation may not be reliable")
            return None

        # Remove any missing PHFSI scores
        valid_data = self.matched_data.dropna(subset=['phfsi_score'])

        if len(valid_data) < 5:
            print("Insufficient data for correlation analysis")
            return None

        print(f"\nCorrelation Analysis (N={len(valid_data)} matched entities):")

        # Pearson correlation
        pearson_r, pearson_p = pearsonr(
            valid_data['phfsi_score'],
            valid_data['allocation_amount']
        )
        print(f"  Pearson r = {pearson_r:.3f} (p={pearson_p:.4f})")

        # Spearman correlation (rank-based, more robust)
        spearman_r, spearman_p = spearmanr(
            valid_data['phfsi_score'],
            valid_data['allocation_amount']
        )
        print(f"  Spearman ρ = {spearman_r:.3f} (p={spearman_p:.4f})")

        # Expected: Negative correlation (lower PHFSI → larger allocation)
        if pearson_r < 0:
            print("  ✓ Negative correlation confirms framework prediction")
        else:
            print("  ✗ Positive correlation contradicts framework prediction")

        return {
            'n': len(valid_data),
            'pearson_r': pearson_r,
            'pearson_p': pearson_p,
            'spearman_r': spearman_r,
            'spearman_p': spearman_p
        }

    def generate_roc_curve(self):
        """Generate ROC curve for PHFSI predicting allocation receipt"""
        # For ROC curve, we need binary outcome (received allocation or not)
        # But we only have allocation recipients here
        # Need to merge with full hospital list

        print("\nROC Analysis:")
        print("Note: ROC analysis requires full hospital list (recipients + non-recipients)")
        print("Current data only includes allocation recipients")
        print("Skipping ROC curve generation - would need complete hospital roster")

        return None

    def create_validation_table(self, output_file=None):
        """Create LaTeX table showing validation results"""
        if len(self.matched_data) == 0:
            print("No matched data - cannot create validation table")
            return

        # Sort by allocation amount (descending)
        top_matched = self.matched_data.nlargest(10, 'allocation_amount')

        latex_lines = [
            "\\begin{tabular}{rlccc}",
            "\\toprule",
            "Rank & Hospital/ULS & Allocation (€M) & 2024 PHFSI & Match Quality \\\\",
            "\\midrule"
        ]

        for i, row in enumerate(top_matched.itertuples(), 1):
            entity_name = row.allocation_entity[:50]  # Truncate long names
            allocation = f"{row.allocation_amount:.1f}"
            phfsi = f"{row.phfsi_score:.3f}" if pd.notna(row.phfsi_score) else "N/A"
            match_quality = f"{row.match_score:.0%}"

            latex_lines.append(
                f"{i} & {entity_name} & {allocation} & {phfsi} & {match_quality} \\\\"
            )

        latex_lines.extend([
            "\\bottomrule",
            "\\end{tabular}"
        ])

        latex_table = "\n".join(latex_lines)

        if output_file:
            output_path = OUTPUT_DIR / "tables" / "main" / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(latex_table)
            print(f"\nValidation table saved to: {output_path}")

        return latex_table

    def create_scatter_plot(self, output_file=None):
        """Create scatter plot of PHFSI vs allocation amount"""
        valid_data = self.matched_data.dropna(subset=['phfsi_score'])

        if len(valid_data) < 5:
            print("Insufficient data for scatter plot")
            return

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.scatter(
            valid_data['phfsi_score'],
            valid_data['allocation_amount'],
            alpha=0.6,
            s=100
        )

        # Add trend line
        z = np.polyfit(valid_data['phfsi_score'], valid_data['allocation_amount'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(valid_data['phfsi_score'].min(), valid_data['phfsi_score'].max(), 100)
        ax.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2, label='Trend line')

        ax.set_xlabel('2024 PHFSI Score', fontsize=12)
        ax.set_ylabel('October 2025 Allocation (€M)', fontsize=12)
        ax.set_title('PHFSI Validation: October 2025 Capital Injection', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()

        # Add correlation text
        pearson_r, _ = pearsonr(valid_data['phfsi_score'], valid_data['allocation_amount'])
        ax.text(0.05, 0.95, f'Pearson r = {pearson_r:.3f}\nN = {len(valid_data)}',
                transform=ax.transAxes, fontsize=11,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()

        if output_file:
            output_path = OUTPUT_DIR / "figures" / "main" / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Scatter plot saved to: {output_path}")

        plt.close()

    def run_validation(self):
        """Run complete validation analysis"""
        print("=" * 70)
        print("OCTOBER 2025 CAPITAL INJECTION - QUANTITATIVE VALIDATION")
        print("=" * 70)

        # Load data
        self.load_data()

        # Match entities
        matched = self.match_entities(threshold=0.7)

        if len(matched) == 0:
            print("\n⚠️  No entities matched - validation cannot proceed")
            print("\nThis confirms the entity name mapping limitation noted in the manuscript.")
            return

        # Calculate correlation
        corr_results = self.calculate_correlation()

        # Create output tables and figures
        self.create_validation_table('table7_oct2025_validation_matched.tex')
        self.create_scatter_plot('figure_oct2025_validation_scatter.pdf')

        # Create summary report
        self.create_summary_report(corr_results)

        print("\n" + "=" * 70)
        print("VALIDATION COMPLETE")
        print("=" * 70)

        return matched, corr_results

    def create_summary_report(self, corr_results):
        """Create summary report of validation findings"""
        report_lines = [
            "# October 2025 Capital Injection - Quantitative Validation Results",
            f"**Date**: January 1, 2026",
            "",
            "## Matching Results",
            f"- Total allocations: {len(self.allocations)} entities (€500M)",
            f"- Matched to 2024 PHFSI: {len(self.matched_data)} entities",
            f"- Match rate: {len(self.matched_data)/len(self.allocations)*100:.1f}%",
            "",
            "## Correlation Analysis",
        ]

        if corr_results:
            report_lines.extend([
                f"- Sample size: N={corr_results['n']} matched entities",
                f"- Pearson correlation: r={corr_results['pearson_r']:.3f} (p={corr_results['pearson_p']:.4f})",
                f"- Spearman correlation: ρ={corr_results['spearman_r']:.3f} (p={corr_results['spearman_p']:.4f})",
                "",
                "## Interpretation",
            ])

            if corr_results['pearson_r'] < 0 and corr_results['pearson_p'] < 0.05:
                report_lines.append("✓ **Validation successful**: Negative correlation confirms that lower PHFSI scores predict larger capital allocations.")
            elif corr_results['pearson_r'] < 0:
                report_lines.append("⚠ **Partial validation**: Negative correlation trend but not statistically significant.")
            else:
                report_lines.append("✗ **Unexpected result**: Positive correlation contradicts framework predictions.")
        else:
            report_lines.append("⚠ Insufficient matched entities for statistical analysis")

        report_text = "\n".join(report_lines)

        # Save report
        report_path = OUTPUT_DIR / "results" / "validation" / "october_2025_quantitative_validation.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            f.write(report_text)

        print(f"\nValidation report saved to: {report_path}")

if __name__ == "__main__":
    validator = October2025Validator()
    validator.run_validation()
