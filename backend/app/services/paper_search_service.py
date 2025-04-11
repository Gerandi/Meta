import httpx
import logging
import time
import unicodedata
from typing import Dict, List, Any, Optional
from datetime import datetime

from app.core.config import settings
from app.schemas.paper import Paper, Author

logger = logging.getLogger(__name__)

async def search_papers_crossref(query: str, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Search for papers using the Crossref API
    
    Args:
        query: Search query
        limit: Maximum number of results to return
        offset: Number of results to skip
    
    Returns:
        List of paper dictionaries
    """
    url = "https://api.crossref.org/works"
    
    params = {
        "query": query,
        "rows": limit,
        "offset": offset,
        "sort": "relevance",
        "order": "desc",
        "mailto": settings.CROSSREF_EMAIL
    }
    
    results = []
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            items = data.get('message', {}).get('items', [])
            
            for item in items:
                try:
                    # Extract authors
                    authors = []
                    for author in item.get('author', []):
                        name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                        affiliation = author.get('affiliation', [{}])[0].get('name') if author.get('affiliation') else None
                        authors.append({"name": name, "affiliation": affiliation})
                    
                    # Extract publication date
                    pub_date = None
                    if 'published-online' in item:
                        date_parts = item['published-online']['date-parts'][0]
                        if len(date_parts) >= 3:
                            pub_date = f"{date_parts[0]}-{date_parts[1]:02d}-{date_parts[2]:02d}"
                    elif 'published-print' in item:
                        date_parts = item['published-print']['date-parts'][0]
                        if len(date_parts) >= 3:
                            pub_date = f"{date_parts[0]}-{date_parts[1]:02d}-{date_parts[2]:02d}"
                    elif 'created' in item:
                        date_parts = item['created']['date-parts'][0]
                        if len(date_parts) >= 3:
                            pub_date = f"{date_parts[0]}-{date_parts[1]:02d}-{date_parts[2]:02d}"
                    
                    # Extract abstract
                    abstract = item.get('abstract', None)
                    
                    paper = {
                        "title": item.get('title', [''])[0],
                        "doi": item.get('DOI'),
                        "authors": authors,
                        "publication_date": pub_date,
                        "abstract": abstract,
                        "journal": item.get('container-title', [''])[0] if item.get('container-title') else None,
                        "volume": item.get('volume'),
                        "issue": item.get('issue'),
                        "pages": item.get('page'),
                        "publisher": item.get('publisher'),
                        "url": f"https://doi.org/{item.get('DOI')}" if item.get('DOI') else None,
                        "citation_count": item.get('is-referenced-by-count', 0),
                        "references_count": item.get('references-count', 0)
                    }
                    
                    results.append(paper)
                except Exception as e:
                    logger.error(f"Error processing paper from Crossref: {str(e)}")
    
    except httpx.HTTPError as e:
        logger.error(f"HTTP error during Crossref search: {str(e)}")
    except Exception as e:
        logger.error(f"Error searching Crossref: {str(e)}")
    
    return results


async def search_papers_unpaywall(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Search for papers that have open access versions using Unpaywall
    
    Since Unpaywall doesn't have a search API, we first search with Crossref
    then enrich the results with Unpaywall data
    
    Args:
        query: Search query
        limit: Maximum number of results to return
    
    Returns:
        List of paper dictionaries with open access information
    """
    # First get results from Crossref
    papers = await search_papers_crossref(query, limit)
    
    # Enrich with Unpaywall data
    for paper in papers:
        if paper.get('doi'):
            try:
                url = f"https://api.unpaywall.org/v2/{paper['doi']}"
                params = {
                    "email": settings.UNPAYWALL_EMAIL
                }
                
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(url, params=params)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        paper['is_open_access'] = data.get('is_oa', False)
                        paper['oa_status'] = data.get('oa_status')
                        paper['journal_is_oa'] = data.get('journal_is_oa', False)
                        
                        best_location = data.get('best_oa_location')
                        if best_location:
                            paper['open_access_url'] = (
                                best_location.get('url_for_pdf') or 
                                best_location.get('url') or 
                                None
                            )
                            paper['oa_license'] = best_location.get('license')
                    else:
                        paper['is_open_access'] = False
                        paper['open_access_url'] = None
            
            except Exception as e:
                logger.error(f"Error retrieving OA data for DOI {paper['doi']}: {str(e)}")
                paper['is_open_access'] = False
                paper['open_access_url'] = None
                
            # Avoid rate limiting
            await asyncio.sleep(0.2)
    
    return papers


async def search_papers_semantic_scholar(query: str, limit: int = 20, year_start: int = None, year_end: int = None) -> List[Dict[str, Any]]:
    """
    Search for papers using the Semantic Scholar API
    
    Args:
        query: Search query
        limit: Maximum number of results to return
        year_start: Earliest publication year
        year_end: Latest publication year
    
    Returns:
        List of paper dictionaries
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    params = {
        "query": query,
        "limit": min(limit, 100),  # API supports max 100 per request
        "fields": "title,abstract,year,authors,venue,url,openAccessPdf,citationCount,influentialCitationCount,externalIds"
    }
    
    # Add year filter if provided
    if year_start and year_end:
        params["year"] = f"{year_start}-{year_end}"
    
    results = []
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                papers = data.get('data', [])
                
                for paper in papers:
                    # Extract authors
                    authors = [{"name": author.get('name', ''), "affiliation": None} for author in paper.get('authors', [])]
                    
                    # Get DOI if available
                    doi = paper.get('externalIds', {}).get('DOI')
                    
                    # Get open access PDF
                    oa_pdf = paper.get('openAccessPdf', {})
                    oa_url = oa_pdf.get('url') if oa_pdf else None
                    
                    paper_data = {
                        "title": paper.get('title', ''),
                        "doi": doi,
                        "authors": authors,
                        "publication_date": f"{paper.get('year')}-01-01" if paper.get('year') else None,
                        "abstract": paper.get('abstract'),
                        "journal": paper.get('venue'),
                        "url": paper.get('url'),
                        "open_access_url": oa_url,
                        "is_open_access": oa_url is not None,
                        "citation_count": paper.get('citationCount', 0)
                    }
                    
                    results.append(paper_data)
            else:
                logger.error(f"Semantic Scholar API error: HTTP {response.status_code}")
    
    except Exception as e:
        logger.error(f"Error searching Semantic Scholar: {str(e)}")
    
    return results


async def search_papers_combined(query: str, limit: int = 20, open_access_only: bool = False) -> List[Dict[str, Any]]:
    """
    Search for papers using multiple APIs and combine results
    
    Args:
        query: Search query
        limit: Maximum number of results to return
        open_access_only: Whether to return only open access papers
    
    Returns:
        List of paper dictionaries
    """
    # Search in both services
    crossref_results = await search_papers_crossref(query, limit)
    semantic_results = await search_papers_semantic_scholar(query, limit)
    
    # Combine results, remove duplicates based on DOI
    combined = {}
    
    # Add Crossref results
    for paper in crossref_results:
        if paper.get('doi'):
            combined[paper['doi']] = paper
    
    # Add Semantic Scholar results, merging with existing when DOI matches
    for paper in semantic_results:
        if paper.get('doi'):
            if paper['doi'] in combined:
                # Merge information, preferring the more complete data
                existing = combined[paper['doi']]
                
                # Keep Semantic Scholar OA URL if available
                if paper.get('open_access_url') and not existing.get('open_access_url'):
                    existing['open_access_url'] = paper['open_access_url']
                    existing['is_open_access'] = True
                
                # Keep abstract if missing
                if paper.get('abstract') and not existing.get('abstract'):
                    existing['abstract'] = paper['abstract']
            else:
                combined[paper['doi']] = paper
        else:
            # No DOI, add as new paper with a generated key
            key = f"noDOI_{paper.get('title', '')[:50]}"
            if key not in combined:
                combined[key] = paper
    
    # Convert to list and apply open access filter if needed
    result = list(combined.values())
    if open_access_only:
        result = [p for p in result if p.get('is_open_access', False)]
    
    # Sort by relevance (for now, citation count as a proxy)
    result.sort(key=lambda x: x.get('citation_count', 0), reverse=True)
    
    # Limit results
    return result[:limit]


# Import missing module
import asyncio
