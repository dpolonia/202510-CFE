
import zipfile
import sys

file_path = "/home/dpolonia/202512-CFE/source/Benchmarking Hospitais - Económico-Financeira_Export (1).xlsx"
keywords = [
    "Capital Próprio", "Fundos Próprios", "Situation Net", "Equity", # Equity
    "Passivo", "Liability", "Liabilities", "Dívida", "Empréstimos", # Debt
    "Ativo", "Activo", "Asset", "Assets", # Assets
    "EBITDA", "Margar", "Resultado Líquido", "Proveitos", "Rendimentos" # P&L
]

try:
    with zipfile.ZipFile(file_path, 'r') as z:
        if 'xl/sharedStrings.xml' in z.namelist():
            with z.open('xl/sharedStrings.xml') as f:
                content = f.read().decode('utf-8')
                print("Scanning for expanded financial keywords...")
                found = []
                for kw in keywords:
                    if kw in content:
                        found.append(kw)
                
                print(f"Keywords found: {found}")
except Exception as e:
    print(f"Error: {e}")
