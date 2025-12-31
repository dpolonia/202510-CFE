from analysis.financial_metrics import FinancialAnalyzer
import logging

logging.basicConfig(level=logging.INFO)

def main():
    analyzer = FinancialAnalyzer()
    print("Running Financial Analysis...")
    
    df = analyzer.run_analysis()
    
    print(f"Result Shape: {df.shape}")
    print("Sample Metrics:")
    print(df[['entidade_fin', 'month_period', 'ossr', 'debt_overdue_ratio']].head())
    
    # Save
    df.to_csv("analysis/preliminary_metrics.csv", index=False)
    print("Saved to analysis/preliminary_metrics.csv")

if __name__ == "__main__":
    main()
