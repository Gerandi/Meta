// frontend/src/services/api.js
import { API_ROUTES } from '../config';
import { useAuthStore } from '../stores/auth'; // Import auth store

// Helper to get headers with auth token
function getAuthHeaders() {
  const authStore = useAuthStore();
  // --- ADD LOGGING ---
  console.log(`[API Service] getAuthHeaders called. IsAuthenticated: ${authStore.isAuthenticated}, Token present: ${!!authStore.token}`);
  // --- END LOGGING ---
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };
  if (authStore.isAuthenticated && authStore.token) {
    headers['Authorization'] = `Bearer ${authStore.token}`;
  } else {
    console.warn('[API Service] getAuthHeaders called, but user is not authenticated or token is missing.'); // Add warning
  }
  return headers;
}

// Processing service for papers that need processing
export const processingService = {
  async getPapersForProcessing(projectId, skip = 0, limit = 100, filters = {}) {
    const params = new URLSearchParams({ skip, limit });
    
    // Add any additional filters
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value);
      }
    });
    
    const url = `${API_ROUTES.PROCESSING.PROJECT_PROCESSING(projectId)}?${params.toString()}`;
    const response = await fetch(url, { headers: getAuthHeaders() });
    return handleResponse(response);
  },

  async retrievePdfForPaper(paperId) {
    const response = await fetch(API_ROUTES.PROCESSING.RETRIEVE_PDF(paperId), {
      method: 'POST',
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  },

  async markPaperReady(paperId) {
    const response = await fetch(API_ROUTES.PROCESSING.MARK_READY(paperId), {
      method: 'PUT',
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  },

  // Find duplicates within a project
  async findProjectDuplicates(projectId) {
    const response = await fetch(`${API_ROUTES.PROCESSING.FIND_DUPLICATES}?project_id=${projectId}`, { 
      headers: getAuthHeaders() 
    });
    return handleResponse(response);
  },
  
  // Fetch metadata for a paper using its DOI or title/author
  async fetchMetadataForPaper(paperId) {
    const response = await fetch(API_ROUTES.PROCESSING.FETCH_METADATA(paperId), {
      method: 'POST',
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  }
};

async function handleResponse(response) {
  // Add logging for non-ok responses
  if (!response.ok) {
    console.error(`[API Service] API call failed: ${response.url} - Status: ${response.status}`);
    let errorDetail = `HTTP error! status: ${response.status}`;
    if (response.status === 401) {
      // Unauthorized - likely invalid/expired token
      const authStore = useAuthStore();
      authStore.logout(); // Log out the user
      // Optionally redirect to login page here using router
      errorDetail = "Authentication failed. Please log in again.";
    } else {
      try {
        const errorData = await response.json();
        errorDetail = errorData.detail || errorData.message || JSON.stringify(errorData);
      } catch (e) {
        // Ignore if response body is not JSON
      }
    }
    throw new Error(errorDetail);
  }
  // Handle cases with no content (e.g., DELETE)
  if (response.status === 204 || response.headers.get('content-length') === '0') {
      return null;
  }
  return response.json();
}

export const projectService = {
  async listProjects() {
    const response = await fetch(API_ROUTES.PROJECTS.LIST, { headers: getAuthHeaders() });
    return handleResponse(response);
  },
  
  async importAndAddPaperToProject(projectId, paperData) {
    const response = await fetch(API_ROUTES.PROJECTS.IMPORT_PAPER(projectId), {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(paperData),
    });
    return handleResponse(response);
  },
  
  async createProject(projectData) {
    const response = await fetch(API_ROUTES.PROJECTS.CREATE, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(projectData),
    });
    return handleResponse(response);
  },
  
  async getProject(projectId) {
    const response = await fetch(API_ROUTES.PROJECTS.GET_BY_ID(projectId), { headers: getAuthHeaders() });
    return handleResponse(response);
  },
  
  async updateProject(projectId, projectData) {
    const response = await fetch(API_ROUTES.PROJECTS.UPDATE(projectId), {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(projectData),
    });
    return handleResponse(response);
  },
  
  async deleteProject(projectId) {
    const response = await fetch(API_ROUTES.PROJECTS.DELETE(projectId), {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  },
  
  async getProjectPapers(projectId) {
    const response = await fetch(API_ROUTES.PROJECTS.GET_PAPERS(projectId), { headers: getAuthHeaders() });
    return handleResponse(response);
  },
  
  async addPaperToProject(projectId, paperId) {
    const response = await fetch(API_ROUTES.PROJECTS.ADD_PAPER(projectId), {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ paper_id: paperId }),
    });
    return handleResponse(response);
  },
  
  async addPapersToProject(projectId, paperIds) {
    const response = await fetch(API_ROUTES.PROJECTS.ADD_PAPERS_BATCH(projectId), {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ paper_ids: paperIds }),
    });
    return handleResponse(response);
  },
  
  async removePaperFromProject(projectId, paperId) {
    const response = await fetch(API_ROUTES.PROJECTS.REMOVE_PAPER(projectId, paperId), {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  }
};

export const paperService = {
  async searchPapers(searchParams) {
    const params = new URLSearchParams();
    Object.entries(searchParams).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value);
      }
    });
    
    const url = `${API_ROUTES.PAPERS.SEARCH}?${params.toString()}`;
    const response = await fetch(url);
    return handleResponse(response);
  },
  
  async uploadPaper(formData, onProgress) {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      const authStore = useAuthStore();
      
      if (onProgress && typeof onProgress === 'function') {
        xhr.upload.addEventListener('progress', (event) => {
          if (event.lengthComputable) {
            const percentComplete = Math.round((event.loaded / event.total) * 100);
            onProgress(percentComplete);
          }
        });
      }
      
      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            const response = JSON.parse(xhr.responseText);
            resolve(response);
          } catch (e) {
            reject(new Error('Invalid response format'));
          }
        } else {
          reject(new Error(`Upload failed: ${xhr.statusText}`));
        }
      });
      
      xhr.addEventListener('error', () => {
        reject(new Error('Network error during upload'));
      });
      
      xhr.open('POST', API_ROUTES.PAPERS.UPLOAD);
      // Set Authorization header for XHR
      if (authStore.isAuthenticated && authStore.token) {
        xhr.setRequestHeader('Authorization', `Bearer ${authStore.token}`);
      }
      xhr.send(formData);
    });
  },
  
  async getPaper(paperId) {
    const response = await fetch(API_ROUTES.PAPERS.GET_BY_ID(paperId), { headers: getAuthHeaders() });
    return handleResponse(response);
  },
  
  async listPapers(skip = 0, limit = 100, filters = {}) {
    const params = new URLSearchParams({ skip, limit });
    
    // Add any additional filters
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value);
      }
    });
    
    const response = await fetch(`${API_ROUTES.PAPERS.LIST}?${params.toString()}`, { headers: getAuthHeaders() });
    return handleResponse(response);
  },
  
  async listImportedPapers(skip = 0, limit = 100) {
    const response = await fetch(`${API_ROUTES.PAPERS.LIST_IMPORTED}?skip=${skip}&limit=${limit}`, { headers: getAuthHeaders() });
    return handleResponse(response);
  },
  
  async deletePaper(paperId) {
    const response = await fetch(API_ROUTES.PAPERS.DELETE(paperId), {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  },
  
  async batchDeletePapers(paperIds) {
    const response = await fetch(API_ROUTES.PAPERS.BATCH_DELETE, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(paperIds), // This should be a list of paper IDs
    });
    return handleResponse(response);
  },
  
  async updatePaper(paperId, paperData) {
    const response = await fetch(API_ROUTES.PAPERS.UPDATE(paperId), {
      method: 'PATCH',
      headers: getAuthHeaders(),
      body: JSON.stringify(paperData),
    });
    return handleResponse(response);
  },
  
  async getPaperPdf(doi) {
    const response = await fetch(API_ROUTES.PAPERS.GET_PDF(doi), { headers: getAuthHeaders() });
    return handleResponse(response);
  },
  
  async importPapersBatch(papers) {
    const response = await fetch(API_ROUTES.PAPERS.IMPORT_BATCH, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(papers),
    });
    return handleResponse(response);
  }
};

