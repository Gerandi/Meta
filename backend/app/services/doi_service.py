import re
import httpx
import logging
import asyncio
from typing import Optional, Dict, Any, List

from app.core.config import settings
# Updated import to use the consolidated direct client
from app.services.openalex_direct import search_papers_direct 

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
    
    try:
        # Use the consolidated direct search function
        results, total_count = await search_papers_direct(
            query=title,
            per_page=3, # Use per_page instead of limit
            page=1,     # Start from page 1
            year_from=int(year) if year else None, # Ensure year is int
            year_to=int(year) if year else None,   # Ensure year is int
            # Removed duplicate year_to=year,
            author=author,
            sort="relevance"
        )
        
        if results and total_count > 0:
            # Enhanced matching - prioritize papers with exact title match
            best_match = None
            best_match_score = 0
            
            for paper in results:
                # Skip items without DOIs
                if not paper.get('doi'):
                    continue
                    
                # Basic score starts at 1
                score = 1
                
                # Give higher score for title similarity
                paper_title = paper.get('title', '').lower()
                search_title = title.lower()
                if paper_title == search_title:
                    score += 3  # Exact match
                elif search_title in paper_title or paper_title in search_title:
                    score += 2  # Partial match
                    
                # Give bonus points for matching author
                if author:
                    has_author = False
                    for paper_author in paper.get('authors', []):
                        author_name = paper_author.get('name', '').lower()
                        if author.lower() in author_name or author_name in author.lower():
                            has_author = True
                            break
                    if has_author:
                        score += 1
                        
                # Update best match if this is better
                if score > best_match_score:
                    best_match = paper
                    best_match_score = score
            
            # Use the best matching paper
            if best_match and 'doi' in best_match:
                logger.info(f"Found DOI for paper: {title} with match score {best_match_score}")
                return best_match['doi']
                
        logger.warning(f"No DOI found for: {title} by {author} ({year})")
        return None
    
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
