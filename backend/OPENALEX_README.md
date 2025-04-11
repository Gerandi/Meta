# OpenAlex Integration for Paper Search

This document explains the integration of OpenAlex through PyAlex for paper search in the Meta project.

## Overview

The original search implementation using multiple APIs (Crossref, Semantic Scholar, Scopus, Exa.ai) has been replaced with a single, robust OpenAlex integration using the PyAlex library. OpenAlex is an index of hundreds of millions of interconnected scholarly papers with a free and open API.

## Benefits

- **Simpler Code**: Single API instead of multiple providers
- **Better Reliability**: Fewer error sources, no [object Object] errors
- **More Consistent Results**: All results come from a single, well-structured source
- **Improved Relevance**: OpenAlex has strong native relevance ranking
- **Better Performance**: The polite pool in OpenAlex offers faster and more consistent response times

## Implementation Details

The implementation includes:

1. A new service module `openalex_search.py` with the `search_papers_openalex` function
2. Updated API endpoints (/search and /advanced-search) to use the new service
3. Maintained the same API response format to ensure backward compatibility with the frontend

## Usage

The API endpoints work the same way as before:

```
GET /papers/search?query=machine+learning&limit=10&offset=0
GET /papers/advanced-search?query=machine+learning&year_from=2020&open_access_only=true
```

The `providers` parameter is kept for backward compatibility but is no longer used.

## Configuration

The PyAlex library is configured with:

- Email for the polite pool (`config.email = "meta@example.com"`) - change this to your actual email
- Retry settings for improved reliability
- Error handling consistent with the rest of the application

## Data Transformation

The OpenAlex data is transformed to match the existing API response format, including:

- Paper metadata (title, authors, DOI, publication date)
- Open access information
- Citation counts
- Abstracts (automatically converted from inverted index format)

## Future Improvements

Potential enhancements:

1. Add support for more advanced filters available in OpenAlex
2. Improve relevance scoring with custom algorithms
3. Implement caching for frequently used queries
4. Add more OpenAlex-specific features like citation networks