export const codingService = {
  async createCodingSheet(codingSheetData) {
    const response = await fetch(API_ROUTES.CODING.SHEETS.CREATE, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(codingSheetData),
    });
    return handleResponse(response);
  },
  
  async listCodingSheets() {
    const response = await fetch(API_ROUTES.CODING.SHEETS.LIST, { headers: getAuthHeaders() });
    return handleResponse(response);
  },
  
  async getCodingSheet(sheetId) {
    const response = await fetch(API_ROUTES.CODING.SHEETS.GET_BY_ID(sheetId), { headers: getAuthHeaders() });
    return handleResponse(response);
  },
  
  async getCodingSheetByProject(projectId) {
    const response = await fetch(API_ROUTES.CODING.SHEETS.GET_BY_PROJECT_ID(projectId), { headers: getAuthHeaders() });
    return handleResponse(response);
  },
  
  async updateCodingSheet(sheetId, codingSheetData) {
    const response = await fetch(API_ROUTES.CODING.SHEETS.UPDATE(sheetId), {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(codingSheetData),
    });
    return handleResponse(response);
  },
  
  async deleteCodingSheet(sheetId) {
    const response = await fetch(API_ROUTES.CODING.SHEETS.DELETE(sheetId), {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  },
  
  async createCodingData(codingData) {
    const response = await fetch(API_ROUTES.CODING.DATA.CREATE, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(codingData),
    });
    return handleResponse(response);
  },
  
  async getCodingData(paperId, sheetId = null) {
    let url = API_ROUTES.CODING.DATA.GET_BY_PAPER_ID(paperId);
    if (sheetId) {
      url += `?sheet_id=${sheetId}`;
    }
    const response = await fetch(url, { headers: getAuthHeaders() });
    return handleResponse(response);
  },
  
  async updateCodingData(codingDataId, codingData) {
    const response = await fetch(API_ROUTES.CODING.DATA.UPDATE(codingDataId), {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(codingData),
    });
    return handleResponse(response);
  },
  
  async deleteCodingData(codingDataId) {
    const response = await fetch(API_ROUTES.CODING.DATA.DELETE(codingDataId), {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  }
};

export const resultsService = {
  async getResultsTable(projectId) {
    const response = await fetch(`${API_ROUTES.RESULTS.TABLE}?project_id=${projectId}`, { headers: getAuthHeaders() });
    return handleResponse(response);
  },
  
  async exportResults(projectId, format = 'csv') {
    const response = await fetch(`${API_ROUTES.RESULTS.EXPORT}?project_id=${projectId}&format=${format}`, { headers: getAuthHeaders() });
    return handleResponse(response);
  }
};
