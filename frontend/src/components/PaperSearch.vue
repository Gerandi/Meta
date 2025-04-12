<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <h1 class="text-2xl font-bold mb-6">Find & Import Papers</h1>

    <div class="bg-white rounded-lg shadow mb-6">
      <div class="flex border-b">
        <button 
          class="py-4 px-6 font-medium flex items-center"
          :class="activeTab === 'search' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'"
          @click="activeTab = 'search'"
        >
          <font-awesome-icon icon="search" class="mr-2" />
          Search Databases
        </button>
        <button 
          class="py-4 px-6 font-medium flex items-center"
          :class="activeTab === 'upload' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'"
          @click="activeTab = 'upload'"
        >
          <font-awesome-icon icon="upload" class="mr-2" />
          Upload PDFs
        </button>
      </div>

      
            <SearchTab v-if="activeTab === 'search'" 
              :isLoading="isLoading"
              :searchQuery="searchQuery"
              :filters="filters"
              :showMoreFilters="showMoreFilters"
              :error="error"
              :results="results"
              :totalResults="totalResults"
              :currentPage="currentPage"
              :totalPages="totalPages"
              :selectedPapers="selectedPapers"
              :allSelected="allSelected"
              @search="searchPapers"
              @update:searchQuery="searchQuery = $event"
              @update:filters="filters = $event"
              @toggle-more-filters="showMoreFilters = !showMoreFilters"
              @clear-filters="clearFilters"
              @toggle-select-all="toggleSelectAll"
              @toggle-selection="toggleSelection"
              @prev-page="prevPage"
              @next-page="nextPage"
              @view-paper="viewPaper"
              @download-pdf="downloadPdf"
              @add-to-project="addToProject"
              @view-details="viewDetails"
              @add-selected-to-project="addSelectedToProject"
            />
            <UploadTab v-else 
              :uploadQueue="uploadQueue"
              :extractionOptions="extractionOptions"
              @upload-files="handleFileUpload"
              @update:extractionOptions="extractionOptions = $event"
              @remove-from-queue="removeFromQueue"
              @process-uploads="processUploads"
            />
    </div>

    <div class="bg-white rounded-lg shadow">
      <div class="p-4 border-b flex justify-between items-center">
        <div class="font-medium">Imported Papers ({{ importedPapers.length || 0 }})</div>
        <div class="flex items-center">
          <button class="flex items-center px-3 py-2 text-sm border rounded-lg mr-2 hover:bg-gray-50">
            <font-awesome-icon icon="filter" class="mr-1" /> Filter
          </button>
          <button 
            class="flex items-center px-3 py-2 text-sm border rounded-lg hover:bg-gray-50"
            @click="showProjectModal = true"
            :disabled="selectedImportedPapers.length === 0"
          >
            <font-awesome-icon icon="plus-circle" class="mr-1" /> Add to Project
          </button>
        </div>
      </div>

      <div class="divide-y">
        <div v-if="isLoading" class="text-center py-8">
          <div class="spinner mb-4"></div>
          <p class="text-gray-500">Loading papers...</p>
        </div>
        
        <template v-else>
          <ImportedPaperItem 
            v-for="paper in importedPapers" 
            :key="paper.id" 
            :paper="paper"
            :selected="isImportedSelected(paper.id)"
            @toggle-selection="toggleImportedSelection(paper.id)"
            @view="viewPaper(paper)"
            @download="downloadPdf(paper)"
            @remove="removePaper(paper.id)"
          />
          <div v-if="importedPapers.length === 0" class="p-10 text-center text-gray-500 border-dashed border-gray-300">
            <font-awesome-icon icon="file-pdf" class="text-gray-300 text-4xl mb-3" />
            <p class="mb-2">No papers imported yet</p>
            <p class="text-sm">Use the tabs above to search databases or upload PDFs</p>
          </div>
        </template>
      </div>
    </div>

    <!-- Project Select Modal -->
    <div v-if="showProjectModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 w-full max-w-xl shadow-xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold">Add to Project</h2>
          <button @click="showProjectModal = false" class="text-gray-500 hover:text-gray-700 p-1 rounded-full hover:bg-gray-100">
            <font-awesome-icon icon="times" />
          </button>
        </div>
        
        <div class="mb-6">
          <label class="block text-gray-700 mb-2 font-medium">Select Project</label>
          <select 
            v-model="selectedProjectId"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          >
            <option value="">-- Select a Project --</option>
            <option v-for="project in projects" :key="project.id" :value="project.id">{{ project.name }}</option>
          </select>
          
          <div class="mt-4">
            <button 
              @click="showCreateProjectForm = !showCreateProjectForm"
              class="text-indigo-600 text-sm flex items-center hover:text-indigo-800"
            >
              <font-awesome-icon icon="plus" class="mr-1" /> Create New Project
            </button>
          </div>
          
          <div v-if="showCreateProjectForm" class="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Project Name*</label>
              <input 
                v-model="newProject.name"
                type="text" 
                class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                placeholder="Enter project name"
              />
            </div>
            
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Description (optional)</label>
              <textarea 
                v-model="newProject.description"
                class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                placeholder="Brief description of this project"
                rows="3"
              ></textarea>
            </div>
            
            <div class="flex justify-end">
              <button 
                @click="createProject"
                class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                :disabled="!newProject.name"
              >
                Create Project
              </button>
            </div>
          </div>
        </div>
        
        <div class="flex justify-end">
          <button 
            @click="showProjectModal = false" 
            class="mr-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >Cancel</button>
          <button 
            @click="addPapersToProject" 
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            :disabled="!selectedProjectId"
          >
            Add to Project
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchTab from './papers/find-papers/search-tab.vue';
import UploadTab from './papers/find-papers/upload-tab.vue';
import ImportedPaperItem from './papers/find-papers/imported-paper-item.vue';
import { API_ROUTES, APP_CONFIG } from '../config.js';

