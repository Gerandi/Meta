import httpx
import asyncio
import json
from typing import Dict, Any, List, Optional

# API keys - replace with your actual keys
SCOPUS_API_KEY = "fba37f1f78cf589c198c81c8bdf035f3"  # Example key, replace this
EXA_API_KEY = "80297ab6-7f57-4bf7-88f9-d9369d23404c"  # Example key, replace this
UNPAYWALL_EMAIL = "testingitout@gmail.com"  # Replace with your email

async def get_crossref_sample(query: str = "machine learning"):
    """Get sample data from Crossref API"""
    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": 1,
        "mailto": UNPAYWALL_EMAIL
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('message', {}).get('items', []):
                return data['message']['items'][0]
        
        return {"error": f"HTTP {response.status_code}", "response": response.text}

async def get_semantic_scholar_sample(query: str = "machine learning"):
    """Get sample data from Semantic Scholar API"""
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": 1,
        "fields": "title,abstract,year,authors,venue,url,openAccessPdf,citationCount,influentialCitationCount,externalIds"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data', []):
                return data['data'][0]
        
        return {"error": f"HTTP {response.status_code}", "response": response.text}

async def get_scopus_sample(query: str = "machine learning"):
    """Get sample data from Scopus API"""
    url = "https://api.elsevier.com/content/search/scopus"
    params = {
        "query": query,
        "count": 1,
        "sort": "-citedby-count"
    }
    
    headers = {
        "X-ELS-APIKey": SCOPUS_API_KEY,
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            entries = data.get('search-results', {}).get('entry', [])
            if entries:
                return entries[0]
        
        return {"error": f"HTTP {response.status_code}", "response": response.text}

async def get_exa_sample(query: str = "machine learning"):
    """Get sample data from Exa.ai API"""
    url = "https://api.exa.ai/search"
    
    headers = {
        "Authorization": f"Bearer {EXA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "query": query,
        "num_results": 1,
        "use_autoprompt": True,
        "category": "research paper",
        "summary": {
            "query": "Summarize the key findings related to the paper."
        }
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            if results:
                return results[0]
        
        return {"error": f"HTTP {response.status_code}", "response": response.text}

async def get_unpaywall_sample(doi: str = "10.1038/nature12373"):
    """Get sample data from Unpaywall API for a DOI"""
    url = f"https://api.unpaywall.org/v2/{doi}"
    
    params = {
        "email": UNPAYWALL_EMAIL
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        
        return {"error": f"HTTP {response.status_code}", "response": response.text}

async def main():
    # Define the search query
    query = "artificial intelligence"
    
    # Gather results from all providers
    results = {
        "crossref": await get_crossref_sample(query),
        "semantic_scholar": await get_semantic_scholar_sample(query),
        "scopus": await get_scopus_sample(query),
        "exa": await get_exa_sample(query),
        "unpaywall": await get_unpaywall_sample("10.1038/nature12373")  # Using a sample DOI
    }
    
    # Pretty print the results with proper indentation
    for provider, data in results.items():
        print(f"\n\n{'=' * 50}")
        print(f"PROVIDER: {provider.upper()}")
        print(f"{'=' * 50}")
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    asyncio.run(main())