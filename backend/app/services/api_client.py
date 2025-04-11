"""
API Client for academic search providers with standardized response format.
This module provides async functions to fetch data from various academic APIs
and standardizes the responses for consistent use throughout the application.
"""

import httpx
import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from functools import wraps

from app.core.config import settings

# Get API keys from settings
SCOPUS_API_KEY = settings.SCOPUS_API_KEY
EXA_API_KEY = settings.EXA_API_KEY
UNPAYWALL_EMAIL = settings.UNPAYWALL_EMAIL
CROSSREF_EMAIL = settings.CROSSREF_EMAIL

logger = logging.getLogger(__name__)


async def calculate_relevance_score(paper: Dict[str, Any], query: str) -> float:
    """Calculate relevance score for a paper based on the query"""
    query_terms = query.lower().split()
    title = paper.get('title', '')
    title_lower = title.lower() if isinstance(title, str) else ''
    abstract = paper.get('abstract', '')
    abstract_lower = abstract.lower() if isinstance(abstract, str) else ''
    journal = paper.get('journal', '')
    journal_lower = journal.lower() if isinstance(journal, str) else ''
    keywords = paper.get('keywords', [])
    
    score = 0
    
    for term in query_terms:
        if term in title_lower:
            score += 3  # Title match is highly relevant
        if term in abstract_lower:
            score += 1  # Abstract match is relevant
        if term in journal_lower:
            score += 1  # Journal match can be relevant
        # Match against keywords
        if any(term in (kw.lower() if isinstance(kw, str) else '') for kw in keywords):
            score += 2  # Keyword match is relevant
    
    return score


async def get_provider_data(provider: str, query: str, params: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], int]:
    """Centralized error handling for provider API calls"""
    try:
        if provider == "exa":
            return await get_exa_data(query, **params)
        elif provider == "scopus":
            return await get_scopus_data(query, **params)
        elif provider == "semantic_scholar":
            return await get_semantic_scholar_data(query, **params)
        elif provider == "crossref":
            return await get_crossref_data(query, **params)
        else:
            logger.error(f"Unknown provider: {provider}")
            return [], 0
    except Exception as e:
        logger.error(f"Error from {provider}: {str(e)}")
        return [], 0  # Return empty list instead of error object


async def get_crossref_data(query: str = "machine learning", limit: int = 10, offset: int = 0,
                           year_from: Optional[int] = None, year_to: Optional[int] = None,
                           journal: Optional[str] = None, author: Optional[str] = None,
                           sort: Optional[str] = None) -> Tuple[List[Dict[str, Any]], int]:
    """Get data from Crossref API with standardized response format"""
    
    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": limit,
        "offset": offset,
        "mailto": CROSSREF_EMAIL
    }
    
    # Add sort parameter if provided
    if sort:
        if sort == "date":
            params["sort"] = "published"
        elif sort == "relevance":
            params["sort"] = "score"
        elif sort == "cited":
            params["sort"] = "is-referenced-by-count"
        params["order"] = "desc"
    
    # Add filters for date range if provided
    filter_parts = []
    if year_from:
        filter_parts.append(f"from-pub-date:{year_from}")
    if year_to:
        filter_parts.append(f"until-pub-date:{year_to}")
    
    # Add journal filter if provided
    if journal:
        filter_parts.append(f"container-title:{journal}")
    
    # Add all filters together if any are present
    if filter_parts:
        params["filter"] = ",".join(filter_parts)
    
    papers = []
    total_results = 0
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('message', {}).get('items', [])
                total_results = data.get('message', {}).get('total-results', 0)
                
                for item in items:
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
                    
                    # Match author filter if provided
                    if author and authors:
                        author_found = False
                        author_query = author.lower() if isinstance(author, str) else ""
                        for auth in authors:
                            auth_name = auth['name'].lower() if isinstance(auth['name'], str) else ""
                            if author_query and author_query in auth_name:
                                author_found = True
                                break
                        if not author_found:
                            continue
                    
                    # Extract keywords if available
                    keywords = []
                    if 'subject' in item:
                        keywords = item.get('subject', [])
                    
                    title = item.get('title', [''])[0] if isinstance(item.get('title'), list) else item.get('title', '')
                    journal_name = item.get('container-title', [''])[0] if isinstance(item.get('container-title'), list) else item.get('container-title', '')
                    
                    paper = {
                        "title": title,
                        "doi": item.get('DOI'),
                        "authors": authors,
                        "publication_date": pub_date,
                        "abstract": abstract,
                        "journal": journal_name,
                        "volume": item.get('volume'),
                        "issue": item.get('issue'),
                        "pages": item.get('page'),
                        "publisher": item.get('publisher'),
                        "url": f"https://doi.org/{item.get('DOI')}" if item.get('DOI') else None,
                        "citation_count": item.get('is-referenced-by-count', 0),
                        "references_count": item.get('references-count', 0),
                        "is_open_access": False,
                        "open_access_url": None,
                        "keywords": keywords,
                        "source": "Crossref"
                    }
                    
                    # Check if the paper matches the query closely (increase its score)
                    # This helps ensure unrelated results don't get included
                    query_terms = query.lower().split()
                    title_lower = title.lower()
                    abstract_lower = abstract.lower() if abstract else ""
                    journal_lower = journal_name.lower()
                    
                    # Calculate a simple relevance score
                    score = 0
                    for term in query_terms:
                        if term in title_lower:
                            score += 3  # Title match is highly relevant
                        if abstract and term in abstract_lower:
                            score += 1  # Abstract match is relevant
                        if term in journal_lower:
                            score += 1  # Journal match can be relevant
                    
                    # Only add papers with at least some relevance
                    if score > 0 or sort != "relevance":  # Always include if sorting by something other than relevance
                        papers.append(paper)
            else:
                logger.error(f"Crossref API error: HTTP {response.status_code}")
                return [], 0
    
    except Exception as e:
        logger.error(f"Error searching Crossref: {str(e)}")
        return [], 0
        
    return papers, total_results


