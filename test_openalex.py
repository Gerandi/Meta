import httpx
import asyncio
import json

async def test_openalex_direct():
    """Test OpenAlex API directly without PyAlex"""
    print("Testing OpenAlex API directly...")
    
    # Base URL for OpenAlex API
    base_url = "https://api.openalex.org/works"
    
    # Parameters
    params = {
        "search": "export performance",
        "per_page": 5,
        "mailto": "meta@example.com"  # Use your email for polite pool
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            print(f"Found {len(results)} results")
            print(f"Total results available: {data.get('meta', {}).get('count', 0)}")
            
            if results:
                print("\nFirst result:")
                first = results[0]
                print(f"Title: {first.get('title')}")
                print(f"DOI: {first.get('doi')}")
                
                # Print authors
                authors = []
                for authorship in first.get('authorships', [])[:2]:
                    authors.append(authorship.get('author', {}).get('display_name', ''))
                print(f"Authors: {', '.join(authors)}")
                
                # Print publication date
                print(f"Publication date: {first.get('publication_date')}")
                
                # Print citation count
                print(f"Citation count: {first.get('cited_by_count')}")
                
                # Print abstract snippet if available
                if 'abstract_inverted_index' in first and first['abstract_inverted_index']:
                    print(f"Abstract available: Yes")
                else:
                    print(f"Abstract available: No")
                
                # Print source info
                if first.get('primary_location', {}).get('source'):
                    source = first['primary_location']['source']
                    print(f"Source: {source.get('display_name')}")
                
                # Print full JSON for reference
                print("\nFull JSON structure (first result):")
                print(json.dumps(first, indent=2)[:1000] + "...")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    asyncio.run(test_openalex_direct())