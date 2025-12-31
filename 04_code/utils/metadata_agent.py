import requests
import pandas as pd
import logging
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Evaluator:
    """Evaluates if a dataset metadata meets research requirements."""
    
    REQUIRED_KEYWORDS = [
        "contas", "financeir", "economic", "divida", "pagamento", 
        "produção", "assistencial", "qualidade", "transferência", 
        "hospital", "uls", "balanço", "demonstração"
    ]
    
    def __init__(self):
        self.results = []

    def evaluate(self, dataset):
        """
        Checks dataset metadata against rules.
        dataset dict should have: title, description, modified_date, source_url, tags (list), format (list).
        """
        score = 0
        reasons = []
        
        # 1. Keyword Match
        text_content = (dataset.get('title', '') + " " + dataset.get('description', '') + " " + " ".join(dataset.get('tags', []))).lower()
        
        matches = [kw for kw in self.REQUIRED_KEYWORDS if kw in text_content]
        if matches:
            score += len(matches)
            reasons.append(f"Keywords found: {', '.join(matches[:5])}")
        
        # 2. Year Validity
        # Simple regex to find years like 2017, 2024
        years = re.findall(r'20(1[7-9]|2[0-5])', text_content)
        if years:
            score += 2
            reasons.append(f"Relevant years found: {set(['20'+y for y in years])}")
            
        # 3. Formats
        formats = [f.lower() for f in dataset.get('formats', [])]
        if any(f in formats for f in ['csv', 'parquet', 'json', 'xlsx', 'xls']):
            score += 1
            reasons.append("Machine-readable format available")
            
        dataset['score'] = score
        dataset['reasons'] = "; ".join(reasons)
        dataset['is_fit'] = score >= 2 # Threshold
        
        self.results.append(dataset)
        return dataset['is_fit']

    def generate_report(self, output_path):
        """Generates a markdown report."""
        df = pd.DataFrame(self.results)
        if df.empty:
            logger.warning("No datasets evaluated.")
            return

        # Sort by score
        df = df.sort_values(by='score', ascending=False)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Dataset Relevance Report\n\n")
            f.write("Evaluation for 'Beyond Bankruptcy' research paper.\n\n")
            
            f.write("## High Relevance Datasets (Score >= 3)\n")
            high_rel = df[df['score'] >= 3]
            if not high_rel.empty:
                for _, row in high_rel.iterrows():
                    f.write(f"### [{row['title']}]({row['source_url']})\n")
                    f.write(f"- **Source**: {row['source_name']}\n")
                    f.write(f"- **Score**: {row['score']}\n")
                    f.write(f"- **Reasons**: {row['reasons']}\n")
                    f.write(f"- **Modified**: {row.get('modified', 'N/A')}\n\n")
            else:
                f.write("No high relevance datasets found.\n\n")
                
            f.write("## Other Potential Candidates\n")
            others = df[(df['score'] >= 1) & (df['score'] < 3)]
            if not others.empty:
                for _, row in others.iterrows():
                    f.write(f"- **{row['title']}** ({row['source_name']}): {row['reasons']}\n")
            
class SNSExtractor:
    BASE_URL = "https://transparencia.sns.gov.pt/api/explore/v2.1"
    
    def fetch_datasets(self):
        """Fetches catalog from Opendatasoft API."""
        datasets = []
        try:
            url = f"{self.BASE_URL}/catalog/datasets?limit=50&timezone=UTC"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            for item in data.get('results', []):
                # Opendatasoft structure
                meta = item.get('metas', {}).get('default', {})
                
                ds = {
                    'source_name': 'SNS Transparencia',
                    'id': item.get('dataset_id'),
                    'title': meta.get('title', 'Untitled'),
                    'description': meta.get('description', ''),
                    'modified': meta.get('modified', ''),
                    'tags': meta.get('keyword', []),
                    'formats': ['json', 'csv', 'parquet'], # ODS usually supports these
                    'source_url': f"https://transparencia.sns.gov.pt/explore/dataset/{item.get('dataset_id')}/information/"
                }
                datasets.append(ds)
                
            logger.info(f"Fetched {len(datasets)} datasets from SNS.")
        except Exception as e:
            logger.error(f"Error fetching SNS data: {e}")
            
        return datasets

class DadosGovExtractor:
    """Scrapes dados.gov.pt search results since API endpoint is uncertain/undocumented for v1/v3."""
    BASE_URL = "https://dados.gov.pt"
    SEARCH_path = "/pt/datasets/"
    
    def fetch_datasets(self, query="hospital"):
        datasets = []
        try:
            # We search for a few key terms to cast a wide net
            queries = ["hospital", "divida", "sns", "saude"]
            seen_ids = set()
            
            for q in queries:
                url = f"{self.BASE_URL}{self.SEARCH_path}?q={q}"
                response = requests.get(url)
                if response.status_code != 200:
                    continue
                    
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Selector for dataset items (may need adjustment based on inspection, 
                # but usually they are inside 'article' or have specific classes)
                # Inspecting standard uData/CKAN widely used: class="dataset-card" or similar
                # Let's try to find articles which usually hold the results
                articles = soup.find_all('article', class_='dataset-card')
                
                for art in articles:
                    link_tag = art.find('a', class_='dataset-card-title')
                    if not link_tag: 
                        continue
                        
                    href = link_tag.get('href')
                    full_url = urljoin(self.BASE_URL, href)
                    title = link_tag.get_text(strip=True)
                    
                    if full_url in seen_ids:
                        continue
                        
                    seen_ids.add(full_url)
                    
                    # Extract basic description or tags if available on card
                    desc = ""
                    desc_tag = art.find('div', class_='dataset-card-description')
                    if desc_tag:
                        desc = desc_tag.get_text(strip=True)
                        
                    # Formats
                    formats = []
                    fmt_tags = art.find_all('span', class_='format-badge')
                    for ft in fmt_tags:
                        formats.append(ft.get_text(strip=True))

                    ds = {
                        'source_name': 'Dados.gov.pt',
                        'id': href, # internal ID
                        'title': title,
                        'description': desc,
                        'modified': 'Unknown', # Scan detail page if needed
                        'tags': [], # detailed tags usually on detail page
                        'formats': formats,
                        'source_url': full_url
                    }
                    datasets.append(ds)
            
            logger.info(f"Fetched {len(datasets)} datasets from Dados.gov.pt (Scraped).")
            
        except Exception as e:
            logger.error(f"Error scraping Dados.gov.pt: {e}")
            
        return datasets

def main():
    evaluator = Evaluator()
    sns_extractor = SNSExtractor()
    dados_extractor = DadosGovExtractor()
    
    # 1. Fetch
    sns_data = sns_extractor.fetch_datasets()
    dados_data = dados_extractor.fetch_datasets()
    
    all_data = sns_data + dados_data
    
    # 2. Evaluate
    for ds in all_data:
        evaluator.evaluate(ds)
        
    # 3. Report
    evaluator.generate_report("requirements_check.md")
    logger.info("Report generated: requirements_check.md")

if __name__ == "__main__":
    main()
