import requests
import shutil
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SNSClient:
    """
    Client for the SNS Transparency Portal API (v2.1).
    Handles fetching datasets directly in Parquet format.
    """
    BASE_URL = "https://transparencia.sns.gov.pt/api/explore/v2.1"

    def __init__(self, output_dir="data/raw/api"):
        """
        Initialize the SNS Client.
        
        Args:
            output_dir (str): Directory where downloaded files will be stored.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def download_dataset_parquet(self, dataset_id):
        """
        Downloads the full dataset export in Parquet format.
        
        Args:
            dataset_id (str): The slug/ID of the dataset (e.g., 'acss-divida-total').
            
        Returns:
            str: Path to the downloaded file, or None if failed.
        """
        url = f"{self.BASE_URL}/catalog/datasets/{dataset_id}/exports/parquet"
        file_path = os.path.join(self.output_dir, f"{dataset_id}.parquet")
        
        logger.info(f"Downloading dataset '{dataset_id}' from {url}...")
        
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(file_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            
            logger.info(f"Successfully downloaded to {file_path}")
            return file_path
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download dataset '{dataset_id}': {e}")
            return None
