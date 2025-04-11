import re
import httpx
import logging
import asyncio
from typing import Optional, Dict, Any, List

from app.core.config import settings

logger = logging.getLogger(__name__)


def clean_author(author_string: str) -> str:
    """Clean up an author string to extract the last name of the first author"""
    author_string = re.sub(r'\s+et al\.?', '', author_string).strip('.')
    authors = author_string.split(',')[0].split('and')[0].split()
    return authors[-1] if authors else ""


async def get_doi_for_paper(title: str, author: str, year: str) -> Optional[str]:
    """Find DOI for a paper based on title, author, and year"""
    # Clean author if it's a full string
    if len(author.split()) > 1:
        author = clean_author(author)
    
    url = "https://api.crossref.org/works"
    
    params = {
        "query.title": title,
        "query.author": author,
        "filter": f"from-pub-date:{year},until-pub-date:{year}",
        "rows": 1
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('message', {}).get('total-results', 0) > 0:
                    items = data['message']['items']
                    if items and 'DOI' in items[0]:
                        logger.info(f"Found DOI for paper: {title}")
                        return items[0]['DOI']
                        
            logger.warning(f"No DOI found for: {title} by {author} ({year})")
    
    except Exception as e:
        logger.error(f"Error retrieving DOI for paper '{title}': {str(e)}")
    
    return None


async def get_dois_for_papers(papers: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Find DOIs for multiple papers"""
    result = []
    
    for paper in papers:
        title = paper.get('title', '')
        authors = paper.get('authors', '')
        year = paper.get('year', '')
        
        # Skip if missing essential information
        if not title or not authors or not year:
            paper['doi'] = None
            result.append(paper)
            continue
        
        # Extract first author's last name
        author = clean_author(authors)
        
        # Get DOI
        doi = await get_doi_for_paper(title, author, year)
        paper['doi'] = doi
        result.append(paper)
        
        # Add a small delay to avoid rate limiting
        await asyncio.sleep(0.5)
    
    return result
