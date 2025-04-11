# OpenAlex Integration for Paper Search

This document explains the integration of OpenAlex for paper search in the Meta project.

## Overview

The original search implementation using multiple APIs (Crossref, Semantic Scholar, Scopus, Exa.ai) has been replaced with a single, robust OpenAlex integration. OpenAlex is an index of hundreds of millions of interconnected scholarly papers with a free and open API.

## Benefits

- **Simpler Code**: Single API instead of multiple providers
- **Better Reliability**: Fewer error sources, no [object Object] errors
- **More Consistent Results**: All results come from a single, well-structured source
- **Improved Relevance**: OpenAlex has strong native relevance ranking
- **Better Performance**: The polite pool in OpenAlex offers faster and more consistent response times

## Architecture

The backend has been refactored to centralize all OpenAlex interactions:

1. **Central API Access**: All OpenAlex API calls are now centralized in `openalex_search.py`
2. **Removed Redundancy**: The `paper_provider.py` abstraction layer has been removed
3. **Service Organization**: 
   - `openalex_search.py`: Contains direct OpenAlex API interactions and search functionality
   - `doi_service.py`: Uses the centralized search function to find DOIs based on metadata
   - `pdf_service.py`: Uses OpenAlex for paper lookups with Unpaywall as a fallback

## Implementation Details

Core functionality includes:

1. `search_papers_openalex()`: Main search function with comprehensive filtering options
2. `get_paper_by_doi_openalex()`: Fetches paper details for a known DOI
3. Date parsing: OpenAlex date strings (YYYY-MM-DD) are automatically converted to datetime objects

## API Endpoints

The API endpoints work the same way as before:

```
GET /papers/search?query=machine+learning&limit=10&offset=0
```

Changes:
- The `providers` parameter and `client_pagination` parameters are removed (no longer needed)
- All search functionality is consolidated into a single endpoint

## Error Handling

The system includes robust error handling:
- Automatic retry for rate limits (429 errors)
- Exponential backoff for server errors
- Detailed logging for all API interactions

## Data Transformation

The OpenAlex data is transformed to match the Paper schema:

- Author information is structured to match the `Author` schema
- Publication dates are parsed into proper datetime objects
- Abstracts are reconstructed from the inverted index format
- Open access information is extracted and formatted consistently

## Configuration

OpenAlex is configured with:

- Email for the polite pool (`settings.OPENALEX_EMAIL`) - change this in your .env file
- Maximum results per page (100)
- Maximum total results for client-side pagination (200)

## Future Improvements

Potential enhancements:

1. Add support for more advanced filters available in OpenAlex
2. Implement caching for frequently used queries 
3. Add citation network visualization using OpenAlex relationships
4. Add check for OpenAlex's 10,000 result limit when using offset pagination
