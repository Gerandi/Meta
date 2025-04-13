// API Configuration
export const API_BASE_URL = 'http://localhost:8000';

// Routes
export const API_ROUTES = {
    PAPERS: {
        BASE_URL: API_BASE_URL,
        SEARCH: `${API_BASE_URL}/search/papers`,
        GET_BY_ID: (id) => `${API_BASE_URL}/papers/${id}`,
        CREATE: `${API_BASE_URL}/papers`,
        LIST: `${API_BASE_URL}/papers`,
        FIND_DOI: `${API_BASE_URL}/papers/find-doi`,
        BATCH_FIND_DOI: `${API_BASE_URL}/papers/batch-find-doi`,
        GET_PDF: (doi) => `${API_BASE_URL}/papers/pdf/${doi}`,
        GET_CONTENT: (id) => `${API_BASE_URL}/papers/${id}/content`,
        UPLOAD: `${API_BASE_URL}/papers/upload`,
        EXTRACT_METADATA: `${API_BASE_URL}/papers/extract-metadata`,
        IMPORT_BATCH: `${API_BASE_URL}/papers/import-batch`,
    },
    PROJECTS: {
        LIST: `${API_BASE_URL}/projects/`,
        GET_BY_ID: (id) => `${API_BASE_URL}/projects/${id}/`,
        CREATE: `${API_BASE_URL}/projects/`,
        UPDATE: (id) => `${API_BASE_URL}/projects/${id}/`,
        DELETE: (id) => `${API_BASE_URL}/projects/${id}/`,
        ADD_PAPERS: (projectId) => `${API_BASE_URL}/projects/${projectId}/papers/`,
        ADD_PAPERS_BATCH: (projectId) => `${API_BASE_URL}/projects/${projectId}/papers/batch/`,
        REMOVE_PAPER: (projectId, paperId) => `${API_BASE_URL}/projects/${projectId}/papers/${paperId}/`,
        GET_PAPERS: (projectId) => `${API_BASE_URL}/projects/${projectId}/papers/`,
    },
    PROCESSING: {
        CLEANUP: `${API_BASE_URL}/papers/cleanup`,
        FIND_DUPLICATES: `${API_BASE_URL}/papers/find-duplicates`,
        UPDATE_METADATA: (id) => `${API_BASE_URL}/papers/${id}/update-metadata`,
        RETRIEVE_PDF: (id) => `${API_BASE_URL}/papers/${id}/retrieve-pdf`,
        COUNTS: `${API_BASE_URL}/papers/counts`,
    },
    CODING: {
        SHEETS: {
            CREATE: `${API_BASE_URL}/coding/sheets`,
            GET_BY_ID: (id) => `${API_BASE_URL}/coding/sheets/${id}`,
            UPDATE: (id) => `${API_BASE_URL}/coding/sheets/${id}`,
            DELETE: (id) => `${API_BASE_URL}/coding/sheets/${id}`,
            GET_BY_PROJECT_ID: (projectId) => `${API_BASE_URL}/coding/sheets/project/${projectId}`,
            LIST: `${API_BASE_URL}/coding/sheets`,
        },
        DATA: {
            CREATE: `${API_BASE_URL}/coding/data`,
            GET_BY_PAPER_ID: (paperId) => `${API_BASE_URL}/coding/data/${paperId}`,
            UPDATE: (id) => `${API_BASE_URL}/coding/data/${id}`,
            DELETE: (id) => `${API_BASE_URL}/coding/data/${id}`,
        },
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
