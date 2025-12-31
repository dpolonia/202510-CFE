
import pandas as pd
import os
import sys

source_dir = "/home/dpolonia/202512-CFE/source"
report_file = "header_report.txt"

sys.stdout = open(report_file, "w", encoding="utf-8")

if not os.path.exists(source_dir):
    print(f"Source directory not found: {source_dir}")
    sys.exit(1)

files = sorted(os.listdir(source_dir))

for file in files:
    if "Identifier" in file or file.startswith("~"):
        continue
        
    path = os.path.join(source_dir, file)
    print(f"\n{'='*30}\nFile: {file}\n{'='*30}")
    
    try:
        if file.endswith(('.xls', '.xlsx')):
            # Load without header first to see structure, or assume header=0
            df = pd.read_excel(path, nrows=1)
            print(f"Shape (cols): {df.shape[1]}")
            print(f"Columns: {list(df.columns)}")
            
        elif file.endswith('.csv'):
            df = pd.read_csv(path, nrows=1)
            print(f"Columns: {list(df.columns)}")
            
    except Exception as e:
        print(f"Error reading {file}: {e}")

print("\nDone.")
