# Multi-Agent Peer Review & Reference Verification Plan
**Date**: 2025-12-31
**Purpose**: Rigorous manuscript review using three AI agents + Scopus reference verification
**Status**: Planning Phase

---

## Executive Summary

This plan implements a multi-agent review system using:
1. **OpenAI GPT-4o** - Healthcare Economics Reviewer
2. **Anthropic Claude Opus 4.5** - Corporate Finance Reviewer
3. **Google Gemini 3 Pro** - Methodological Rigor Reviewer
4. **Scopus API** - Reference verification and formatting validation

**Total Review Stages**: 4 (API Verification → Agent Reviews → Reference Verification → Synthesis)
**Estimated Time**: 3-4 hours
**Output**: Comprehensive review report with actionable recommendations

---

## Phase 1: API Key Verification (30 minutes)

### Objective
Verify all API keys are valid and have sufficient quota before initiating expensive review operations.

### Available API Keys (from .env)

| Provider | API Key | Model | Purpose |
|----------|---------|-------|---------|
| **OpenAI** | `sk-proj-Fla66...` | `gpt-4o-mini` (cost-optimized) | Healthcare Economics Review |
| **Anthropic** | `sk-ant-api03-Rdv2...` | `claude-opus-4-5-20251101` (max intelligence) | Corporate Finance Review |
| **Google Gemini** | `AQ.Ab8RN6LXFWt...` | `gemini-3-pro-preview` | Methodological Rigor Review |
| **Scopus** | `794f87fe4933b144...` | N/A (REST API) | Reference verification |

### Verification Tests

#### Test 1: OpenAI API Verification
```python
import openai
import os

def verify_openai_api():
    """Test OpenAI API connectivity and quota"""
    try:
        client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("OPENAI_ORG_ID"),
            project=os.getenv("OPENAI_PROJECT_ID")
        )

        # Test with minimal request
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=10
        )

        return {
            'status': 'SUCCESS',
            'model': 'gpt-4o-mini',
            'response_time': '...',
            'quota_remaining': 'Check via dashboard'
        }
    except Exception as e:
        return {'status': 'FAILED', 'error': str(e)}
```

**Expected Output**:
```
✅ OpenAI API: VERIFIED
   Model: gpt-4o-mini
   Latency: <500ms
   Organization: org-RbVgiMqQqSxPBAVmqkk8bQRw
   Project: proj_VGA53L7hvdS2YVvqHJ2Uu1lM
```

#### Test 2: Anthropic API Verification
```python
import anthropic

def verify_anthropic_api():
    """Test Anthropic API connectivity"""
    try:
        client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        # Test with minimal request
        response = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=10,
            messages=[{"role": "user", "content": "Test"}]
        )

        return {
            'status': 'SUCCESS',
            'model': 'claude-opus-4-5-20251101',
            'response_time': '...',
            'tokens_used': response.usage.total_tokens
        }
    except Exception as e:
        return {'status': 'FAILED', 'error': str(e)}
```

**Expected Output**:
```
✅ Anthropic API: VERIFIED
   Model: claude-opus-4-5-20251101
   Latency: <1000ms
   Tokens: 10 input + 10 output
```

#### Test 3: Gemini API Verification
```python
import google.generativeai as genai

def verify_gemini_api():
    """Test Gemini API connectivity"""
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-3-pro-preview')

        # Test with minimal request
        response = model.generate_content("Test",
            generation_config={'max_output_tokens': 10})

        return {
            'status': 'SUCCESS',
            'model': 'gemini-3-pro-preview',
            'response_time': '...',
            'response': response.text
        }
    except Exception as e:
        return {'status': 'FAILED', 'error': str(e)}
```

**Expected Output**:
```
✅ Gemini API: VERIFIED
   Model: gemini-3-pro-preview
   Latency: <800ms
   Response: [test output]
```

#### Test 4: Scopus API Verification
```python
import requests

def verify_scopus_api():
    """Test Scopus API connectivity and quota"""
    try:
        api_key = os.getenv("SCOPUS_API_KEY")
        headers = {
            'X-ELS-APIKey': api_key,
            'Accept': 'application/json'
        }

        # Test with single document lookup
        test_doi = "10.1016/j.jfineco.2023.103737"
        url = f"https://api.elsevier.com/content/search/scopus?query=DOI({test_doi})"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            quota = response.headers.get('X-RateLimit-Remaining', 'Unknown')
            return {
                'status': 'SUCCESS',
                'quota_remaining': quota,
                'weekly_limit': response.headers.get('X-RateLimit-Limit', 'Unknown'),
                'test_result': data.get('search-results', {}).get('opensearch:totalResults', 0)
            }
        else:
            return {'status': 'FAILED', 'error': f"HTTP {response.status_code}"}
    except Exception as e:
        return {'status': 'FAILED', 'error': str(e)}
```

