"""
Descriptive Statistics for PHFSI Analysis

Generates publication-quality descriptive statistics tables for the paper:
- Table 1: Summary Statistics (by period)
- Table 2: PHFSI Distribution and Clusters

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
OUTPUT_DIR = PROJECT_ROOT / "06_output" / "tables" / "main"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class DescriptiveStatisticsGenerator:
    """
    Generates descriptive statistics tables for PHFSI analysis.
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

        # Merge PHFSI scores with panel for full data
        # Include all component columns
        merge_cols = ['entidade', 'year', 'phfsi', 'phfsi_cluster']
        for col in ['ossr', 'spi', 'lrr', 'tlr', 'cqmi']:
            if col in self.phfsi_scores.columns:
                merge_cols.append(col)

        self.panel = self.panel.merge(
            self.phfsi_scores[merge_cols],
            on=['entidade', 'year'],
            how='left'
        )

    def create_period_labels(self):
        """Add period labels (pre-COVID, COVID, post-COVID)."""
        logger.info("Creating period labels...")

        self.panel['period'] = 'Post-COVID (2022-2024)'
        self.panel.loc[self.panel['year'].between(2020, 2021), 'period'] = 'COVID (2020-2021)'
        self.panel.loc[self.panel['year'] < 2020, 'period'] = 'Pre-COVID (2017-2019)'

    def filter_hospitals_only(self):
        """Filter to actual hospitals (exclude administrative entities)."""
        logger.info("Filtering to hospitals only...")

        # Identify hospital keywords
        hospital_keywords = [
            'Hospital', 'Hospitalar', 'Unidade Local de Saúde',
            'ULS', 'IPO', 'Instituto Português'
        ]

        # Filter
        hospital_mask = self.panel['entidade'].str.contains(
            '|'.join(hospital_keywords),
            case=False,
            na=False
        )

        logger.info(f"Total entities: {self.panel['entidade'].nunique()}")
        logger.info(f"Hospital entities: {self.panel.loc[hospital_mask, 'entidade'].nunique()}")

        self.panel['is_hospital'] = hospital_mask

    def generate_summary_statistics_table(self):
        """
        Generate Table 1: Summary Statistics by Period

        Variables:
        - PHFSI and components (OSSR, SPI, LRR, TLR)
        - Key financial metrics (revenues, expenses, debt)
        - Control variables (GDP, unemployment)
        """
        logger.info("Generating Table 1: Summary Statistics...")

        # Filter to hospitals with data
        df = self.panel[
            (self.panel['is_hospital'] == True) &
            (self.panel['phfsi'].notna())
        ].copy()

        logger.info(f"Analyzing {len(df)} hospital-year observations")

        # Define variables for table
        variables = {
            # PHFSI and components
            'phfsi': 'PHFSI',
            'ossr': 'OSSR',
            'spi': 'SPI',
            'lrr': 'LRR',
            'tlr': 'TLR',
            # Financial metrics (in millions)
            'rendimentos_operacionais': 'Operating Revenue (€M)',
            'gastos_operacionais': 'Operating Expenses (€M)',
            'resultado_liquido': 'Net Result (€M)',
            'divida_total_fornecedores_externos': 'Total Supplier Debt (€M)',
            'divida_vencida_fornecedores_externos': 'Overdue Debt (€M)',
            'pagamentos_em_atraso': 'Payment Delays (days)',
            # Macro controls
            'gdp_per_capita_eur': 'GDP per Capita (€)',
            'gdp_growth_rate_pct': 'GDP Growth Rate (%)',
        }

        # Convert financial variables to millions
        for col in ['rendimentos_operacionais', 'gastos_operacionais', 'resultado_liquido',
                    'divida_total_fornecedores_externos', 'divida_vencida_fornecedores_externos']:
            if col in df.columns:
                df[col] = df[col] / 1000  # Convert to thousands (€k)

        # Calculate statistics by period
        results = []

        for period in ['Pre-COVID (2017-2019)', 'COVID (2020-2021)', 'Post-COVID (2022-2024)']:
            period_df = df[df['period'] == period]

            for var_col, var_name in variables.items():
                if var_col in period_df.columns:
                    stats = {
                        'Variable': var_name,
                        'Period': period,
                        'N': period_df[var_col].notna().sum(),
                        'Mean': period_df[var_col].mean(),
                        'SD': period_df[var_col].std(),
                        'Min': period_df[var_col].min(),
                        'P25': period_df[var_col].quantile(0.25),
                        'Median': period_df[var_col].median(),
                        'P75': period_df[var_col].quantile(0.75),
                        'Max': period_df[var_col].max(),
                    }
                    results.append(stats)

        # Create DataFrame
        table1 = pd.DataFrame(results)

        # Format numbers
        table1['Mean'] = table1['Mean'].round(3)
        table1['SD'] = table1['SD'].round(3)
        table1['Min'] = table1['Min'].round(3)
        table1['P25'] = table1['P25'].round(3)
        table1['Median'] = table1['Median'].round(3)
        table1['P75'] = table1['P75'].round(3)
        table1['Max'] = table1['Max'].round(3)

        # Save as CSV
        csv_path = OUTPUT_DIR / "table1_summary_statistics.csv"
        table1.to_csv(csv_path, index=False)
        logger.info(f"Table 1 saved to: {csv_path}")

        # Generate LaTeX version
        self.generate_latex_table1(table1)

        return table1

    def generate_latex_table1(self, table1):
        """Generate LaTeX formatted version of Table 1."""
        logger.info("Generating LaTeX version of Table 1...")

        # Pivot to wide format (periods as columns)
        latex_parts = []
        latex_parts.append("\\begin{table}[htbp]")
        latex_parts.append("\\centering")
        latex_parts.append("\\caption{Summary Statistics by Period}")
        latex_parts.append("\\label{tab:summary_stats}")
        latex_parts.append("\\begin{tabular}{lcccccccc}")
        latex_parts.append("\\hline\\hline")
        latex_parts.append("Variable & N & Mean & SD & Min & P25 & Median & P75 & Max \\\\")
        latex_parts.append("\\hline")

        # Group by variable and period
        for period in ['Pre-COVID (2017-2019)', 'COVID (2020-2021)', 'Post-COVID (2022-2024)']:
            latex_parts.append(f"\\multicolumn{{9}}{{l}}{{\\textit{{{period}}}}} \\\\")

            period_data = table1[table1['Period'] == period]

            for _, row in period_data.iterrows():
                line = f"{row['Variable']} & {row['N']:.0f} & {row['Mean']:.3f} & {row['SD']:.3f} & "
                line += f"{row['Min']:.3f} & {row['P25']:.3f} & {row['Median']:.3f} & "
                line += f"{row['P75']:.3f} & {row['Max']:.3f} \\\\"
                latex_parts.append(line)

            latex_parts.append("\\\\")

        latex_parts.append("\\hline\\hline")
        latex_parts.append("\\end{tabular}")
        latex_parts.append("\\begin{tablenotes}")
        latex_parts.append("\\small")
        latex_parts.append("\\item Notes: Financial variables in thousands of euros (€k). ")
        latex_parts.append("Sample restricted to hospital entities with available PHFSI scores. ")
        latex_parts.append("Pre-COVID: 2017-2019; COVID: 2020-2021; Post-COVID: 2022-2024.")
        latex_parts.append("\\end{tablenotes}")
        latex_parts.append("\\end{table}")

        # Save LaTeX
        tex_path = OUTPUT_DIR / "table1_summary_statistics.tex"
        with open(tex_path, 'w') as f:
            f.write('\n'.join(latex_parts))

        logger.info(f"Table 1 LaTeX saved to: {tex_path}")

    def generate_phfsi_clusters_table(self):
        """
        Generate Table 2: PHFSI Distribution and Clusters

        Shows:
        - Number of hospitals by cluster
        - Average PHFSI and components by cluster
        - Average debt and subsidies by cluster
        """
        logger.info("Generating Table 2: PHFSI Clusters...")

        # Filter to hospitals with PHFSI
        df = self.panel[
            (self.panel['is_hospital'] == True) &
            (self.panel['phfsi'].notna())
        ].copy()

        # Group by cluster
        cluster_stats = df.groupby('phfsi_cluster').agg({
            'entidade': 'count',  # Count observations
            'phfsi': ['mean', 'std', 'min', 'max'],
            'ossr': 'mean',
            'spi': 'mean',
            'lrr': 'mean',
            'tlr': 'mean',
            'divida_total_fornecedores_externos': 'mean',
            'divida_vencida_fornecedores_externos': 'mean',
            'pagamentos_em_atraso': 'mean',
            'rendimentos_operacionais': 'mean',
        }).round(3)

        # Flatten columns
        cluster_stats.columns = ['_'.join(col).strip() for col in cluster_stats.columns.values]
        cluster_stats = cluster_stats.reset_index()

        # Rename columns
        cluster_stats = cluster_stats.rename(columns={
            'entidade_count': 'N_obs',
            'phfsi_mean': 'PHFSI_Mean',
            'phfsi_std': 'PHFSI_SD',
            'phfsi_min': 'PHFSI_Min',
            'phfsi_max': 'PHFSI_Max',
            'ossr_mean': 'OSSR',
            'spi_mean': 'SPI',
            'lrr_mean': 'LRR',
            'tlr_mean': 'TLR',
            'divida_total_fornecedores_externos_mean': 'Avg_Total_Debt',
            'divida_vencida_fornecedores_externos_mean': 'Avg_Overdue_Debt',
            'pagamentos_em_atraso_mean': 'Avg_Payment_Days',
            'rendimentos_operacionais_mean': 'Avg_Revenue',
        })

        # Save as CSV
        csv_path = OUTPUT_DIR / "table2_phfsi_clusters.csv"
        cluster_stats.to_csv(csv_path, index=False)
        logger.info(f"Table 2 saved to: {csv_path}")

        # Generate LaTeX version
        self.generate_latex_table2(cluster_stats)

        return cluster_stats

    def generate_latex_table2(self, table2):
        """Generate LaTeX formatted version of Table 2."""
        logger.info("Generating LaTeX version of Table 2...")

        latex_parts = []
        latex_parts.append("\\begin{table}[htbp]")
        latex_parts.append("\\centering")
        latex_parts.append("\\caption{PHFSI Distribution by Cluster}")
        latex_parts.append("\\label{tab:phfsi_clusters}")
        latex_parts.append("\\begin{tabular}{lcccccccc}")
        latex_parts.append("\\hline\\hline")
        latex_parts.append("Cluster & N & PHFSI & OSSR & SPI & LRR & TLR & Avg Debt & Avg Payment Days \\\\")
        latex_parts.append("\\hline")

        for _, row in table2.iterrows():
            cluster = row['phfsi_cluster']
            line = f"{cluster} & {row['N_obs']:.0f} & "
            line += f"{row['PHFSI_Mean']:.3f} & {row['OSSR']:.3f} & {row['SPI']:.3f} & "
            line += f"{row['LRR']:.3f} & {row['TLR']:.3f} & "
            line += f"{row['Avg_Total_Debt']:.0f} & {row['Avg_Payment_Days']:.0f} \\\\"
            latex_parts.append(line)

        latex_parts.append("\\hline\\hline")
        latex_parts.append("\\end{tabular}")
        latex_parts.append("\\begin{tablenotes}")
        latex_parts.append("\\small")
        latex_parts.append("\\item Notes: Distressed: PHFSI < 0.4; Stable: 0.4 ≤ PHFSI < 0.7; ")
        latex_parts.append("Self-Sustaining: PHFSI ≥ 0.7. Debt in thousands of euros (€k). ")
        latex_parts.append("Payment days measured in days overdue.")
        latex_parts.append("\\end{tablenotes}")
        latex_parts.append("\\end{table}")

        # Save LaTeX
        tex_path = OUTPUT_DIR / "table2_phfsi_clusters.tex"
        with open(tex_path, 'w') as f:
            f.write('\n'.join(latex_parts))

        logger.info(f"Table 2 LaTeX saved to: {tex_path}")

    def run_pipeline(self):
        """Execute full pipeline to generate all descriptive tables."""
        logger.info("Starting descriptive statistics pipeline...")
        logger.info("="*60 + "\n")

        # Load data
        self.load_data()

        # Create period labels
        self.create_period_labels()

        # Filter to hospitals
        self.filter_hospitals_only()

        # Generate tables
        table1 = self.generate_summary_statistics_table()
        table2 = self.generate_phfsi_clusters_table()

        logger.info("\n" + "="*60)
        logger.info("DESCRIPTIVE STATISTICS PIPELINE COMPLETE")
        logger.info("="*60)
        logger.info("\nGenerated files:")
        logger.info(f"  - {OUTPUT_DIR / 'table1_summary_statistics.csv'}")
        logger.info(f"  - {OUTPUT_DIR / 'table1_summary_statistics.tex'}")
        logger.info(f"  - {OUTPUT_DIR / 'table2_phfsi_clusters.csv'}")
        logger.info(f"  - {OUTPUT_DIR / 'table2_phfsi_clusters.tex'}")

        return table1, table2


def main():
    """Main execution function."""
    generator = DescriptiveStatisticsGenerator()
    table1, table2 = generator.run_pipeline()

    print("\n" + "="*60)
    print("TABLE 1: SUMMARY STATISTICS (SAMPLE)")
    print("="*60)
    print(table1.head(15))

    print("\n" + "="*60)
    print("TABLE 2: PHFSI CLUSTERS")
    print("="*60)
    print(table2)


if __name__ == "__main__":
    main()
