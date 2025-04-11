# MetaReview Project Tracker

## Last Updated: April 11, 2025

## Overall Progress
- [🟢] Backend API Structure - 85% complete
- [🟢] Frontend Implementation - 75% complete 
- [🟠] AI Integration - 10% complete
- [🔴] User Management - 0% complete

## MVP Components
| Component | Status | Priority | Next Steps |
|-----------|--------|----------|-----------|
| Paper Search & Import | 🟢 Enhanced | 1-High | Implement citation network visualization |
| PDF Viewer | 🟡 Partial | 1-High | Add actual PDF rendering (post-MVP) |
| Coding Sheet | 🟡 Partial | 1-High | Connect to backend API |
| Results Table | 🟡 Started | 2-Medium | Implement data fetching and display |
| Inter-rater Tools | 🔴 Not Started | 3-Low | MVP will use single-coder approach |
| Collections Management | 🟢 Enhanced | 1-High | Batch operations implemented |

## Current Sprint Completed Tasks
- ✅ Completed migration to OpenAlex as the single search provider
- ✅ Removed unused provider implementations (Crossref, Semantic Scholar, etc.)
- ✅ Updated configuration for OpenAlex API with proper email settings
- ✅ Simplified search service to rely solely on OpenAlex
- ✅ Updated DOI lookup service to use OpenAlex
- ✅ Updated documentation to reflect completed migration
- ✅ Implemented Vue components for paper search
- ✅ Created PDF viewer UI (without full PDF.js integration for MVP)
- ✅ Implemented coding sheet interface
- ✅ Fixed dependency and configuration issues
- ✅ Connected paper search frontend to backend API
- ✅ Implemented paper collections management
- ✅ Added data persistence (papers and collections)
- ✅ Added CSV export functionality for collections
- ✅ Implemented paper selection and batch operations
- ✅ Enhanced result standardization across different providers
- ✅ Fixed circular import issues in backend API
- ✅ Improved error handling for search providers
- ✅ Fixed relevance scoring for search results
- ✅ Improved paper metadata extraction and formatting
- ✅ Implemented advanced filtering of search results
- ✅ Fixed API parameter handling to prevent unprocessable entity errors

## Current Sprint Remaining Tasks
- Add citation network visualization using OpenAlex relationships
- Connect coding sheet to backend API
- Implement results table data integration
- Add user feedback for long-running operations

## Notes
- Successfully migrated to OpenAlex as the sole search provider for better consistency and reliability
- PDF viewer functionality simplified for MVP
- All critical frontend components are now in place
- Paper search and collections management fully functional
- Batch operations for collections now available
- Focus areas for next sprint: advanced filtering, coding sheet integration, and results table
- Search algorithm improved to return more relevant results
- Fixed issues with provider-specific searches by standardizing on OpenAlex