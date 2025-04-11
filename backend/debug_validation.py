"""
Debug script to validate OpenAlex API parameters
"""

import httpx
import asyncio
import json

async def test_openalex_search_debug():
    """Test a search with the problematic parameters"""
    base_url = "https://api.openalex.org/works"
    
    # Trying with different parameter sets
    test_cases = [
        {
            "search": "export performance",
            "per_page": 10,
            "page": 1,
            "mailto": "meta@example.com"
        },
        {
            "search": "export perfromance",  # Note the typo
            "per_page": 10,
            "page": 1,
            "mailto": "meta@example.com"
        }
    ]
    
    for idx, params in enumerate(test_cases):
        print(f"\nTest case {idx+1}: {params}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(base_url, params=params)
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Results count: {len(data.get('results', []))}")
                print(f"Total results: {data.get('meta', {}).get('count', 0)}")
            else:
                print(f"Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_openalex_search_debug())