**Expected Output**:
```
✅ Scopus API: VERIFIED
   Quota Remaining: 5000/5000 weekly requests
   Test Query: Found 1 result for test DOI
   Rate Limit: 9 requests/second
```

### Verification Script Implementation

**File**: `04_code/06_review/01_verify_api_keys.py`

```python
#!/usr/bin/env python3
"""
API Key Verification Script
Verifies all API keys before initiating multi-agent review

Author: Research Team
Date: 2025-12-31
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
import openai
import anthropic
import google.generativeai as genai
import requests

# Load environment variables
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

def verify_all_apis():
    """Run all API verification tests"""

    print("="*70)
    print("API KEY VERIFICATION")
    print("="*70)

    results = {}

    # Test 1: OpenAI
    print("\n[1/4] Verifying OpenAI API...")
    results['openai'] = verify_openai_api()
    print(f"  Status: {results['openai']['status']}")

    # Test 2: Anthropic
    print("\n[2/4] Verifying Anthropic API...")
    results['anthropic'] = verify_anthropic_api()
    print(f"  Status: {results['anthropic']['status']}")

    # Test 3: Gemini
    print("\n[3/4] Verifying Gemini API...")
    results['gemini'] = verify_gemini_api()
    print(f"  Status: {results['gemini']['status']}")

    # Test 4: Scopus
    print("\n[4/4] Verifying Scopus API...")
    results['scopus'] = verify_scopus_api()
    print(f"  Status: {results['scopus']['status']}")

    # Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)

    all_success = all(r['status'] == 'SUCCESS' for r in results.values())

    if all_success:
        print("✅ ALL API KEYS VERIFIED - Ready to proceed")
        return True
    else:
        print("❌ VERIFICATION FAILED - Fix errors before proceeding:")
        for api, result in results.items():
            if result['status'] == 'FAILED':
                print(f"  - {api.upper()}: {result.get('error', 'Unknown error')}")
        return False

if __name__ == "__main__":
    success = verify_all_apis()
    sys.exit(0 if success else 1)
```

### Contingency Plans

**If OpenAI fails**: Use Anthropic Haiku as backup (faster, cheaper)
**If Anthropic fails**: Use OpenAI GPT-4 as backup
**If Gemini fails**: Use HuggingFace Llama 3.1 (requires different setup)
**If Scopus fails**: Manual reference verification using CrossRef API

---

## Phase 2: Multi-Agent Review System (2 hours)

### Review Agent Specifications

#### Agent 1: Healthcare Economics Reviewer (OpenAI GPT-4o-mini)

**Role**: Evaluate healthcare-specific contributions and policy relevance

**Expertise Areas**:
- Healthcare financing and reimbursement mechanisms
- Public hospital management and governance
- Health system performance measurement
- Healthcare policy in Beveridgean systems (NHS, SNS, etc.)

**Review Criteria** (20 items):
1. **Conceptual Contribution**: Does PHFSI advance healthcare finance measurement?
2. **Policy Relevance**: Are ULS integration insights actionable?
3. **Context Appropriateness**: Is SNS institutional context adequately explained?
4. **Quality Metrics**: Are CQMI components (mortality, length of stay) appropriate?
5. **Payment Mechanism Analysis**: Is DRG/subsidy discussion accurate?
6. **Comparative Context**: Does paper position Portuguese SNS vs other Beveridgean systems?
7. **Clinical Relevance**: Are quality degradation mechanisms clinically plausible?
8. **Supplier Dynamics**: Is healthcare supply chain analysis realistic?
9. **Staff Implications**: Are workforce retention/turnover mechanisms validated?
10. **Patient Impact**: Are quality deterioration consequences adequately documented?
11. **ULS Reform Assessment**: Is integration reform analysis credible?
12. **Replicability**: Can PHFSI be adapted to Spain, Italy, Greece, UK?
13. **Data Appropriateness**: Are SNS Transparency Portal metrics suitable?
14. **Outcome Metrics**: Are mortality/readmission rates correctly interpreted?
15. **Efficiency Measures**: Is length of stay a valid efficiency proxy?
16. **Subsidy Classification**: Are operating subsidies vs capital transfers correctly distinguished?
17. **Budget Constraint Mechanisms**: Is soft budget constraint theory correctly applied to healthcare?
18. **Political Economy**: Are bailout dynamics politically realistic?
19. **Regulatory Environment**: Is Portuguese hospital regulation accurately described?
20. **Healthcare Literature**: Are key healthcare finance papers adequately cited?

