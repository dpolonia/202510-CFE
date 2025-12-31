import pandas as pd
import re
import logging

logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self):
        pass

    def normalize_name(self, name):
        """Standardizes hospital names for matching."""
        if not isinstance(name, str):
            return ""
        
        # Lowercase and strip
        n = name.lower().strip()
        
        # Remove common suffixes/prefixes
        n = re.sub(r',?\s*e\.?p\.?e\.?', '', n) # Remove E.P.E.
        n = re.sub(r'hospital distrital', 'hospital', n)
        n = re.sub(r'centro hospitalar', 'centro hospitalar', n) # keep for now
        n = re.sub(r'unidade local de sa[úu]de', 'uls', n)
        
        # Remove extra spaces
        n = re.sub(r'\s+', ' ', n)
        
        return n.strip()

    def create_entity_map(self, financial_entities, debt_entities):
        """
        Creates a mapping dictionary between two sets of entities.
        financial_entities: list of strings from financial dataset
        debt_entities: list of strings from debt dataset
        Returns: {fin_name: debt_name} (best match or None)
        """
        mapping = {}
        # Simple exact normalized match first
        debt_norm = {self.normalize_name(d): d for d in debt_entities}
        
        for f in financial_entities:
            f_norm = self.normalize_name(f)
            if f_norm in debt_norm:
                mapping[f] = debt_norm[f_norm]
            else:
                # Try simple containment
                match = None
                for d_n, d_orig in debt_norm.items():
                    if f_norm in d_n or d_n in f_norm:
                        match = d_orig
                        break
                mapping[f] = match
                
        return mapping
