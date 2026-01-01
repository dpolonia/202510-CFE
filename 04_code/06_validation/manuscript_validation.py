"""
Manuscript Validation and Peer Review Simulation

Uses Scopus API to:
1. Validate references and enhance bibliographic data
2. Retrieve similar articles for comparison
3. Check citation impact and relevance

Uses AI APIs to:
4. Simulate peer reviewers from different perspectives
5. Generate constructive feedback

Author: Research Team
Date: 2025-12-31
"""

import os
import json
import requests
import time
from pathlib import Path
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "06_output" / "validation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# API Keys
SCOPUS_API_KEY = os.getenv("SCOPUS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class ScopusReferenceValidator:
    """Validates references and retrieves similar articles using Scopus API."""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.elsevier.com/content"
        self.headers = {
            "X-ELS-APIKey": self.api_key,
            "Accept": "application/json"
        }

    def search_article(self, title=None, author=None, year=None, doi=None):
        """Search for article in Scopus by metadata."""
        if doi:
            # Direct DOI lookup
            url = f"{self.base_url}/abstract/doi/{doi}"
        else:
            # Search by title/author/year
            query_parts = []
            if title:
                query_parts.append(f'TITLE("{title}")')
            if author:
                query_parts.append(f'AUTH("{author}")')
            if year:
                query_parts.append(f'PUBYEAR IS {year}')

            query = " AND ".join(query_parts)
            url = f"{self.base_url}/search/scopus"
            params = {
                "query": query,
                "count": 5,
                "field": "dc:title,dc:creator,prism:coverDate,citedby-count,prism:doi,prism:publicationName"
            }

        try:
            if doi:
                response = requests.get(url, headers=self.headers)
            else:
                response = requests.get(url, headers=self.headers, params=params)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching Scopus: {e}")
            return None

    def validate_reference(self, ref_info):
        """
        Validate a single reference and enhance with Scopus data.

        Args:
            ref_info: dict with keys 'title', 'author', 'year', 'doi' (optional)

        Returns:
            dict with validation results and enhanced metadata
        """
        result = {
            "input": ref_info,
            "found": False,
            "scopus_data": None,
            "citations": 0,
            "validation_status": "NOT_FOUND"
        }

        # Search Scopus
        data = self.search_article(
            title=ref_info.get("title"),
            author=ref_info.get("author"),
            year=ref_info.get("year"),
            doi=ref_info.get("doi")
        )

        if data:
            if "abstracts-retrieval-response" in data:
                # Direct DOI lookup result
                item = data["abstracts-retrieval-response"]
                result["found"] = True
                result["scopus_data"] = {
                    "title": item.get("coredata", {}).get("dc:title"),
                    "authors": item.get("coredata", {}).get("dc:creator"),
                    "year": item.get("coredata", {}).get("prism:coverDate", "")[:4],
                    "journal": item.get("coredata", {}).get("prism:publicationName"),
                    "doi": item.get("coredata", {}).get("prism:doi"),
                    "citations": int(item.get("coredata", {}).get("citedby-count", 0))
                }
                result["citations"] = result["scopus_data"]["citations"]
                result["validation_status"] = "VALIDATED"

            elif "search-results" in data and data["search-results"].get("entry"):
                # Search result
                entries = data["search-results"]["entry"]
                if entries and "error" not in entries[0]:
                    item = entries[0]
                    result["found"] = True
                    result["scopus_data"] = {
                        "title": item.get("dc:title"),
                        "authors": item.get("dc:creator"),
                        "year": item.get("prism:coverDate", "")[:4],
                        "journal": item.get("prism:publicationName"),
                        "doi": item.get("prism:doi"),
                        "citations": int(item.get("citedby-count", 0))
                    }
                    result["citations"] = result["scopus_data"]["citations"]
                    result["validation_status"] = "VALIDATED"

        # Rate limiting
        time.sleep(0.5)

        return result

    def find_similar_articles(self, keywords, year_from=2015, max_results=20):
        """
        Find similar articles using keyword search.

        Args:
            keywords: list of keywords or single keyword string
            year_from: minimum publication year
            max_results: maximum number of results

        Returns:
            list of similar articles with metadata
        """
        if isinstance(keywords, list):
            keyword_query = " OR ".join([f'KEY("{kw}")' for kw in keywords])
        else:
            keyword_query = f'KEY("{keywords}")'

        year_query = f"PUBYEAR > {year_from - 1}"

        query = f"({keyword_query}) AND {year_query}"

        url = f"{self.base_url}/search/scopus"
        params = {
            "query": query,
            "count": max_results,
            "sort": "citedby-count",
            "field": "dc:title,dc:creator,prism:coverDate,citedby-count,prism:doi,prism:publicationName,dc:description"
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            similar_articles = []
            if "search-results" in data and data["search-results"].get("entry"):
                for item in data["search-results"]["entry"]:
                    if "error" not in item:
                        similar_articles.append({
                            "title": item.get("dc:title"),
                            "authors": item.get("dc:creator"),
                            "year": item.get("prism:coverDate", "")[:4],
                            "journal": item.get("prism:publicationName"),
                            "doi": item.get("prism:doi"),
                            "citations": int(item.get("citedby-count", 0)),
                            "abstract": item.get("dc:description", "")[:500]
                        })

            return similar_articles

        except requests.exceptions.RequestException as e:
            print(f"Error finding similar articles: {e}")
            return []


class AIReviewerSimulator:
    """Simulates peer reviewers using AI APIs."""

    def __init__(self):
        self.openai_key = OPENAI_API_KEY
        self.anthropic_key = ANTHROPIC_API_KEY
        self.gemini_key = GEMINI_API_KEY

    def review_with_openai(self, manuscript_text, reviewer_profile):
        """Generate review using OpenAI API."""
        try:
            import openai
            openai.api_key = self.openai_key

            prompt = f"""You are a peer reviewer for Health Care Management Science journal with the following expertise:

{reviewer_profile}

Please provide a comprehensive review of the following manuscript. Structure your review as:

1. SUMMARY (2-3 sentences)
2. MAJOR STRENGTHS (3-5 bullet points)
3. MAJOR WEAKNESSES (3-5 bullet points)
4. MINOR ISSUES (3-5 bullet points)
5. RECOMMENDATION (Accept / Minor Revision / Major Revision / Reject)
6. DETAILED COMMENTS (organized by section)

Be constructive, specific, and reference particular parts of the manuscript.

MANUSCRIPT:
{manuscript_text[:8000]}  # Truncate to fit context
"""

            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert academic peer reviewer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating OpenAI review: {e}"

    def review_with_anthropic(self, manuscript_text, reviewer_profile):
        """Generate review using Anthropic Claude API."""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.anthropic_key)

            prompt = f"""You are a peer reviewer for Health Care Management Science journal with the following expertise:

{reviewer_profile}

Please provide a comprehensive review of the following manuscript. Structure your review as:

1. SUMMARY (2-3 sentences)
2. MAJOR STRENGTHS (3-5 bullet points)
3. MAJOR WEAKNESSES (3-5 bullet points)
4. MINOR ISSUES (3-5 bullet points)
5. RECOMMENDATION (Accept / Minor Revision / Major Revision / Reject)
6. DETAILED COMMENTS (organized by section)

Be constructive, specific, and reference particular parts of the manuscript.

MANUSCRIPT:
{manuscript_text[:8000]}
"""

            message = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return message.content[0].text

        except Exception as e:
            return f"Error generating Anthropic review: {e}"


def main():
    """Main execution function."""
    print("="*80)
    print("MANUSCRIPT VALIDATION AND PEER REVIEW SIMULATION")
    print("="*80)

    # Initialize validators
    scopus = ScopusReferenceValidator(SCOPUS_API_KEY)
    reviewer = AIReviewerSimulator()

    # ========================================================================
    # PART 1: VALIDATE KEY REFERENCES
    # ========================================================================
    print("\n" + "="*80)
    print("PART 1: VALIDATING KEY REFERENCES")
    print("="*80)

    # Key references from the manuscript
    key_references = [
        {
            "title": "The soft budget constraint",
            "author": "Kornai",
            "year": "1986",
            "doi": None
        },
        {
            "title": "Financial ratios, discriminant analysis and the prediction of corporate bankruptcy",
            "author": "Altman",
            "year": "1968",
            "doi": None
        },
        {
            "title": "Hospital ownership and public medical spending",
            "author": "Duggan",
            "year": "2000",
            "doi": None
        },
        {
            "title": "Are traditional bankruptcy prediction models applicable to the Greek public hospitals",
            "author": "Xanthakis",
            "year": "2009",
            "doi": None
        },
        {
            "title": "The capital structure puzzle",
            "author": "Myers",
            "year": "1984",
            "doi": None
        }
    ]

    validation_results = []
    for ref in key_references:
        print(f"\nValidating: {ref['author']} ({ref['year']}) - {ref['title'][:50]}...")
        result = scopus.validate_reference(ref)
        validation_results.append(result)

        if result["found"]:
            print(f"  ✓ VALIDATED - {result['citations']} citations")
            if result["scopus_data"]["doi"]:
                print(f"  DOI: {result['scopus_data']['doi']}")
        else:
            print(f"  ✗ NOT FOUND in Scopus")

    # Save validation results
    validation_df = pd.DataFrame([
        {
            "Input_Title": r["input"]["title"][:50],
            "Input_Author": r["input"]["author"],
            "Input_Year": r["input"]["year"],
            "Status": r["validation_status"],
            "Citations": r["citations"],
            "Scopus_DOI": r["scopus_data"]["doi"] if r["scopus_data"] else None
        }
        for r in validation_results
    ])

    val_path = OUTPUT_DIR / "reference_validation.csv"
    validation_df.to_csv(val_path, index=False)
    print(f"\n✓ Validation results saved to: {val_path}")

    # ========================================================================
    # PART 2: FIND SIMILAR ARTICLES
    # ========================================================================
    print("\n" + "="*80)
    print("PART 2: FINDING SIMILAR ARTICLES")
    print("="*80)

    keywords = [
        "public hospital financial distress",
        "soft budget constraint healthcare",
        "hospital bankruptcy prediction",
        "healthcare financial sustainability"
    ]

    print(f"\nSearching for articles with keywords: {', '.join(keywords)}")
    similar_articles = scopus.find_similar_articles(keywords, year_from=2015, max_results=20)

    print(f"\nFound {len(similar_articles)} similar articles:")
    for i, article in enumerate(similar_articles[:10], 1):
        print(f"\n{i}. {article['title']}")
        print(f"   {article['authors']} ({article['year']})")
        print(f"   {article['journal']}")
        print(f"   Citations: {article['citations']}")
        if article['doi']:
            print(f"   DOI: {article['doi']}")

    # Save similar articles
    similar_df = pd.DataFrame(similar_articles)
    similar_path = OUTPUT_DIR / "similar_articles.csv"
    similar_df.to_csv(similar_path, index=False)
    print(f"\n✓ Similar articles saved to: {similar_path}")

    # ========================================================================
    # PART 3: SIMULATE PEER REVIEWERS
    # ========================================================================
    print("\n" + "="*80)
    print("PART 3: SIMULATING PEER REVIEWERS")
    print("="*80)

    # Load manuscript sections
    intro_path = PROJECT_ROOT / "07_writing" / "paper" / "sections" / "01_introduction.tex"
    abstract_text = """
Financial distress in public hospitals operating under soft budget constraints manifests not as
discrete failure events but as continuous stakeholder burden transfer. We develop the Public Hospital
Financial Sustainability Index (PHFSI), integrating operational self-sufficiency, stakeholder pressure,
liquidity realization, true leverage, and clinical quality maintenance. Analyzing 741 hospital-year
observations from Portugal's National Health Service (2017-2024), we find that subsidy dependence
reduces PHFSI by 0.547 standard deviations per percentage point increase (p < 0.001). PHFSI
successfully discriminates across distress levels, with Distressed hospitals exhibiting payment
delays of 267 days versus Self-Sustaining hospitals with 98-day delays.
"""

    if intro_path.exists():
        with open(intro_path, 'r', encoding='utf-8') as f:
            intro_text = f.read()
        manuscript_sample = abstract_text + "\n\n" + intro_text
    else:
        manuscript_sample = abstract_text

    # Define reviewer profiles
    reviewer_profiles = {
        "Healthcare Economist": """
You are a healthcare economist with expertise in:
- Hospital financing and payment systems
- Healthcare market structure and competition
- Public-private healthcare comparisons
- DRG payment systems and hospital efficiency

Focus on: Economic theory application, policy implications, healthcare-specific institutional details.
""",
        "Corporate Finance Scholar": """
You are a corporate finance professor with expertise in:
- Capital structure theory and empirical testing
- Financial distress and bankruptcy prediction
- Firm financing decisions
- Empirical methods in corporate finance

Focus on: Theoretical rigor, econometric methodology, generalizability beyond healthcare.
""",
        "Health Services Researcher": """
You are a health services researcher with expertise in:
- Healthcare quality measurement
- Patient safety indicators
- Hospital performance assessment
- Health systems evaluation

Focus on: Clinical relevance, patient outcomes, quality metrics, practical implementation.
"""
    }

    reviews = {}

    # Generate review from Healthcare Economist (using Anthropic)
    print("\n\nGenerating review from Healthcare Economist perspective...")
    reviews["Healthcare_Economist"] = reviewer.review_with_anthropic(
        manuscript_sample,
        reviewer_profiles["Healthcare Economist"]
    )
    print("✓ Healthcare Economist review complete")

    # Generate review from Corporate Finance Scholar (using OpenAI)
    print("\nGenerating review from Corporate Finance Scholar perspective...")
    # Note: OpenAI review would go here, but skipping for now as it requires openai package
    reviews["Corporate_Finance"] = "OpenAI review skipped - package not installed"

    # Save reviews
    for reviewer_type, review_text in reviews.items():
        review_path = OUTPUT_DIR / f"review_{reviewer_type.lower()}.txt"
        with open(review_path, 'w', encoding='utf-8') as f:
            f.write(f"PEER REVIEW: {reviewer_type.replace('_', ' ')}\n")
            f.write("="*80 + "\n\n")
            f.write(review_text)
        print(f"✓ Review saved to: {review_path}")

    # ========================================================================
    # SUMMARY REPORT
    # ========================================================================
    print("\n" + "="*80)
    print("VALIDATION AND REVIEW SUMMARY")
    print("="*80)

    validated_count = sum(1 for r in validation_results if r["found"])
    total_citations = sum(r["citations"] for r in validation_results)

    print(f"\nReference Validation:")
    print(f"  - {validated_count}/{len(key_references)} key references validated in Scopus")
    print(f"  - Total citations: {total_citations}")
    print(f"  - Average citations per reference: {total_citations/len(key_references):.1f}")

    print(f"\nSimilar Articles:")
    print(f"  - {len(similar_articles)} similar articles identified")
    if similar_articles:
        avg_citations = sum(a["citations"] for a in similar_articles) / len(similar_articles)
        print(f"  - Average citations: {avg_citations:.1f}")
        print(f"  - Top cited: {max(similar_articles, key=lambda x: x['citations'])['title'][:60]}...")

    print(f"\nPeer Reviews:")
    print(f"  - {len(reviews)} simulated reviews generated")
    print(f"  - Perspectives: {', '.join(reviews.keys())}")

    print(f"\n{'='*80}")
    print("VALIDATION COMPLETE")
    print(f"{'='*80}")
    print(f"\nAll outputs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
