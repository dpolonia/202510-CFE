
import zipfile
import re
import sys

file_path = "/home/dpolonia/202512-CFE/source/Benchmarking Hospitais - Económico-Financeira_Export (1).xlsx"
keywords = ["Capital Próprio", "Passivo", "Ativo", "EBITDA", "Resultados", "Dívida", "Gastos com Pessoal", "Proveitos"]

try:
    with zipfile.ZipFile(file_path, 'r') as z:
        if 'xl/sharedStrings.xml' in z.namelist():
            with z.open('xl/sharedStrings.xml') as f:
                content = f.read().decode('utf-8')
                print("Found file. Scanning for keywords...")
                found = []
                for kw in keywords:
                    if kw in content:
                        found.append(kw)
                
                print(f"Keywords found: {found}")
                if len(found) > 3:
                     print("CONCLUSION: High probability this is the Financial Data file.")
                else:
                     print("CONCLUSION: Low match count.")
        else:
            print("xl/sharedStrings.xml not found. Is this a standard .xlsx?")
except Exception as e:
    print(f"Error: {e}")
