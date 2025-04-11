"""
Test script to verify the standardized API client is working correctly.
"""

import asyncio
import json
import sys
import os

# Add the backend directory to the sys.path to import the app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.api_client import (
    get_crossref_data,
    get_semantic_scholar_data,
    get_scopus_data,
    get_exa_data,
    get_unpaywall_data
)


async def test_api_client():
    """Test each API client function and print results"""
    
    # Define the query
    query = "artificial intelligence"
    limit = 2
    
    # Test each API client with the query
    print("\n=== Testing Crossref API Client ===")
    crossref_papers, crossref_total = await get_crossref_data(query=query, limit=limit)
    print(f"Found {len(crossref_papers)} papers out of {crossref_total} total results")
    print(json.dumps(crossref_papers[0], indent=2) if crossref_papers else "No results")
    
    print("\n=== Testing Semantic Scholar API Client ===")
    ss_papers, ss_total = await get_semantic_scholar_data(query=query, limit=limit)
    print(f"Found {len(ss_papers)} papers out of {ss_total} total results")
    print(json.dumps(ss_papers[0], indent=2) if ss_papers else "No results")
    
    print("\n=== Testing Scopus API Client ===")
    scopus_papers, scopus_total = await get_scopus_data(query=query, limit=limit)
    print(f"Found {len(scopus_papers)} papers out of {scopus_total} total results")
    print(json.dumps(scopus_papers[0], indent=2) if scopus_papers else "No results")
    
    print("\n=== Testing Exa.ai API Client ===")
    exa_papers, exa_total = await get_exa_data(query=query, limit=limit)
    print(f"Found {len(exa_papers)} papers out of {exa_total} total results")
    print(json.dumps(exa_papers[0], indent=2) if exa_papers else "No results")
    
    print("\n=== Testing Unpaywall API Client ===")
    # Use a known DOI for testing
    doi = "10.1038/nature12373"
    unpaywall_data = await get_unpaywall_data(doi=doi)
    print(f"Unpaywall data for DOI {doi}:")
    print(json.dumps(unpaywall_data, indent=2))
    
    # Verify standardized fields
    print("\n=== Verifying Standardized Fields ===")
    for provider, papers in [
        ("Crossref", crossref_papers),
        ("Semantic Scholar", ss_papers),
        ("Scopus", scopus_papers),
        ("Exa.ai", exa_papers)
    ]:
        if not papers:
            print(f"{provider}: No results to verify")
            continue
            
        paper = papers[0]
        print(f"{provider} standardized fields:")
        for field in ["title", "doi", "authors", "publication_date", "abstract", 
                      "journal", "url", "citation_count", "is_open_access", 
                      "open_access_url", "source"]:
            print(f"  - {field}: {'Present' if field in paper else 'Missing'}")


if __name__ == "__main__":
    # Run the test
    asyncio.run(test_api_client())
