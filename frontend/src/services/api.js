// frontend/src/services/api.js
import { API_ROUTES } from '../config';

async function handleResponse(response) {
  if (!response.ok) {
    let errorDetail = `HTTP error! status: ${response.status}`;
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorData.message || JSON.stringify(errorData);
    } catch (e) {
      // Ignore if response body is not JSON
    }
    throw new Error(errorDetail);
  }
  // Handle cases with no content (e.g., DELETE)
  if (response.status === 204) {
      return null;
  }
  return response.json();
}

export const projectService = {
  async listProjects() {
    const response = await fetch(API_ROUTES.PROJECTS.LIST);
    return handleResponse(response);
  },
  
  async createProject(projectData) {
    const response = await fetch(API_ROUTES.PROJECTS.CREATE, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(projectData),
    });
    return handleResponse(response);
  },
  
  async getProject(projectId) {
    const response = await fetch(API_ROUTES.PROJECTS.GET_BY_ID(projectId));
    return handleResponse(response);
  },
  
  async updateProject(projectId, projectData) {
    const response = await fetch(API_ROUTES.PROJECTS.UPDATE(projectId), {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(projectData),
    });
    return handleResponse(response);
  },
  
  async deleteProject(projectId) {
    const response = await fetch(API_ROUTES.PROJECTS.DELETE(projectId), {
      method: 'DELETE',
    });
    return handleResponse(response);
  },
  
  async getProjectPapers(projectId) {
    const response = await fetch(API_ROUTES.PROJECTS.GET_PAPERS(projectId));
    return handleResponse(response);
  },
  
  async addPaperToProject(projectId, paperId) {
    const response = await fetch(API_ROUTES.PROJECTS.ADD_PAPER(projectId), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ paper_id: paperId }),
    });
    return handleResponse(response);
  },
  
  async addPapersToProject(projectId, paperIds) {
    const response = await fetch(API_ROUTES.PROJECTS.ADD_PAPERS_BATCH(projectId), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ paper_ids: paperIds }),
    });
    return handleResponse(response);
  },
  
  async removePaperFromProject(projectId, paperId) {
    const response = await fetch(API_ROUTES.PROJECTS.REMOVE_PAPER(projectId, paperId), {
      method: 'DELETE',
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
      xhr.send(formData);
    });
  },
  
  async getPaper(paperId) {
    const response = await fetch(API_ROUTES.PAPERS.GET_BY_ID(paperId));
    return handleResponse(response);
  },
  
  async listPapers(skip = 0, limit = 100) {
    const response = await fetch(`${API_ROUTES.PAPERS.LIST}?skip=${skip}&limit=${limit}`);
    return handleResponse(response);
  },
  
  async deletePaper(paperId) {
    const response = await fetch(API_ROUTES.PAPERS.DELETE(paperId), {
      method: 'DELETE',
    });
    return handleResponse(response);
  },
  
  async updatePaper(paperId, paperData) {
    const response = await fetch(API_ROUTES.PAPERS.UPDATE(paperId), {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(paperData),
    });
    return handleResponse(response);
  },
  
  async getPaperPdf(doi) {
    const response = await fetch(API_ROUTES.PAPERS.GET_PDF(doi));
    return handleResponse(response);
  },
  
  async importPapersBatch(papers) {
    const response = await fetch(API_ROUTES.PAPERS.IMPORT_BATCH, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(papers),
    });
    return handleResponse(response);
  }
};

export const codingService = {
  async createCodingSheet(codingSheetData) {
    const response = await fetch(API_ROUTES.CODING.CREATE, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(codingSheetData),
    });
    return handleResponse(response);
  },
  
  async listCodingSheets() {
    const response = await fetch(API_ROUTES.CODING.LIST);
    return handleResponse(response);
  },
  
  async getCodingSheet(sheetId) {
    const response = await fetch(API_ROUTES.CODING.GET_BY_ID(sheetId));
    return handleResponse(response);
  },
  
  async getCodingSheetByProject(projectId) {
    const response = await fetch(API_ROUTES.CODING.GET_BY_PROJECT_ID(projectId));
    return handleResponse(response);
  },
  
  async updateCodingSheet(sheetId, codingSheetData) {
    const response = await fetch(API_ROUTES.CODING.UPDATE(sheetId), {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(codingSheetData),
    });
    return handleResponse(response);
  },
  
  async deleteCodingSheet(sheetId) {
    const response = await fetch(API_ROUTES.CODING.DELETE(sheetId), {
      method: 'DELETE',
    });
    return handleResponse(response);
  },
  
  async createCodingData(codingData) {
    const response = await fetch(API_ROUTES.CODING.SAVE_PAPER_CODING, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(codingData),
    });
    return handleResponse(response);
  },
  
  async getCodingData(paperId, sheetId = null) {
    let url = API_ROUTES.CODING.GET_FOR_PAPER(paperId);
    if (sheetId) {
      url += `?sheet_id=${sheetId}`;
    }
    const response = await fetch(url);
    return handleResponse(response);
  },
  
  async updateCodingData(codingDataId, codingData) {
    const response = await fetch(API_ROUTES.CODING.UPDATE(codingDataId), {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(codingData),
    });
    return handleResponse(response);
  },
  
  async deleteCodingData(codingDataId) {
    const response = await fetch(API_ROUTES.CODING.DELETE(codingDataId), {
      method: 'DELETE',
    });
    return handleResponse(response);
  }
};

export const resultsService = {
  async getResultsTable(projectId) {
    const response = await fetch(`${API_ROUTES.RESULTS.TABLE}?project_id=${projectId}`);
    return handleResponse(response);
  },
  
  async exportResults(projectId, format = 'csv') {
    const response = await fetch(`${API_ROUTES.RESULTS.EXPORT}?project_id=${projectId}&format=${format}`);
    return handleResponse(response);
  }
};
