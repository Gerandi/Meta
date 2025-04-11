# OpenAlex Migration Guide

This document outlines the changes made to migrate from multiple search providers to OpenAlex for paper searching in the Meta project.

## Overview

We've replaced the previous search implementation that used multiple APIs (Crossref, Semantic Scholar, Scopus, Exa.ai) with a single, robust OpenAlex integration using the PyAlex library. OpenAlex is an index of hundreds of millions of interconnected scholarly papers with a free and open API.

## Changes

### Backend Changes
1. Added new `openalex_search.py` service with the `search_papers_openalex` function
2. Configured PyAlex with proper settings for reliability
3. Updated API endpoints to use OpenAlex instead of multiple providers
4. Maintained API response format for backward compatibility

### Frontend Changes
1. Updated the database selector to use only OpenAlex
2. Modified loading message to reflect the single database
3. Fixed provider parameter handling
4. Added announcement banner about the new search engine
5. Fixed variable references to prevent undefined errors

## Benefits

- **Simpler Code**: Single API instead of multiple providers
- **Better Reliability**: Fewer error sources, no more [object Object] errors 
- **More Consistent Results**: All results come from a single, well-structured source
- **Improved Relevance**: OpenAlex has strong native relevance ranking
- **Better Performance**: The polite pool in OpenAlex offers faster and more consistent response times

## Testing

To test the implementation:
1. Start the backend server
2. Start the frontend application
3. Search for papers using various filters
4. Verify results appear correctly
5. Test pagination
6. Test sorting options

## References

- [OpenAlex Documentation](https://docs.openalex.org/)
- [PyAlex Documentation](https://pyalex.readthedocs.io/)
