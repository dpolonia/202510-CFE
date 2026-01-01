#!/usr/bin/env python3
"""
October 2025 Capital Injection - Quantitative Validation WITH Entity Crosswalk
==============================================================================

Uses hospital_to_uls_mapping_corrected.csv to link 2024 PHFSI scores to
October 2025 capital allocations.

Author: Claude Code
Date: January 1, 2026
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import roc_curve, auc

# Paths
BASE_DIR = Path("/home/dpolonia/202512-CFE")
DATA_DIR = BASE_DIR / "03_data"
OUTPUT_DIR = BASE_DIR / "06_output"

print("=" * 70)
print("OCTOBER 2025 VALIDATION - WITH ENTITY CROSSWALK")
print("=" * 70)

# Load hospital to ULS mapping
print("\n1. Loading entity crosswalk...")
mapping = pd.read_csv(DATA_DIR / "processed" / "crosswalks" / "hospital_to_uls_mapping_corrected.csv")
print(f"   Loaded {len(mapping)} hospital→ULS mappings")
print(f"   Mapped entities: {mapping['parent_uls'].notna().sum()} ({mapping['parent_uls'].notna().sum()/len(mapping)*100:.1f}%)")

# Load October 2025 allocations
print("\n2. Loading October 2025 allocations...")
allocations_raw = pd.read_csv(DATA_DIR / "external" / "interventions" / "dr_allocations_found.csv")
allocations = allocations_raw[allocations_raw['dr_number'] == 'Despacho 12497/2025'].copy()
allocations['amount_millions'] = allocations['amount_eur'] / 1_000_000
print(f"   October 2025 allocations: {len(allocations)} entities")
print(f"   Total: €{allocations['amount_millions'].sum():.1f}M")

# Load 2024 PHFSI scores
print("\n3. Loading 2024 PHFSI scores...")
phfsi = pd.read_parquet(DATA_DIR / "processed" / "variables" / "phfsi_scores.parquet")
phfsi_2024 = phfsi[phfsi['year'] == 2024].copy()
print(f"   2024 PHFSI: {len(phfsi_2024)} entities")

# Normalize entity names for matching
def normalize_uls_name(name):
    """Normalize ULS names for matching"""
    if pd.isna(name):
        return ""

    name = str(name).upper()

    # Common replacements
    replacements = {
        'E.P.E.': '', 'E. P. E.': '', 'EPE': '',
        ', E.P.E.': '', ',': '', '.': ''
    }
    for old, new in replacements.items():
        name = name.replace(old, new)

    # Standardize ULS prefix
    if 'UNIDADE LOCAL DE SAUDE' in name or 'UNIDADE LOCAL DE SAÚDE' in name:
        name = name.replace('UNIDADE LOCAL DE SAUDE', 'ULS')
        name = name.replace('UNIDADE LOCAL DE SAÚDE', 'ULS')

    # Remove extra spaces
    name = ' '.join(name.split())
    return name.strip()

# Normalize allocation entity names
allocations['entity_normalized'] = allocations['entity'].apply(normalize_uls_name)

# Normalize mapping parent_uls names
mapping['parent_uls_normalized'] = mapping['parent_uls'].apply(normalize_uls_name)

print("\n4. Matching October 2025 allocations to parent ULS...")
print("\nAllocation entities to match:")
for entity in allocations['entity'].values:
    print(f"  - {entity} → {normalize_uls_name(entity)}")

# Match allocations to ULS via crosswalk
matched_allocations = []

for _, alloc_row in allocations.iterrows():
    alloc_entity = alloc_row['entity']
    alloc_norm = alloc_row['entity_normalized']
    alloc_amount = alloc_row['amount_millions']

    # Try to match to parent_uls in mapping
    # First try exact match on normalized names
    parent_match = mapping[mapping['parent_uls_normalized'] == alloc_norm]

    if len(parent_match) == 0:
        # Try partial matching
        for _, map_row in mapping.iterrows():
            parent_norm = map_row['parent_uls_normalized']
            if pd.notna(parent_norm) and len(parent_norm) > 0:
                # Check if allocation name contains parent name or vice versa
                if (alloc_norm in parent_norm) or (parent_norm in alloc_norm):
                    parent_match = pd.DataFrame([map_row])
                    break

    if len(parent_match) > 0:
        # Found mapping
        parent_uls = parent_match.iloc[0]['parent_uls']

        matched_allocations.append({
            'allocation_entity': alloc_entity,
            'parent_uls': parent_uls,
            'allocation_millions': alloc_amount,
            'match_type': 'crosswalk'
        })
        print(f"  ✓ {alloc_entity} → {parent_uls}")
    else:
        # Try direct match to IPO names (these don't change)
        if 'IPO' in alloc_entity.upper():
            # IPO entities keep same names
            matched_allocations.append({
                'allocation_entity': alloc_entity,
                'parent_uls': alloc_entity,  # IPO names unchanged
                'allocation_millions': alloc_amount,
                'match_type': 'ipo_direct'
            })
            print(f"  ✓ {alloc_entity} (IPO - direct match)")
        else:
            print(f"  ✗ {alloc_entity} - NO MATCH FOUND")

matched_alloc_df = pd.DataFrame(matched_allocations)

print(f"\n5. Matching summary:")
print(f"   Total allocations: {len(allocations)}")
print(f"   Matched: {len(matched_alloc_df)} ({len(matched_alloc_df)/len(allocations)*100:.1f}%)")

if len(matched_alloc_df) == 0:
    print("\n⚠️ No matches found - cannot proceed with validation")
    exit(1)

# Now match to 2024 PHFSI using both old hospital names and ULS names
print("\n6. Matching to 2024 PHFSI scores...")

validation_data = []

for _, alloc_match in matched_alloc_df.iterrows():
    parent_uls = alloc_match['parent_uls']
    alloc_amount = alloc_match['allocation_millions']

    # Get all old hospitals that map to this parent ULS
    old_hospitals = mapping[mapping['parent_uls'] == parent_uls]['old_hospital_name'].tolist()

    # Try to find PHFSI score using either:
    # 1. Old hospital name (if 2024 PHFSI uses pre-integration names)
    # 2. Parent ULS name (if 2024 PHFSI uses post-integration names)

    phfsi_score = None
    matched_entity_name = None

    # Try old hospital names first
    for old_name in old_hospitals:
        phfsi_match = phfsi_2024[phfsi_2024['entidade'] == old_name]
        if len(phfsi_match) > 0:
            phfsi_score = phfsi_match.iloc[0]['phfsi']
            matched_entity_name = old_name
            break

    # If not found, try parent ULS name directly
    if phfsi_score is None:
        phfsi_match = phfsi_2024[phfsi_2024['entidade'].str.contains(parent_uls, case=False, na=False)]
        if len(phfsi_match) > 0:
            phfsi_score = phfsi_match.iloc[0]['phfsi']
            matched_entity_name = phfsi_match.iloc[0]['entidade']

    # Try IPO exact match
    if phfsi_score is None and 'IPO' in parent_uls:
        # Try to find IPO by name
        ipo_search = parent_uls.replace('IPO ', 'INSTITUTO PORTUGUES DE ONCOLOGIA DE ')
        phfsi_match = phfsi_2024[phfsi_2024['entidade'].str.contains(ipo_search, case=False, na=False)]
        if len(phfsi_match) > 0:
            phfsi_score = phfsi_match.iloc[0]['phfsi']
            matched_entity_name = phfsi_match.iloc[0]['entidade']

    if phfsi_score is not None:
        validation_data.append({
            'allocation_entity': alloc_match['allocation_entity'],
            'parent_uls': parent_uls,
            'phfsi_entity': matched_entity_name,
            'allocation_millions': alloc_amount,
            'phfsi_score': phfsi_score
        })
        print(f"  ✓ {alloc_match['allocation_entity']} → {matched_entity_name} (PHFSI={phfsi_score:.3f})")
    else:
        print(f"  ✗ {alloc_match['allocation_entity']} (parent={parent_uls}) - No PHFSI found")

validation_df = pd.DataFrame(validation_data)

print(f"\n7. Validation dataset:")
print(f"   Allocations matched to PHFSI: {len(validation_df)} of {len(allocations)}")
print(f"   Match rate: {len(validation_df)/len(allocations)*100:.1f}%")

if len(validation_df) < 5:
    print(f"\n⚠️ Only {len(validation_df)} entities matched - insufficient for reliable validation")
    print("   Minimum recommended: 10 entities")

# Correlation analysis
if len(validation_df) >= 3:
    print(f"\n8. Correlation Analysis (N={len(validation_df)}):")

    pearson_r, pearson_p = pearsonr(validation_df['phfsi_score'], validation_df['allocation_millions'])
    spearman_r, spearman_p = spearmanr(validation_df['phfsi_score'], validation_df['allocation_millions'])

    print(f"   Pearson r  = {pearson_r:.3f} (p = {pearson_p:.4f})")
    print(f"   Spearman ρ = {spearman_r:.3f} (p = {spearman_p:.4f})")

    print(f"\n   Framework prediction: Lower PHFSI → Larger allocation (negative r)")
    if pearson_r < 0:
        if pearson_p < 0.05:
            print(f"   ✓✓ STRONG VALIDATION: Significant negative correlation (p<0.05)")
        else:
            print(f"   ✓ PARTIAL VALIDATION: Negative correlation but not significant (p={pearson_p:.3f})")
    else:
        print(f"   ✗ Positive correlation contradicts framework (may reflect sample bias)")

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(10, 7))

    ax.scatter(validation_df['phfsi_score'], validation_df['allocation_millions'],
              s=120, alpha=0.7, c='steelblue', edgecolors='black', linewidth=1.5)

    # Add labels
    for _, row in validation_df.iterrows():
        ax.annotate(row['allocation_entity'][:20],
                   (row['phfsi_score'], row['allocation_millions']),
                   fontsize=8, alpha=0.8, xytext=(5, 5),
                   textcoords='offset points')

    # Add trend line
    if len(validation_df) >= 2:
        z = np.polyfit(validation_df['phfsi_score'], validation_df['allocation_millions'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(validation_df['phfsi_score'].min(),
                            validation_df['phfsi_score'].max(), 100)
        ax.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2, label='Trend line')

    ax.set_xlabel('2024 PHFSI Score', fontsize=13)
    ax.set_ylabel('October 2025 Capital Allocation (€M)', fontsize=13)
    ax.set_title('PHFSI Validation: October 2025 Capital Injection\n(Using Entity Crosswalk)',
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Stats box
    stats_text = f'N = {len(validation_df)}\nPearson r = {pearson_r:.3f}\np = {pearson_p:.3f}'
    if pearson_p < 0.05:
        stats_text += '\n(Significant)'
    ax.text(0.05, 0.95, stats_text,
           transform=ax.transAxes, fontsize=11,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    plt.tight_layout()

    fig_path = OUTPUT_DIR / "figures" / "main" / "figure_oct2025_validation_with_crosswalk.pdf"
    fig_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    print(f"\n   Figure saved: {fig_path}")

    # Create validation table
    table_path = OUTPUT_DIR / "tables" / "main" / "table6_oct2025_validation_quantitative.tex"

    latex_lines = [
        "\\begin{tabular}{lcccc}",
        "\\toprule",
        "Entity & Allocation (€M) & 2024 PHFSI & Rank & Validation \\\\",
        "\\midrule"
    ]

    # Sort by allocation amount
    validation_sorted = validation_df.sort_values('allocation_millions', ascending=False)

    for i, row in enumerate(validation_sorted.itertuples(), 1):
        entity = row.allocation_entity[:35]
        alloc = f"{row.allocation_millions:.1f}"
        phfsi = f"{row.phfsi_score:.3f}"
        rank = i

        # Validation check: Lower PHFSI should mean higher allocation
        # Check if this entity's rank matches expected (lower PHFSI = higher rank)
        expected_rank = len(validation_sorted) - validation_sorted['phfsi_score'].rank(method='average').iloc[i-1] + 1
        if abs(rank - expected_rank) <= 2:
            validation = "\\checkmark"
        else:
            validation = ""

        latex_lines.append(f"{entity} & {alloc} & {phfsi} & {rank} & {validation} \\\\")

    latex_lines.extend([
        "\\bottomrule",
        "\\end{tabular}"
    ])

    with open(table_path, 'w') as f:
        f.write('\n'.join(latex_lines))

    print(f"   Table saved: {table_path}")

    # Save validation data
    validation_df.to_csv(OUTPUT_DIR / "results" / "validation" / "october_2025_validation_with_crosswalk.csv", index=False)

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)

print(f"\nKEY FINDINGS:")
print(f"  - Matched allocations: {len(validation_df)} of {len(allocations)} ({len(validation_df)/len(allocations)*100:.1f}%)")
if len(validation_df) >= 3:
    print(f"  - Correlation: r = {pearson_r:.3f} (p = {pearson_p:.3f})")
    if pearson_r < 0 and pearson_p < 0.05:
        print(f"  - ✓✓ FRAMEWORK VALIDATED: Significant negative correlation")
    elif pearson_r < 0:
        print(f"  - ✓ Framework consistent but not statistically significant (small N)")
    else:
        print(f"  - Note: Positive correlation may reflect limited sample or IPO-specific dynamics")

print(f"\nNOTE: ULS integration included primary care (ACES) which is not in our hospital")
print(f"financial data. Validation uses hospital component only.")
