import httpx
import logging
from typing import Optional, Dict, Any

from app.core.config import settings
# Updated import to use the consolidated direct client
from app.services.openalex_direct import get_paper_by_doi_direct 

logger = logging.getLogger(__name__)

async def get_paper_pdf_url(doi: str) -> Optional[str]:
    """
    Get PDF URL for a paper primarily using OpenAlex, with fallback to Unpaywall.
    
    Args:
        doi: The DOI of the paper
        
    Returns:
        URL to the PDF if available, None otherwise
    """
    # First try OpenAlex using the consolidated direct function
    paper_data = await get_paper_by_doi_direct(doi)
    
    if paper_data:
        # Extract open access URL from the formatted OpenAlex data
        # The direct function now returns 'open_access_url' directly
        oa_url = paper_data.get("open_access_url")
        if oa_url:
            logger.info(f"PDF URL found in OpenAlex for DOI {doi}")
            return oa_url

    # Fallback to Unpaywall if OpenAlex didn't have the PDF URL
    logger.info(f"OpenAlex didn't have PDF URL for DOI {doi}, falling back to Unpaywall")
    from app.services.unpaywall import get_paper_access
    
    access_info = await get_paper_access(doi)
    return access_info.get("open_access_url")

async def get_paper_details(doi: str) -> Dict[str, Any]:
    """
    Get detailed information about a paper primarily using OpenAlex, with fallback to Unpaywall.
    
    Args:
        doi: The DOI of the paper
    
    Returns:
        Dictionary with paper details
    """
    # First try OpenAlex using the consolidated direct function
    paper_data = await get_paper_by_doi_direct(doi)
    
    if paper_data:
        # Use the formatted data directly from get_paper_by_doi_direct
        logger.info(f"Found paper details in OpenAlex for DOI {doi}")
        # Return a subset relevant to this function's purpose if needed, 
        # or the full formatted data. Let's return relevant fields.
        return {
            "is_oa": paper_data.get("is_open_access", False),
            "pdf_url": paper_data.get("open_access_url"),
            "url": paper_data.get("url"),
            "oa_status": "open" if paper_data.get("is_open_access") else "closed",
            # Journal OA status might need re-evaluation based on available fields in formatted_paper
            # For now, let's assume it's not directly available in the simplified format
            "journal_is_oa": None, 
            "journal_issns": None # Also not directly in the simplified format
        }
    
    # Fallback to Unpaywall
    logger.info(f"OpenAlex didn't have details for DOI {doi}, falling back to Unpaywall")
    url = f"https://api.unpaywall.org/v2/{doi}"
    
    params = {
        "email": settings.UNPAYWALL_EMAIL
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
