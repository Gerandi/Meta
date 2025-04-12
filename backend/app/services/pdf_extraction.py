import os
import tempfile
import logging
import asyncio
import httpx
from typing import Dict, Any, Optional, List, Tuple
import json
import PyPDF2
from io import BytesIO

logger = logging.getLogger(__name__)

async def extract_metadata_from_pdf(file_content: bytes) -> Dict[str, Any]:
    """
    Extract basic metadata from a PDF file.
    
    Args:
        file_content: Raw PDF file content as bytes
    
    Returns:
        Dict containing extracted metadata (title, authors, etc.)
    """
    try:
        # Use PyPDF2 to extract basic metadata
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
        
        # Extract info from PDF metadata
        info = pdf_reader.metadata
        
        # Basic metadata extraction
        metadata = {
            "title": None,
            "authors": [],
            "year": None,
            "journal": None,
            "doi": None,
            "abstract": None,
        }
        
        # Try to extract title from PDF metadata
        if info and '/Title' in info:
            metadata["title"] = info['/Title']
        
        # Try to extract authors from PDF metadata
        if info and '/Author' in info:
            authors_text = info['/Author']
            # Handle different author separator formats
            if ',' in authors_text:
                authors = [a.strip() for a in authors_text.split(',')]
            elif ';' in authors_text:
                authors = [a.strip() for a in authors_text.split(';')]
            elif ' and ' in authors_text.lower():
                authors = [a.strip() for a in authors_text.split(' and ')]
            else:
                authors = [authors_text]
                
            metadata["authors"] = [{"name": author} for author in authors if author]
        
        # Extract year if available
        if info and '/CreationDate' in info:
            creation_date = info['/CreationDate']
            # Typical format: D:20220315...
            if creation_date.startswith('D:') and len(creation_date) >= 10:
                year = creation_date[2:6]  # Extract year portion
                try:
                    metadata["year"] = int(year)
                except ValueError:
                    pass
        
        # Try to extract text from first page for title if not found in metadata
        if not metadata["title"] and len(pdf_reader.pages) > 0:
            first_page_text = pdf_reader.pages[0].extract_text()
            if first_page_text:
                # Simple heuristic: first line of text is often the title
                lines = first_page_text.strip().split('\n')
                if lines:
                    candidate_title = lines[0].strip()
                    # Use first line if it's not too short and not too long
                    if len(candidate_title) > 10 and len(candidate_title) < 300:
                        metadata["title"] = candidate_title
        
        # Try to extract abstract if available
        if len(pdf_reader.pages) > 0:
            first_page_text = pdf_reader.pages[0].extract_text()
            if first_page_text:
                # Look for abstract section
                abstract_indicators = [
                    "abstract", "summary", "synopsis", "background"
                ]
                
                lower_text = first_page_text.lower()
                for indicator in abstract_indicators:
                    if indicator in lower_text:
                        # Find the position of the indicator
                        start_pos = lower_text.find(indicator)
                        if start_pos != -1:
                            # Start after the indicator word
                            abstract_start = start_pos + len(indicator)
                            # Extract text up to 1000 chars after the indicator
                            abstract_text = first_page_text[abstract_start:abstract_start+1000]
                            # Truncate at the next section header if present
                            next_section_pos = float('inf')
                            for section in ["introduction", "methods", "results", "discussion", "keywords"]:
                                pos = abstract_text.lower().find(section)
                                if pos != -1 and pos < next_section_pos:
                                    next_section_pos = pos
                            
                            if next_section_pos < float('inf'):
                                abstract_text = abstract_text[:next_section_pos]
                            
                            metadata["abstract"] = abstract_text.strip()
                            break
        
        # Look for DOI in the text
        doi_patterns = [
            "doi:", "doi.org/", "doi: ", "doi "
        ]
        
        all_text = ""
        for page in pdf_reader.pages[:3]:  # Check first 3 pages for DOI
            page_text = page.extract_text()
            if page_text:
                all_text += page_text
        
        all_text_lower = all_text.lower()
        for pattern in doi_patterns:
            if pattern in all_text_lower:
                start_idx = all_text_lower.find(pattern) + len(pattern)
                end_idx = start_idx
                while end_idx < len(all_text) and not all_text[end_idx].isspace():
                    end_idx += 1
                
                potential_doi = all_text[start_idx:end_idx].strip()
                if potential_doi and len(potential_doi) > 5:
                    metadata["doi"] = potential_doi
                    break
        
        return metadata
    
    except Exception as e:
        logger.error(f"Error extracting metadata from PDF: {str(e)}")
        return {
            "title": None,
            "authors": [],
            "year": None,
            "journal": None,
            "doi": None,
            "abstract": None,
            "error": str(e)
        }


async def enhance_metadata_with_api(basic_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhance the basic metadata extracted from PDF using external APIs 
    (e.g., DOI lookup, search by title)
    
    Args:
        basic_metadata: Basic metadata extracted from PDF
    
    Returns:
        Enhanced metadata with additional information from APIs
    """
    enhanced_metadata = basic_metadata.copy()
    
    try:
        # If we have a DOI, use it to fetch more complete metadata
        if enhanced_metadata.get("doi"):
            # This could be implemented to call DOI resolution services
            pass
        
        # If we have a title but no DOI, try to search by title to find matching paper
        elif enhanced_metadata.get("title"):
            # This could be implemented to search OpenAlex by title
            pass
        
        return enhanced_metadata
    
    except Exception as e:
        logger.error(f"Error enhancing metadata: {str(e)}")
        enhanced_metadata["enhancement_error"] = str(e)
        return enhanced_metadata


async def process_pdf_file(file_content: bytes, filename: str, project_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Process a PDF file to extract metadata and store the file.
    
    Args:
        file_content: Raw PDF file content
        filename: Original filename
        project_id: Optional project ID to organize files by project
    
    Returns:
        Dict containing the extracted metadata and file info
    """
    # Extract basic metadata from PDF
    metadata = await extract_metadata_from_pdf(file_content)
    
    # Add filename to metadata
    metadata["filename"] = filename
    metadata["file_size"] = len(file_content)
    metadata["project_id"] = project_id
    
    # Store the file in the appropriate project directory if project_id is provided
    file_path = await store_pdf_file(file_content, filename, project_id)
    
    if file_path:
        metadata["file_path"] = file_path
    
    return metadata


async def store_pdf_file(file_content: bytes, filename: str, project_id: Optional[int] = None) -> Optional[str]:
    """
    Store a PDF file to disk.
    
    Args:
        file_content: Raw PDF file content
        filename: Original filename
        project_id: Optional project ID to organize files by project
    
    Returns:
        Path to the stored file or None if storage failed
    """
    try:
        # Create base uploads directory if it doesn't exist
        base_upload_dir = os.path.join(os.getcwd(), "uploads")
        os.makedirs(base_upload_dir, exist_ok=True)
        
        # If project_id is provided, create a subdirectory for the project
        if project_id:
            upload_dir = os.path.join(base_upload_dir, f"project_{project_id}")
            os.makedirs(upload_dir, exist_ok=True)
        else:
            upload_dir = base_upload_dir
        
        # Generate a safe filename with UUID to avoid conflicts
        import uuid
        safe_filename = f"{uuid.uuid4()}_{os.path.basename(filename)}"
        file_path = os.path.join(upload_dir, safe_filename)
        
        # Write the file to disk
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        return file_path
    
    except Exception as e:
        logger.error(f"Error storing PDF file: {str(e)}")
        return None
