"""
Test script to verify that the fixed search functionality is working correctly
"""
import asyncio
import json
import sys

sys.path.append('.')

from app.services.additional_providers import search_papers_combined


async def test_search():
    """Test search for the term 'export performance' which should return relevant results"""
    query = "export performance"
    print(f"Searching for: {query}")
    
    results, total = await search_papers_combined(
        query=query,
        limit=5,
        providers=["crossref", "semantic_scholar", "scopus", "exa"]
    )
    
    print(f"Found {total} total results. Showing first {len(results)} results:\n")
    
    for i, paper in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Title: {paper['title']}")
        print(f"Authors: {', '.join([a['name'] for a in paper['authors']])}")
        print(f"Journal: {paper.get('journal', 'Unknown')}")
        print(f"Year: {paper.get('publication_date')}")
        print(f"Keywords: {paper.get('keywords', [])}")
        print(f"Source: {paper.get('source', 'Unknown')}")
        
        # Check if the paper is actually related to "export performance"
        title_lower = paper['title'].lower()
        abstract_lower = paper.get('abstract', '').lower() if paper.get('abstract') else ''
        is_relevant = ('export' in title_lower and 'performance' in title_lower) or \
                    ('export' in abstract_lower and 'performance' in abstract_lower)
        
        print(f"Is directly relevant: {'Yes' if is_relevant else 'No'}")


if __name__ == "__main__":
    asyncio.run(test_search())
