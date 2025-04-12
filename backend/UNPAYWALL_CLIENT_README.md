# Academic Paper API Implementation

This document outlines the API implementation for the Meta Research Review project and how it retrieves academic paper data.

## Overview

The system now exclusively uses the OpenAlex API as the primary data source for academic papers, with Unpaywall as a fallback for obtaining PDF URLs and open access information.

## API Structure

### Main Components

- `openalex_direct.py`: Core implementation for paper search using OpenAlex API
- `doi_service.py`: Retrieves detailed paper information by DOI
- `pdf_service.py`: Obtains PDF URLs using Unpaywall when needed
- `unpaywall_client.py`: Simplified implementation for Unpaywall functionality

### Configuration

API keys are configured in:
1. `.env` file - contains OpenAlex email and Unpaywall email
2. `config.py` - reads keys from environment variables

## Standardized Data Format

The OpenAlex search service returns data in a standardized format with the following common fields:

```json
{
  "title": "Paper title",
  "doi": "10.xxxx/xxxxx",
  "authors": [
    {
      "name": "Author Name",
      "affiliation": "Author Institution"
    }
  ],
  "publication_date": "YYYY-MM-DD",
  "abstract": "Paper abstract text",
  "journal": "Journal name",
  "volume": "Volume number",
  "issue": "Issue number",
  "pages": "Page range",
  "publisher": "Publisher name",
  "url": "URL to paper",
  "citation_count": 123,
  "references_count": 45,
  "is_open_access": true,
  "open_access_url": "URL to open access version",
  "source": "OpenAlex"
}
```

## Testing

To test the OpenAlex search implementation:

1. Run the search test script:
   ```
   run_search_test.bat
   ```

## Next Steps

1. Further optimize OpenAlex API usage for efficiency
2. Enhance PDF retrieval capabilities
3. Add more detailed error handling and user feedback in the UI
