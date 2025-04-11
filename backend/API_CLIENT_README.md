# Standardized API Client Implementation

This document outlines the standardized API client for the Meta Research Review project and how it integrates with various academic paper APIs.

## Overview

The API client provides a consistent interface for retrieving academic paper data from multiple providers, including:

- Crossref
- Semantic Scholar
- Scopus
- Exa.ai
- Unpaywall

All responses are standardized to ensure a consistent data format across providers.

## API Client Structure

### Main Components

- `api_client.py`: Core implementation of all provider-specific API clients
- Integration with existing services:
  - `additional_providers.py`: Uses standardized API client for combined search
  - `paper_provider.py`: Uses standardized API client for Crossref search
  - `unpaywall.py`: Uses standardized API client for Unpaywall data

### Configuration

API keys are configured in:
1. `.env` file - contains all API keys
2. `config.py` - reads keys from environment variables
3. `api_client.py` - uses settings from config

## Standardized Data Format

All API clients return data in a standardized format with the following common fields:

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
  "source": "Provider name"
}
```

## Testing

To test the API client implementation:

1. Run the test script:
   ```
   run_test.bat
   ```

2. View the implementation summary:
   ```
   show_summary.bat
   ```

## Next Steps

1. Implement the paper processing component in the frontend
2. Connect the frontend to the backend API endpoints
3. Add more detailed error handling and user feedback in the UI