**Prompt Template**:
```
You are a senior healthcare economist reviewing a manuscript for Health Care Management Science.

MANUSCRIPT CONTEXT:
- Title: Public Hospital Financial Sustainability Index (PHFSI) for Soft Budget Constraint Environments
- Setting: Portuguese National Health Service (SNS), 2017-2024
- Method: Panel econometrics + Granger causality + Difference-in-differences
- Key Contribution: PHFSI composite measure for public hospital distress prediction

REVIEW TASK:
Evaluate the manuscript across 20 healthcare-specific criteria. For each:
1. Score 1-5 (1=Major Revision Needed, 5=Excellent)
2. Provide 2-3 sentence justification
3. Suggest specific improvements

Focus on:
- Healthcare finance accuracy
- Policy relevance and actionability
- Clinical plausibility
- Institutional context appropriateness
- Generalizability to other healthcare systems

MANUSCRIPT SECTIONS TO REVIEW:
[Introduction, Theory, Methods, Results, Discussion]

OUTPUT FORMAT:
## Healthcare Economics Review

### Summary Assessment
[Overall evaluation in 200 words]

### Detailed Criteria Scores
1. Conceptual Contribution: [Score]/5
   Justification: ...
   Improvement: ...

[Repeat for all 20 criteria]

### Major Strengths (Top 3)
### Critical Weaknesses (Top 3)
### Recommended Decision: [Accept / Minor Revision / Major Revision / Reject]
```

#### Agent 2: Corporate Finance Reviewer (Anthropic Claude Opus 4.5)

**Role**: Evaluate corporate finance theory and econometric methodology

**Expertise Areas**:
- Financial distress prediction models (Altman Z-score, Ohlson, etc.)
- Soft budget constraint theory (Kornai, Maskin, Dewatripont)
- Capital structure theory (Myers, trade-off, pecking order)
- Panel econometrics and causal inference (fixed effects, DiD, IV)

**Review Criteria** (20 items):
1. **Theoretical Framework**: Is soft budget constraint theory correctly applied?
2. **Distress Reconceptualization**: Does stakeholder-distributed distress advance theory?
3. **Capital Structure Logic**: Is zero-leverage prediction valid?
4. **Pecking Order Extension**: Is "subsidies → retained earnings → supplier credit" formalization correct?
5. **Altman Z-score Comparison**: Is criticism of traditional models justified?
6. **PHFSI Construction**: Are component weights theoretically justified?
7. **Normalization**: Are component normalization procedures valid?
8. **Composite Index**: Is equal-weighting approach defensible vs PCA/factor analysis?
9. **Panel Regression**: Are fixed effects specifications appropriate?
10. **Endogeneity**: Is subsidy dependence potentially endogenous? Are instruments needed?
11. **Standard Errors**: Are clustered SEs at hospital level sufficient?
12. **Granger Causality**: Is temporal precedence evidence convincing?
13. **Difference-in-Differences**: Are parallel trends assumptions validated?
14. **Event Study**: Is pre-reform improvement (2023) adequately explained?
15. **Robustness Checks**: Are 8 specifications sufficient?
16. **Sample Selection**: Is survivorship bias a concern (only active hospitals)?
17. **External Validity**: Does single-country focus limit generalizability?
18. **Measurement Error**: Are quality metrics (mortality, LOS) subject to reporting bias?
19. **Identification Strategy**: Is subsidy-distress relationship causal or correlational?
20. **Finance Literature**: Are canonical finance papers (Myers, Altman, Ohlson) adequately engaged?

