import httpx
import logging
from typing import Optional, Dict, Any

from app.core.config import settings

logger = logging.getLogger(__name__)

async def get_paper_by_doi_openalex(doi: str) -> Optional[Dict[str, Any]]:
    """
    Get paper details from OpenAlex using DOI
    
    Args:
        doi: The DOI of the paper
        
    Returns:
        Paper details if available, None otherwise
    """
    try:
        # OpenAlex uses DOIs with "https://doi.org/" prefix
        formatted_doi = doi
        if not formatted_doi.startswith("https://doi.org/"):
            formatted_doi = f"https://doi.org/{doi}"
        
        url = f"https://api.openalex.org/works/{formatted_doi}"
        params = {"mailto": settings.OPENALEX_EMAIL}
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"OpenAlex API error for DOI {doi}: HTTP {response.status_code}")
                return None
    
    except Exception as e:
        logger.error(f"Error retrieving paper details from OpenAlex for DOI {doi}: {str(e)}")
        return None

async def get_paper_pdf_url(doi: str) -> Optional[str]:
    """
    Get PDF URL for a paper primarily using OpenAlex, with fallback to Unpaywall.
    
    Args:
        doi: The DOI of the paper
        
    Returns:
        URL to the PDF if available, None otherwise
    """
    # First try OpenAlex
    paper_data = await get_paper_by_doi_openalex(doi)
    
    if paper_data:
        # Extract open access URL from OpenAlex data
        if paper_data.get("open_access") and paper_data["open_access"].get("is_oa"):
            oa_url = paper_data["open_access"].get("oa_url")
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
    paper_info = {
        "is_oa": False,
        "pdf_url": None,
        "url": None,
        "oa_status": None,
        "journal_is_oa": False
    }
    
    # First try OpenAlex
    paper_data = await get_paper_by_doi_openalex(doi)
    
    if paper_data:
        # Extract data from OpenAlex
        paper_info["is_oa"] = paper_data.get("open_access", {}).get("is_oa", False)
        if paper_info["is_oa"]:
            paper_info["pdf_url"] = paper_data.get("open_access", {}).get("oa_url")
        
        # Get URL
        paper_info["url"] = paper_data.get("doi") or paper_data.get("primary_location", {}).get("landing_page_url")
        
        # Get OA status
        paper_info["oa_status"] = "open" if paper_info["is_oa"] else "closed"
        
        # Get journal info
        if paper_data.get("primary_location") and paper_data["primary_location"].get("source"):
            paper_info["journal_is_oa"] = paper_data["primary_location"]["source"].get("is_oa", False)
            paper_info["journal_issns"] = paper_data["primary_location"]["source"].get("issn", [])
        
        logger.info(f"Found paper details in OpenAlex for DOI {doi}")
        return paper_info
    
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
