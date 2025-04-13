// API Configuration
export const API_BASE_URL = 'http://localhost:8000';

// Routes
export const API_ROUTES = {
    AUTH: {
        TOKEN: `${API_BASE_URL}/auth/token`,
        REGISTER: `${API_BASE_URL}/auth/register`,
        GET_ME: `${API_BASE_URL}/auth/users/me`,
    },
    PAPERS: {
        BASE_URL: API_BASE_URL,
        SEARCH: `${API_BASE_URL}/search/papers`,
        GET_BY_ID: (id) => `${API_BASE_URL}/papers/${id}`,
        CREATE: `${API_BASE_URL}/papers`,
        LIST: `${API_BASE_URL}/papers`,
        LIST_IMPORTED: `${API_BASE_URL}/papers/imported`,
        FIND_DOI: `${API_BASE_URL}/papers/find-doi`,
        BATCH_FIND_DOI: `${API_BASE_URL}/papers/batch-find-doi`,
        GET_PDF: (doi) => `${API_BASE_URL}/papers/pdf/${doi}`,
        GET_CONTENT: (id) => `${API_BASE_URL}/papers/${id}/content`,
        PROXY_PDF: (id) => `${API_BASE_URL}/papers/${id}/proxy-pdf`,
        UPLOAD: `${API_BASE_URL}/papers/upload`,
        EXTRACT_METADATA: `${API_BASE_URL}/papers/extract-metadata`,
        IMPORT_BATCH: `${API_BASE_URL}/papers/import-batch`,
        BATCH_DELETE: `${API_BASE_URL}/papers/batch-delete`,
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
        IMPORT_PAPER: (projectId) => `${API_BASE_URL}/projects/${projectId}/import-paper`,
    },
    PROCESSING: {
        CLEANUP: `${API_BASE_URL}/papers/cleanup`,
        FIND_DUPLICATES: `${API_BASE_URL}/processing/find-duplicates`,
        UPDATE_METADATA: (id) => `${API_BASE_URL}/papers/${id}/update-metadata`,
        RETRIEVE_PDF: (id) => `${API_BASE_URL}/papers/${id}/retrieve-pdf`,
        MARK_READY: (id) => `${API_BASE_URL}/papers/${id}/mark-ready`,
        PROJECT_PROCESSING: (projectId) => `${API_BASE_URL}/projects/${projectId}/processing`,
        COUNTS: `${API_BASE_URL}/papers/counts`,
        FETCH_METADATA: (id) => `${API_BASE_URL}/processing/papers/${id}/fetch-metadata`,
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
        TABLE: `${API_BASE_URL}/results/table`,
        EXPORT: `${API_BASE_URL}/results/export`,
    }
};

// Application configuration
export const APP_CONFIG = {
    ITEMS_PER_PAGE: 10,
    MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
};