**Prompt Template**:
```
You are a corporate finance professor reviewing a manuscript for Health Care Management Science.

MANUSCRIPT FOCUS:
- Reconceptualizing financial distress in soft budget constraint environments
- Extending Kornai (1986) soft budget constraint theory to healthcare
- Panel econometrics: Fixed effects, Granger causality, DiD

THEORETICAL CLAIMS:
1. Traditional distress models (Altman Z-score) fail for public hospitals
2. Distress distributes across stakeholders sequentially (not concentrated at bankruptcy)
3. Optimal leverage = 0 when bankruptcy costs = infinity, tax benefits = 0
4. Subsidy dependence → moral hazard → debt accumulation

EMPIRICAL STRATEGY:
- PHFSI = f(OSSR, SPI, LRR, TLR, CQMI) with equal weights
- Panel regression: PHFSI ~ subsidy dependence + controls + hospital FE + year FE
- Granger causality: Payment delays → Financial deterioration (92.9% significant)
- DiD: ULS integration → PHFSI improvement

REVIEW TASK:
Evaluate theoretical rigor and econometric validity across 20 criteria.

Focus on:
- Theoretical coherence and novelty
- Econometric identification
- Causality vs correlation
- Robustness and external validity

OUTPUT FORMAT:
## Corporate Finance Review

### Summary Assessment
[Overall evaluation in 200 words]

### Detailed Criteria Scores
[1-20 as above]

### Theoretical Contributions (Strengths/Weaknesses)
### Methodological Rigor (Strengths/Weaknesses)
### Recommended Decision: [Accept / Minor Revision / Major Revision / Reject]
```

#### Agent 3: Methodological Rigor Reviewer (Gemini 3 Pro)

**Role**: Evaluate statistical methodology, data quality, and reproducibility

**Expertise Areas**:
- Time series econometrics (Granger causality, cointegration, stationarity)
- Panel data methods (fixed effects, random effects, dynamic panels)
- Causal inference (DiD, RDD, instrumental variables, matching)
- Data quality assessment and measurement validation

**Review Criteria** (20 items):
1. **Sample Size**: Are 741 hospital-years sufficient for panel estimation?
2. **Unbalanced Panel**: How does entity attrition affect estimates?
3. **Stationarity**: Are Granger causality tests on stationary series?
4. **Lag Selection**: Is 1-3 month lag structure for Granger tests justified?
5. **Multicollinearity**: Are PHFSI components correlated? Does this affect regressions?
6. **Heteroskedasticity**: Are errors homoskedastic or robust SEs needed?
7. **Serial Correlation**: Is Durbin-Watson test reported for panel errors?
8. **Fixed vs Random Effects**: Is Hausman test conducted?
9. **Time Fixed Effects**: Are year FE sufficient or should month FE be used?
10. **Cluster Robustness**: Should SEs be two-way clustered (hospital + year)?
11. **Parallel Trends**: Is DiD assumption graphically demonstrated?
12. **Event Study Lags**: Are leads/lags (-3, -2, -1, 0, +1, +2, +3) reported?
13. **Placebo Tests**: Are alternative event dates tested?
14. **Permutation Tests**: Is statistical significance robust to randomization inference?
15. **Missing Data**: How are missing CQMI values (pre-2019) handled?
16. **Outliers**: Are extreme values (payment delays, debt ratios) winsorized?
17. **Data Quality**: Are SNS Transparency Portal metrics audited?
18. **Reproducibility**: Is code/data available for replication?
19. **Power Analysis**: Is sample size sufficient to detect hypothesized effects?
20. **Multiple Testing**: Are p-values corrected for multiple comparisons (8 robustness checks)?

**Prompt Template**:
```
You are a quantitative methodologist reviewing a manuscript for Health Care Management Science.

DATA CONTEXT:
- Sample: 741 hospital-years, 149 entities (unbalanced panel)
- Timespan: 2017-2024 (monthly for payment delays, annual for quality metrics)
- Sources: SNS Transparency Portal (administrative data)

STATISTICAL METHODS:
1. Panel regressions: Two-way fixed effects (hospital + year), clustered SEs
2. Granger causality: Monthly time series, max 6-month lags, ADF stationarity tests
3. Difference-in-Differences: ULS integration reform (2024 treatment)
4. Robustness: 8 specifications (alternative samples, SEs, specifications)

MEASUREMENT:
- PHFSI: 5-component composite (equal-weighted, normalized to [0,1])
- Components: OSSR, SPI, LRR, TLR, CQMI
- Key variables: Subsidy dependence, payment delays, mortality rates, length of stay

REVIEW TASK:
Assess statistical validity, data quality, and reproducibility across 20 criteria.

Focus on:
- Econometric assumptions (stationarity, heteroskedasticity, serial correlation)
- Causal identification (parallel trends, exogeneity, confounders)
- Data quality and measurement error
- Reproducibility and transparency

OUTPUT FORMAT:
## Methodological Rigor Review

### Summary Assessment
[Overall evaluation in 200 words]

### Detailed Criteria Scores
[1-20 as above]

### Statistical Strengths (Top 3)
### Critical Methodological Concerns (Top 3)
### Data Quality Assessment
### Reproducibility Rating: [High / Medium / Low]
### Recommended Decision: [Accept / Minor Revision / Major Revision / Reject]
```

