from data_manager import DataManager
from database import DatabaseDB
import logging

# Configure logging to see output
logging.getLogger().setLevel(logging.INFO)

def main():
    print(">>> 1. Starting Data Ingestion...")
    dm = DataManager()
    
    # Ingest the batch
    results = dm.ingest_batch_standard()
    
    print("\n>>> Ingestion Results:")
    for k, v in results.items():
        status = "SUCCESS" if v else "FAILED"
        print(f"  - {k}: {status} ({v})")
        
    print("\n>>> 2. Initializing Database...")
    db = DatabaseDB(data_dir=dm.processed_dir)
    
    print("\n>>> 3. Verifying Tables...")
    tables = db.list_tables()
    print(tables)
    
    if tables.empty:
        print("!!! No tables found. Something went wrong.")
        return

    # Basic Data Check
    print("\n>>> 4. Running Sample Queries...")
    
    # Check 'agregados_economico_financeiros' if it exists
    table_name = 'agregados_economico_financeiros'
    if table_name in tables['name'].values:
        print(f"  Querying {table_name}...")
        df = db.query(f"SELECT count(*) as total_rows FROM {table_name}")
        print(f"  Rows: {df['total_rows'][0]}")
        
        print("  Sample Data:")
        sample = db.query(f"SELECT * FROM {table_name} LIMIT 3")
        print(sample.to_string())
    else:
        print(f"  Table {table_name} not found in registered tables.")

    print("\n>>> Verification Complete.")

if __name__ == "__main__":
    main()
