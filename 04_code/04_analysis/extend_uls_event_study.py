#!/usr/bin/env python3
"""
Extend ULS Event Study Through 2024
Calculate 4-component PHFSI (excl. CQMI) for 2024 to assess post-reform effects
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path("/home/dpolonia/202512-CFE")
DATA_DIR = BASE_DIR / "03_data"
OUTPUT_DIR = BASE_DIR / "06_output"

print("=" * 70)
print("EXTENDING ULS EVENT STUDY THROUGH 2024")
print("=" * 70)

# Load PHFSI data
print("\n1. Loading PHFSI data...")
phfsi = pd.read_parquet(DATA_DIR / "processed" / "variables" / "phfsi_scores.parquet")

print(f"   Total observations: {len(phfsi)}")
print(f"   Years: {sorted(phfsi['year'].unique())}")
print(f"   Components: {[c for c in phfsi.columns if c not in ['entidade', 'year', 'phfsi', 'phfsi_n_components', 'phfsi_cluster']]}")

# Check 2024 data availability
print("\n2. Checking 2024 data availability:")
phfsi_2024 = phfsi[phfsi['year'] == 2024].copy()
print(f"   2024 observations: {len(phfsi_2024)}")

# Check component availability
for comp in ['ossr', 'spi', 'lrr', 'tlr', 'cqmi']:
    n_available = phfsi_2024[comp].notna().sum()
    print(f"   {comp.upper()}: {n_available}/{len(phfsi_2024)} ({n_available/len(phfsi_2024)*100:.1f}%)")

# Calculate 4-component PHFSI for 2024 (excluding CQMI)
print("\n3. Calculating 4-component PHFSI for 2024...")

phfsi_4comp = phfsi.copy()

# Normalize components (if not already 0-1)
# OSSR: already 0-1 (ratio)
# SPI: invert so higher = better (1 - SPI)
# LRR: already 0-1 (ratio)
# TLR: invert so higher = better (1 - TLR)

phfsi_4comp['phfsi_4comp'] = (
    phfsi_4comp['ossr'] +
    (1 - phfsi_4comp['spi']) +
    phfsi_4comp['lrr'] +
    (1 - phfsi_4comp['tlr'])
) / 4

print(f"   4-component PHFSI calculated")
print(f"\n   By year:")
summary = phfsi_4comp.groupby('year')['phfsi_4comp'].agg([
    'count',
    ('mean', lambda x: x.mean()),
    ('std', lambda x: x.std())
])
print(summary)

# Identify ULS reform hospitals (entities that were "Centro Hospitalar" before 2024)
# For simplicity, filter to entities present in both 2023 and 2024
print("\n4. Identifying ULS reform hospitals...")

entities_2023 = set(phfsi[phfsi['year'] == 2023]['entidade'].unique())
entities_2024 = set(phfsi[phfsi['year'] == 2024]['entidade'].unique())

# Find entities present in all years 2017-2024
all_years = set(range(2017, 2025))
entity_years = phfsi.groupby('entidade')['year'].apply(set)
entities_all_years = entity_years[entity_years.apply(lambda x: all_years.issubset(x))].index.tolist()

print(f"   Entities in all years (2017-2024): {len(entities_all_years)}")

# Filter to these stable entities
phfsi_stable = phfsi_4comp[phfsi_4comp['entidade'].isin(entities_all_years)].copy()

print(f"   Stable panel: {len(phfsi_stable)} observations ({len(entities_all_years)} entities × 8 years)")

# Calculate annual means for event study
print("\n5. Generating event study data...")
event_study = phfsi_stable.groupby('year').agg({
    'phfsi_4comp': ['mean', 'std', 'count'],
    'ossr': 'mean',
    'spi': 'mean',
    'lrr': 'mean',
    'tlr': 'mean'
}).reset_index()

event_study.columns = ['year', 'phfsi_mean', 'phfsi_std', 'phfsi_n',
                       'ossr_mean', 'spi_mean', 'lrr_mean', 'tlr_mean']

print("\n   Event Study Summary (4-component PHFSI):")
print(event_study[['year', 'phfsi_mean', 'phfsi_std', 'phfsi_n']])

# Create extended event study figure
print("\n6. Creating event study figure...")

fig, ax = plt.subplots(figsize=(12, 7))

# Plot mean PHFSI with 95% CI
years = event_study['year'].values
means = event_study['phfsi_mean'].values
stds = event_study['phfsi_std'].values
ns = event_study['phfsi_n'].values

# Calculate 95% CI
se = stds / np.sqrt(ns)
ci_95 = 1.96 * se

ax.plot(years, means, 'o-', linewidth=2, markersize=8, color='steelblue', label='Mean PHFSI (4-component)')
ax.fill_between(years, means - ci_95, means + ci_95, alpha=0.3, color='steelblue', label='95% CI')

# Add vertical line at 2024 (reform year)
ax.axvline(x=2024, color='red', linestyle='--', linewidth=2, alpha=0.7, label='ULS Integration (2024)')

# Add COVID period shading
ax.axvspan(2020, 2021, alpha=0.1, color='gray', label='COVID Period')

# Labels and title
ax.set_xlabel('Year', fontsize=13)
ax.set_ylabel('PHFSI (4-component)', fontsize=13)
ax.set_title('ULS Integration Event Study: Extended Through 2024\n(4-component PHFSI: OSSR + SPI + LRR + TLR)',
            fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10, loc='best')

# Set x-axis to show all years
ax.set_xticks(years)

plt.tight_layout()

# Save figure
output_path = OUTPUT_DIR / "figures" / "main" / "figure5_uls_event_study_extended.pdf"
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"   Figure saved: {output_path}")

# Also save PNG for quick viewing
output_path_png = output_path.with_suffix('.png')
plt.savefig(output_path_png, dpi=150, bbox_inches='tight')
print(f"   PNG saved: {output_path_png}")

# Create LaTeX table with extended event study results
print("\n7. Creating LaTeX table...")

latex_lines = [
    "\\begin{tabular}{lcccccccc}",
    "\\toprule",
    "Year & PHFSI & OSSR & SPI & LRR & TLR & N & SD \\\\",
    "\\midrule"
]

for _, row in event_study.iterrows():
    year = int(row['year'])
    phfsi = f"{row['phfsi_mean']:.3f}"
    ossr = f"{row['ossr_mean']:.3f}"
    spi = f"{row['spi_mean']:.3f}"
    lrr = f"{row['lrr_mean']:.3f}"
    tlr = f"{row['tlr_mean']:.3f}"
    n = int(row['phfsi_n'])
    sd = f"{row['phfsi_std']:.3f}"

    latex_lines.append(
        f"{year} & {phfsi} & {ossr} & {spi} & {lrr} & {tlr} & {n} & {sd} \\\\"
    )

latex_lines.extend([
    "\\bottomrule",
    "\\end{tabular}"
])

latex_table = "\n".join(latex_lines)

table_path = OUTPUT_DIR / "tables" / "appendix" / "tableA5_uls_event_study_extended.tex"
table_path.parent.mkdir(parents=True, exist_ok=True)
with open(table_path, 'w') as f:
    f.write(latex_table)

print(f"   Table saved: {table_path}")

# Assess 2024 change
print("\n8. Assessing 2024 post-reform change...")

phfsi_2023 = event_study[event_study['year'] == 2023]['phfsi_mean'].values[0]
phfsi_2024 = event_study[event_study['year'] == 2024]['phfsi_mean'].values[0]

change = phfsi_2024 - phfsi_2023
pct_change = (change / phfsi_2023) * 100

print(f"   2023 PHFSI (4-comp): {phfsi_2023:.3f}")
print(f"   2024 PHFSI (4-comp): {phfsi_2024:.3f}")
print(f"   Change: {change:+.3f} ({pct_change:+.1f}%)")

if change > 0:
    print(f"   ✓ PHFSI improved post-reform (+{change:.3f})")
    print("     Suggests ULS integration may have positive effects")
elif change < 0:
    print(f"   ✗ PHFSI declined post-reform ({change:.3f})")
    print("     Suggests integration did not immediately improve sustainability")
else:
    print("   → No change post-reform")

print("\n" + "=" * 70)
print("EVENT STUDY EXTENSION COMPLETE")
print("=" * 70)
print(f"\nOutputs:")
print(f"  - Figure: {output_path.name}")
print(f"  - Table: {table_path.name}")
print(f"\nKey finding: 2024 PHFSI = {phfsi_2024:.3f} (vs 2023: {phfsi_2023:.3f}, change: {change:+.3f})")
