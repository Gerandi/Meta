import logging
import httpx
import asyncio
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime

from app.core.config import settings
from app.services.api_client import (
    get_crossref_data,
    get_semantic_scholar_data,
    get_scopus_data,
    get_exa_data,
    get_unpaywall_data
)

logger = logging.getLogger(__name__)


def standardize_paper(paper: Dict[str, Any]) -> Dict[str, Any]:
    """
    Standardize paper data from different providers to ensure consistent format
    
    Args:
        paper: Raw paper data from any provider
        
    Returns:
        Standardized paper data with consistent fields
    """
    source = paper.get("source", "")
    
    # Create base standardized structure with defaults
    standardized = {
        # Required fields
        "id": paper.get("id", 0),
        "title": paper.get("title", ""),
        "doi": paper.get("doi") or paper.get("DOI"),
        "created_at": paper.get("created_at", datetime.now().isoformat()),
        "updated_at": paper.get("updated_at", datetime.now().isoformat()),
        
        # Standard metadata
        "authors": [],
        "publication_date": paper.get("publication_date"),
        "abstract": paper.get("abstract"),
        "journal": paper.get("journal"),
        "volume": paper.get("volume"),
        "issue": paper.get("issue"),
        "pages": paper.get("pages"),
        "publisher": paper.get("publisher"),
        "url": paper.get("url"),
        "keywords": paper.get("keywords", []),
        
        # Access information
        "is_open_access": paper.get("is_open_access", False),
        "open_access_url": paper.get("open_access_url"),
        
        # Metrics
        "citation_count": paper.get("citation_count", 0),
        "references_count": paper.get("references_count", 0),
        
        # Source tracking
        "source": source or paper.get("source")
    }
    
    # Handle specific provider formats
    if "DOI" in paper and not standardized["doi"]:  # Crossref format
        standardized["doi"] = paper.get("DOI")
        standardized["title"] = paper.get("title", [""])[0] if isinstance(paper.get("title"), list) else paper.get("title", "")
        standardized["abstract"] = paper.get("abstract")
        standardized["publisher"] = paper.get("publisher")
        standardized["journal"] = paper.get("container-title", [""])[0] if isinstance(paper.get("container-title"), list) else paper.get("container-title")
        standardized["volume"] = paper.get("volume")
        standardized["issue"] = paper.get("issue")
        standardized["pages"] = paper.get("page")
        standardized["url"] = paper.get("URL")
        standardized["citation_count"] = paper.get("is-referenced-by-count", 0)
        standardized["references_count"] = paper.get("references-count", 0)
        standardized["source"] = "Crossref"
        
        # Handle publication date
        if paper.get("published-print"):
            date_parts = paper["published-print"]["date-parts"][0]
            if len(date_parts) >= 3:
                standardized["publication_date"] = f"{date_parts[0]}-{date_parts[1]:02d}-{date_parts[2]:02d}"
        elif paper.get("published-online"):
            date_parts = paper["published-online"]["date-parts"][0]
            if len(date_parts) >= 3:
                standardized["publication_date"] = f"{date_parts[0]}-{date_parts[1]:02d}-{date_parts[2]:02d}"
        elif paper.get("created"):
            date_parts = paper["created"]["date-parts"][0]
            if len(date_parts) >= 3:
                standardized["publication_date"] = f"{date_parts[0]}-{date_parts[1]:02d}-{date_parts[2]:02d}"
    
    elif "paperId" in paper:  # Semantic Scholar format
        standardized["doi"] = paper.get("externalIds", {}).get("DOI")
        standardized["title"] = paper.get("title", "")
        standardized["abstract"] = paper.get("abstract")
        standardized["journal"] = paper.get("venue")
        standardized["url"] = paper.get("url")
        standardized["publication_date"] = f"{paper.get('year')}-01-01" if paper.get("year") else None
        standardized["citation_count"] = paper.get("citationCount", 0)
        standardized["source"] = "Semantic Scholar"
        
        # Handle open access
        if paper.get("openAccessPdf") and paper["openAccessPdf"].get("url"):
            standardized["is_open_access"] = True
            standardized["open_access_url"] = paper["openAccessPdf"]["url"]
    
    elif "prism:doi" in paper:  # Scopus format
        standardized["doi"] = paper.get("prism:doi")
        standardized["title"] = paper.get("dc:title", "")
        standardized["journal"] = paper.get("prism:publicationName")
        standardized["volume"] = paper.get("prism:volume")
        standardized["issue"] = paper.get("prism:issueIdentifier")
        standardized["pages"] = paper.get("prism:pageRange")
        standardized["publication_date"] = paper.get("prism:coverDate")
        standardized["url"] = f"https://doi.org/{paper.get('prism:doi')}" if paper.get("prism:doi") else None
        standardized["citation_count"] = int(paper.get("citedby-count", 0))
        standardized["publisher"] = paper.get("dc:publisher")
        standardized["is_open_access"] = paper.get("openaccess") == "1" or paper.get("openaccessFlag") == True
        standardized["source"] = "Scopus"
        
        # Handle authors - Scopus often has single creator string
        if paper.get("dc:creator"):
            standardized["authors"] = [{"name": paper.get("dc:creator"), "affiliation": None}]
        elif paper.get("affiliation"):
            authors = []
            for aff in paper.get("affiliation", []):
                authors.append({"name": "Unknown", "affiliation": aff.get("affilname")})
            standardized["authors"] = authors
    
    elif ("url" in paper and "title" in paper and 
          ("id" in paper or paper.get("source") == "Exa.ai")):  # Exa format
        standardized["title"] = paper.get("title", "")
        standardized["url"] = paper.get("url")
        standardized["publication_date"] = paper.get("publishedDate")
        standardized["source"] = "Exa.ai"
        
        # Handle authors - Exa might provide author as string
        if paper.get("author"):
            if isinstance(paper["author"], str) and "," in paper["author"]:
                # Multiple authors in comma-separated string
                author_names = [name.strip() for name in paper["author"].split(",")]
                authors = [{"name": name, "affiliation": None} for name in author_names]
                standardized["authors"] = authors
            elif paper["author"] is not None:
                standardized["authors"] = [{"name": paper["author"], "affiliation": None}]
    
    elif "doi" in paper and "journal_name" in paper:  # Unpaywall format
        standardized["doi"] = paper.get("doi")
        standardized["title"] = paper.get("title", "")
        standardized["journal"] = paper.get("journal_name")
        standardized["publication_date"] = paper.get("published_date")
        standardized["url"] = paper.get("doi_url")
        standardized["publisher"] = paper.get("publisher")
        standardized["is_open_access"] = paper.get("is_oa", False)
        standardized["source"] = "Unpaywall"
        
        # Handle open access URL
        if paper.get("best_oa_location"):
            oa_location = paper["best_oa_location"]
            if oa_location.get("url_for_pdf"):
                standardized["open_access_url"] = oa_location["url_for_pdf"]
            elif oa_location.get("url"):
                standardized["open_access_url"] = oa_location["url"]
        
        # Handle authors
        if paper.get("z_authors"):
            authors = []
            for author in paper.get("z_authors", []):
                name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                authors.append({"name": name, "affiliation": None})
            standardized["authors"] = authors
    
    # Standardize authors if not already set by a specific provider format
    if not standardized["authors"]:
        authors = paper.get("authors", [])
        standardized_authors = []
        
        if authors:
            for author in authors:
                if isinstance(author, str):
                    standardized_authors.append({"name": author, "affiliation": None})
                elif isinstance(author, dict):
                    # Handle all possible variations of author dict formats
                    if "name" in author:
                        author_name = author["name"]
                    elif "given" in author and "family" in author:
                        author_name = f"{author['given']} {author['family']}".strip()
                    elif "firstName" in author and "lastName" in author:
                        author_name = f"{author['firstName']} {author['lastName']}".strip()
                    elif "first" in author and "last" in author:
                        author_name = f"{author['first']} {author['last']}".strip()
                    elif "$" in author:  # Scopus format
                        author_name = author.get("$", "Unknown")
                    elif "author" in author:
                        author_name = author["author"]
                    else:
                        # If no recognizable format is found, convert the whole dict to string
                        author_name = str(author)
                        if author_name.startswith("{") and author_name.endswith("}"):
                            author_name = "Unknown"
                    
                    # Get affiliation if available
                    affiliation = None
                    if "affiliation" in author:
                        affiliation = author["affiliation"]
                    elif "affiliations" in author and author["affiliations"]:
                        if isinstance(author["affiliations"], list) and author["affiliations"]:
                            affiliation = author["affiliations"][0].get("name", None)
                        else:
                            affiliation = author["affiliations"]
                    
                    standardized_authors.append({
                        "name": author_name,
                        "affiliation": affiliation
                    })
                elif author is not None:
                    # If it's not a string or dict but has some value
                    standardized_authors.append({"name": str(author), "affiliation": None})
        
        # If no valid authors were found, add placeholder
        if not standardized_authors:
            standardized_authors = [{"name": "Unknown", "affiliation": None}]
        
        standardized["authors"] = standardized_authors
    
    # Ensure valid publication date
    pub_date = standardized.get("publication_date")
    if pub_date and isinstance(pub_date, str):
        if len(pub_date) == 4 and pub_date.isdigit():  # Just a year
            standardized["publication_date"] = f"{pub_date}-01-01"
    
    return standardized




