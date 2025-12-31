import duckdb
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseDB:
    def __init__(self, data_dir="data/processed"):
        self.data_dir = Path(data_dir)
        self.con = duckdb.connect(database=':memory:') # In-memory DB, reads from files
        self.register_tables()

    def register_tables(self):
        """
        Scans the processed directory and registers every parquet file as a view.
        View name = file stem (e.g. 'agregados-economico-financeiros').
        """
        if not self.data_dir.exists():
            logger.warning(f"Data directory {self.data_dir} does not exist.")
            return

        # Find all parquet files recursively
        files = list(self.data_dir.glob("**/*.parquet"))
        
        count = 0
        for f in files:
            table_name = f.stem.replace('-', '_') # SQL friendly
            # We use absolute path to be safe
            abs_path = str(f.absolute())
            
            try:
                # Create a view directly on the parquet file
                query = f"CREATE OR REPLACE VIEW {table_name} AS SELECT * FROM read_parquet('{abs_path}')"
                self.con.execute(query)
                logger.debug(f"Registered view: {table_name}")
                count += 1
            except Exception as e:
                logger.error(f"Failed to register {table_name}: {e}")
                
        logger.info(f"Registered {count} tables in DuckDB.")

    def query(self, sql):
        """Executes a SQL query and returns result as DataFrame."""
        try:
            return self.con.execute(sql).df()
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return None

    def list_tables(self):
        return self.con.execute("SHOW TABLES").df()
