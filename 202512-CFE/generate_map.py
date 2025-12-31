from database import DatabaseDB
from analysis.cleaner import DataCleaner
import json
import logging

logging.basicConfig(level=logging.INFO)

def main():
    db = DatabaseDB()
    cleaner = DataCleaner()
    
    # Get unique entities
    fin_df = db.query("SELECT DISTINCT entidade FROM agregados_economico_financeiros")
    debt_df = db.query("SELECT DISTINCT entidade FROM divida_total_vencida_e_pagamentos")
    
    fin_entities = fin_df['entidade'].dropna().unique().tolist()
    debt_entities = debt_df['entidade'].dropna().unique().tolist()
    
    print(f"Financial Entities: {len(fin_entities)}")
    print(f"Debt Entities: {len(debt_entities)}")
    
    # Create Map
    mapping = cleaner.create_entity_map(fin_entities, debt_entities)
    
    # Stats
    mapped_count = sum(1 for v in mapping.values() if v is not None)
    print(f"Mapped: {mapped_count} / {len(fin_entities)}")
    
    # Save
    with open('analysis/entity_map.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
        
    print("Mapping saved to analysis/entity_map.json")

if __name__ == "__main__":
    main()
