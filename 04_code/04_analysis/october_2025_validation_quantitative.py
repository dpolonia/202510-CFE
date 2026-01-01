#!/usr/bin/env python3
"""
October 2025 Capital Injection - Quantitative Validation
=========================================================

Uses entity crosswalk to link October 2025 ULS allocations (€500M to 42 entities)
to 2024 PHFSI scores, enabling quantitative validation of framework predictions.

Framework Prediction: Lower PHFSI → Higher allocation (negative correlation)

Addresses Reviewer Concern: "Methods promise ROC analysis, Results provide only
qualitative patterns. Where is the quantitative validation?"

Output:
- figure5_october2025_validation.pdf (2-panel: scatter + quartiles)
- table6_october2025_validation.tex (validation results table)
- october2025_validation_results.csv (detailed results)

Author: Research Team
Date: January 1, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "03_data"
OUTPUT_DIR = PROJECT_ROOT / "06_output"

print("="*70)
print("OCTOBER 2025 CAPITAL INJECTION - QUANTITATIVE VALIDATION")
print("="*70)

# ==============================================================================
# STEP 1: Load October 2025 Capital Injection Data
# ==============================================================================

print("\n1. Loading October 2025 capital injection data...")

allocations_path = DATA_DIR / "external" / "interventions" / "october_2025_complete_allocations.csv"
oct2025 = pd.read_csv(allocations_path)
oct2025['amount_millions'] = oct2025['amount_eur'] / 1_000_000

print(f"   October 2025 allocations: {len(oct2025)} entities")
print(f"   Total amount: €{oct2025['amount_millions'].sum():.1f}M")
print(f"   Range: €{oct2025['amount_millions'].min():.2f}M to €{oct2025['amount_millions'].max():.1f}M")

# ==============================================================================
# STEP 2: Load Entity Crosswalk
# ==============================================================================

print("\n2. Loading entity crosswalk (hospital → ULS mapping)...")

crosswalk_path = DATA_DIR / "processed" / "crosswalks" / "hospital_to_uls_mapping_corrected.csv"
crosswalk = pd.read_csv(crosswalk_path)

print(f"   Crosswalk: {len(crosswalk)} hospital entities")
print(f"   Mapped to: {crosswalk['parent_uls'].nunique()} unique ULS entities")

# ==============================================================================
# STEP 3: Load PHFSI Scores (2024 or most recent)
# ==============================================================================

print("\n3. Loading PHFSI scores...")

phfsi_path = DATA_DIR / "processed" / "variables" / "phfsi_scores.parquet"
phfsi = pd.read_parquet(phfsi_path)

# Try 2024 first, fallback to 2023 if unavailable
phfsi_2024 = phfsi[phfsi['year'] == 2024].copy()

if len(phfsi_2024) == 0:
    print("   ⚠️ No 2024 PHFSI data available, using 2023...")
    phfsi_recent = phfsi[phfsi['year'] == 2023].copy()
    validation_year = 2023
else:
    phfsi_recent = phfsi_2024.copy()
    validation_year = 2024

print(f"   Using {validation_year} PHFSI: {len(phfsi_recent)} entities")

# ==============================================================================
# STEP 4: Entity Matching Strategy
# ==============================================================================

print("\n4. Matching October 2025 allocations to PHFSI via crosswalk...")

def normalize_entity_name(name):
    """Normalize entity names for matching."""
    if pd.isna(name):
        return ""
    name = str(name).upper()
    replacements = {
        'E.P.E.': '', 'E. P. E.': '', 'EPE': '', ',': '', '.': '',
        'UNIDADE LOCAL DE SAUDE': 'ULS',
        'UNIDADE LOCAL DE SAÚDE': 'ULS',
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    return ' '.join(name.split()).strip()

# Normalize all entity names
oct2025['entity_normalized'] = oct2025['entity'].apply(normalize_entity_name)
crosswalk['parent_uls_normalized'] = crosswalk['parent_uls'].apply(normalize_entity_name)
crosswalk['old_hospital_normalized'] = crosswalk['old_hospital_name'].apply(normalize_entity_name)
phfsi_recent['entidade_normalized'] = phfsi_recent['entidade'].apply(normalize_entity_name)

validation_data = []

print("\n   Matching results:")
print("   " + "-"*66)

for _, alloc_row in oct2025.iterrows():
    uls_name = alloc_row['entity']
    uls_normalized = alloc_row['entity_normalized']
    allocation_amount = alloc_row['amount_millions']

    # Step 4a: Find old hospital names that map to this ULS
    old_hospitals = crosswalk[crosswalk['parent_uls_normalized'] == uls_normalized]['old_hospital_name'].tolist()

    # If no exact match, try partial matching
    if len(old_hospitals) == 0:
        partial_matches = crosswalk[crosswalk['parent_uls_normalized'].str.contains(uls_normalized[:20], na=False)]
        if len(partial_matches) > 0:
            old_hospitals = partial_matches['old_hospital_name'].tolist()

    # Step 4b: Try to find PHFSI for any old hospital variant
    phfsi_score = None
    matched_entity_name = None
    match_method = None

    if len(old_hospitals) > 0:
        for old_name in old_hospitals:
            old_normalized = normalize_entity_name(old_name)

            # Try exact match
            exact_match = phfsi_recent[phfsi_recent['entidade_normalized'] == old_normalized]
            if len(exact_match) > 0:
                phfsi_score = exact_match.iloc[0]['phfsi']
                matched_entity_name = exact_match.iloc[0]['entidade']
                match_method = 'exact'
                break

            # Try partial match (first 30 chars)
            if len(old_normalized) > 10:
                partial_match = phfsi_recent[phfsi_recent['entidade_normalized'].str.contains(old_normalized[:30], na=False)]
                if len(partial_match) > 0:
                    phfsi_score = partial_match.iloc[0]['phfsi']
                    matched_entity_name = partial_match.iloc[0]['entidade']
                    match_method = 'partial'
                    break

    # Step 4c: Try direct ULS match (for entities that didn't change names much)
    if phfsi_score is None:
        direct_match = phfsi_recent[phfsi_recent['entidade_normalized'].str.contains(uls_normalized[:25], na=False)]
        if len(direct_match) > 0:
            phfsi_score = direct_match.iloc[0]['phfsi']
            matched_entity_name = direct_match.iloc[0]['entidade']
            match_method = 'direct_uls'

    # Step 4d: IPO special handling (IPO names relatively stable)
    if phfsi_score is None and 'IPO' in uls_name.upper():
        ipo_keywords = uls_name.upper().split()
        for keyword in ipo_keywords:
            if len(keyword) > 4:  # City names
                ipo_match = phfsi_recent[phfsi_recent['entidade'].str.contains(keyword, case=False, na=False)]
                if len(ipo_match) > 0:
                    phfsi_score = ipo_match.iloc[0]['phfsi']
                    matched_entity_name = ipo_match.iloc[0]['entidade']
                    match_method = 'ipo_keyword'
                    break

    # Record result
    if phfsi_score is not None:
        validation_data.append({
            'uls_entity': uls_name,
            'old_hospital_name': matched_entity_name,
            'allocation_millions': allocation_amount,
            'phfsi_score': phfsi_score,
            'match_method': match_method,
            'validation_year': validation_year
        })
        print(f"   ✓ {uls_name[:45]:45s} → PHFSI={phfsi_score:.3f}, €{allocation_amount:6.1f}M ({match_method})")
    else:
        print(f"   ✗ {uls_name[:45]:45s} → No PHFSI match found")

validation_df = pd.DataFrame(validation_data)

print("\n   " + "-"*66)
print(f"   Matched: {len(validation_df)} of {len(oct2025)} allocations ({len(validation_df)/len(oct2025)*100:.1f}%)")

# ==============================================================================
# STEP 5: Statistical Analysis
# ==============================================================================

print("\n" + "="*70)
print("STATISTICAL VALIDATION")
print("="*70)

# Drop rows with missing PHFSI (can't validate without PHFSI scores)
validation_df_complete = validation_df.dropna(subset=['phfsi_score']).copy()
print(f"\n   After dropping NaN PHFSI: {len(validation_df_complete)} entities with complete data")

if len(validation_df_complete) < 3:
    print(f"\n⚠️ Only {len(validation_df_complete)} entities with non-missing PHFSI - insufficient for statistical analysis")
    print("   Minimum recommended: 5 entities for correlation analysis")
    print("   Proceeding with descriptive analysis only...")

    # Save what we have
    validation_df.to_csv(OUTPUT_DIR / "results" / "validation" / "october2025_validation_data.csv", index=False)

    print("\n" + "="*70)
    print("VALIDATION INCOMPLETE - INSUFFICIENT MATCHES")
    print("="*70)
    exit(1)

# Correlation Analysis
print(f"\n1. Correlation Analysis (N={len(validation_df_complete)}):")
print("   " + "-"*66)

pearson_r, pearson_p = pearsonr(validation_df_complete['phfsi_score'], validation_df_complete['allocation_millions'])
spearman_r, spearman_p = spearmanr(validation_df_complete['phfsi_score'], validation_df_complete['allocation_millions'])

print(f"   Pearson correlation:  r = {pearson_r:7.3f} (p = {pearson_p:.4f})")
print(f"   Spearman correlation: ρ = {spearman_r:7.3f} (p = {spearman_p:.4f})")

print(f"\n   Framework prediction: Lower PHFSI → Higher allocation (negative r)")

if pearson_r < 0:
    if pearson_p < 0.05:
        print(f"   ✓✓ STRONG VALIDATION: Significant negative correlation (p < 0.05)")
        validation_strength = "Strong"
    elif pearson_p < 0.10:
        print(f"   ✓  MODERATE VALIDATION: Negative correlation (p < 0.10)")
        validation_strength = "Moderate"
    else:
        print(f"   ~  WEAK VALIDATION: Negative correlation not significant (p = {pearson_p:.3f})")
        print(f"      Note: Small sample (N={len(validation_df_complete)}) limits statistical power")
        validation_strength = "Weak"
else:
    print(f"   ✗  Positive correlation contradicts framework")
    print(f"      Possible explanations:")
    print(f"        - Measurement error from ULS-ACES aggregation")
    print(f"        - Political allocation mechanisms override distress signals")
    print(f"        - Sample selection bias (only certain hospital types matched)")
    validation_strength = "Contradictory"

# Regression Analysis (if N >= 5)
if len(validation_df_complete) >= 5:
    print(f"\n2. Regression Analysis:")
    print("   " + "-"*66)

    # Simple regression: allocation ~ PHFSI
    X = validation_df_complete[['phfsi_score']].values
    y = validation_df_complete['allocation_millions'].values

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)

    print(f"   Model: Allocation (€M) = {model.intercept_:.2f} + {model.coef_[0]:.2f} × PHFSI")
    print(f"   R² = {r2:.3f} ({r2*100:.1f}% of variance explained)")

    # Interpret slope
    if model.coef_[0] < 0:
        print(f"   → Each 0.1-point decrease in PHFSI predicts €{abs(model.coef_[0]*0.1):.1f}M higher allocation")
    else:
        print(f"   → Each 0.1-point increase in PHFSI predicts €{model.coef_[0]*0.1:.1f}M higher allocation")

    regression_results = {
        'intercept': model.intercept_,
        'coefficient': model.coef_[0],
        'r_squared': r2
    }
else:
    print(f"\n2. Regression Analysis: Skipped (N < 5)")
    regression_results = None

# Quartile Analysis (if N >= 8)
if len(validation_df_complete) >= 8:
    print(f"\n3. Quartile Analysis:")
    print("   " + "-"*66)

    validation_df_complete['allocation_quartile'] = pd.qcut(
        validation_df_complete['allocation_millions'],
        q=4,
        labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)']
    )

    quartile_means = validation_df_complete.groupby('allocation_quartile', observed=True)['phfsi_score'].agg(['mean', 'count'])

    print("   Mean PHFSI by Allocation Quartile:")
    for quartile, row in quartile_means.iterrows():
        print(f"     {quartile:12s}: PHFSI = {row['mean']:.3f} (n={row['count']:.0f})")

    print(f"\n   Expected: Lower PHFSI in higher allocation quartiles")
    if quartile_means.loc['Q1 (Low)', 'mean'] > quartile_means.loc['Q4 (High)', 'mean']:
        print(f"   ✓ Q1 mean ({quartile_means.loc['Q1 (Low)', 'mean']:.3f}) > Q4 mean ({quartile_means.loc['Q4 (High)', 'mean']:.3f}) - consistent with framework")
    else:
        print(f"   ✗ Pattern does not support framework")

# ==============================================================================
# STEP 6: Create Validation Figure
# ==============================================================================

print("\n" + "="*70)
print("CREATING VALIDATION FIGURE")
print("="*70)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Panel A: Scatter plot with trend line
ax1 = axes[0]

ax1.scatter(validation_df_complete['phfsi_score'], validation_df_complete['allocation_millions'],
           s=150, alpha=0.7, c='steelblue', edgecolors='black', linewidth=1.5)

# Add entity labels
for _, row in validation_df_complete.iterrows():
    label = row['uls_entity'][:30]
    ax1.annotate(label, (row['phfsi_score'], row['allocation_millions']),
                fontsize=7, alpha=0.8, xytext=(3, 3), textcoords='offset points')

# Trend line
if len(validation_df_complete) >= 2:
    z = np.polyfit(validation_df_complete['phfsi_score'], validation_df_complete['allocation_millions'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(validation_df_complete['phfsi_score'].min(),
                        validation_df_complete['phfsi_score'].max(), 100)
    ax1.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2,
            label=f'Trend: r={pearson_r:.3f}, p={pearson_p:.3f}')
    ax1.legend(loc='best')

ax1.set_xlabel(f'{validation_year} PHFSI Score', fontsize=12, fontweight='bold')
ax1.set_ylabel('October 2025 Capital Allocation (€M)', fontsize=12, fontweight='bold')
ax1.set_title('Panel A: PHFSI vs Allocation Amount', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3, linestyle='--')

# Stats box
stats_text = f'N = {len(validation_df_complete)}\nPearson r = {pearson_r:.3f}\np = {pearson_p:.3f}'
if pearson_p < 0.05:
    stats_text += '\n(Significant)'
elif pearson_p < 0.10:
    stats_text += '\n(Marginal)'

box_props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)
ax1.text(0.05, 0.95, stats_text, transform=ax1.transAxes, fontsize=10,
        verticalalignment='top', bbox=box_props)

# Panel B: Box plot by quartile (if enough data)
ax2 = axes[1]

if len(validation_df_complete) >= 8 and 'allocation_quartile' in validation_df_complete.columns:
    validation_df_complete.boxplot(column='phfsi_score', by='allocation_quartile', ax=ax2)
    ax2.set_xlabel('Allocation Quartile', fontsize=12, fontweight='bold')
    ax2.set_ylabel(f'{validation_year} PHFSI Score', fontsize=12, fontweight='bold')
    ax2.set_title('Panel B: PHFSI Distribution by Allocation', fontsize=13, fontweight='bold')
    plt.suptitle('')  # Remove default title
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
else:
    # Alternative: histogram of PHFSI scores
    ax2.hist(validation_df_complete['phfsi_score'], bins=min(10, len(validation_df_complete)),
            alpha=0.7, color='steelblue', edgecolor='black')
    ax2.set_xlabel(f'{validation_year} PHFSI Score', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax2.set_title('Panel B: PHFSI Distribution (Validation Sample)', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')

plt.tight_layout()

# Save figure
fig_path = OUTPUT_DIR / "figures" / "main" / "figure5_october2025_validation.pdf"
fig_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(fig_path, dpi=300, bbox_inches='tight')

print(f"\n✓ Figure saved: {fig_path}")

# ==============================================================================
# STEP 7: Create Validation Table
# ==============================================================================

print("\n" + "="*70)
print("CREATING VALIDATION TABLE")
print("="*70)

# Sort by allocation amount (descending)
validation_sorted = validation_df_complete.sort_values('allocation_millions', ascending=False).reset_index(drop=True)
validation_sorted['actual_rank'] = range(1, len(validation_sorted) + 1)

# Predicted rank based on PHFSI (lower PHFSI = higher predicted allocation = lower rank number)
validation_sorted['predicted_rank'] = validation_sorted['phfsi_score'].rank(method='average')

# Create LaTeX table
latex_lines = [
    "\\begin{tabular}{lcccc}",
    "\\toprule",
    "ULS Entity & Allocation (€M) & PHFSI & Predicted Rank & Actual Rank \\\\",
    "\\midrule"
]

for _, row in validation_sorted.iterrows():
    entity = row['uls_entity'][:40]
    alloc = f"{row['allocation_millions']:.1f}"
    phfsi = f"{row['phfsi_score']:.3f}"
    pred_rank = int(row['predicted_rank'])
    actual_rank = int(row['actual_rank'])

    # Check if prediction matches (within ±2 ranks tolerance)
    match = "\\checkmark" if abs(pred_rank - actual_rank) <= 2 else ""

    latex_lines.append(f"{entity} & {alloc} & {phfsi} & {pred_rank} & {actual_rank} {match} \\\\")

latex_lines.extend([
    "\\midrule",
    f"\\multicolumn{{5}}{{l}}{{\\textit{{Validation Statistics (N={len(validation_df_complete)}):}}}} \\\\",
    f"\\multicolumn{{5}}{{l}}{{Pearson r = {pearson_r:.3f} (p = {pearson_p:.3f}), Spearman ρ = {spearman_r:.3f} (p = {spearman_p:.3f})}} \\\\",
])

if regression_results:
    latex_lines.append(
        f"\\multicolumn{{5}}{{l}}{{Regression: R² = {regression_results['r_squared']:.3f}, β = {regression_results['coefficient']:.2f}}} \\\\"
    )

latex_lines.extend([
    "\\bottomrule",
    "\\end{tabular}"
])

table_path = OUTPUT_DIR / "tables" / "main" / "table6_october2025_validation.tex"
table_path.parent.mkdir(parents=True, exist_ok=True)

with open(table_path, 'w') as f:
    f.write('\n'.join(latex_lines))

print(f"\n✓ Table saved: {table_path}")

# ==============================================================================
# STEP 8: Save Detailed Results
# ==============================================================================

results_path = OUTPUT_DIR / "results" / "validation" / "october2025_validation_results.csv"
results_path.parent.mkdir(parents=True, exist_ok=True)

validation_df.to_csv(results_path, index=False)

print(f"\n✓ Detailed results saved: {results_path}")

# ==============================================================================
# FINAL SUMMARY
# ==============================================================================

print("\n" + "="*70)
print("VALIDATION COMPLETE")
print("="*70)

print(f"\nKEY FINDINGS:")
print(f"  Matched allocations: {len(validation_df)} of {len(oct2025)} ({len(validation_df)/len(oct2025)*100:.1f}%)")
print(f"  Validation year: {validation_year}")
print(f"  Correlation: r = {pearson_r:.3f} (p = {pearson_p:.3f})")

if pearson_r < 0 and pearson_p < 0.05:
    print(f"  ✓✓ FRAMEWORK VALIDATED: Significant negative correlation")
    interpretation = "Strong validation"
elif pearson_r < 0 and pearson_p < 0.10:
    print(f"  ✓ FRAMEWORK CONSISTENT: Negative correlation (marginal significance)")
    interpretation = "Moderate validation"
elif pearson_r < 0:
    print(f"  ~ Framework consistent but not statistically significant (small N={len(validation_df)})")
    interpretation = "Weak validation (insufficient power)"
else:
    print(f"  ⚠ Positive correlation observed - framework not validated")
    interpretation = "Not validated"

print(f"\nINTERPRETATION: {interpretation}")

if len(validation_df) < 10:
    print(f"\nLIMITATION: Small sample (N={len(validation_df)}) limits statistical power.")
    print(f"  - Entity renaming prevents matching most 2024 ULS allocations to {validation_year} PHFSI")
    print(f"  - ULS allocations include ACES (primary care) not captured in hospital PHFSI")
    print(f"  - Measurement error attenuates correlations toward zero")

print(f"\nOUTPUT FILES:")
print(f"  1. {fig_path}")
print(f"  2. {table_path}")
print(f"  3. {results_path}")

print(f"\nNEXT STEPS:")
print(f"  1. Review figure and table quality")
print(f"  2. Update Results section 4.6 with quantitative validation")
print(f"  3. Update Discussion section with honest interpretation")

print("\n" + "="*70)