### Agent Coordination Strategy

**Sequential Review** (not parallel) to allow later agents to respond to earlier critiques:

1. **Stage 1** (30 min): Healthcare Economics Reviewer (GPT-4o-mini)
   - Fast model, healthcare-specific focus
   - Output: 20 scored criteria + narrative review

2. **Stage 2** (45 min): Corporate Finance Reviewer (Claude Opus 4.5)
   - Maximum intelligence model for theoretical depth
   - Output: 20 scored criteria + theoretical assessment

3. **Stage 3** (30 min): Methodological Rigor Reviewer (Gemini 3 Pro)
   - Technical statistical review
   - Output: 20 scored criteria + data quality report

4. **Stage 4** (15 min): Meta-Review Synthesis (Claude Opus 4.5)
   - Aggregate three reviews
   - Identify consensus strengths/weaknesses
   - Prioritize revisions by impact × feasibility

---

## Phase 3: Reference Verification (1 hour)

### Scopus API Reference Validation

**Objective**: Verify all citations exist in Scopus database and are correctly formatted

#### Step 1: Extract Citations from Manuscript

**Script**: `04_code/06_review/02_extract_citations.py`

```python
import re
from pathlib import Path

def extract_citations(tex_content):
    """Extract all \cite{} and \citep{} references"""

    # Match \cite{key}, \citep{key}, \citet{key}
    pattern = r'\\cite[tp]?\{([^}]+)\}'
    matches = re.findall(pattern, tex_content)

    # Split multiple citations (e.g., \cite{A,B,C})
    citations = []
    for match in matches:
        citations.extend([c.strip() for c in match.split(',')])

    return list(set(citations))  # Deduplicate

def extract_all_citations(sections_dir):
    """Extract citations from all .tex files"""

    all_citations = []

    for tex_file in sections_dir.glob("*.tex"):
        content = tex_file.read_text()
        citations = extract_citations(content)
        all_citations.extend(citations)

    return sorted(set(all_citations))
```

**Expected Output**:
```
Found 48 unique citations:
- Altman1968
- Baker2002
- Barboza2017
- Barros2013
- Barros2023ULS
- Bebchuk1988
...
```

#### Step 2: Map Citations to DOIs

**Challenge**: BibTeX keys (e.g., `Altman1968`) need to be mapped to DOIs for Scopus lookup

**Solution**: Parse references.bib OR construct search queries from citation keys

```python
def parse_bibtex_entry(entry):
    """Extract key, author, year, title, DOI from BibTeX entry"""

    # Example entry:
    # @article{Altman1968,
    #   author = {Altman, Edward I.},
    #   title = {Financial Ratios, Discriminant Analysis...},
    #   journal = {The Journal of Finance},
    #   year = {1968},
    #   doi = {10.1111/j.1540-6261.1968.tb00843.x}
    # }

    doi_match = re.search(r'doi\s*=\s*\{([^}]+)\}', entry)
    title_match = re.search(r'title\s*=\s*\{([^}]+)\}', entry)
    author_match = re.search(r'author\s*=\s*\{([^}]+)\}', entry)
    year_match = re.search(r'year\s*=\s*\{([^}]+)\}', entry)

    return {
        'doi': doi_match.group(1) if doi_match else None,
        'title': title_match.group(1) if title_match else None,
        'author': author_match.group(1) if author_match else None,
        'year': year_match.group(1) if year_match else None
    }
```

#### Step 3: Scopus Lookup

**Script**: `04_code/06_review/03_verify_references_scopus.py`

