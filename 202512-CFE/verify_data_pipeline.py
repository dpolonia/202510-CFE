import unittest
import os
import shutil
import json
import pandas as pd
import logging
from unittest.mock import MagicMock, patch
from data_manager import DataManager

# Configure logging to show info during tests
logging.basicConfig(level=logging.INFO)

class TestDataPipeline(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary test directory structure
        self.test_dir = "test_data_env"
        os.makedirs(self.test_dir, exist_ok=True)
        self.dm = DataManager(base_dir=self.test_dir)
        
    def tearDown(self):
        # Cleanup
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('sns_client.SNSClient.download_dataset_parquet')
    def test_ingest_api(self, mock_download):
        """Test API ingestion with mocked download"""
        # mock return of a parquet file path
        dummy_parquet = os.path.join(self.test_dir, "dummy_api.parquet")
        df_dummy = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        df_dummy.to_parquet(dummy_parquet)
        
        mock_download.return_value = dummy_parquet
        
        # Inject the mock SNS client into the DataManager
        self.dm.sns_client.download_dataset_parquet = mock_download
        
        result_path = self.dm.ingest_api("dummy-dataset")
        
        self.assertIsNotNone(result_path)
        self.assertTrue(os.path.exists(result_path))
        self.assertTrue("processed" in result_path)
        
        # Verify content
        df_processed = pd.read_parquet(result_path)
        self.assertEqual(len(df_processed), 2)
        print("API Ingestion Test Passed")

    def test_ingest_impic_entidades(self):
        """Test manual ingestion of IMPIC Entidades JSON"""
        # Create dummy JSON file
        dummy_json = os.path.join(self.test_dir, "entidades.json")
        data = {
            "classes": [
                {"nifEntidade": "123456789", "desigEntidade": "Test Entity", "totAdjudicanteValorContratIni": 1000.50},
                {"nifEntidade": "987654321", "desigEntidade": "Entity 2", "totAdjudicanteValorContratIni": 500.00}
            ]
        }
        with open(dummy_json, 'w') as f:
            json.dump(data, f)
            
        result_path = self.dm.ingest_impic_entidades(dummy_json)
        
        self.assertIsNotNone(result_path)
        self.assertTrue(os.path.exists(result_path))
        
        df = pd.read_parquet(result_path)
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['nifEntidade'], "123456789")
        print("IMPIC Entidades Ingestion Test Passed")

    def test_ingest_impic_anuncios(self):
        """Test manual ingestion of IMPIC Anuncios JSON"""
        # Create dummy JSON file (list format)
        dummy_json = os.path.join(self.test_dir, "anuncios2024.json")
        data = [
            {"idAnuncio": 1, "tipoContrato": "Aquisicao", "precoContratual": 5000},
            {"idAnuncio": 2, "tipoContrato": "Empreitada", "precoContratual": 15000}
        ]
        with open(dummy_json, 'w') as f:
            json.dump(data, f)
            
        result_path = self.dm.ingest_impic_anuncios(dummy_json)
        
        self.assertIsNotNone(result_path)
        self.assertTrue("impic_anuncios2024.parquet" in result_path)
        
        df = pd.read_parquet(result_path)
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[1]['precoContratual'], 15000)
        print("IMPIC Anuncios Ingestion Test Passed")

    def test_ingest_impic_contratos(self):
        """Test manual ingestion of IMPIC Contratos ZIP"""
        import zipfile
        
        # Create dummy JSON content
        dummy_json_name = "contratos2024.json"
        data = [
            {"idContrato": 99, "precoContratual": 25000}
        ]
        
        # Create a ZIP file containing the JSON
        zip_path = os.path.join(self.test_dir, "contratos2024.zip")
        with zipfile.ZipFile(zip_path, 'w') as z:
            z.writestr(dummy_json_name, json.dumps(data))
            
        result_path = self.dm.ingest_impic_contratos(zip_path)
        
        self.assertIsNotNone(result_path)
        self.assertTrue("impic_contratos2024.parquet" in result_path)
        
        df = pd.read_parquet(result_path)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['precoContratual'], 25000)
        print("IMPIC Contratos (ZIP) Ingestion Test Passed")

if __name__ == '__main__':
    unittest.main()
