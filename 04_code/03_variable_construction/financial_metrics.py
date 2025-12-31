from database import DatabaseDB
from analysis.cleaner import DataCleaner
import pandas as pd
import json
import logging

logger = logging.getLogger(__name__)

class FinancialAnalyzer:
    def __init__(self):
        self.db = DatabaseDB()
        self.cleaner = DataCleaner()
        self.map_file = 'analysis/entity_map.json'
        
        try:
            with open(self.map_file, 'r', encoding='utf-8') as f:
                self.entity_map = json.load(f)
        except Exception:
            logger.warning("Entity map not found. Merging might fail.")
            self.entity_map = {}

    def get_financials_merged(self):
        """
        Loads and merges Agregados (P&L) and Divida (Debt).
        Returns a single DataFrame with mapped entities.
        """
        # Load Data
        fin_df = self.db.query("SELECT * FROM agregados_economico_financeiros")
        debt_df = self.db.query("SELECT * FROM divida_total_vencida_e_pagamentos")
        
        # Standardize Dates (assuming 'periodo' is YYYY-MM-DD or similar) -> to Year-Month or Year
        # Agregados 'tempo' is YYYY-MM-DD. Divida 'periodo' is YYYY-MM.
        # Let's inspect format first. 
        # For now, simplistic conversion to datetime
        fin_df['date'] = pd.to_datetime(fin_df['tempo'])
        debt_df['date'] = pd.to_datetime(debt_df['periodo'])
        
        # Convert to Monthly period for merging
        fin_df['month_period'] = fin_df['date'].dt.to_period('M')
        debt_df['month_period'] = debt_df['date'].dt.to_period('M')
        
        # Map Entities in Financials to match Debt (Link Key: specific standardized name)
        # We use the cleaners 'normalize_name' on both and link via that?
        # Or use the map: Map Fin -> Debt Name
        
        fin_df['mapped_entity'] = fin_df['entidade'].map(self.entity_map)
        # Fill unmapped with original (normalized)
        fin_df['mapped_entity'] = fin_df['mapped_entity'].fillna(fin_df['entidade'])
        
        # Merge
        # Outer merge to keep all data
        merged = pd.merge(
            fin_df, 
            debt_df, 
            left_on=['mapped_entity', 'month_period'], 
            right_on=['entidade', 'month_period'],
            suffixes=('_fin', '_debt'),
            how='outer'
        )
        
        return merged

    def calculate_metrics(self, df):
        """
        Calculates OSSR, Debt Burden, etc.
        """
        # OSSR: Rendimentos / Gastos
        # Avoid division by zero
        df['ossr'] = df['rendimentos_operacionais'] / df['gastos_operacionais'].replace(0, 1)
        
        # Debt Ratio: Overdue / Total Debt
        # (Using 'divida_total_fornecedores_externos' vs 'divida_vencida...')
        df['debt_overdue_ratio'] = df['divida_vencida_fornecedores_externos'] / df['divida_total_fornecedores_externos'].replace(0, 1)
        
        # EBITDA Margin
        df['ebitda_margin'] = df['ebitda'] / df['rendimentos_operacionais'].replace(0, 1)
        
        return df

    def run_analysis(self):
        merged = self.get_financials_merged()
        analyzed = self.calculate_metrics(merged)
        return analyzed
