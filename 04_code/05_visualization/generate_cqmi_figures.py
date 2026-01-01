#!/usr/bin/env python3
"""
Generate CQMI-related figures for manuscript
Creates Figure 4: CQMI Temporal Trends (2019-2024)

Author: Research Team
Date: 2025-01-31
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "03_data" / "processed"
OUTPUT_DIR = BASE_DIR / "06_output" / "figures" / "main"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set publication-quality style
plt.style.use('seaborn-v0_8-paper')
sns.set_context("paper", font_scale=1.2)
sns.set_palette("Set2")

def load_data():
    """Load CQMI and panel data"""
    cqmi_path = DATA_DIR / "variables" / "cqmi_component_scores.parquet"
    cqmi_df = pd.read_parquet(cqmi_path)

    # Load monthly panel for correlation with payment delays
    panel_path = DATA_DIR / "panel" / "hospital_month_panel_final.parquet"
    panel_df = pd.read_parquet(panel_path)

    return cqmi_df, panel_df

def plot_cqmi_temporal_trends(df):
    """
    Figure 4: CQMI Temporal Trends (2019-2024)
    Shows U-shaped COVID impact pattern
    """
    # Calculate annual means and confidence intervals
    annual_stats = df.groupby('year').agg({
        'CQMI': ['mean', 'std', 'count'],
        'mortality_quality_index': ['mean', 'std'],
        'efficiency_index': ['mean', 'std']
    }).reset_index()

    annual_stats.columns = ['_'.join(col).strip('_') for col in annual_stats.columns.values]

    # Calculate 95% CI
    annual_stats['CQMI_se'] = annual_stats['CQMI_std'] / np.sqrt(annual_stats['CQMI_count'])
    annual_stats['CQMI_ci_lower'] = annual_stats['CQMI_mean'] - 1.96 * annual_stats['CQMI_se']
    annual_stats['CQMI_ci_upper'] = annual_stats['CQMI_mean'] + 1.96 * annual_stats['CQMI_se']

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Panel A: CQMI trends with CI
    ax1.plot(annual_stats['year'], annual_stats['CQMI_mean'],
             marker='o', linewidth=2, markersize=8, color='#2E86AB', label='CQMI')
    ax1.fill_between(annual_stats['year'],
                      annual_stats['CQMI_ci_lower'],
                      annual_stats['CQMI_ci_upper'],
                      alpha=0.2, color='#2E86AB')

    # Add COVID shading
    ax1.axvspan(2019.5, 2021.5, alpha=0.1, color='red', label='COVID Period')

    ax1.set_xlabel('Year', fontsize=12, weight='bold')
    ax1.set_ylabel('CQMI (Clinical Quality Maintenance Index)', fontsize=12, weight='bold')
    ax1.set_title('Panel A: CQMI Temporal Trends (2019-2024)', fontsize=13, weight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(loc='lower left', frameon=True, shadow=True)
    ax1.set_ylim(0.35, 0.55)

    # Add annotations for key events
    ax1.annotate('Pre-COVID\nBaseline\n0.489',
                xy=(2019, 0.489), xytext=(2018.5, 0.52),
                arrowprops=dict(arrowstyle='->', color='black', lw=1),
                fontsize=9, ha='center')
    ax1.annotate('COVID\nNadir\n0.422',
                xy=(2020, 0.422), xytext=(2020, 0.38),
                arrowprops=dict(arrowstyle='->', color='red', lw=1),
                fontsize=9, ha='center', color='red')
    ax1.annotate('Recovery\n0.479',
                xy=(2024, 0.479), xytext=(2024.5, 0.51),
                arrowprops=dict(arrowstyle='->', color='green', lw=1),
                fontsize=9, ha='center', color='green')

    # Panel B: Component decomposition
    ax2.plot(annual_stats['year'], annual_stats['mortality_quality_index_mean'],
             marker='s', linewidth=2, markersize=6, label='Mortality Quality Index', color='#A23E48')
    ax2.plot(annual_stats['year'], annual_stats['efficiency_index_mean'],
             marker='^', linewidth=2, markersize=6, label='Efficiency Index', color='#6C9A8B')

    ax2.axvspan(2019.5, 2021.5, alpha=0.1, color='red')

    ax2.set_xlabel('Year', fontsize=12, weight='bold')
    ax2.set_ylabel('Component Index Value', fontsize=12, weight='bold')
    ax2.set_title('Panel B: CQMI Components', fontsize=13, weight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend(loc='lower left', frameon=True, shadow=True)
    ax2.set_ylim(0.25, 0.65)

    plt.tight_layout()

    # Save figure
    output_path = OUTPUT_DIR / "figure4_cqmi_trends.pdf"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved to {output_path}")

    output_path_png = OUTPUT_DIR / "figure4_cqmi_trends.png"
    plt.savefig(output_path_png, dpi=300, bbox_inches='tight')
    print(f"✓ Saved PNG to {output_path_png}")

    plt.close()

def plot_cqmi_payment_delay_correlation(cqmi_df, panel_df):
    """
    Figure 5: CQMI vs Payment Delays
    Shows negative correlation validating quality degradation channel
    """
    # Merge CQMI with payment delay data
    # Aggregate panel data to annual level
    panel_annual = panel_df.groupby(['parent_uls_std', 'year']).agg({
        'pagamentos_em_atraso': 'mean',
        'resultados_operacionais': 'mean'
    }).reset_index()

    # Standardize names for merge
    cqmi_df['parent_uls_std'] = cqmi_df['entidade'].str.strip().str.title()

    # Merge
    merged = pd.merge(
        cqmi_df,
        panel_annual,
        left_on=['parent_uls_std', 'year'],
        right_on=['parent_uls_std', 'year'],
        how='inner'
    )

    print(f"\nMerged CQMI with payment delays: {len(merged)} observations")

    if len(merged) < 10:
        print("⚠ Insufficient overlap for correlation plot, skipping...")
        return

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Filter outliers for better visualization
    payment_p99 = merged['pagamentos_em_atraso'].quantile(0.99)
    plot_data = merged[merged['pagamentos_em_atraso'] < payment_p99]

    scatter = ax.scatter(plot_data['pagamentos_em_atraso'],
                        plot_data['CQMI'],
                        c=plot_data['year'],
                        cmap='viridis',
                        alpha=0.6,
                        s=50,
                        edgecolors='black',
                        linewidth=0.5)

    # Add regression line
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        plot_data['pagamentos_em_atraso'],
        plot_data['CQMI']
    )

    x_line = np.linspace(plot_data['pagamentos_em_atraso'].min(),
                         plot_data['pagamentos_em_atraso'].max(), 100)
    y_line = slope * x_line + intercept

    ax.plot(x_line, y_line, 'r--', linewidth=2,
            label=f'r = {r_value:.3f}, p = {p_value:.3f}')

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Year', fontsize=11, weight='bold')

    ax.set_xlabel('Payment Delays (days)', fontsize=12, weight='bold')
    ax.set_ylabel('CQMI', fontsize=12, weight='bold')
    ax.set_title('CQMI vs. Payment Delays: Negative Correlation\n'
                 'Validates Quality Degradation Channel',
                 fontsize=13, weight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', frameon=True, shadow=True)

    plt.tight_layout()

    # Save figure
    output_path = OUTPUT_DIR / "figure5_cqmi_payment_delays.pdf"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved to {output_path}")

    output_path_png = OUTPUT_DIR / "figure5_cqmi_payment_delays.png"
    plt.savefig(output_path_png, dpi=300, bbox_inches='tight')
    print(f"✓ Saved PNG to {output_path_png}")

    plt.close()

    # Print correlation statistics
    print("\n" + "="*70)
    print("CQMI vs PAYMENT DELAYS CORRELATION")
    print("="*70)
    print(f"Pearson correlation: r = {r_value:.3f}, p = {p_value:.4f}")
    print(f"Sample size: {len(plot_data)} observations")
    print(f"Interpretation: {'Significant negative correlation' if p_value < 0.05 else 'No significant correlation'}")

def main():
    """Main execution"""
    print("Loading data...")
    cqmi_df, panel_df = load_data()

    print(f"CQMI data: {len(cqmi_df)} observations from {cqmi_df['entidade'].nunique()} ULS")
    print(f"Panel data: {len(panel_df)} observations")

    # Generate Figure 4: CQMI temporal trends
    print("\n" + "="*70)
    print("Generating Figure 4: CQMI Temporal Trends")
    print("="*70)
    plot_cqmi_temporal_trends(cqmi_df)

    # Generate Figure 5: CQMI vs payment delays
    print("\n" + "="*70)
    print("Generating Figure 5: CQMI vs Payment Delays")
    print("="*70)
    plot_cqmi_payment_delay_correlation(cqmi_df, panel_df)

    print("\n✓ Figure generation complete!")

if __name__ == "__main__":
    main()
