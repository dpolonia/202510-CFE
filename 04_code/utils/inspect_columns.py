from database import DatabaseDB
import pandas as pd

def main():
    db = DatabaseDB()
    tables = ['agregados_economico_financeiros', 'conta_do_servico_nacional_de_saude', 'divida_total_vencida_e_pagamentos']
    
    with open('analysis/columns_info.txt', 'w') as f:
        for t in tables:
            try:
                cols = db.query(f"DESCRIBE {t}")['column_name'].tolist()
                f.write(f"--- {t} ---\n")
                for c in cols:
                    f.write(f"{c}\n")
                f.write("\n")
            except:
                f.write(f"--- {t} (Not Found) ---\n")

if __name__ == "__main__":
    main()
