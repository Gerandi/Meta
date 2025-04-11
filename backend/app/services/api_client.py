"""
API Client for Unpaywall PDF lookup.
This module provides async functions to fetch open access availability data from Unpaywall.
"""

import httpx
import logging
from typing import Dict, Any

from app.core.config import settings

# Get Unpaywall email from settings
UNPAYWALL_EMAIL = settings.UNPAYWALL_EMAIL

logger = logging.getLogger(__name__)

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
