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

# Load environment variables
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

def verify_openai_api():
    """Test OpenAI API connectivity and quota"""
    try:
        import openai

        client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("OPENAI_ORG_ID"),
            project=os.getenv("OPENAI_PROJECT_ID")
        )

        # Test with minimal request
        start_time = time.time()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Test connection"}],
            max_tokens=10
        )
        latency = (time.time() - start_time) * 1000  # Convert to ms

        return {
            'status': 'SUCCESS',
            'model': 'gpt-4o-mini',
            'latency_ms': round(latency, 2),
            'tokens_used': response.usage.total_tokens,
            'organization': os.getenv("OPENAI_ORG_ID"),
            'project': os.getenv("OPENAI_PROJECT_ID")
        }
    except Exception as e:
        return {'status': 'FAILED', 'error': str(e)}

def verify_anthropic_api():
    """Test Anthropic API connectivity"""
    try:
        import anthropic

        client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        # Test with minimal request
        start_time = time.time()
        response = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=10,
            messages=[{"role": "user", "content": "Test connection"}]
        )
        latency = (time.time() - start_time) * 1000

        return {
            'status': 'SUCCESS',
            'model': 'claude-opus-4-5-20251101',
            'latency_ms': round(latency, 2),
            'input_tokens': response.usage.input_tokens,
            'output_tokens': response.usage.output_tokens
        }
    except Exception as e:
        return {'status': 'FAILED', 'error': str(e)}

def verify_gemini_api():
    """Test Gemini API connectivity"""
    try:
        import google.generativeai as genai

        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.0-flash')  # Use flash for testing

        # Test with minimal request
        start_time = time.time()
        response = model.generate_content(
            "Test connection",
            generation_config={'max_output_tokens': 10}
        )
        latency = (time.time() - start_time) * 1000

        return {
            'status': 'SUCCESS',
            'model': 'gemini-2.0-flash',
            'latency_ms': round(latency, 2),
            'response': response.text[:50] + '...' if len(response.text) > 50 else response.text
        }
    except Exception as e:
        return {'status': 'FAILED', 'error': str(e)}

def verify_scopus_api():
    """Test Scopus API connectivity and quota"""
    try:
        import requests

        api_key = os.getenv("SCOPUS_API_KEY")
        headers = {
            'X-ELS-APIKey': api_key,
            'Accept': 'application/json'
        }

        # Test with single document lookup (Altman 1968 - classic finance paper)
        test_doi = "10.1111/j.1540-6261.1968.tb00843.x"  # Altman Z-score paper
        url = f"https://api.elsevier.com/content/search/scopus?query=DOI({test_doi})"

        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=10)
        latency = (time.time() - start_time) * 1000

        if response.status_code == 200:
            data = response.json()
            quota_remaining = response.headers.get('X-RateLimit-Remaining', 'Unknown')
            quota_limit = response.headers.get('X-RateLimit-Limit', 'Unknown')
            reset_time = response.headers.get('X-RateLimit-Reset', 'Unknown')

            total_results = int(data.get('search-results', {}).get('opensearch:totalResults', 0))

            return {
                'status': 'SUCCESS',
                'quota_remaining': quota_remaining,
                'quota_limit': quota_limit,
                'reset_time': reset_time,
                'latency_ms': round(latency, 2),
                'test_result': f"Found {total_results} result(s) for Altman (1968)"
            }
        else:
            return {
                'status': 'FAILED',
                'error': f"HTTP {response.status_code}: {response.text[:200]}"
            }
    except Exception as e:
        return {'status': 'FAILED', 'error': str(e)}

