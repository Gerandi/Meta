import httpx
import logging
from typing import Optional, Dict, Any

from app.core.config import settings

logger = logging.getLogger(__name__)

async def get_paper_pdf_url(doi: str) -> Optional[str]:
    """
    Get PDF URL for a paper using the Unpaywall API.
    
    Args:
        doi: The DOI of the paper
        
    Returns:
        URL to the PDF if available, None otherwise
    """
    # Get paper access info from Unpaywall
    from app.services.unpaywall import get_paper_access
    
    access_info = await get_paper_access(doi)
    return access_info.get("open_access_url")


async def get_paper_details(doi: str) -> Dict[str, Any]:
    """
    Get detailed information about a paper using the Unpaywall API
    
    Args:
        doi: The DOI of the paper
    
    Returns:
        Dictionary with paper details
    """
    url = f"https://api.unpaywall.org/v2/{doi}"
    
    params = {
        "email": settings.UNPAYWALL_EMAIL
    }
    
    paper_info = {
        "is_oa": False,
        "pdf_url": None,
        "url": None,
        "oa_status": None,
        "journal_is_oa": False
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                paper_info["is_oa"] = data.get("is_oa", False)
                paper_info["oa_status"] = data.get("oa_status")
                paper_info["journal_is_oa"] = data.get("journal_is_oa", False)
                paper_info["journal_issns"] = data.get("journal_issns")
                
                # Get PDF URL and other URLs
                best_location = data.get('best_oa_location')
                if best_location:
                    paper_info["pdf_url"] = best_location.get('url_for_pdf')
                    paper_info["url"] = best_location.get('url')
                    paper_info["version"] = best_location.get('version')
                    paper_info["license"] = best_location.get('license')
            elif response.status_code == 422:
                logger.warning(f"Unpaywall API error for DOI {doi}: Invalid DOI format")
            else:
                logger.warning(f"Unpaywall API error for DOI {doi}: HTTP {response.status_code}")
    
    except Exception as e:
        logger.error(f"Error retrieving paper details for DOI {doi}: {str(e)}")
    
    return paper_info