async def search_papers_semantic_scholar(query: str, limit: int = 20, 
                                        year_from: Optional[int] = None, 
                                        year_to: Optional[int] = None) -> Tuple[List[Dict[str, Any]], int]:
    """
    Search for papers using the Semantic Scholar API
    
    Args:
        query: Search query
        limit: Maximum number of results to return
        year_from: Earliest publication year
        year_to: Latest publication year
        
    Returns:
        Tuple of (list of papers, total results count)
    """
    # Import from api_client.py
    from app.services.api_client import get_provider_data
    
    # Prepare parameters
    params = {
        "limit": limit,
        "year_from": year_from,
        "year_to": year_to
    }
    
    # Use centralized provider function
    results, total = await get_provider_data("semantic_scholar", query, params)
    
    return results, total


async def search_papers_scopus(query: str, limit: int = 20, 
                              year_from: Optional[int] = None, 
                              year_to: Optional[int] = None,
                              author: Optional[str] = None,
                              journal: Optional[str] = None) -> Tuple[List[Dict[str, Any]], int]:
    """
    Search for papers using the Scopus API
    
    Args:
        query: Search query
        limit: Maximum number of results to return
        year_from: Earliest publication year
        year_to: Latest publication year
        author: Filter by author name
        journal: Filter by journal name
        
    Returns:
        Tuple of (list of papers, total results count)
    """
    # Import from api_client.py
    from app.services.api_client import get_provider_data
    
    # Prepare parameters
    params = {
        "limit": limit,
        "year_from": year_from,
        "year_to": year_to,
        "author": author,
        "journal": journal
    }
    
    # Use centralized provider function
    results, total = await get_provider_data("scopus", query, params)
    
    return results, total