export default {
  name: 'PaperSearch',
  components: {
    SearchTab,
    UploadTab,
    ImportedPaperItem
  },
  data() {
    return {
      activeTab: 'search',
      searchQuery: '',
      filters: {
        yearFrom: null,
        yearTo: null,
        studyType: '',
        sortBy: 'relevance',
        journal: '',
        author: '',
        openAccessOnly: false
      },
      selectedPapers: [],
      selectedImportedPapers: [],
      allSelected: false,
      showMoreFilters: false,
      isLoading: false,
      error: null,
      results: [],
      totalResults: 0,
      currentPage: 1,
      totalPages: 1,
      itemsPerPage: APP_CONFIG.ITEMS_PER_PAGE,
      
      // Upload tab
      uploadQueue: [],
      extractionOptions: {
        extractMetadata: true,
        applyCodingSheet: false,
        addToProject: false
      },
      
      // Project management
      showProjectModal: false,
      projects: [],
      selectedProjectId: '',
      showCreateProjectForm: false,
      papersToAddToProject: [], // Stores imported papers with their database IDs
      newProject: {
        name: '',
        description: ''
      },
      
      // Imported Papers
      importedPapers: []
    };
  },
  mounted() {
    this.fetchProjects();
    this.fetchImportedPapers();
  },
  methods: {
    // Paper selection methods
    isSelected(paper) {
      return this.selectedPapers.some(p => this.isSamePaper(p, paper));
    },
    
    isImportedSelected(paperId) {
      return this.selectedImportedPapers.includes(paperId);
    },
    
    isSamePaper(paper1, paper2) {
      // Compare by DOI if available
      if (paper1.doi && paper2.doi) {
        return paper1.doi === paper2.doi;
      }
      // Otherwise compare by title
      return paper1.title === paper2.title;
    },
    
    toggleSelection(paper) {
      console.log('Toggling selection for paper:', paper.title);
      if (this.isSelected(paper)) {
        this.selectedPapers = this.selectedPapers.filter(p => !this.isSamePaper(p, paper));
      } else {
        this.selectedPapers.push(paper);
      }
      this.updateAllSelected();
      console.log('Selected papers:', this.selectedPapers.length);
    },
    
    toggleImportedSelection(paperId) {
      if (this.isImportedSelected(paperId)) {
        this.selectedImportedPapers = this.selectedImportedPapers.filter(id => id !== paperId);
      } else {
        this.selectedImportedPapers.push(paperId);
      }
    },
    
    toggleSelectAll() {
      console.log('Toggling select all. Current state:', this.allSelected);
      if (this.allSelected) {
        // If currently all selected, deselect all
        this.selectedPapers = [];
        this.allSelected = false;
      } else {
        // If not all selected, select all current results
        this.selectedPapers = [...this.results];
        this.allSelected = true;
      }
      console.log('New selection state:', this.selectedPapers.length, 'papers selected');
    },
    
    updateAllSelected() {
      this.allSelected = this.results.length > 0 && 
        this.results.every(paper => this.isSelected(paper));
    },
    
    // Paper search methods
    async searchPapers() {
      // Clear previous error message
      this.error = null;
      
      // Validate search query
      if (!this.searchQuery || !this.searchQuery.trim()) {
        this.error = "Please enter a search term";
        this.results = [];
        this.totalResults = 0;
        return;
      }
      this.isLoading = true;
      this.error = null;
      
      try {
        // Build query parameters for search
        const params = new URLSearchParams();
        params.append('query', this.searchQuery);
        params.append('per_page', this.itemsPerPage.toString());
        params.append('page', this.currentPage.toString());
        
        // Add filters if provided
        if (this.filters.yearFrom) params.append('year_from', this.filters.yearFrom.toString());
        if (this.filters.yearTo) params.append('year_to', this.filters.yearTo.toString());
        if (this.filters.journal) params.append('journal', this.filters.journal);
        if (this.filters.author) params.append('author', this.filters.author);
        if (this.filters.openAccessOnly) params.append('open_access_only', 'true');
        
        // Add sort parameter
        params.append('sort', this.filters.sortBy);
        
        // Build URL with all parameters
        const endpoint = API_ROUTES.PAPERS.SEARCH;
        const searchUrl = `${endpoint}?${params.toString()}`;
        
        console.log('Search URL:', searchUrl);
        console.log('Search parameters:', { 
          query: this.searchQuery,
          filters: this.filters,
          page: this.currentPage,
          perPage: this.itemsPerPage
        });
        
        const response = await fetch(searchUrl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          let errorDetail = 'Failed to search papers';
          try {
            const errorData = await response.json();
            console.error('Search API error response:', errorData);
            
            if (errorData && typeof errorData === 'object') {
              if (errorData.detail) {
                errorDetail = errorData.detail;
              } else if (errorData.message) {
                errorDetail = errorData.message;
              }
            }
          } catch (e) {
            console.error('Error parsing error response:', e);
            errorDetail = `Server error: ${response.status} ${response.statusText}`;
          }
          throw new Error(errorDetail);
        }
        
        const data = await response.json();
        console.log('Search response data:', data);
        
        // Use results directly from backend
        this.results = data.results || [];
        this.totalResults = data.totalResults || 0;
        
        // Calculate total pages based on backend total and itemsPerPage
        this.totalPages = Math.ceil(this.totalResults / this.itemsPerPage);
        console.log(`Found ${this.totalResults} results, ${this.totalPages} pages`);
        
        // Ensure currentPage is not out of bounds after search
        if (this.currentPage > this.totalPages && this.totalPages > 0) {
          this.currentPage = this.totalPages;
        } else if (this.totalPages === 0) {
          this.currentPage = 1; // Reset to page 1 if no results
        }

        if (this.results.length === 0 && this.searchQuery.trim() !== '') {
           this.error = `No results found for "${this.searchQuery}". Try different search terms or remove some filters.`;
        }
        
        // Reset selection when performing a new search (not just pagination)
        this.selectedPapers = [];
        this.allSelected = false;
      } catch (err) {
        let errorMessage = 'Failed to search papers';
        
        if (err.message && err.message !== '[object Object]') {
          errorMessage = err.message;
        }
        
        console.error('Error searching papers:', err);
        this.error = errorMessage;
        this.results = [];
        this.totalResults = 0;
      } finally {
        this.isLoading = false;
      }
    },
    
    clearFilters() {
      this.filters = {
        yearFrom: null,
        yearTo: null,
        studyType: '',
        sortBy: 'relevance',
        journal: '',
        author: '',
        openAccessOnly: false
      };
      
      // Reset pagination
      this.currentPage = 1;
      this.totalPages = 1;
      
      // If there was a search query, perform a new search with cleared filters
      if (this.searchQuery.trim()) {
        this.searchPapers();
      }
    },
    
    prevPage() {
      if (this.currentPage > 1) {
        console.log(`Moving to previous page: ${this.currentPage} -> ${this.currentPage - 1}`);
        this.currentPage--;
        this.searchPapers();
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        console.log(`Moving to next page: ${this.currentPage} -> ${this.currentPage + 1}`);
        this.currentPage++;
        this.searchPapers();
      }
    },
    
    // File upload methods
    handleFileUpload(files) {
      // Convert FileList to array and add to upload queue
      const fileArray = Array.from(files);
      
      this.uploadQueue = [
        ...this.uploadQueue,
        ...fileArray.map(file => ({
          file,
          name: file.name,
          size: file.size,
          progress: 0,
          status: 'queued'
        }))
      ];
    },
    
    removeFromQueue(index) {
      this.uploadQueue.splice(index, 1);
    },
    
    async processUploads() {
      if (this.uploadQueue.length === 0) return;
      
      for (let i = 0; i < this.uploadQueue.length; i++) {
        const item = this.uploadQueue[i];
        if (item.status !== 'complete') {
          // Update status
          this.$set(this.uploadQueue, i, { ...item, status: 'uploading' });
          
          try {
            await this.uploadFile(item.file, i);
            this.$set(this.uploadQueue, i, { ...this.uploadQueue[i], status: 'complete', progress: 100 });
          } catch (error) {
            this.$set(this.uploadQueue, i, { ...this.uploadQueue[i], status: 'error', error: error.message });
            console.error(`Error uploading ${item.name}:`, error);
          }
        }
      }
      
      // After all uploads complete, extract metadata if enabled
      if (this.extractionOptions.extractMetadata) {
        await this.extractMetadataFromUploads();
      }
      
      // Add to project if enabled and project selected
      if (this.extractionOptions.addToProject && this.selectedProjectId) {
        await this.addUploadsToProject();
      }
      
      // Refresh imported papers list
      this.fetchImportedPapers();
    },
    
    async uploadFile(file, index) {
      return new Promise((resolve, reject) => {
        const formData = new FormData();
        formData.append('file', file);
        
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', (event) => {
          if (event.lengthComputable) {
            const percentComplete = Math.round((event.loaded / event.total) * 100);
            this.$set(this.uploadQueue, index, { ...this.uploadQueue[index], progress: percentComplete });
          }
        });
        
        xhr.addEventListener('load', () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            try {
              const response = JSON.parse(xhr.responseText);
              // Store file ID and other metadata returned from the server
              this.$set(this.uploadQueue, index, {
                ...this.uploadQueue[index],
                id: response.file_id || response.id,
                title: response.title,
                authors: response.authors,
                metadata: response
              });
              resolve(response);
            } catch (e) {
              console.error('Error parsing upload response:', e);
              resolve(xhr.responseText);
            }
          } else {
            reject(new Error(`Upload failed: ${xhr.statusText}`));
          }
        });
        
        xhr.addEventListener('error', () => {
          reject(new Error('Network error occurred during upload'));
        });
        
        xhr.open('POST', API_ROUTES.PAPERS.UPLOAD);
        xhr.send(formData);
      });
    },
    
    async extractMetadataFromUploads() {
      // Extract metadata from the uploaded PDFs
      try {
        // Get file IDs from completed uploads
        const uploadIds = this.uploadQueue
          .filter(item => item.status === 'complete' && item.id)
          .map(item => item.id);
          
        if (uploadIds.length === 0) {
          console.log('No files with IDs found for metadata extraction');
          return;
        }
        
        console.log('Extracting metadata for files:', uploadIds);
        
        const response = await fetch(API_ROUTES.PAPERS.EXTRACT_METADATA, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ file_ids: uploadIds })
        });
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || 'Failed to extract metadata');
        }
        
        const data = await response.json();
        console.log('Metadata extraction results:', data);
        
        // Update queue items with extracted metadata
        data.forEach(result => {
          if (result.file_id && result.status === 'success') {
            const queueIndex = this.uploadQueue.findIndex(item => item.id === result.file_id);
            if (queueIndex !== -1) {
              this.$set(this.uploadQueue, queueIndex, { 
                ...this.uploadQueue[queueIndex],
                metadata: result.metadata,
                title: result.metadata.title,
                authors: result.metadata.authors
              });
            }
          }
        });
        
        // After metadata extraction, we can import the papers to the library
        this.importExtractedPapers();
        
      } catch (error) {
        console.error('Error extracting metadata:', error);
        alert('There was a problem extracting metadata from the uploaded files: ' + error.message);
      }
    },
    
    async importExtractedPapers() {
      // Import papers with extracted metadata
      try {
        const papersToImport = this.uploadQueue
          .filter(item => item.status === 'complete' && item.metadata)
          .map(item => ({
            title: item.metadata.title || item.name,
            abstract: item.metadata.abstract,
            authors: item.metadata.authors || [],
            publication_date: item.metadata.year ? new Date(item.metadata.year, 0, 1).toISOString() : null,
            journal: item.metadata.journal,
            doi: item.metadata.doi,
            file_path: item.metadata.file_path,
            file_name: item.name,
            source: 'PDF Upload'
          }));
        
        if (papersToImport.length === 0) {
          console.log('No papers with metadata to import');
          return;
        }
        
        console.log('Importing papers from uploads:', papersToImport);
        
        const response = await fetch(API_ROUTES.PAPERS.IMPORT_BATCH, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ papers: papersToImport })
        });
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || 'Failed to import papers');
        }
        
        const result = await response.json();
        console.log('Import result:', result);
        
        if (result.imported_count > 0) {
          alert(`${result.imported_count} paper(s) imported successfully.`);
          // Refresh imported papers list with real data
          await this.fetchImportedPapers();
          // Clear upload queue for successfully imported papers
          this.uploadQueue = this.uploadQueue.filter(item => {
            return item.status !== 'complete' || !item.metadata;
          });
        }
        
      } catch (error) {
        console.error('Error importing papers from uploads:', error);
        alert('There was a problem importing the papers: ' + error.message);
      }
    },
    
    // Viewing/managing papers
    viewPaper(paper) {
      // Navigate to PDF viewer with the selected paper
      this.$emit('select-paper', paper);
    },
    
    async downloadPdf(paper) {
      this.isLoading = true;
      console.log('Attempting to download PDF for paper:', paper.title);
      
      try {
        // First check if we have a direct open_access_url
        if (paper.open_access_url) {
          console.log('Using direct open access URL:', paper.open_access_url);
          window.open(paper.open_access_url, '_blank');
          this.isLoading = false;
          return;
        }
        
        // Next try using the DOI if available
        if (paper.doi) {
          console.log('Looking up PDF using DOI:', paper.doi);
          const response = await fetch(`${API_ROUTES.PAPERS.GET_PDF}/${encodeURIComponent(paper.doi)}`);
          
          if (response.ok) {
            const data = await response.json();
            console.log('PDF lookup response:', data);
            
            if (data.pdf_url) {
              window.open(data.pdf_url, '_blank');
              this.isLoading = false;
              return;
            } else {
              throw new Error('No PDF URL returned from server');
            }
          } else {
            // If API call fails, try to get error details
            try {
              const errorData = await response.json();
              throw new Error(errorData.detail || `Server error: ${response.status}`);
            } catch (e) {
              throw new Error(`Server error: ${response.status} ${response.statusText}`);
            }
          }
        } else {
          throw new Error('No DOI or open access URL available for this paper');
        }
      } catch (err) {
        console.error('Error downloading PDF:', err);
        alert(`Could not download PDF: ${err.message}. The PDF may not be publicly accessible.`);
      } finally {
        this.isLoading = false;
      }
    },
    
    viewDetails(paper) {
      // View paper details
      console.log('View details:', paper);
    },
    
    removePaper(paperId) {
      // Remove a paper from imported list
      this.importedPapers = this.importedPapers.filter(paper => paper.id !== paperId);
      this.selectedImportedPapers = this.selectedImportedPapers.filter(id => id !== paperId);
    },
    
    // Project management
    async fetchProjects() {
      try {
        console.log('Fetching projects from:', API_ROUTES.PROJECTS.LIST);
        const response = await fetch(API_ROUTES.PROJECTS.LIST);
        
        if (!response.ok) {
          throw new Error('Failed to fetch projects');
        }
        
        this.projects = await response.json();
        console.log(`Fetched ${this.projects.length} projects`);
      } catch (error) {
        console.error('Error fetching projects:', error);
        this.projects = []; // Empty projects, no mock data
      }
    },
    
    async createProject() {
      try {
        const response = await fetch(API_ROUTES.PROJECTS.CREATE, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.newProject)
        });
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || 'Failed to create project');
        }
        
        // Handle successful project creation
        const project = await response.json();
        this.projects.push(project);
        this.selectedProjectId = project.id;
        
        // Reset form
        this.showCreateProjectForm = false;
        this.newProject = { name: '', description: '' };
      } catch (error) {
        console.error('Error creating project:', error);
        alert('There was a problem creating the project: ' + error.message);
      }
    },
    
    async addPapersToProject() {
      if (!this.selectedProjectId || this.papersToAddToProject.length === 0) {
        alert('Please select a project and papers to add');
        return;
      }
      
      try {
        console.log(`Adding ${this.papersToAddToProject.length} papers to project ${this.selectedProjectId}`);
        
        // Extract just the IDs from the papersToAddToProject array
        const paperIds = this.papersToAddToProject.map(paper => paper.id);
        
        const response = await fetch(API_ROUTES.PROJECTS.ADD_PAPERS_BATCH(this.selectedProjectId), {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ paper_ids: paperIds })
        });
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || `Failed to add papers to project: ${response.status}`);
        }
        
        // Handle successful project batch API response
        const result = await response.json();
        console.log('Project batch API result:', result);
        alert(`${result.added_count || 0} paper(s) added to project successfully. ${result.skipped_count || 0} were already in the project.`);
        this.showProjectModal = false;
        this.papersToAddToProject = [];
      } catch (error) {
        console.error('Error adding papers to project:', error);
        alert('There was a problem adding papers to the project: ' + error.message);
      }
    },
    
    addToProject(paper) {
      // Add single paper to selected project
      if (paper.id) {
        this.selectedImportedPapers = [paper.id];
        this.showProjectModal = true;
      } else {
        console.error('Paper has no ID:', paper);
      }
    },
    
    addSelectedToProject() {
      // First check if we have any papers selected
      if (this.selectedPapers.length === 0) {
        alert('Please select papers first');
        return;
      }
      
      // Import the selected papers
      this.importSelectedPapers();
    },
    
    async importSelectedPapers() {
      if (this.selectedPapers.length === 0) return;
      
      try {
        this.isLoading = true;
        console.log('Importing papers:', this.selectedPapers);
        
        const response = await fetch(API_ROUTES.PAPERS.IMPORT_BATCH, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ papers: this.selectedPapers })
        });
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || 'Failed to import papers');
        }
        
        const result = await response.json();
        console.log('Import result:', result);
        
        // Store the imported papers with their database IDs
        this.papersToAddToProject = result.imported_papers || [];
        
        if (this.papersToAddToProject.length > 0) {
          // Open the project selection modal
          this.showProjectModal = true;
          alert(`${result.imported_count || 0} paper(s) imported successfully.`);
          
          // Refresh imported papers to show real data
          await this.fetchImportedPapers();
        } else {
          alert('No papers were successfully imported. Please try again.');
        }
        
        // Clear selection
        this.selectedPapers = [];
        this.allSelected = false;
      } catch (error) {
        console.error('Error importing papers:', error);
        alert('There was a problem importing the selected papers: ' + error.message);
      } finally {
        this.isLoading = false;
      }
    },
    
    // Fetch imported papers
    async fetchImportedPapers() {
      try {
        console.log('Fetching imported papers from:', API_ROUTES.PAPERS.LIST);
        const response = await fetch(API_ROUTES.PAPERS.LIST);
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || `Failed to fetch imported papers: ${response.status}`);
        }
        
        this.importedPapers = await response.json();
        console.log(`Fetched ${this.importedPapers.length} imported papers`);
      } catch (error) {
        console.error('Error fetching imported papers:', error);
        // Don't use mock data - show empty state
        this.importedPapers = [];
      }
    }
  }
}
</script>

<style scoped>
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #4f46e5;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
