#!/usr/bin/env python3
"""
Extract Citations from Manuscript
Extracts all \cite{} references from LaTeX files

Author: Research Team
Date: 2025-12-31
"""

import re
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parents[2]
SECTIONS_DIR = BASE_DIR / "07_writing" / "paper" / "sections"

def extract_citations(tex_content):
    """Extract all \cite{} and \citep{}/\citet{} references"""

    # Match \cite{key}, \citep{key}, \citet{key}, \citeauthor{key}, \citeyear{key}
    pattern = r'\\cite[tpauthoryear]*\{([^}]+)\}'
    matches = re.findall(pattern, tex_content)

    # Split multiple citations (e.g., \cite{A,B,C})
    citations = []
    for match in matches:
        citations.extend([c.strip() for c in match.split(',')])

    return citations

def extract_all_citations():
    """Extract citations from all .tex files"""

    all_citations = []
    file_citations = {}

    print("="*70)
    print("CITATION EXTRACTION")
    print("="*70)

    for tex_file in sorted(SECTIONS_DIR.glob("*.tex")):
        try:
            content = tex_file.read_text()
            citations = extract_citations(content)

            if citations:
                file_citations[tex_file.name] = citations
                all_citations.extend(citations)

                print(f"\n{tex_file.name}:")
                print(f"  Found {len(citations)} citation(s)")

        except Exception as e:
            print(f"\n{tex_file.name}:")
            print(f"  ERROR: {e}")

    # Count unique citations
    unique_citations = sorted(set(all_citations))
    citation_counts = Counter(all_citations)

    print("\n" + "="*70)
    print("CITATION SUMMARY")
    print("="*70)

    print(f"\nTotal citations (with duplicates): {len(all_citations)}")
    print(f"Unique citations: {len(unique_citations)}")

    # Show most frequently cited
    print(f"\nMost Frequently Cited (Top 10):")
    for cite_key, count in citation_counts.most_common(10):
        print(f"  {cite_key}: {count} time(s)")

    # Save to file
    output_file = BASE_DIR / "04_code" / "06_review" / "citations_extracted.txt"
    with open(output_file, 'w') as f:
        f.write("UNIQUE CITATIONS EXTRACTED FROM MANUSCRIPT\n")
        f.write("="*70 + "\n\n")
        for i, cite_key in enumerate(unique_citations, 1):
            f.write(f"{i}. {cite_key} (cited {citation_counts[cite_key]} time(s))\n")

    print(f"\n✓ Saved to: {output_file}")

    return unique_citations, citation_counts

if __name__ == "__main__":
    citations, counts = extract_all_citations()

    print("\n" + "="*70)
    print("NEXT STEP: Run 03_verify_references_scopus.py")
    print("="*70)
