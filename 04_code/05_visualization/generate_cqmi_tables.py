#!/usr/bin/env python3
"""
Generate CQMI-related tables for manuscript
Creates Table 3 (CQMI Summary Statistics) for the main paper

Author: Research Team
Date: 2025-01-31
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "03_data" / "processed"
OUTPUT_DIR = BASE_DIR / "06_output" / "tables" / "main"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_cqmi_data():
    """Load CQMI component scores"""
    cqmi_path = DATA_DIR / "variables" / "cqmi_component_scores.parquet"
    return pd.read_parquet(cqmi_path)

def calculate_summary_stats(df, var_name):
    """Calculate summary statistics for a variable"""
    return {
        'N': df[var_name].notna().sum(),
        'Mean': df[var_name].mean(),
        'SD': df[var_name].std(),
        'Min': df[var_name].min(),
        'P25': df[var_name].quantile(0.25),
        'Median': df[var_name].median(),
        'P75': df[var_name].quantile(0.75),
        'Max': df[var_name].max()
    }

def generate_cqmi_summary_table(df):
    """Generate Table 3: CQMI Summary Statistics by Period"""

    # Define periods
    df['period'] = pd.cut(df['year'],
                          bins=[2018, 2020, 2022, 2025],
                          labels=['Pre-COVID (2019)', 'COVID (2020-2021)', 'Post-COVID (2022-2024)'],
                          include_lowest=True)

    # Variables to summarize
    variables = ['CQMI', 'mortality_quality_index', 'efficiency_index',
                 'taxa_mortalidade', 'dias_internamento']
    var_labels = {
        'CQMI': 'CQMI (Clinical Quality Maintenance Index)',
        'mortality_quality_index': 'Mortality Quality Index',
        'efficiency_index': 'Efficiency Index',
        'taxa_mortalidade': 'Mortality Rate (\%)',
        'dias_internamento': 'Average Length of Stay (days)'
    }

    # Create LaTeX table
    latex = []
    latex.append(r'\begin{table}[htbp]')
    latex.append(r'\centering')
    latex.append(r'\caption{Clinical Quality Maintenance Index (CQMI) Summary Statistics}')
    latex.append(r'\label{tab:cqmi_summary}')
    latex.append(r'\begin{tabular}{lcccccccc}')
    latex.append(r'\hline\hline')
    latex.append(r'Variable & N & Mean & SD & Min & P25 & Median & P75 & Max \\')
    latex.append(r'\hline')

    # Add all periods
    latex.append(r'\multicolumn{9}{l}{\textit{All Periods (2019-2024)}} \\')
    for var in variables:
        stats = calculate_summary_stats(df, var)
        label = var_labels.get(var, var)
        latex.append(f"{label} & {stats['N']:.0f} & {stats['Mean']:.3f} & {stats['SD']:.3f} & "
                    f"{stats['Min']:.3f} & {stats['P25']:.3f} & {stats['Median']:.3f} & "
                    f"{stats['P75']:.3f} & {stats['Max']:.3f} \\\\")
    latex.append(r'\\')

    # Add by period
    for period in ['Pre-COVID (2019)', 'COVID (2020-2021)', 'Post-COVID (2022-2024)']:
        period_df = df[df['period'] == period]
        if len(period_df) == 0:
            continue

        latex.append(f"\\multicolumn{{9}}{{l}}{{\\textit{{{period}}}}} \\\\")

        for var in variables:
            stats = calculate_summary_stats(period_df, var)
            label = var_labels.get(var, var)
            latex.append(f"{label} & {stats['N']:.0f} & {stats['Mean']:.3f} & {stats['SD']:.3f} & "
                        f"{stats['Min']:.3f} & {stats['P25']:.3f} & {stats['Median']:.3f} & "
                        f"{stats['P75']:.3f} & {stats['Max']:.3f} \\\\")
        latex.append(r'\\')

    latex.append(r'\hline\hline')
    latex.append(r'\end{tabular}')
    latex.append(r'\begin{tablenotes}')
    latex.append(r'\small')
    latex.append(r'\item \textit{Notes:} CQMI calculated from quality metrics aggregated by ULS. '
                r'Mortality Quality Index = inverse of mortality rate. '
                r'Efficiency Index = inverse of average length of stay. '
                r'CQMI = mean of normalized Mortality Quality Index and Efficiency Index. '
                r'Sample includes 43 ULS entities observed annually from 2019-2024 (258 ULS-period observations). '
                r'Pre-COVID: 2019; COVID: 2020-2021; Post-COVID: 2022-2024.')
    latex.append(r'\end{tablenotes}')
    latex.append(r'\end{table}')

    return '\n'.join(latex)

def generate_cqmi_temporal_table(df):
    """Generate supplementary table: CQMI by year"""

    latex = []
    latex.append(r'\begin{table}[htbp]')
    latex.append(r'\centering')
    latex.append(r'\caption{CQMI Temporal Trends (2019-2024)}')
    latex.append(r'\label{tab:cqmi_temporal}')
    latex.append(r'\begin{tabular}{lccccccc}')
    latex.append(r'\hline\hline')
    latex.append(r'Metric & 2019 & 2020 & 2021 & 2022 & 2023 & 2024 & Overall \\')
    latex.append(r'\hline')

    years = [2019, 2020, 2021, 2022, 2023, 2024]
    metrics = {
        'CQMI': 'CQMI',
        'mortality_quality_index': 'Mortality Quality Index',
        'efficiency_index': 'Efficiency Index'
    }

    for var, label in metrics.items():
        row = [label]
        for year in years:
            year_data = df[df['year'] == year][var]
            if len(year_data) > 0:
                row.append(f"{year_data.mean():.3f}")
            else:
                row.append("--")
        # Overall
        row.append(f"{df[var].mean():.3f}")
        latex.append(' & '.join(row) + r' \\')

    latex.append(r'\\')
    latex.append(r'\multicolumn{8}{l}{\textit{Standard Deviations}} \\')

    for var, label in metrics.items():
        row = [label]
        for year in years:
            year_data = df[df['year'] == year][var]
            if len(year_data) > 0:
                row.append(f"({year_data.std():.3f})")
            else:
                row.append("--")
        row.append(f"({df[var].std():.3f})")
        latex.append(' & '.join(row) + r' \\')

    latex.append(r'\hline\hline')
    latex.append(r'\end{tabular}')
    latex.append(r'\begin{tablenotes}')
    latex.append(r'\small')
    latex.append(r'\item \textit{Notes:} Mean values with standard deviations in parentheses. '
                r'CQMI exhibits U-shaped pattern: decline during COVID (2020-2021) followed by recovery (2022-2024).')
    latex.append(r'\end{tablenotes}')
    latex.append(r'\end{table}')

    return '\n'.join(latex)

def main():
    """Main execution"""
    print("Loading CQMI data...")
    df = load_cqmi_data()

    print(f"Loaded {len(df)} observations from {df['entidade'].nunique()} ULS entities")
    print(f"Years: {sorted(df['year'].unique())}")

    # Generate summary statistics table
    print("\nGenerating CQMI summary statistics table...")
    summary_table = generate_cqmi_summary_table(df)

    summary_path = OUTPUT_DIR / "table3_cqmi_summary.tex"
    with open(summary_path, 'w') as f:
        f.write(summary_table)
    print(f"✓ Saved to {summary_path}")

    # Generate temporal trends table
    print("\nGenerating CQMI temporal trends table...")
    temporal_table = generate_cqmi_temporal_table(df)

    temporal_path = OUTPUT_DIR / "table4_cqmi_temporal.tex"
    with open(temporal_path, 'w') as f:
        f.write(temporal_table)
    print(f"✓ Saved to {temporal_path}")

    # Display summary statistics
    print("\n" + "="*70)
    print("CQMI SUMMARY STATISTICS")
    print("="*70)
    print(f"\nTotal observations: {len(df)}")
    print(f"ULS entities: {df['entidade'].nunique()}")
    print(f"\nCQMI Statistics:")
    print(f"  Mean: {df['CQMI'].mean():.3f}")
    print(f"  SD: {df['CQMI'].std():.3f}")
    print(f"  Range: [{df['CQMI'].min():.3f}, {df['CQMI'].max():.3f}]")

    print(f"\nBy Year:")
    year_stats = df.groupby('year')['CQMI'].agg(['count', 'mean', 'std'])
    print(year_stats)

    print("\n✓ Table generation complete!")

if __name__ == "__main__":
    main()