async def get_semantic_scholar_data(query: str = "machine learning", limit: int = 10, 
                                  year_from: Optional[int] = None, 
                                  year_to: Optional[int] = None) -> Tuple[List[Dict[str, Any]], int]:
    """Get data from Semantic Scholar API with standardized response format"""
    
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    params = {
        "query": query,
        "limit": min(limit, 100),  # API supports max 100 per request
        "fields": "title,abstract,year,authors,venue,url,openAccessPdf,citationCount,influentialCitationCount,externalIds,fieldsOfStudy"
    }
    
    # Add year filter if provided
    if year_from and year_to:
        params["year"] = f"{year_from}-{year_to}"
    
    papers = []
    total_results = 0
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('data', [])
                total_results = data.get('total', len(items))
                
                for item in items:
                    # Extract authors
                    authors = []
                    for author in item.get('authors', []):
                        authors.append({"name": author.get('name', ''), "affiliation": None})
                    
                    # Get title and extract other fields
                    title = item.get('title', '')
                    
                    # Get DOI if available
                    doi = item.get('externalIds', {}).get('DOI')
                    
                    # Get open access PDF
                    oa_pdf = item.get('openAccessPdf', {})
                    oa_url = oa_pdf.get('url') if oa_pdf else None
                    
                    # Extract fields of study as keywords
                    keywords = item.get('fieldsOfStudy', [])
                    
                    # Calculate relevance score based on query match
                    query_terms = query.lower().split()
                    title_lower = title.lower()
                    abstract = item.get('abstract')
                    abstract_lower = abstract.lower() if abstract else ""
                    journal = item.get('venue')
                    journal_lower = journal.lower() if journal else ""
                    
                    score = 0
                    for term in query_terms:
                        if term in title_lower:
                            score += 3  # Title match is highly relevant
                        if abstract and term in abstract_lower:
                            score += 1  # Abstract match is relevant
                        if journal and term in journal_lower:
                            score += 1  # Journal match can be relevant
                        # Match against keywords/fields of study
                        if any(term in field.lower() for field in keywords):
                            score += 2  # Field of study match is relevant
                    
                    # Only include papers with some relevance
                    if score > 0:
                        paper = {
                            "title": title,
                            "doi": doi,
                            "authors": authors,
                            "publication_date": f"{item.get('year')}-01-01" if item.get('year') else None,
                            "abstract": abstract,
                            "journal": journal,
                            "url": item.get('url'),
                            "open_access_url": oa_url,
                            "is_open_access": oa_url is not None,
                            "citation_count": item.get('citationCount', 0),
                            "references_count": 0,  # Not provided by the API
                            "publisher": None,  # Not provided by the API
                            "volume": None,  # Not provided by the API
                            "issue": None,  # Not provided by the API 
                            "pages": None,  # Not provided by the API
                            "keywords": keywords,
                            "source": "Semantic Scholar"
                        }
                        papers.append(paper)
            else:
                logger.error(f"Semantic Scholar API error: HTTP {response.status_code}")
                return [], 0
    
    except Exception as e:
        logger.error(f"Error searching Semantic Scholar: {str(e)}")
        return [], 0
        
    return papers, total_results