```python
import requests
import time
import json

def lookup_scopus_by_doi(doi, api_key):
    """Lookup reference in Scopus by DOI"""

    url = f"https://api.elsevier.com/content/search/scopus?query=DOI({doi})"
    headers = {
        'X-ELS-APIKey': api_key,
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        results = data.get('search-results', {}).get('entry', [])

        if len(results) > 0:
            return {
                'found': True,
                'title': results[0].get('dc:title', ''),
                'authors': results[0].get('dc:creator', ''),
                'year': results[0].get('prism:coverDate', '')[:4],
                'journal': results[0].get('prism:publicationName', ''),
                'citations': results[0].get('citedby-count', 0),
                'scopus_id': results[0].get('dc:identifier', '')
            }
        else:
            return {'found': False, 'error': 'No results'}
    else:
        return {'found': False, 'error': f'HTTP {response.status_code}'}

def lookup_scopus_by_title(title, author, year, api_key):
    """Fallback: Lookup by title + author if DOI missing"""

    # Construct query
    query = f'TITLE("{title}")'
    if author:
        query += f' AND AUTHOR-NAME({author.split(",")[0].strip()})'
    if year:
        query += f' AND PUBYEAR IS {year}'

    url = f"https://api.elsevier.com/content/search/scopus?query={query}"
    headers = {
        'X-ELS-APIKey': api_key,
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    # [Similar parsing as lookup_by_doi]

def verify_all_references(citations, bibtex_data, api_key):
    """Verify all citations against Scopus"""

    results = []

    for i, citation_key in enumerate(citations):
        print(f"[{i+1}/{len(citations)}] Verifying {citation_key}...")

        bib_entry = bibtex_data.get(citation_key, {})

        # Try DOI lookup first
        if bib_entry.get('doi'):
            result = lookup_scopus_by_doi(bib_entry['doi'], api_key)
        else:
            # Fallback to title/author/year
            result = lookup_scopus_by_title(
                bib_entry.get('title', ''),
                bib_entry.get('author', ''),
                bib_entry.get('year', ''),
                api_key
            )

        results.append({
            'citation_key': citation_key,
            'bibtex': bib_entry,
            'scopus': result
        })

        # Rate limiting: 9 requests/second max
        time.sleep(0.15)

    return results
```

**Expected Output**:
```
REFERENCE VERIFICATION REPORT
==================================================

Total Citations: 48
Verified in Scopus: 45 (93.8%)
Not Found: 3 (6.2%)

NOT FOUND IN SCOPUS:
1. Barros2023ULS - "Portuguese ULS Integration Reform"
   Issue: Too recent, not yet indexed
   Recommendation: Cite government report instead

2. MinisterioFinancas2024 - "€500M Capital Injection Announcement"
   Issue: Government press release, not academic publication
   Recommendation: Keep as grey literature citation

3. ACSS2023 - "SNS Financial Transparency Portal"
   Issue: Data repository, not publication
   Recommendation: Keep as data source citation

HIGH-IMPACT CITATIONS (>500 Scopus citations):
- Altman1968: 15,234 citations ✅
- Kornai1986: 3,421 citations ✅
- Myers1984: 8,765 citations ✅
- Maskin1999: 1,234 citations ✅

FORMATTING ISSUES DETECTED:
- Citation 12 (Duggan2000): Author name inconsistent (Duggan vs Duggan, M.)
- Citation 28 (Propper2008): Journal name abbreviated incorrectly
- Citation 35 (Gaynor2015): Year mismatch (2015 in key, 2016 in Scopus)

RECOMMENDATIONS:
✅ 45/48 citations verified (93.8% - EXCELLENT)
⚠️ 3 formatting inconsistencies to correct
📊 Average citation count: 287 (indicates high-quality literature base)
```

#### Step 4: Reference Formatting Validation

**Check**:
1. Author names consistent (LastName, FirstInitial format)
2. Journal names match official abbreviations
3. Years match between citation key and publication year
4. DOIs present for all journal articles (post-2000)
5. Page numbers included
6. Volume/Issue numbers correct

**Script**: `04_code/06_review/04_check_bibtex_formatting.py`

