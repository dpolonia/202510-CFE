from metadata_agent import SNSExtractor
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def deep_search():
    extractor = SNSExtractor()
    datasets = extractor.fetch_datasets()
    
    # Needs: Quality (Mortality, Readmission), Staff (Turnover, Satisfaction)
    keywords = {
        "Quality": ["mortalidade", "obito", "readmiss", "reinvern", "seguranca", "infec", "incident"],
        "Staff": ["absentismo", "rotatividade", "satisfacao", "clima", "greve", "horas extra"],
        "Access": ["tempos", "lista de espera", "consulta", "cirurgia"]
    }
    
    hits = {k: [] for k in keywords}
    
    for ds in datasets:
        text = (ds['title'] + " " + ds['description']).lower()
        for category, terms in keywords.items():
            for term in terms:
                if term in text:
                    hits[category].append(ds)
                    break
                    
    # Report
    print(">>> Deep Search Results <<<")
    for cat, items in hits.items():
        print(f"\n## {cat} ({len(items)})")
        for i in items:
            print(f"- {i['title']} ({i['id']})")
    
    # Save to file for review
    with open("analysis/quality_search_results.json", "w") as f:
        json.dump(hits, f, indent=2)

if __name__ == "__main__":
    deep_search()
