# MetaReview Project Tracker

## Project Overview
MetaReview is a web application for researchers to find academic papers, code them systematically, and produce final tables for meta-analysis purposes. The app facilitates the entire meta-analysis workflow from paper discovery to final data export.

## Technology Stack
- **Frontend**: Vue.js, Vite, TailwindCSS
- **Backend**: Python with FastAPI 
- **Database**: SQL-based local file storage (SQLAlchemy)
- **External APIs**: 
  - Crossref (paper metadata)
  - Unpaywall (PDF access)
  - Semantic Scholar (paper search)
  - Scopus (paper search)
  - Exa.ai (paper search)
  - Scite (citation analytics - future feature)
  - Gemini (AI assistance - future feature)

## MVP Requirements
1. Paper search functionality
2. Metadata retrieval
3. Coding sheet configuration
4. Manual coding data entry
5. Results table generation
6. Data export

## Deferred Features
1. PDF viewing and annotation
2. AI-assisted coding
3. Team management and collaboration
4. User authentication
5. Advanced inter-rater reliability features

## Development Progress

### Phase 1: Core Setup & Search (MVP)
| Task | Status | Notes |
|------|--------|-------|
| Project structure setup | ✅ Complete | Basic directories created |
| API adapter for Crossref | ✅ Complete | Implementation working |
| API adapter for Unpaywall | ✅ Complete | Open Access PDF detection |
| API adapter for Semantic Scholar | ✅ Complete | Search integration working |
| API adapter for Scopus | ✅ Complete | Academic paper search |
| API adapter for Exa.ai | ✅ Complete | Additional search capability |
| Backend endpoints for search | ✅ Complete | Unified search API |
| Paper metadata storage system | ✅ Complete | SQLAlchemy models created |
| Frontend search interface | ✅ Complete | Multi-provider search with filters |
| PDF acquisition links | ✅ Complete | Open access PDFs supported |

### Phase 2: Coding System (MVP)
| Task | Status | Notes |
|------|--------|-------|
| Coding sheet data model | ✅ Complete | SQLAlchemy model implemented |
| Coding sheet configuration UI | ✅ Complete | Form fields and configuration |
| Coding sheet configuration backend | ✅ Complete | API endpoints created |
| Manual coding data entry UI | ✅ Complete | Form-based data entry |
| Manual coding data storage & retrieval | In Progress | API integration needed |
| Basic coding statistics calculations | Not Started | Planned for next sprint |

### Phase 3: Results & Analysis (MVP)
| Task | Status | Notes |
|------|--------|-------|
| Results table data model | ✅ Complete | SQLAlchemy model created |
| Results table UI | In Progress | Table view implemented, needs data |
| Results export functionality | ✅ Complete | CSV export working |
| Basic filtering and sorting | ✅ Complete | Client-side filters working |
| Data visualization placeholders | In Progress | Framework in place |

### Phase 4: Advanced Features
| Task | Status | Notes |
|------|--------|-------|
| Multi-provider search | ✅ Complete | Crossref, Semantic Scholar, Scopus, Exa.ai |
| Result standardization | ✅ Complete | Uniform data structure across providers |
| Batch paper operations | ✅ Complete | Mass selection and collection management |
| Advanced search filters | In Progress | Provider-specific filters needed |
| Relevance scoring | ✅ Complete | Implemented for better search results |
| Keyword extraction | ✅ Complete | Improves search relevance |
| Citation metrics integration | Not Started | After MVP |

### Future Development
| Feature | Priority | Notes |
|---------|----------|-------|
| PDF viewer integration | Medium | Basic placeholder in MVP |
| AI-assisted coding | Medium | Planned for next phase |
| Team management | Low | After MVP |
| User authentication | Low | After MVP |
| Inter-rater reliability tools | Medium | After MVP |
| Advanced search refinement | High | Next task after MVP |

## Current Sprint
Focus: Multi-provider search and batch operations

### Completed Tasks
- [✅] Added Semantic Scholar integration
- [✅] Added Scopus integration
- [✅] Added Exa.ai integration
- [✅] Implemented result standardization
- [✅] Added multi-selection for papers
- [✅] Implemented batch operations for collections
- [✅] Fixed circular import issues
- [✅] Improved error handling
- [✅] Standardized API client implementation
- [✅] Fixed relevance scoring algorithm
- [✅] Improved paper metadata extraction
- [✅] Fixed provider-specific search issues
- [✅] Implemented keyword extraction from papers

### In Progress
- [ ] Advanced search filtering improvements
- [ ] Provider-specific search options
- [ ] Coding sheet backend integration

## Next Sprint
Focus: Results table and coding sheet integration
