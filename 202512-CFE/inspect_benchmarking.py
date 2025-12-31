
import pandas as pd
import sys

file_path = "/home/dpolonia/202512-CFE/source/Benchmarking Hospitais - Económico-Financeira_Export (1).xlsx"
report_file = "benchmarking_columns.txt"

sys.stdout = open(report_file, "w", encoding="utf-8")

try:
    df = pd.read_excel(file_path, nrows=5)
    print("Columns found:")
    for col in df.columns:
        print(f"- {col}")
except Exception as e:
    print(f"Error reading excel: {e}")
