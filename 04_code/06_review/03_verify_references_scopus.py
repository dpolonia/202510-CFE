#!/usr/bin/env python3
"""
Verify References Using Scopus API
Checks all citations against Scopus database

Author: Research Team
Date: 2025-12-31
"""

import os
import time
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

# Manual DOI mapping for key citations (to speed up verification)
# Extracted from common finance/healthcare papers
KNOWN_DOIS = {
    'Altman1968': '10.1111/j.1540-6261.1968.tb00843.x',
    'Myers1984': '10.1111/j.1540-6261.1984.tb03646.x',
    'Myers2001': '10.1111/0022-1082.00354',
    'Ohlson1980': '10.1016/0304-405X(80)90011-1',
    'Kornai1986': None,  # Book - not in Scopus typically
    'Maskin1999': '10.2307/2564874',
    'Baker2002': '10.1111/1540-6261.00424',
    'Gilson1990': '10.1016/0304-405X(90)90059-9',
    'Hotchkiss1995': '10.1111/j.1540-6261.1995.tb05175.x',
}

def lookup_scopus_by_doi(doi, api_key):
    """Lookup reference in Scopus by DOI"""

    url = f"https://api.elsevier.com/content/search/scopus?query=DOI({doi})"
    headers = {
        'X-ELS-APIKey': api_key,
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            results = data.get('search-results', {}).get('entry', [])

            if len(results) > 0:
                result = results[0]
                return {
                    'found': True,
                    'title': result.get('dc:title', 'N/A'),
                    'authors': result.get('dc:creator', 'N/A'),
                    'year': result.get('prism:coverDate', 'N/A')[:4] if result.get('prism:coverDate') else 'N/A',
                    'journal': result.get('prism:publicationName', 'N/A'),
                    'citations': result.get('citedby-count', 0),
                    'scopus_id': result.get('dc:identifier', 'N/A'),
                    'doi': doi
                }
            else:
                return {'found': False, 'error': 'No results for DOI'}
        else:
            return {'found': False, 'error': f'HTTP {response.status_code}'}

    except Exception as e:
        return {'found': False, 'error': str(e)}

def lookup_scopus_by_author_year(citation_key, api_key):
    """Fallback: Lookup by author last name + year extracted from citation key"""

    # Extract author and year from citation key (e.g., Altman1968 → Altman, 1968)
    import re
    match = re.match(r'([A-Za-z]+)(\d{4})', citation_key)

    if not match:
        return {'found': False, 'error': 'Could not parse citation key'}

    author_last = match.group(1)
    year = match.group(2)

    # Construct query
    query = f'AUTHOR-NAME({author_last}) AND PUBYEAR IS {year}'

    url = f"https://api.elsevier.com/content/search/scopus?query={query}&count=5"
    headers = {
        'X-ELS-APIKey': api_key,
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            results = data.get('search-results', {}).get('entry', [])

            if len(results) > 0:
                # Return first result (most likely match)
                result = results[0]
                return {
                    'found': True,
                    'title': result.get('dc:title', 'N/A'),
                    'authors': result.get('dc:creator', 'N/A'),
                    'year': result.get('prism:coverDate', 'N/A')[:4] if result.get('prism:coverDate') else 'N/A',
                    'journal': result.get('prism:publicationName', 'N/A'),
                    'citations': result.get('citedby-count', 0),
                    'scopus_id': result.get('dc:identifier', 'N/A'),
                    'match_quality': 'fuzzy',
                    'total_matches': len(results)
                }
            else:
                return {'found': False, 'error': 'No results for author+year query'}
        else:
            return {'found': False, 'error': f'HTTP {response.status_code}'}

    except Exception as e:
        return {'found': False, 'error': str(e)}

def verify_all_references(citations, api_key):
    """Verify all citations against Scopus"""

    results = []
    verified_count = 0
    high_impact_count = 0

    print("\n" + "="*70)
    print("SCOPUS REFERENCE VERIFICATION")
    print("="*70)

    for i, citation_key in enumerate(citations, 1):
        print(f"\n[{i}/{len(citations)}] Verifying {citation_key}...", end=" ")

        # Try DOI lookup first (if known)
        if citation_key in KNOWN_DOIS and KNOWN_DOIS[citation_key]:
            result = lookup_scopus_by_doi(KNOWN_DOIS[citation_key], api_key)
        else:
            # Fallback to author+year search
            result = lookup_scopus_by_author_year(citation_key, api_key)

        if result['found']:
            print(f"✅ FOUND")
            print(f"    Title: {result['title'][:60]}...")
            print(f"    Journal: {result.get('journal', 'N/A')[:40]}...")
            print(f"    Citations: {result.get('citations', 0)}")
            verified_count += 1

            if int(result.get('citations', 0)) > 500:
                high_impact_count += 1
        else:
            print(f"❌ NOT FOUND")
            print(f"    Error: {result.get('error', 'Unknown')}")

        results.append({
            'citation_key': citation_key,
            'scopus_result': result
        })

        # Rate limiting: 9 requests/second max for Scopus
        # We use 6/second to be conservative
        time.sleep(0.17)

    # Generate summary report
    print("\n" + "="*70)
    print("VERIFICATION REPORT")
    print("="*70)

    print(f"\nTotal Citations: {len(citations)}")
    print(f"Verified in Scopus: {verified_count} ({100*verified_count/len(citations):.1f}%)")
    print(f"Not Found: {len(citations) - verified_count} ({100*(len(citations)-verified_count)/len(citations):.1f}%)")
    print(f"High-Impact (>500 citations): {high_impact_count}")

    # List not found
    not_found = [r for r in results if not r['scopus_result']['found']]
    if not_found:
        print(f"\nNOT FOUND IN SCOPUS ({len(not_found)}):")
        for r in not_found:
            print(f"  - {r['citation_key']}: {r['scopus_result'].get('error', 'Unknown error')}")

    # List high-impact papers
    high_impact = [r for r in results if r['scopus_result'].get('found') and
                   int(r['scopus_result'].get('citations', 0)) > 500]
    if high_impact:
        print(f"\nHIGH-IMPACT CITATIONS (>500 Scopus citations):")
        for r in sorted(high_impact, key=lambda x: int(x['scopus_result'].get('citations', 0)), reverse=True):
            print(f"  - {r['citation_key']}: {r['scopus_result']['citations']} citations")
            print(f"    {r['scopus_result']['title'][:70]}...")

    # Save detailed results
    output_file = BASE_DIR / "06_output" / "results" / "scopus_verification_report.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump({
            'summary': {
                'total_citations': len(citations),
                'verified_count': verified_count,
                'verification_rate': f"{100*verified_count/len(citations):.1f}%",
                'high_impact_count': high_impact_count
            },
            'results': results
        }, f, indent=2)

    print(f"\n✓ Detailed results saved to: {output_file}")

    # Generate text report
    text_output = BASE_DIR / "06_output" / "results" / "scopus_verification_report.txt"

    with open(text_output, 'w') as f:
        f.write("SCOPUS REFERENCE VERIFICATION REPORT\n")
        f.write("="*70 + "\n\n")
        f.write(f"Total Citations: {len(citations)}\n")
        f.write(f"Verified in Scopus: {verified_count} ({100*verified_count/len(citations):.1f}%)\n")
        f.write(f"Not Found: {len(citations) - verified_count}\n")
        f.write(f"High-Impact (>500 citations): {high_impact_count}\n\n")

        if not_found:
            f.write(f"NOT FOUND ({len(not_found)}):\n")
            for r in not_found:
                f.write(f"  {r['citation_key']}: {r['scopus_result'].get('error', 'Unknown')}\n")
            f.write("\n")

        f.write("ALL VERIFIED CITATIONS:\n")
        f.write("-"*70 + "\n")
        for r in [x for x in results if x['scopus_result']['found']]:
            f.write(f"\n{r['citation_key']}:\n")
            f.write(f"  Title: {r['scopus_result']['title']}\n")
            f.write(f"  Authors: {r['scopus_result'].get('authors', 'N/A')}\n")
            f.write(f"  Journal: {r['scopus_result'].get('journal', 'N/A')}\n")
            f.write(f"  Year: {r['scopus_result'].get('year', 'N/A')}\n")
            f.write(f"  Citations: {r['scopus_result'].get('citations', 0)}\n")
            if 'doi' in r['scopus_result']:
                f.write(f"  DOI: {r['scopus_result']['doi']}\n")

    print(f"✓ Text report saved to: {text_output}")

    return results

def main():
    """Main execution"""

    # Load extracted citations
    citations_file = BASE_DIR / "04_code" / "06_review" / "citations_extracted.txt"

    print("Loading extracted citations...")

    # Parse citations from file
    citations = []
    with open(citations_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('=') and not line.startswith('UNIQUE'):
                # Extract citation key (format: "1. CitationKey (cited X time(s))")
                import re
                match = re.search(r'\d+\.\s+(\w+)', line)
                if match:
                    citations.append(match.group(1))

    print(f"Found {len(citations)} citations to verify")

    # Verify with Scopus
    api_key = os.getenv("SCOPUS_API_KEY")

    if not api_key:
        print("ERROR: SCOPUS_API_KEY not found in .env file")
        return

    results = verify_all_references(citations, api_key)

    print("\n" + "="*70)
    print("VERIFICATION COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