def verify_all_apis():
    """Run all API verification tests"""

    print("="*70)
    print("API KEY VERIFICATION")
    print("="*70)

    results = {}

    # Test 1: OpenAI
    print("\n[1/4] Verifying OpenAI API...")
    results['openai'] = verify_openai_api()
    if results['openai']['status'] == 'SUCCESS':
        print(f"  ✅ Status: {results['openai']['status']}")
        print(f"     Model: {results['openai']['model']}")
        print(f"     Latency: {results['openai']['latency_ms']}ms")
        print(f"     Tokens: {results['openai']['tokens_used']}")
    else:
        print(f"  ❌ Status: FAILED")
        print(f"     Error: {results['openai']['error']}")

    # Test 2: Anthropic
    print("\n[2/4] Verifying Anthropic API...")
    results['anthropic'] = verify_anthropic_api()
    if results['anthropic']['status'] == 'SUCCESS':
        print(f"  ✅ Status: {results['anthropic']['status']}")
        print(f"     Model: {results['anthropic']['model']}")
        print(f"     Latency: {results['anthropic']['latency_ms']}ms")
        print(f"     Tokens: {results['anthropic']['input_tokens']} in + {results['anthropic']['output_tokens']} out")
    else:
        print(f"  ❌ Status: FAILED")
        print(f"     Error: {results['anthropic']['error']}")

    # Test 3: Gemini
    print("\n[3/4] Verifying Gemini API...")
    results['gemini'] = verify_gemini_api()
    if results['gemini']['status'] == 'SUCCESS':
        print(f"  ✅ Status: {results['gemini']['status']}")
        print(f"     Model: {results['gemini']['model']}")
        print(f"     Latency: {results['gemini']['latency_ms']}ms")
        print(f"     Response: {results['gemini']['response']}")
    else:
        print(f"  ❌ Status: FAILED")
        print(f"     Error: {results['gemini']['error']}")

    # Test 4: Scopus
    print("\n[4/4] Verifying Scopus API...")
    results['scopus'] = verify_scopus_api()
    if results['scopus']['status'] == 'SUCCESS':
        print(f"  ✅ Status: {results['scopus']['status']}")
        print(f"     Quota: {results['scopus']['quota_remaining']}/{results['scopus']['quota_limit']}")
        print(f"     Latency: {results['scopus']['latency_ms']}ms")
        print(f"     Test: {results['scopus']['test_result']}")
    else:
        print(f"  ❌ Status: FAILED")
        print(f"     Error: {results['scopus']['error']}")

    # Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)

    all_success = all(r['status'] == 'SUCCESS' for r in results.values())
    success_count = sum(1 for r in results.values() if r['status'] == 'SUCCESS')

    print(f"\nAPIs Verified: {success_count}/4")

    if all_success:
        print("\n✅ ALL API KEYS VERIFIED - Ready to proceed with multi-agent review")
        print("\nEstimated Costs:")
        print("  - OpenAI (GPT-4o-mini): ~$0.03 per review")
        print("  - Anthropic (Claude Opus): ~$1.20 per review")
        print("  - Gemini (Gemini 3 Pro): ~$0.04 per review")
        print("  - Scopus (48 references): $0.00 (within free quota)")
        print("  - TOTAL: ~$1.27 for complete review")
        return True
    else:
        print("\n❌ VERIFICATION FAILED - Fix errors before proceeding:")
        for api, result in results.items():
            if result['status'] == 'FAILED':
                print(f"\n  {api.upper()}:")
                print(f"    Error: {result.get('error', 'Unknown error')}")

                # Provide troubleshooting suggestions
                if 'authentication' in result.get('error', '').lower() or '401' in result.get('error', ''):
                    print(f"    Suggestion: Check API key in .env file")
                elif 'rate limit' in result.get('error', '').lower() or '429' in result.get('error', ''):
                    print(f"    Suggestion: Wait for rate limit reset or upgrade quota")
                elif 'timeout' in result.get('error', '').lower():
                    print(f"    Suggestion: Check internet connection")
                else:
                    print(f"    Suggestion: Verify API key is active and has sufficient credits")
        return False

def main():
    """Main execution"""
    print("\nStarting API verification process...\n")

    success = verify_all_apis()

    print("\n" + "="*70)
    if success:
        print("NEXT STEP: Run 02_multi_agent_review.py to start peer review")
    else:
        print("NEXT STEP: Fix API issues above, then re-run this script")
    print("="*70 + "\n")

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
