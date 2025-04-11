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
    """Find DOI for a paper based on title, author, and year using OpenAlex"""
    # Clean author if it's a full string
    if len(author.split()) > 1:
        author = clean_author(author)
    
    url = "https://api.openalex.org/works"
    
    # Improved parameter handling with better search focus
    params = {
        "search": title,
        "filter": f"publication_year:{year}",
        "per_page": 3,  # Get top 3 results to find the best match
        "mailto": settings.OPENALEX_EMAIL
    }
    
    # Add author filter if available
    if author:
        params["filter"] += f",author.display_name.search:{author}"
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:  # Extended timeout
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('meta', {}).get('count', 0) > 0:
                    items = data['results']
                    
                    # Enhanced matching - prioritize papers with exact title match
                    best_match = None
                    best_match_score = 0
                    
                    for item in items:
                        # Skip items without DOIs
                        if not item.get('doi'):
                            continue
                            
                        # Basic score starts at 1
                        score = 1
                        
                        # Give higher score for title similarity
                        item_title = item.get('title', '').lower()
                        search_title = title.lower()
                        if item_title == search_title:
                            score += 3  # Exact match
                        elif search_title in item_title or item_title in search_title:
                            score += 2  # Partial match
                            
                        # Give bonus points for matching author
                        if author:
                            has_author = False
                            for authorship in item.get('authorships', []):
                                author_name = authorship.get('author', {}).get('display_name', '').lower()
                                if author.lower() in author_name or author_name in author.lower():
                                    has_author = True
                                    break
                            if has_author:
                                score += 1
                                
                        # Update best match if this is better
                        if score > best_match_score:
                            best_match = item
                            best_match_score = score
                    
                    # Use the best matching paper
                    if best_match and 'doi' in best_match:
                        logger.info(f"Found DOI for paper: {title} with match score {best_match_score}")
                        return best_match['doi']
                        
            logger.warning(f"No DOI found for: {title} by {author} ({year})")
    
    except Exception as e:
        logger.error(f"Error retrieving DOI for paper '{title}': {str(e)}")
    
    return None


async def get_dois_for_papers(papers: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Find DOIs for multiple papers using OpenAlex"""
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
