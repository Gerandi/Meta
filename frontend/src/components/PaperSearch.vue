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
          <Search class="mr-2" size="18" />
          Search Databases
        </button>
        <button 
          class="py-4 px-6 font-medium flex items-center"
          :class="activeTab === 'upload' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'"
          @click="activeTab = 'upload'"
        >
          <Upload class="mr-2" size="18" />
          Upload PDFs
        </button>
      </div>

      
            <SearchTab v-if="activeTab === 'search'" 
              :activeProject="activeProject"
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
              :importedPaperIds="importedPaperIds"
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
              @import-to-project="handleImportToProject"
              @import-to-staging="handleImportToStaging"
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

    <ImportedPapersSection
      ref="importedPapersSection"
      :isLoading="isLoading"
      :activeProject="activeProject"
      @view-paper="viewPaper"
      @download-pdf="downloadPdf"
      @paper-added-to-project="handlePaperAddedToProject"
      @refresh-imported-papers="fetchImportedPapers"
    />



    <!-- Project Select Modal -->
    <div v-if="showProjectModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 w-full max-w-xl shadow-xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold">Add to Project</h2>
          <button @click="showProjectModal = false" class="text-gray-500 hover:text-gray-700 p-1 rounded-full hover:bg-gray-100">
            <X size="18" />
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
              <Plus class="mr-1" size="16" /> Create New Project
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
import ImportedPapersSection from './papers/ImportedPapersSection.vue';
import { API_ROUTES, APP_CONFIG } from '../config.js';
import { paperService, projectService } from '../services/api.js';
import { 
  Search, 
  Upload, 
  Filter, 
  PlusCircle, 
  FileText, 
  X, 
  Plus 
} from 'lucide-vue-next';
import { useProjectStore } from '../stores/project';
import { mapState } from 'pinia';

