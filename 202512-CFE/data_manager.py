import pandas as pd
import os
import json
import logging
import zipfile
from pathlib import Path
from sns_client import SNSClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataManager:
    """
    Manages data ingestion, processing, and storage.
    """
    
    def __init__(self, base_dir=None):
        if base_dir is None:
            # Default to current working directory
            self.base_dir = Path(os.getcwd())
        else:
            self.base_dir = Path(base_dir)
            
        self.raw_api_dir = self.base_dir / "data" / "raw" / "api"
        self.raw_manual_dir = self.base_dir / "data" / "raw" / "manual"
        self.processed_dir = self.base_dir / "data" / "processed"
        self.metadata_dir = self.base_dir / "data" / "metadata"
        
        # Ensure directories exist
        for d in [self.raw_api_dir, self.raw_manual_dir, self.processed_dir, self.metadata_dir]:
            os.makedirs(d, exist_ok=True)
            
        self.sns_client = SNSClient(output_dir=str(self.raw_api_dir))

    def ingest_api(self, dataset_id):
        """
        Downloads a dataset from SNS API and standardizes it if needed.
        Since it's Parquet, we might just move/copy it to processed or apply minimal transform.
        """
        raw_path = self.sns_client.download_dataset_parquet(dataset_id)
        if raw_path:
            # For now, we consider the raw Parquet from API as "processed" enough to be readable.
            # In a full pipeline, we might apply schema validation here.
            # Using the same filename for processed.
            
            # Determine destination subfolder if needed, or just root processed
            # We want to organize by type if possible, but generic ingest_api might just dump to root
            dest_dir = self.processed_dir
            if 'agregados' in dataset_id or 'conta-' in dataset_id:
                dest_dir = self.processed_dir / "financial"
            elif 'atividade' in dataset_id or 'stock' in dataset_id:
                dest_dir = self.processed_dir / "operational"
            
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = dest_dir / f"{dataset_id}.parquet"
            
            # Read and Write to ensure standardized compression/format if needed, 
            # or just copy. Let's read/write to sanity check.
            try:
                df = pd.read_parquet(raw_path)
                logger.info(f"Ingested '{dataset_id}': {df.shape[0]} rows, {df.shape[1]} cols.")
                df.to_parquet(dest_path)
                logger.info(f"Saved processed file to {dest_path}")
                return str(dest_path)
            except Exception as e:
                logger.error(f"Error processing Parquet file {raw_path}: {e}")
                return None
        return None

    def ingest_impic_entidades(self, file_path):
        """
        Ingests the IMPIC Entidades file (JSON or Excel).
        Exepcts a path to a manually downloaded file.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None
            
        logger.info(f"Processing IMPIC Entidades from {file_path}...")
        try:
            if file_path.suffix.lower() == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Handle if strict list or dict wrapper
                    if isinstance(data, dict) and 'classes' in data:
                        df = pd.DataFrame(data['classes'])
                    else:
                        df = pd.DataFrame(data)
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                logger.error("Unsupported file format for IMPIC Entidades")
                return None
            
            # Basic validation/renaming could happen here based on schema
            dest_path = self.processed_dir / "impic_entidades.parquet"
            df.to_parquet(dest_path)
            logger.info(f"Saved IMPIC Entidades to {dest_path}")
            return str(dest_path)
            
        except Exception as e:
            logger.error(f"Failed to ingest IMPIC Entidades: {e}")
            return None

    def ingest_impic_anuncios(self, file_path):
        """
        Ingests an IMPIC Anuncios JSON file (e.g. anuncios2024.json).
        """
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None
            
        logger.info(f"Processing IMPIC Anuncios from {file_path}...")
        try:
            # These can be large, but pandas read_json usually handles them if memory allows.
            # If not, we'd need chunked processing.
            df = pd.read_json(file_path)
            
            # Generate a year based or filename based output name to avoid overwriting?
            # Or assume we append? For now, let's keep separate files by year/name.
            out_name = f"impic_{file_path.stem}.parquet"
            dest_path = self.processed_dir / out_name
            
            df.to_parquet(dest_path)
            logger.info(f"Saved IMPIC Anuncios to {dest_path}")
            return str(dest_path)
            
        except Exception as e:
            logger.error(f"Failed to ingest IMPIC Anuncios {file_path}: {e}")
            return None

    def ingest_impic_contratos(self, file_path):
        """
        Ingests an IMPIC Contratos ZIP file (e.g. contratos2024.zip).
        Extracts content (expected JSON/CSV) and converts to Parquet.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None
            
        logger.info(f"Processing IMPIC Contratos from {file_path}...")
        try:
            with zipfile.ZipFile(file_path, 'r') as z:
                # Assuming one main data file inside, or we look for .json/.csv
                files = z.namelist()
                target_file = None
                for f in files:
                    if f.endswith('.json') or f.endswith('.csv'):
                        target_file = f
                        break
                
                if not target_file:
                    logger.error(f"No valid data file (json/csv) found in zip: {files}")
                    return None
                    
                with z.open(target_file) as f:
                    if target_file.endswith('.json'):
                         df = pd.read_json(f)
                    else:
                         df = pd.read_csv(f, sep=';', encoding='utf-8', on_bad_lines='skip') # Common gov csv format
            
            out_name = f"impic_{file_path.stem}.parquet"
            dest_path = self.processed_dir / out_name
            
            df.to_parquet(dest_path)
            logger.info(f"Saved IMPIC Contratos to {dest_path}")
            return str(dest_path)

        except Exception as e:
            logger.error(f"Failed to ingest IMPIC Contratos {file_path}: {e}")
            return None

    def ingest_batch_standard(self):
        """
        Ingests the standard high-relevance datasets identified for the project.
        """
        datasets = [
            "agregados-economico-financeiros",
            "conta-do-servico-nacional-de-saude",
            "atividade-de-internamento-hospitalar",
            "divida-total-vencida-e-pagamentos" # Adding this one as it's critical for the paper (Payment Delays)
        ]
        
        results = {}
        for ds in datasets:
            res = self.ingest_api(ds)
            results[ds] = res
        return results

    def load_data(self, filename, folder=""):
        """
        Simple loader for processed parquet files.
        """
        if folder:
             path = self.processed_dir / folder / filename
        else:
             # Try recursive search if just filename given? Or just root
             path = self.processed_dir / filename
             if not path.exists():
                 # Try to find it in subfolders
                 found = list(self.processed_dir.glob(f"**/{filename}"))
                 if found:
                     path = found[0]

        if path.exists():
            return pd.read_parquet(path)
        else:
            logger.warning(f"File not found: {path}")
            return None
