"""
Test script to verify that the OpenAlex search functionality is working correctly
"""
import asyncio
import json
import sys

sys.path.append('.')

# Updated import to use the consolidated direct client
from app.services.openalex_direct import search_papers_direct 


async def test_search():
    """Test search for the term 'export performance' using OpenAlex"""
    query = "export performance"
    print(f"Searching for: {query} using OpenAlex")
    
    # Use the consolidated direct search function
    results, total = await search_papers_direct(
        query=query,
        per_page=5, # Use per_page
        page=1      # Specify page
    )
    
    print(f"Found {total} total results. Showing first {len(results)} results:\n")
    
    for i, paper in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Title: {paper['title']}")
        
        # Handle different author formats
        if isinstance(paper.get('authors', []), list):
            if len(paper['authors']) > 0 and isinstance(paper['authors'][0], dict):
                authors = ', '.join([a.get('name', 'Unknown') for a in paper['authors']])
            else:
                authors = ', '.join(paper['authors'])
        else:
            authors = paper.get('authors', 'Unknown')
        
        print(f"Authors: {authors}")
        print(f"Journal: {paper.get('journal', 'Unknown')}")
        print(f"Year: {paper.get('publication_date')}")
        print(f"Keywords: {paper.get('keywords', [])}")
        print(f"Source: {paper.get('source', 'OpenAlex')}")
        
        # Check if the paper is actually related to "export performance"
        title_lower = paper['title'].lower()
        abstract_lower = paper.get('abstract', '').lower() if paper.get('abstract') else ''
        is_relevant = ('export' in title_lower and 'performance' in title_lower) or \
                    ('export' in abstract_lower and 'performance' in abstract_lower)
        
        print(f"Is directly relevant: {'Yes' if is_relevant else 'No'}")
        print(f"Citation count: {paper.get('citation_count', 'Unknown')}")
        print(f"DOI: {paper.get('doi', 'None')}")


if __name__ == "__main__":
    asyncio.run(test_search())