```python
def validate_bibtex_formatting(bibtex_entries):
    """Check BibTeX entries for formatting consistency"""

    issues = []

    for key, entry in bibtex_entries.items():
        # Check 1: Author format
        if 'author' in entry:
            authors = entry['author']
            if ' and ' in authors:
                # Check each author is "Last, First" format
                for author in authors.split(' and '):
                    if ',' not in author:
                        issues.append({
                            'key': key,
                            'field': 'author',
                            'issue': f'Author "{author}" not in "Last, First" format',
                            'severity': 'MINOR'
                        })

        # Check 2: Required fields by entry type
        if entry['type'] == 'article':
            required = ['author', 'title', 'journal', 'year']
            recommended = ['volume', 'pages', 'doi']

            for field in required:
                if field not in entry:
                    issues.append({
                        'key': key,
                        'field': field,
                        'issue': f'Missing required field: {field}',
                        'severity': 'MAJOR'
                    })

            for field in recommended:
                if field not in entry:
                    issues.append({
                        'key': key,
                        'field': field,
                        'issue': f'Missing recommended field: {field}',
                        'severity': 'MINOR'
                    })

        # Check 3: Year consistency
        if 'year' in entry and key[-4:].isdigit():
            key_year = key[-4:]
            entry_year = entry['year']
            if key_year != entry_year:
                issues.append({
                    'key': key,
                    'field': 'year',
                    'issue': f'Year mismatch: key has {key_year}, entry has {entry_year}',
                    'severity': 'MAJOR'
                })

        # Check 4: DOI format
        if 'doi' in entry:
            doi = entry['doi']
            if not doi.startswith('10.'):
                issues.append({
                    'key': key,
                    'field': 'doi',
                    'issue': f'DOI should start with "10.": {doi}',
                    'severity': 'MINOR'
                })

    return issues
```

---

## Phase 4: Review Synthesis (30 minutes)

### Aggregation Strategy

**Script**: `04_code/06_review/05_synthesize_reviews.py`

```python
def synthesize_reviews(healthcare_review, finance_review, methods_review):
    """Aggregate three agent reviews into unified report"""

    # Calculate average scores per criterion type
    avg_scores = {
        'healthcare': calculate_average_score(healthcare_review),
        'finance': calculate_average_score(finance_review),
        'methods': calculate_average_score(methods_review)
    }

    # Identify consensus issues (flagged by 2+ reviewers)
    consensus_issues = find_consensus_issues([
        healthcare_review,
        finance_review,
        methods_review
    ])

    # Prioritize revisions
    revision_priorities = prioritize_revisions(consensus_issues)

    # Generate synthesis report
    report = f"""
    MULTI-AGENT REVIEW SYNTHESIS
    ====================================================

    OVERALL ASSESSMENT:
    - Healthcare Economics: {avg_scores['healthcare']}/5 ({"STRONG" if avg_scores['healthcare'] >= 4 else "ACCEPTABLE" if avg_scores['healthcare'] >= 3 else "WEAK"})
    - Corporate Finance: {avg_scores['finance']}/5 ({"STRONG" if avg_scores['finance'] >= 4 else "ACCEPTABLE" if avg_scores['finance'] >= 3 else "WEAK"})
    - Methodological Rigor: {avg_scores['methods']}/5 ({"STRONG" if avg_scores['methods'] >= 4 else "ACCEPTABLE" if avg_scores['methods'] >= 3 else "WEAK"})

    CONSENSUS STRENGTHS (Identified by all 3 reviewers):
    {format_consensus_items(consensus_issues['strengths'])}

    CONSENSUS WEAKNESSES (Identified by 2+ reviewers):
    {format_consensus_items(consensus_issues['weaknesses'])}

    PRIORITIZED REVISION ROADMAP:

    HIGH PRIORITY (Address before submission):
    {format_revision_list(revision_priorities['high'])}

    MEDIUM PRIORITY (Address in revision round):
    {format_revision_list(revision_priorities['medium'])}

    LOW PRIORITY (Nice-to-have):
    {format_revision_list(revision_priorities['low'])}

    REFERENCE VERIFICATION:
    - Scopus Verified: {scopus_results['verified_count']}/48 (93.8%)
    - Formatting Issues: {scopus_results['formatting_issues']} MINOR corrections needed

    RECOMMENDED DECISION:
    {calculate_recommendation(avg_scores, consensus_issues)}

    ESTIMATED REVISION TIME:
    - High Priority: 8-12 hours
    - Medium Priority: 4-6 hours
    - Total: 12-18 hours before resubmission
    """

    return report
```

### Output Files

1. **01_healthcare_economics_review.md** (GPT-4o-mini output)
2. **02_corporate_finance_review.md** (Claude Opus output)
3. **03_methodological_rigor_review.md** (Gemini 3 Pro output)
4. **04_reference_verification_report.md** (Scopus API output)
5. **05_synthesis_report.md** (Meta-review aggregation)