async def get_scopus_data(query: str = "machine learning", limit: int = 10,
                         year_from: Optional[int] = None, 
                         year_to: Optional[int] = None,
                         author: Optional[str] = None,
                         journal: Optional[str] = None) -> Tuple[List[Dict[str, Any]], int]:
    """Get data from Scopus API with standardized response format"""
    
    url = "https://api.elsevier.com/content/search/scopus"
    
    # Build the query
    search_query = query
    if year_from:
        search_query += f" AND PUBYEAR > {year_from}"
    if year_to:
        search_query += f" AND PUBYEAR < {year_to}"
    if author:
        search_query += f" AND AUTHOR-NAME({author})"
    if journal:
        search_query += f" AND SRCTITLE({journal})"
    
    params = {
        "query": search_query,
        "count": limit,
        "sort": "-citedby-count"
    }
    
    headers = {
        "X-ELS-APIKey": SCOPUS_API_KEY,
        "Accept": "application/json"
    }
    
    papers = []
    total_results = 0
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                search_results = data.get('search-results', {})
                total_results = int(search_results.get('opensearch:totalResults', 0))
                entries = search_results.get('entry', [])
                
                for item in entries:
                    # Extract authors
                    authors = []
                    if 'author' in item:
                        for author in item['author']:
                            if isinstance(author, dict) and '$' in author:
                                authors.append({"name": author.get('$', ''), "affiliation": None})
                    elif 'dc:creator' in item:  # Sometimes Scopus provides a single author string
                        authors.append({"name": item['dc:creator'], "affiliation": None})
                    
                    pub_date = item.get('prism:coverDate', '')
                    
                    paper = {
                        "title": item.get('dc:title', ''),
                        "doi": item.get('prism:doi'),
                        "authors": authors,
                        "publication_date": pub_date,
                        "abstract": item.get('dc:description', ''),
                        "journal": item.get('prism:publicationName'),
                        "url": f"https://doi.org/{item.get('prism:doi')}" if item.get('prism:doi') else None,
                        "is_open_access": item.get('openaccess') == "1" or item.get('openaccessFlag') == True,
                        "open_access_url": None,  # Not provided directly by Scopus
                        "citation_count": int(item.get('citedby-count', 0)),
                        "references_count": 0,  # Not provided directly
                        "volume": item.get('prism:volume'),
                        "issue": item.get('prism:issueIdentifier'),
                        "pages": item.get('prism:pageRange'),
                        "publisher": item.get('dc:publisher'),
                        "source": "Scopus"
                    }
                    papers.append(paper)
            else:
                logger.error(f"Scopus API error: HTTP {response.status_code}")
                return [], 0
    
    except Exception as e:
        logger.error(f"Error searching Scopus: {str(e)}")
        return [], 0
        
    return papers, total_results


