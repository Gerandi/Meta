// API Configuration
export const API_BASE_URL = 'http://localhost:8000';

// Routes
export const API_ROUTES = {
    PAPERS: {
        BASE_URL: API_BASE_URL,
        SEARCH: `${API_BASE_URL}/papers/search`,
        GET_BY_ID: (id) => `${API_BASE_URL}/papers/${id}`,
        CREATE: `${API_BASE_URL}/papers`,
        FIND_DOI: `${API_BASE_URL}/papers/find-doi`,
        BATCH_FIND_DOI: `${API_BASE_URL}/papers/batch-find-doi`,
        GET_PDF: (doi) => `${API_BASE_URL}/papers/pdf/${doi}`,
        ADVANCED_SEARCH: `${API_BASE_URL}/papers/advanced-search`,
        TEST_SEARCH: `${API_BASE_URL}/papers/test-search`,
        SEARCH: `${API_BASE_URL}/papers/search`,
    },
    COLLECTIONS: {
        LIST: `${API_BASE_URL}/collections`,
        GET_BY_ID: (id) => `${API_BASE_URL}/collections/${id}`,
        CREATE: `${API_BASE_URL}/collections`,
        ADD_PAPER: (collectionId, paperId) => `${API_BASE_URL}/collections/${collectionId}/papers/${paperId}`,
        REMOVE_PAPER: (collectionId, paperId) => `${API_BASE_URL}/collections/${collectionId}/papers/${paperId}`,
        GET_PAPERS: (collectionId) => `${API_BASE_URL}/collections/${collectionId}/papers`,
    },
    CODING: {
        CREATE: `${API_BASE_URL}/coding`,
        GET_BY_ID: (id) => `${API_BASE_URL}/coding/${id}`,
    },
    RESULTS: {
        GENERATE: `${API_BASE_URL}/results/generate`,
        GET_BY_ID: (id) => `${API_BASE_URL}/results/${id}`,
    }
};

// Application configuration
export const APP_CONFIG = {
    ITEMS_PER_PAGE: 10,
    MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
};