---

## Implementation Timeline

| Phase | Task | Duration | Dependencies |
|-------|------|----------|--------------|
| **Phase 1** | API Verification | 30 min | .env file |
| **Phase 2.1** | Healthcare Economics Review (GPT-4o) | 30 min | Phase 1 ✅ |
| **Phase 2.2** | Corporate Finance Review (Claude Opus) | 45 min | Phase 1 ✅ |
| **Phase 2.3** | Methodological Rigor Review (Gemini) | 30 min | Phase 1 ✅ |
| **Phase 3.1** | Extract Citations | 10 min | Phase 1 ✅ |
| **Phase 3.2** | Scopus Verification | 40 min | Phase 1 ✅, Phase 3.1 ✅ |
| **Phase 3.3** | Formatting Check | 10 min | Phase 3.2 ✅ |
| **Phase 4** | Review Synthesis | 30 min | Phases 2.1-2.3 ✅, Phase 3 ✅ |
| **TOTAL** | | **3.5 hours** | |

---

## Cost Estimate

### API Costs (Estimated)

| Provider | Model | Input Tokens | Output Tokens | Cost/1M Tokens | Estimated Cost |
|----------|-------|--------------|---------------|----------------|----------------|
| OpenAI | GPT-4o-mini | ~15,000 | ~5,000 | $0.15 / $0.60 | $0.03 |
| Anthropic | Claude Opus 4.5 | ~30,000 | ~10,000 | $15 / $75 | $1.20 |
| Gemini | Gemini 3 Pro | ~15,000 | ~5,000 | $1.25 / $5.00 | $0.04 |
| Scopus | API Calls | 48 requests | N/A | Free (5000/week quota) | $0.00 |
| **TOTAL** | | | | | **$1.27** |

**Note**: Extremely cost-effective for comprehensive peer review (manual peer review costs $500-1000/reviewer)

---

## Success Criteria

### Phase 1 (API Verification)
- ✅ All 4 APIs return successful test responses
- ✅ Scopus quota > 100 requests remaining
- ✅ No authentication errors

### Phase 2 (Agent Reviews)
- ✅ Each agent completes 20-criteria review
- ✅ Each agent provides narrative summary (200+ words)
- ✅ Each agent gives explicit decision recommendation
- ✅ Reviews identify at least 3 strengths and 3 weaknesses each

### Phase 3 (Reference Verification)
- ✅ >90% of citations verified in Scopus
- ✅ All missing citations explained (grey literature, data sources, etc.)
- ✅ Formatting issues documented with corrections
- ✅ High-impact citations (>500 Scopus citations) confirmed

### Phase 4 (Synthesis)
- ✅ Consensus strengths/weaknesses identified
- ✅ Revisions prioritized by impact × feasibility
- ✅ Estimated revision time provided
- ✅ Clear recommended decision (Accept/Revise/Reject)

---

## Contingency Plans

### If API Rate Limits Hit
- **OpenAI**: Switch to GPT-4o-mini (slower, same model)
- **Anthropic**: Switch to Claude Sonnet 4.5 (faster, slightly lower quality)
- **Gemini**: Retry with exponential backoff (5s, 10s, 20s delays)
- **Scopus**: Batch requests to stay under 9 requests/second limit

### If References.bib Missing
- **Fallback**: Extract citations from .tex files only
- **Manual Mapping**: Create citation → DOI mapping manually for top 20 cited papers
- **CrossRef Alternative**: Use CrossRef API (free) instead of Scopus

### If Review Quality Poor
- **GPT-4o-mini → GPT-4o**: Upgrade model if healthcare review lacks depth
- **Claude Opus → Re-prompt**: Refine prompt with more specific instructions
- **Gemini → Claude Haiku**: Switch if Gemini output is too generic

---

## Next Steps

1. **Execute Phase 1**: Run API verification script (`01_verify_api_keys.py`)
2. **If verification succeeds**: Proceed to Phase 2 (multi-agent reviews)
3. **If verification fails**: Debug API issues, check .env file, verify quotas
4. **Sequential Execution**: Complete phases 2→3→4 in order
5. **Generate Final Report**: Synthesize all reviews into actionable revision plan

---

**Ready to Execute**: Awaiting user approval to proceed with Phase 1 (API Verification)
