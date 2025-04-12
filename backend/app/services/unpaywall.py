import httpx
import logging
from typing import Dict, Any, Optional

from app.core.config import settings
from app.services.unpaywall_client import get_unpaywall_data

logger = logging.getLogger(__name__)

async def get_paper_access(doi: str) -> Dict[str, Any]:
    """
    Get open access information for a paper using the Unpaywall API.
    """
    # Call our standardized API client
    data = await get_unpaywall_data(doi)
    
    # Handle error case
    if 'error' in data:
        logger.warning(f"Unpaywall API error for DOI {doi}: {data.get('error')}")
        return {
            "is_open_access": False,
            "open_access_url": None,
            "open_access_status": None,
            "journal_is_oa": False,
            "error": data.get('error')
        }
    
    # Extract the fields we need
    result = {
        "is_open_access": data.get("is_open_access", False),
        "open_access_url": data.get("open_access_url"),
        "open_access_status": data.get("oa_status"),
        "journal_is_oa": data.get("journal_is_oa", False)
    }
    
    return result