async def get_exa_data(query: str = "machine learning", limit: int = 10,
                      year_from: Optional[int] = None, 
                      year_to: Optional[int] = None) -> Tuple[List[Dict[str, Any]], int]:
    """Get data from Exa.ai API with standardized response format"""
    
    # API key validation - fail gracefully if key isn't valid
    if not EXA_API_KEY or len(EXA_API_KEY) < 10:
        logger.error("Invalid or missing Exa.ai API key")
        return [], 0
    
    url = "https://api.exa.ai/search"
    
    headers = {
        "Authorization": f"Bearer {EXA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Add date constraints if provided
    date_constraint = ""
    if year_from:
        date_constraint += f"start_published_date:{year_from}-01-01T00:00:00.000Z,"
    if year_to:
        date_constraint += f"end_published_date:{year_to}-12-31T23:59:59.999Z,"
    
    data = {
        "query": query,
        "num_results": limit,
        "use_autoprompt": True,
        "category": "research paper",
        "exclude_domains": ["en.wikipedia.org"],
        "summary": {
            "query": "Summarize the key findings related to the paper."
        }
    }
    
    # Add date constraints if present
    if date_constraint:
        data["date_constraint"] = date_constraint.rstrip(',')
    
    papers = []
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                result_data = response.json()
                items = result_data.get('results', [])
                
                for item in items:
                    # Skip items without title or URL
                    if not item.get('title') or not item.get('url'):
                        continue
                    
                    # Create a simplified author representation
                    authors = []
                    if 'author' in item and item['author']:
                        if isinstance(item['author'], str) and "," in item['author']:
                            # Multiple authors in comma-separated string
                            author_names = [name.strip() for name in item['author'].split(",")]
                            authors = [{"name": name, "affiliation": None} for name in author_names]
                        else:
                            authors = [{"name": item['author'], "affiliation": None}]
                    
                    # Default author if none found
                    if not authors:
                        authors = [{"name": "Unknown Author", "affiliation": None}]
                    
                    # Format publication date
                    pub_date = None
                    if 'publishedDate' in item and item['publishedDate']:
                        pub_date = item['publishedDate']
                    
                    # Extract summary as abstract
                    abstract = ""
                    if item.get('summary'):
                        abstract = item.get('summary')
                    
                    # Get keywords from content if available
                    keywords = []
                    if item.get('title'):
                        # Extract possible keywords from title
                        title_words = item.get('title', '').split()
                        if len(title_words) > 2:
                            keywords = [w for w in title_words if len(w) > 5][:5]  # Just use longer words as keywords
                    
                    # Use query terms as relevance check
                    query_terms = query.lower().split()
                    title = item.get('title', '')
                    title_lower = title.lower()
                    abstract_lower = abstract.lower() if abstract else ""
                    
                    # Calculate relevance score
                    score = 0
                    for term in query_terms:
                        if term in title_lower:
                            score += 3  # Title match is highly relevant
                        if abstract and term in abstract_lower:
                            score += 1  # Abstract match is relevant
                    
                    # Only include relevant results
                    if score > 0:
                        paper = {
                            "title": title,
                            "doi": None,  # Exa doesn't return DOIs directly
                            "authors": authors,
                            "publication_date": pub_date,
                            "abstract": abstract,
                            "journal": None,  # Not provided directly
                            "url": item.get('url'),
                            "is_open_access": True,  # Exa typically indexes accessible content
                            "open_access_url": item.get('url'),  # Use the same URL
                            "citation_count": 0,  # Not provided directly
                            "references_count": 0,  # Not provided directly
                            "volume": None,  # Not provided directly
                            "issue": None,  # Not provided directly
                            "pages": None,  # Not provided directly
                            "publisher": None,  # Not provided directly
                            "keywords": keywords,
                            "source": "Exa.ai"
                        }
                        papers.append(paper)
            else:
                error_msg = f"Exa.ai API error: HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    if isinstance(error_data, dict) and 'error' in error_data:
                        error_msg += f" - {error_data['error']}"
                except:
                    pass
                logger.error(error_msg)
                return [], 0
    
    except Exception as e:
        logger.error(f"Error searching Exa.ai: {str(e)}")
        return [], 0
        
    return papers, len(papers)


async def get_unpaywall_data(doi: str = "10.1038/nature12373") -> Dict[str, Any]:
    """Get open access information for a paper using the Unpaywall API"""
    
    url = f"https://api.unpaywall.org/v2/{doi}"
    
    params = {
        "email": UNPAYWALL_EMAIL
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract authors from z_authors if available
                authors = []
                if data.get('z_authors'):
                    for author in data['z_authors']:
                        name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                        authors.append({"name": name, "affiliation": None})
                
                # Find best open access URL
                is_open_access = data.get('is_oa', False)
                open_access_url = None
                
                if is_open_access and data.get('best_oa_location'):
                    oa_location = data['best_oa_location']
                    if oa_location.get('url_for_pdf'):
                        open_access_url = oa_location['url_for_pdf']
                    elif oa_location.get('url'):
                        open_access_url = oa_location['url']
                
                result = {
                    "doi": data.get('doi'),
                    "title": data.get('title', ''),
                    "authors": authors,
                    "publication_date": data.get('published_date'),
                    "journal": data.get('journal_name'),
                    "publisher": data.get('publisher'),
                    "is_open_access": is_open_access,
                    "open_access_url": open_access_url,
                    "url": data.get('doi_url'),
                    "source": "Unpaywall"
                }
                
                return result
            else:
                logger.error(f"Unpaywall API error: HTTP {response.status_code}")
                return {"error": f"HTTP {response.status_code}", "doi": doi}
    
    except Exception as e:
        logger.error(f"Error fetching Unpaywall data: {str(e)}")
        return {"error": str(e), "doi": doi}