export default {
  name: 'PaperSearch',
  computed: {
    ...mapState(useProjectStore, ['activeProject', 'hasActiveProject'])
  },
  components: {
    SearchTab,
    UploadTab,
    ImportedPapersSection,
    Search,
    Upload,
    Filter,
    PlusCircle,
    FileText,
    X,
    Plus
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
      // selectedImportedPapers moved to ImportedPapersSection
      allSelected: false,
      showMoreFilters: false,
      isLoading: false,
      error: null,
      results: [],
      totalResults: 0,
      currentPage: 1,
      totalPages: 1,
      itemsPerPage: APP_CONFIG.ITEMS_PER_PAGE,
      importedPaperIds: new Set(),
      
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
      
      // Note: importedPapers state has been moved to ImportedPapersSection component
    };
  },
  mounted() {
    this.fetchProjects();
  },
  methods: {
    // Paper selection methods
    isSelected(paper) {
      return this.selectedPapers.some(p => this.isSamePaper(p, paper));
    },
    
    // Paper selection methods for imported papers moved to ImportedPapersSection component
    
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
      this.$emit('view-details', paper);
    },
    
    // Paper removal method moved to ImportedPapersSection component
    
    // Project management
    async fetchProjects() {
      try {
        console.log('Fetching projects');
        this.projects = await projectService.listProjects();
        console.log(`Fetched ${this.projects.length} projects`);
      } catch (error) {
        console.error('Error fetching projects:', error);
        this.projects = []; // Empty projects, no mock data
      }
    },
    
    async createProject() {
      try {
        // Create project using the service
        const project = await projectService.createProject(this.newProject);
        
        // Update local data
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
        
        // Use the service to add papers to project
        const result = await projectService.addPapersToProject(this.selectedProjectId, paperIds);
        console.log('Project batch API result:', result);
        
        // If papers were added successfully, notify the user
        alert(`${result.added_count || 0} paper(s) added to project successfully. ${result.skipped_count || 0} were already in the project.`);
        this.showProjectModal = false;
        this.papersToAddToProject = [];
        
        // Refresh the imported papers list to show updated associations
        // After papers are added to a project, their status changes from IMPORTED to PROCESSING
        // so they should no longer appear in the imported papers list
        await this.fetchImportedPapers();
        
        // Clear selection
        this.selectedImportedPapers = [];
      } catch (error) {
        console.error('Error adding papers to project:', error);
        alert('There was a problem adding papers to the project: ' + error.message);
      }
    },
    
    // Method for handling paper added to project event from ImportedPapersSection
    handlePaperAddedToProject() {
      // Refresh the active project data if needed
      if (this.activeProject) {
        this.$emit('refresh-project', this.activeProject.id);
      }
    },
    
    // Handle direct import to active project
    async handleImportToProject(paper) {
      if (!this.hasActiveProject) {
        alert("Cannot import directly: No active project.");
        return;
      }
      this.isLoading = true; // Show loading indicator
      try {
        // Prepare paper data for the backend
        const formattedPaper = this.formatPaperForImport(paper);
        formattedPaper.status = 'processing'; // Ensure status is set correctly

        const result = await projectService.importAndAddPaperToProject(
          this.activeProject.id,
          formattedPaper
        );
        alert(`Paper "${result.title}" added directly to project "${this.activeProject.name}".`);
        // Optionally: Refresh project paper count
        this.$emit('refresh-project', this.activeProject.id);
      } catch (error) {
        console.error('Error importing paper directly to project:', error);
        alert(`Failed to add paper directly to project: ${error.message}`);
      } finally {
        this.isLoading = false;
      }
    },

    // Handle import to staging area (imported list)
    async handleImportToStaging(paper) {
      this.isLoading = true;
      try {
        const formattedPaper = this.formatPaperForImport(paper);
        formattedPaper.status = 'imported'; // Ensure status is imported

        const result = await paperService.importPapersBatch([formattedPaper]);
        if (result.imported_count > 0) {
          alert(`Paper "${formattedPaper.title}" imported. Go to 'Imported Papers' to add it to a project.`);
          // Add imported paper ID to set
          if (result.imported_papers && result.imported_papers[0] && result.imported_papers[0].id) {
            this.importedPaperIds.add(result.imported_papers[0].id);
          }
          // Refresh the imported papers list
          this.$refs.importedPapersSection?.fetchImportedPapers();
        } else {
          alert(`Failed to import paper: ${result.errors?.[0]?.error || 'Unknown error'}`);
        }
      } catch (error) {
        console.error('Error importing paper to staging:', error);
        alert(`Failed to import paper: ${error.message}`);
      } finally {
        this.isLoading = false;
      }
    },

    // Helper to format paper data
    formatPaperForImport(paper) {
      let formattedAuthors = [];
      if (Array.isArray(paper.authors)) {
        formattedAuthors = paper.authors.map(author => {
          if (typeof author === 'object' && author !== null && author.name) return author;
          if (typeof author === 'string') return { name: author };
          return { name: 'Unknown Author' };
        });
      } else if (typeof paper.authors === 'string') {
        formattedAuthors = [{ name: paper.authors }];
      }

      return {
        title: paper.title || 'Unknown Title',
        abstract: paper.abstract || '',
        doi: paper.doi,
        authors: formattedAuthors,
        publication_date: paper.publication_date,
        journal: paper.journal,
        volume: paper.volume,
        issue: paper.issue,
        pages: paper.pages,
        publisher: paper.publisher,
        url: paper.url,
        keywords: Array.isArray(paper.keywords) ? paper.keywords : [],
        is_open_access: paper.is_open_access || false,
        open_access_url: paper.open_access_url,
        source: paper.source || 'Search Import'
        // Status will be set by the calling method
      };
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
    
    // Add selected imported papers to the active project if available
    addSelectedImportedToProject() {
      // This method now checks for activeProject first
      if (this.activeProject && this.activeProject.id) {
        // We have an active project, call the ImportedPapersSection method directly
        this.$refs.importedPapersSection.addSelectedImportedToProject();
      } else {
        // No active project, show the modal as before
        this.showProjectModal = true;
      }
    },
    
    async importSelectedPapers() {
      if (this.selectedPapers.length === 0) return;
      
      try {
        this.isLoading = true;
        console.log('Importing papers:', this.selectedPapers);
        
        // Format papers for import - convert from search results to importable format
        const formattedPapers = this.selectedPapers.map(paper => {
          // Format authors properly according to the schema
          let formattedAuthors = [];
          if (Array.isArray(paper.authors)) {
            formattedAuthors = paper.authors.map(author => {
              // If author is already in the right format, use it
              if (typeof author === 'object' && author !== null && author.name) {
                return author;
              }
              // Otherwise create a proper author object
              if (typeof author === 'string') {
                return { name: author };
              }
              if (typeof author === 'object' && author !== null) {
                if (author.firstName && author.lastName) {
                  return { name: `${author.firstName} ${author.lastName}` };
                }
                if (author.given && author.family) {
                  return { name: `${author.given} ${author.family}` };
                }
              }
              return { name: 'Unknown Author' };
            });
          } else if (typeof paper.authors === 'string') {
            formattedAuthors = [{ name: paper.authors }];
          } else {
            formattedAuthors = [{ name: 'Unknown Author' }];
          }
          
          return {
            title: paper.title || 'Unknown Title',
            abstract: paper.abstract || '',
            doi: paper.doi,
            authors: formattedAuthors,
            publication_date: paper.publication_date,
            journal: paper.journal,
            volume: paper.volume,
            issue: paper.issue,
            pages: paper.pages,
            publisher: paper.publisher,
            url: paper.url,
            keywords: Array.isArray(paper.keywords) ? paper.keywords : [],
            is_open_access: paper.is_open_access || false,
            open_access_url: paper.open_access_url,
            source: paper.source || 'Search Import',
            status: 'imported' // Explicitly set the status to 'imported'
          };
        });
        
        console.log('Formatted papers for import:', formattedPapers);
        
        // Use the paper service to import papers
        const result = await paperService.importPapersBatch(formattedPapers);
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
    
    // This method is now a wrapper that delegates to ImportedPapersSection component
    async fetchImportedPapers() {
      // Signal to ImportedPapersSection that it should refresh its data
      this.$emit('refresh-imported-papers');
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
