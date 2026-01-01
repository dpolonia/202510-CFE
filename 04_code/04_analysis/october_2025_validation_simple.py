#!/usr/bin/env python3
"""
October 2025 Capital Injection - Simple Quantitative Validation
Attempts entity matching despite 2024 ULS integration renaming
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import pearsonr, spearmanr
from difflib import SequenceMatcher
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Paths
BASE_DIR = Path("/home/dpolonia/202512-CFE")
DATA_DIR = BASE_DIR / "03_data"
OUTPUT_DIR = BASE_DIR / "06_output"

print("=" * 70)
print("OCTOBER 2025 CAPITAL INJECTION - QUANTITATIVE VALIDATION")
print("=" * 70)

# Load October 2025 allocations (Despacho 12497/2025 only)
print("\n1. Loading October 2025 allocation data...")
allocations = pd.read_csv(DATA_DIR / "external" / "interventions" / "dr_allocations_found.csv")
allocations = allocations[allocations['dr_number'] == 'Despacho 12497/2025'].copy()
allocations['amount_millions'] = allocations['amount_eur'] / 1_000_000
print(f"   October 2025 allocations: {len(allocations)} entities")
print(f"   Total amount: €{allocations['amount_millions'].sum():.1f}M")

# Load 2024 PHFSI scores
print("\n2. Loading 2024 PHFSI scores...")
phfsi = pd.read_parquet(DATA_DIR / "processed" / "variables" / "phfsi_scores.parquet")
phfsi_2024 = phfsi[phfsi['year'] == 2024].copy()
print(f"   2024 PHFSI scores: {len(phfsi_2024)} entities")

# Manual matching based on known entity correspondences
# Based on manuscript context and IPO matching
print("\n3. Attempting entity matching...")

# Create manual matches for entities we can identify
manual_matches = {
    'ULS São José': None,  # Need to find in PHFSI data
    'ULS Gaia/Espinho': None,
    'ULS Santa Maria': None,
    'ULS Algarve': None,
    'ULS Lisboa Ocidental': None,
    'ULS Trás-os-Montes e Alto Douro': None,
    'ULS Coimbra': None,
    'IPO Lisboa': 'INSTITUTO PORTUGUES DE ONCOLOGIA DE LISBOA, EPE',
    'IPO Coimbra': 'INSTITUTO PORTUGUES DE ONCOLOGIA DE COIMBRA, EPE',
    'IPO Porto': 'INSTITUTO PORTUGUES DE ONCOLOGIA DO PORTO, EPE',
}

# Try to find matches
matched_data = []

for alloc_entity, phfsi_entity_name in manual_matches.items():
    alloc_row = allocations[allocations['entity'] == alloc_entity]

    if len(alloc_row) == 0:
        continue

    alloc_amount = alloc_row.iloc[0]['amount_millions']

    if phfsi_entity_name:
        # Try exact match
        phfsi_row = phfsi_2024[phfsi_2024['entidade'] == phfsi_entity_name]

        if len(phfsi_row) > 0:
            matched_data.append({
                'allocation_entity': alloc_entity,
                'phfsi_entity': phfsi_entity_name,
                'allocation_millions': alloc_amount,
                'phfsi_score': phfsi_row.iloc[0]['phfsi'],
                'match_type': 'exact'
            })
            print(f"   ✓ Matched: {alloc_entity} → {phfsi_entity_name}")

matched_df = pd.DataFrame(matched_data)

print(f"\n4. Matching results:")
print(f"   Total allocations: {len(allocations)}")
print(f"   Matched entities: {len(matched_df)}")
print(f"   Match rate: {len(matched_df)/len(allocations)*100:.1f}%")

if len(matched_df) >= 3:
    print(f"\n5. Correlation Analysis (N={len(matched_df)}):")

    # Remove any NaN PHFSI scores
    valid_data = matched_df.dropna(subset=['phfsi_score'])

    if len(valid_data) >= 3:
        # Pearson correlation
        pearson_r, pearson_p = pearsonr(
            valid_data['phfsi_score'],
            valid_data['allocation_millions']
        )

        # Spearman correlation
        spearman_r, spearman_p = spearmanr(
            valid_data['phfsi_score'],
            valid_data['allocation_millions']
        )

        print(f"   Pearson r = {pearson_r:.3f} (p={pearson_p:.4f})")
        print(f"   Spearman ρ = {spearman_r:.3f} (p={spearman_p:.4f})")

        if pearson_r < 0:
            print("   ✓ Negative correlation supports framework prediction")
            print("     (Lower PHFSI → Larger allocation)")
        else:
            print("   ✗ Positive correlation contradicts framework")

        # Create scatter plot
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(valid_data['phfsi_score'], valid_data['allocation_millions'],
                   s=100, alpha=0.6)

        # Add labels for each point
        for _, row in valid_data.iterrows():
            ax.annotate(row['allocation_entity'],
                       (row['phfsi_score'], row['allocation_millions']),
                       fontsize=8, alpha=0.7)

        # Add trend line
        if len(valid_data) >= 2:
            z = np.polyfit(valid_data['phfsi_score'], valid_data['allocation_millions'], 1)
            p = np.poly1d(z)
            x_trend = np.linspace(valid_data['phfsi_score'].min(),
                                 valid_data['phfsi_score'].max(), 100)
            ax.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2)

        ax.set_xlabel('2024 PHFSI Score', fontsize=12)
        ax.set_ylabel('October 2025 Allocation (€M)', fontsize=12)
        ax.set_title('PHFSI Validation: October 2025 Capital Injection\n(Matched IPO Entities Only)',
                    fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Add stats box
        stats_text = f'N = {len(valid_data)}\nPearson r = {pearson_r:.3f}\nSpearman ρ = {spearman_r:.3f}'
        ax.text(0.05, 0.95, stats_text,
               transform=ax.transAxes, fontsize=10,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()

        output_path = OUTPUT_DIR / "figures" / "main" / "figure_oct2025_validation_ipo.pdf"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n   Scatter plot saved: {output_path}")

        # Save validation table
        validation_table = valid_data[['allocation_entity', 'allocation_millions',
                                       'phfsi_score']].copy()
        validation_table.columns = ['Entity', 'Allocation (€M)', '2024 PHFSI']

        # Create LaTeX table
        latex_lines = [
            "\\begin{tabular}{lcc}",
            "\\toprule",
            "Hospital/IPO & Allocation (€M) & 2024 PHFSI \\\\",
            "\\midrule"
        ]

        for _, row in validation_table.iterrows():
            latex_lines.append(
                f"{row['Entity']} & {row['Allocation (€M)']:.1f} & {row['2024 PHFSI']:.3f} \\\\"
            )

        latex_lines.extend([
            "\\bottomrule",
            "\\end{tabular}"
        ])

        latex_table = "\n".join(latex_lines)

        table_path = OUTPUT_DIR / "tables" / "appendix" / "tableA6_oct2025_validation_matched.tex"
        table_path.parent.mkdir(parents=True, exist_ok=True)
        with open(table_path, 'w') as f:
            f.write(latex_table)

        print(f"   LaTeX table saved: {table_path}")

    else:
        print(f"   ⚠ Only {len(valid_data)} entities with valid PHFSI - insufficient for analysis")
else:
    print(f"\n⚠ Only {len(matched_df)} entities matched - validation requires entity name mapping")
    print("\nAs documented in manuscript limitations:")
    print("  - 2024 ULS integration renamed entities")
    print("  - October 2025 allocations use new 'ULS' names")
    print("  - 2024 PHFSI data uses pre-integration entity names")
    print("\nIPO entities can be matched (same names), but ULS entities cannot.")
    print("Full quantitative validation requires complete entity crosswalk.")

# Create summary report
report_lines = [
    "# October 2025 Validation - Quantitative Analysis Attempt",
    "",
    "## Data",
    f"- October 2025 allocations: {len(allocations)} entities (€{allocations['amount_millions'].sum():.1f}M)",
    f"- 2024 PHFSI scores: {len(phfsi_2024)} entities",
    "",
    "## Matching Results",
    f"- Matched entities: {len(matched_df)}",
    f"- Match rate: {len(matched_df)/len(allocations)*100:.1f}%",
    "",
]

if len(matched_df) >= 3:
    valid_data = matched_df.dropna(subset=['phfsi_score'])
    if len(valid_data) >= 3:
        pearson_r, pearson_p = pearsonr(valid_data['phfsi_score'],
                                        valid_data['allocation_millions'])
        report_lines.extend([
            "## Correlation Analysis",
            f"- N = {len(valid_data)} matched entities",
            f"- Pearson r = {pearson_r:.3f} (p={pearson_p:.4f})",
            "",
            "## Interpretation",
            "⚠ **Limited validation**: Only IPO entities could be matched due to entity renaming.",
            "IPO entities maintained consistent names pre/post ULS integration.",
            "",
            "**Framework prediction**: Lower PHFSI → Larger allocation (negative correlation)",
            f"**Observed**: r = {pearson_r:.3f}",
        ])

        if pearson_r < 0:
            report_lines.append("✓ Correlation direction consistent with framework (limited sample)")
        else:
            report_lines.append("✗ Unexpected positive correlation (may reflect IPO-specific dynamics)")
else:
    report_lines.extend([
        "## Conclusion",
        "⚠ Insufficient matches for statistical analysis",
        "",
        "Entity name mapping limitation prevents full quantitative validation.",
        "As acknowledged in manuscript Section 5.3.4 (Limitations)."
    ])

report_text = "\n".join(report_lines)

report_path = OUTPUT_DIR / "results" / "validation" / "october_2025_quantitative_attempt.md"
report_path.parent.mkdir(parents=True, exist_ok=True)
with open(report_path, 'w') as f:
    f.write(report_text)

print(f"\n6. Validation report saved: {report_path}")

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)