async def search_papers_exa(query: str, limit: int = 20, 
                           year_from: Optional[int] = None, 
                           year_to: Optional[int] = None) -> Tuple[List[Dict[str, Any]], int]:
    """
    Search for papers using the Exa.ai API
    
    Args:
        query: Search query
        limit: Maximum number of results to return
        year_from: Earliest publication year
        year_to: Latest publication year
        
    Returns:
        Tuple of (list of papers, total results count)
    """
    # Import from api_client.py
    from app.services.api_client import get_provider_data
    
    # Prepare parameters
    params = {
        "limit": limit,
        "year_from": year_from,
        "year_to": year_to
    }
    
    # Use centralized provider function
    results, total = await get_provider_data("exa", query, params)
    
    return results, total


async def search_papers_combined(query: str, limit: int = 20, 
                                offset: int = 0,
                                year_from: Optional[int] = None,
                                year_to: Optional[int] = None,
                                author: Optional[str] = None,
                                journal: Optional[str] = None,
                                open_access_only: bool = False,
                                providers: List[str] = None,
                                sort: Optional[str] = None) -> Tuple[List[Dict[str, Any]], int]:
    """
    Search for papers using multiple academic APIs
    
    Args:
        query: Search query
        limit: Maximum number of results per provider
        offset: Number of results to skip (only supported by some providers)
        year_from: Earliest publication year
        year_to: Latest publication year
        author: Filter by author name
        journal: Filter by journal name
        open_access_only: Whether to return only open access papers
        providers: List of provider names to use (default: all available)
        sort: Sort order for results (only supported by some providers)
        
    Returns:
        Tuple of (list of papers, total results count)
    """
    if providers is None:
        providers = ["crossref", "semantic_scholar", "scopus", "exa"]
    
    # Handle single string provider to be consistent
    if isinstance(providers, str):
        providers = [providers]
    
    # Validate providers
    valid_providers = ["crossref", "semantic_scholar", "scopus", "exa"]
    providers = [p for p in providers if p in valid_providers]
    
    # Default to crossref if no valid providers
    if not providers:
        providers = ["crossref"]
    
    # Import from api_client.py
    from app.services.api_client import get_provider_data, calculate_relevance_score
    
    # Prepare search parameters for each provider
    all_results = []
    total_count = 0
    
    # Set a higher limit to get more results for local filtering
    search_limit = limit * 3  # Get more results than needed to handle filtering
    
    # Common params for all providers
    params = {
        "limit": search_limit,
        "year_from": year_from,
        "year_to": year_to,
        "author": author,
        "journal": journal,
        "sort": sort,
        "offset": offset  # Only used by some providers
    }
    
    # Process each provider and combine results
    for provider in providers:
        results, count = await get_provider_data(provider, query, params)
        
        # Filter by keyword relevance
        filtered_results = []
        for paper in results:
            # Skip papers without essential data
            if not paper.get("title"):
                continue
                
            # Calculate relevance score
            score = await calculate_relevance_score(paper, query)
            if score > 0:  # Only include relevant results
                paper['relevance_score'] = score
                filtered_results.append(paper)
        
        all_results.extend(filtered_results)
        total_count += len(filtered_results)
    
    # Apply open access filter if needed
    if open_access_only:
        all_results = [p for p in all_results if p.get('is_open_access', False)]
    
    # Remove duplicates based on DOI
    if all_results:
        unique_results = {}
        for paper in all_results:
            doi = paper.get('doi')
            if doi:
                # If the DOI already exists, keep the one with more information
                if doi in unique_results:
                    existing = unique_results[doi]
                    # Prefer papers with more information or higher relevance
                    existing_score = existing.get('relevance_score', 0) 
                    paper_score = paper.get('relevance_score', 0)
                    
                    if paper_score > existing_score:
                        unique_results[doi] = paper
                    elif paper_score == existing_score:
                        # Use additional criteria if scores are equal
                        if not existing.get('abstract') and paper.get('abstract'):
                            unique_results[doi] = paper
                        elif (not existing.get('citation_count') or existing.get('citation_count', 0) == 0) and paper.get('citation_count', 0) > 0:
                            unique_results[doi] = paper
                else:
                    unique_results[doi] = paper
            else:
                # For papers without DOI, use title as key
                title = paper.get('title', '')
                if title:
                    title_key = title.lower()
                    if title_key not in unique_results:
                        unique_results[title_key] = paper
        
        all_results = list(unique_results.values())
    
    # Sort by relevance score first, then by citation count
    all_results.sort(key=lambda x: (x.get('relevance_score', 0), x.get('citation_count', 0)), reverse=True)
    
    # Handle pagination locally based on the sorted results
    paginated_results = all_results[offset:offset+limit] if offset < len(all_results) else []
    
    # Make sure all papers have standard fields
    standardized_results = []
    for paper in paginated_results:
        # Ensure all required fields exist
        standardized = standardize_paper(paper)
        standardized_results.append(standardized)
    
    return standardized_results, min(len(all_results), 1000)  # Return actual result count for correct pagination
