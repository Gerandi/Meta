import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from app.core.config import settings
from app.schemas.paper import Paper, Author


async def search_papers(query: str, limit: int = 10, offset: int = 0, sort: Optional[str] = None, order: Optional[str] = "desc") -> List[Paper]:
    """
    Search for papers using the Crossref API.
    """
    url = "https://api.crossref.org/works"
    
    params = {
        "query": query,
        "rows": limit,
        "offset": offset,
        "mailto": settings.CROSSREF_EMAIL,
    }
    
    # Add sort and order if provided
    if sort:
        params["sort"] = sort
        params["order"] = order
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        items = data.get("message", {}).get("items", [])
        
        papers: List[Paper] = []
        for item in items:
            try:
                # Extract authors
                authors = []
                for author in item.get("author", []):
                    name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                    affiliation = author.get("affiliation", [{}])[0].get("name") if author.get("affiliation") else None
                    authors.append(Author(name=name, affiliation=affiliation))
                
                # Extract publication date
                pub_date = None
                if "published-online" in item:
                    date_parts = item["published-online"]["date-parts"][0]
                    if len(date_parts) >= 3:
                        pub_date = datetime(date_parts[0], date_parts[1], date_parts[2])
                elif "published-print" in item:
                    date_parts = item["published-print"]["date-parts"][0]
                    if len(date_parts) >= 3:
                        pub_date = datetime(date_parts[0], date_parts[1], date_parts[2])
                elif "created" in item:
                    date_parts = item["created"]["date-parts"][0]
                    if len(date_parts) >= 3:
                        pub_date = datetime(date_parts[0], date_parts[1], date_parts[2])
                
                # Try to extract abstract if available
                abstract = None
                if "abstract" in item:
                    abstract = item.get("abstract")
                    
                # Try to extract keywords if available
                keywords = []
                if "subject" in item:
                    keywords = item.get("subject", [])
                    
                # Create paper object
                paper = Paper(
                    id=hash(item.get("DOI", "")),  # Temporary ID
                    title=item.get("title", [""])[0],
                    abstract=abstract,
                    doi=item.get("DOI"),
                    authors=authors,
                    publication_date=pub_date,
                    journal=item.get("container-title", [""])[0] if item.get("container-title") else None,
                    volume=item.get("volume"),
                    issue=item.get("issue"),
                    pages=item.get("page"),
                    publisher=item.get("publisher"),
                    url=f"https://doi.org/{item.get('DOI')}" if item.get("DOI") else None,
                    keywords=keywords,
                    is_open_access=False,  # Will be filled by Unpaywall
                    open_access_url=None,  # Will be filled by Unpaywall
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                papers.append(paper)
            except Exception as e:
                # Skip papers that can't be processed
                print(f"Error processing paper: {e}")
                continue
        
        return papers
