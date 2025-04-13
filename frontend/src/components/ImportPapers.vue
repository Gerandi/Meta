<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold">Import Papers</h1>
        <p class="text-gray-600">Upload your own papers and automatically extract metadata</p>
      </div>
      <div class="flex">
        <button 
          class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center"
          @click="continueToProcessing"
          :disabled="importedPapers.length === 0"
        >
          <ArrowRight class="mr-1" size="18" /> Continue to Processing
        </button>
      </div>
    </div>
    
    <div class="bg-white rounded-lg shadow-lg mb-6 p-6">
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6 flex">
        <div class="text-blue-500 mr-3 mt-0.5">
          <Info size="24" />
        </div>
        <div>
          <h3 class="font-medium text-blue-800 mb-1">Import Your Papers</h3>
          <p class="text-blue-700 text-sm">
            Upload your PDFs in bulk or individually. We'll automatically extract titles, authors, and other metadata.
            You can review and edit the extracted metadata before adding papers to your project.
          </p>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-lg border p-6 text-center hover:shadow-md transition-shadow">
          <div class="inline-flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 text-indigo-600 mb-4">
            <UploadCloud size="24" />
          </div>
          <h3 class="text-lg font-medium mb-2">PDF Uploads</h3>
          <p class="text-gray-600 text-sm mb-4">
            Upload PDF files from your computer and we'll extract the metadata
          </p>
          <input 
            type="file" 
            ref="fileInput"
            accept=".pdf"
            multiple
            class="hidden"
            @change="handleFileUpload"
          />
          <button 
            class="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            @click="$refs.fileInput.click()"
          >
            Upload PDFs
          </button>
        </div>
        
        <div class="bg-white rounded-lg border p-6 text-center hover:shadow-md transition-shadow">
          <div class="inline-flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 text-indigo-600 mb-4">
            <Import size="24" />
          </div>
          <h3 class="text-lg font-medium mb-2">Bulk Import</h3>
          <p class="text-gray-600 text-sm mb-4">
            Drop multiple files at once or import from a folder
          </p>
          <button 
            class="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            @click="openBulkImportModal"
          >
            Bulk Import
          </button>
        </div>
        
        <div class="bg-white rounded-lg border p-6 text-center hover:shadow-md transition-shadow">
          <div class="inline-flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 text-indigo-600 mb-4">
            <ClipboardList size="24" />
          </div>
          <h3 class="text-lg font-medium mb-2">Manual Entry</h3>
          <p class="text-gray-600 text-sm mb-4">
            Manually enter paper details if you don't have the PDFs
          </p>
          <button 
            class="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            @click="openManualEntryModal"
          >
            Add Manually
          </button>
        </div>
      </div>
      
      <!-- Import Status -->
      <div v-if="isUploading" class="mb-6">
        <h3 class="text-lg font-medium mb-3">Uploading Files</h3>
        <div 
          v-for="(file, index) in uploadingFiles" 
          :key="index"
          class="bg-white p-3 rounded border shadow-sm mb-2"
        >
          <div class="flex justify-between items-center mb-2">
            <div class="font-medium flex items-center">
              <FileText class="text-gray-500 mr-2" size="18" />
              {{ file.name }}
            </div>
            <div class="text-sm text-gray-500">{{ formatFileSize(file.size) }}</div>
          </div>
          
          <div class="w-full bg-gray-200 rounded-full h-2 mb-1">
            <div 
              class="h-2 rounded-full bg-indigo-600"
              :style="{ width: `${file.progress}%` }"
            ></div>
          </div>
          
          <div class="text-xs text-gray-500">
            {{ file.status === 'complete' ? 'Upload complete' : `Uploading... ${file.progress}%` }}
          </div>
        </div>
        
        <div v-if="extractingMetadata" class="text-center py-4">
          <div class="spinner mb-2"></div>
          <p class="text-indigo-600">Extracting metadata from PDFs...</p>
        </div>
      </div>
      
      <!-- Imported Papers Table -->
      <div v-if="importedPapers.length > 0">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium">Imported Papers ({{ importedPapers.length }})</h3>
          <div>
            <button 
              class="px-3 py-2 border rounded-lg text-gray-700 hover:bg-gray-50 flex items-center text-sm"
              @click="removeSelectedPapers"
              :disabled="selectedPaperIds.length === 0"
            >
              <Trash class="mr-1" size="16" /> Remove Selected
            </button>
          </div>
        </div>
        
        <div class="bg-white border rounded-lg overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <input 
                    type="checkbox" 
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    :checked="isAllSelected"
                    @change="toggleSelectAll"
                  />
                </th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Title & Authors
                </th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Journal & Year
                </th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th scope="col" class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr 
                v-for="paper in importedPapers" 
                :key="paper.id"
                :class="isSelected(paper.id) ? 'bg-indigo-50' : 'hover:bg-gray-50'"
              >
                <td class="px-4 py-4 whitespace-nowrap">
                  <input 
                    type="checkbox" 
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    :checked="isSelected(paper.id)"
                    @change="togglePaperSelection(paper.id)"
                  />
                </td>
                <td class="px-4 py-4">
                  <div class="font-medium text-gray-900">{{ paper.title || 'Unknown Title' }}</div>
                  <div class="text-sm text-gray-500">{{ formatAuthors(paper.authors) }}</div>
                  <div v-if="paper.needsReview" class="mt-1 text-xs text-yellow-600">
                    <AlertTriangle class="inline mr-1" size="14" /> Needs review
                  </div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ paper.journal || "—" }}</div>
                  <div class="text-sm text-gray-500">{{ paper.year || "—" }}</div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm">
                  <div class="flex items-center">
                    <span 
                      class="px-2 py-1 rounded-full text-xs" 
                      :class="getStatusClass(paper.status)"
                    >
                      {{ getStatusText(paper.status) }}
                    </span>
                  </div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button 
                    class="text-indigo-600 hover:text-indigo-900 mr-3"
                    @click="editPaper(paper)"
                  >
                    Edit
                  </button>
                  <button 
                    class="text-red-600 hover:text-red-900"
                    @click="removePaper(paper.id)"
                  >
                    Remove
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <div v-else-if="!isUploading" class="text-center py-8">
        <FileText class="text-gray-400 mx-auto mb-4" size="48" />
        <h3 class="text-xl font-medium mb-2">No Papers Imported Yet</h3>
        <p class="text-gray-600 mb-4">Upload PDF files to get started</p>
      </div>
    </div>
    
    <!-- Bulk Import Modal -->
    <div v-if="showBulkImportModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-2xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold">Bulk Import Papers</h2>
          <button 
            class="text-gray-400 hover:text-gray-600"
            @click="showBulkImportModal = false"
          >
            <X size="18" />
          </button>
        </div>
        
        <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6">
          <div class="mx-auto w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
            <UploadCloud class="text-indigo-600" size="32" />
          </div>
          <h3 class="text-lg font-medium mb-2">Drop PDF files here</h3>
          <p class="text-gray-500 mb-4">or select multiple files from your computer</p>
          <input 
            type="file" 
            ref="bulkFileInput"
            multiple
            accept=".pdf"
            class="hidden"
            @change="handleBulkFileUpload"
          />
          <button 
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
            @click="$refs.bulkFileInput.click()"
          >
            Select Files
          </button>
          <p class="mt-4 text-sm text-gray-500">
            You can also drag and drop files here
          </p>
        </div>
        
        <div class="flex justify-end">
          <button 
            class="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-100 mr-2"
            @click="showBulkImportModal = false"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
    
    <!-- Manual Entry Modal -->
    <div v-if="showManualEntryModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-2xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold">Manual Paper Entry</h2>
          <button 
            class="text-gray-400 hover:text-gray-600"
            @click="showManualEntryModal = false"
          >
            <X size="18" />
          </button>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Title *</label>
          <input 
            v-model="manualPaper.title"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Enter paper title"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Authors *</label>
          <input 
            v-model="manualPaper.authors"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Author names separated by commas"
          />
          <p class="text-xs text-gray-500 mt-1">Example: John Smith, Jane Doe, Robert Johnson</p>
        </div>
        
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Journal/Source</label>
            <input 
              v-model="manualPaper.journal"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              placeholder="Journal or publication name"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Year</label>
            <input 
              v-model="manualPaper.year"
              type="number" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              placeholder="Publication year"
            />
          </div>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">DOI (if available)</label>
          <input 
            v-model="manualPaper.doi"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="https://doi.org/10.xxxx/xxxxx"
          />
        </div>
        
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">Abstract</label>
          <textarea 
            v-model="manualPaper.abstract"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            rows="4"
            placeholder="Enter paper abstract"
          ></textarea>
        </div>
        
        <div class="flex justify-end">
          <button 
            class="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-100 mr-2"
            @click="showManualEntryModal = false"
          >
            Cancel
          </button>
          <button 
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            @click="addManualPaper"
            :disabled="!manualPaper.title || !manualPaper.authors"
          >
            Add Paper
          </button>
        </div>
      </div>
    </div>
    
    <!-- Edit Paper Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-2xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold">Edit Paper Details</h2>
          <button 
            class="text-gray-400 hover:text-gray-600"
            @click="showEditModal = false"
          >
            <X size="18" />
          </button>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Title *</label>
          <input 
            v-model="editingPaper.title"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Authors *</label>
          <input 
            v-model="editingPaper.authors"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
        </div>
        
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Journal/Source</label>
            <input 
              v-model="editingPaper.journal"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Year</label>
            <input 
              v-model="editingPaper.year"
              type="number" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">DOI</label>
          <input 
            v-model="editingPaper.doi"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Abstract</label>
          <textarea 
            v-model="editingPaper.abstract"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            rows="4"
          ></textarea>
        </div>
        
        <div class="flex justify-end">
          <button 
            class="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-100 mr-2"
            @click="showEditModal = false"
          >
            Cancel
          </button>
          <button 
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            @click="updatePaper"
            :disabled="!editingPaper.title || !editingPaper.authors"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { API_ROUTES } from '../config.js';
import { 
  ArrowRight, 
  Info, 
  UploadCloud, 
  Import, 
  ClipboardList, 
  FileText, 
  Trash, 
  AlertTriangle,
  X
} from 'lucide-vue-next';
import { paperService } from '../services/api.js';

export default {
  name: 'ImportPapers',
  components: {
    ArrowRight,
    Info,
    UploadCloud,
    Import,
    ClipboardList,
    FileText,
    Trash,
    AlertTriangle,
    X
  },
  props: {
    activeProject: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      isUploading: false,
      extractingMetadata: false,
      uploadingFiles: [],
      importedPapers: [],
      selectedPaperIds: [],
      showBulkImportModal: false,
      showManualEntryModal: false,
      showEditModal: false,
      manualPaper: {
        title: '',
        authors: '',
        journal: '',
        year: '',
        doi: '',
        abstract: ''
      },
      editingPaper: null
    };
  },
  computed: {
    isAllSelected() {
      return this.importedPapers.length > 0 && this.selectedPaperIds.length === this.importedPapers.length;
    }
  },
  mounted() {
    this.fetchImportedPapers();
  },
  methods: {
    continueToProcessing() {
      // Continue to processing page with selected papers
      this.$emit('continue-to-processing', this.selectedPaperIds);
    },
    async fetchImportedPapers() {
      try {
        // Use paperService instead of direct fetch
        this.importedPapers = await paperService.listImportedPapers();
        console.log(`Fetched ${this.importedPapers.length} imported papers`);
      } catch (error) {
        console.error('Error fetching imported papers:', error);
        this.importedPapers = [];
      }
    },
    handleFileUpload(event) {
      if (!event.target.files || event.target.files.length === 0) return;
      
      const files = Array.from(event.target.files);
      this.processFiles(files);
    },
    handleBulkFileUpload(event) {
      if (!event.target.files || event.target.files.length === 0) return;
      
      const files = Array.from(event.target.files);
      this.processFiles(files);
      this.showBulkImportModal = false;
    },
    processFiles(files) {
      this.isUploading = true;
      
      // Create file upload queue with initial status
      this.uploadingFiles = files.map(file => ({
        file,
        name: file.name,
        size: file.size,
        progress: 0,
        status: 'queued'
      }));
      
      // Start uploading each file
      this.uploadFiles();
    },
    async uploadFiles() {
      for (let i = 0; i < this.uploadingFiles.length; i++) {
        const item = this.uploadingFiles[i];
        if (item.status === 'queued') {
          try {
            // Update status to uploading
            this.$set(this.uploadingFiles, i, { ...item, status: 'uploading' });
            
            // Upload the file
            const fileId = await this.uploadFile(item.file, i);
            
            // Mark as complete with the file ID
            this.$set(this.uploadingFiles, i, {
              ...this.uploadingFiles[i],
              status: 'complete',
              progress: 100,
              fileId
            });
          } catch (error) {
            console.error(`Error uploading ${item.name}:`, error);
            this.$set(this.uploadingFiles, i, {
              ...this.uploadingFiles[i],
              status: 'error',
              error: error.message
            });
          }
        }
      }
      
      // Process metadata after all uploads
      if (this.uploadingFiles.some(f => f.status === 'complete')) {
        await this.extractMetadata();
        
        // Refresh imported papers list
        this.fetchImportedPapers();
      }
      
      this.isUploading = false;
    },
    uploadFile(file, index) {
      return new Promise((resolve, reject) => {
        const formData = new FormData();
        formData.append('file', file);
        
        // If an active project is set, associate the file with it
        if (this.activeProject && this.activeProject.id) {
          formData.append('project_id', this.activeProject.id);
        }
        
        // Use the paperService for upload with progress tracking
        paperService.uploadPaper(formData, (percentComplete) => {
          // Update progress in the UI
          this.$set(this.uploadingFiles, index, {
            ...this.uploadingFiles[index],
            progress: percentComplete
          });
        }).then(response => {
          // Return the file ID or other identifier
          const fileId = response.file_id || response.filename || file.name;
          
          // Store project association in metadata if available
          if (this.activeProject && this.activeProject.id) {
            this.$set(this.uploadingFiles, index, {
              ...this.uploadingFiles[index],
              project_id: this.activeProject.id
            });
          }
          
          resolve(fileId);
        }).catch(error => {
          reject(error);
        });
      });
    },
    async extractMetadata() {
      try {
        this.extractingMetadata = true;
        
        // Get file IDs from completed uploads
        const fileIds = this.uploadingFiles
          .filter(item => item.status === 'complete' && item.fileId)
          .map(item => item.fileId);
          
        if (fileIds.length === 0) {
          throw new Error('No files available for metadata extraction');
        }
        
        // Call the API to extract metadata
        const response = await fetch(API_ROUTES.PAPERS.EXTRACT_METADATA, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ file_ids: fileIds })
        });
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || 'Failed to extract metadata');
        }
        
        const data = await response.json();
        console.log('Metadata extraction results:', data);
        
        // Process each file's metadata
        const papersToImport = [];
        
        for (const result of data) {
          if (result.status === 'success' || result.status === 'partial') {
            const metadata = result.metadata;
            
            // Add to import list
            papersToImport.push({
              title: metadata.title || 'Unknown Title',
              abstract: metadata.abstract || '',
              authors: metadata.authors || [],
              journal: metadata.journal || '',
              publication_date: metadata.year ? new Date(metadata.year, 0, 1).toISOString() : null,
              doi: metadata.doi || null,
              file_path: metadata.file_path || '',
              is_open_access: false,
              source: 'PDF Upload'
            });
          }
        }
        
        // Import the papers to the database
        if (papersToImport.length > 0) {
          await this.importPapers(papersToImport);
        }
      } catch (error) {
        console.error('Error extracting metadata:', error);
        alert('Error extracting metadata: ' + error.message);
      } finally {
        this.extractingMetadata = false;
      }
    },
    async importPapers(papers) {
      try {
        // Use paperService instead of direct fetch
        const result = await paperService.importPapersBatch(papers);
        console.log('Import result:', result);
        
        if (result.imported_count > 0) {
          alert(`${result.imported_count} paper(s) imported successfully.`);
        } else {
          alert('No papers were imported. Please check the metadata and try again.');
        }
      } catch (error) {
        console.error('Error importing papers:', error);
        alert('Error importing papers: ' + error.message);
      }
    },
    openBulkImportModal() {
      this.showBulkImportModal = true;
    },
    openManualEntryModal() {
      this.showManualEntryModal = true;
    },
    async addManualPaper() {
      try {
        // Convert the manual paper input to the expected format
        const authors = this.manualPaper.authors.split(',').map(name => ({
          name: name.trim()
        }));
        
        const paper = {
          title: this.manualPaper.title,
          authors: authors,
          journal: this.manualPaper.journal || null,
          publication_date: this.manualPaper.year ? new Date(this.manualPaper.year, 0, 1).toISOString() : null,
          doi: this.manualPaper.doi || null,
          abstract: this.manualPaper.abstract || null,
          source: 'Manual Entry'
        };
        
        // Import the paper
        await this.importPapers([paper]);
        
        // Reset form and close modal
        this.manualPaper = {
          title: '',
          authors: '',
          journal: '',
          year: '',
          doi: '',
          abstract: ''
        };
        
        this.showManualEntryModal = false;
        
        // Refresh imported papers
        this.fetchImportedPapers();
      } catch (error) {
        console.error('Error adding manual paper:', error);
        alert('Error adding paper: ' + error.message);
      }
    },
    editPaper(paper) {
      // Convert authors array to string for editing
      let authorsString = '';
      if (paper.authors) {
        if (Array.isArray(paper.authors)) {
          authorsString = paper.authors.map(author => {
            if (typeof author === 'string') return author;
            return author.name || 'Unknown';
          }).join(', ');
        } else {
          authorsString = String(paper.authors);
        }
      }
      
      // Extract year from publication_date
      let year = null;
      if (paper.publication_date) {
        const date = new Date(paper.publication_date);
        if (!isNaN(date.getTime())) {
          year = date.getFullYear();
        }
      }
      
      this.editingPaper = {
        ...paper,
        authors: authorsString,
        year: year
      };
      
      this.showEditModal = true;
    },
    async updatePaper() {
      try {
        // Convert the editing paper back to proper format
        const authors = this.editingPaper.authors.split(',').map(name => ({
          name: name.trim()
        }));
        
        const paperId = this.editingPaper.id;
        const updatedPaper = {
          title: this.editingPaper.title,
          authors: authors,
          journal: this.editingPaper.journal || null,
          publication_date: this.editingPaper.year ? new Date(this.editingPaper.year, 0, 1).toISOString() : null,
          doi: this.editingPaper.doi || null,
          abstract: this.editingPaper.abstract || null
        };
        
        // Use paperService instead of direct fetch
        await paperService.updatePaper(paperId, updatedPaper);
        
        // Close modal and refresh list
        this.showEditModal = false;
        this.fetchImportedPapers();
        
        alert('Paper updated successfully.');
      } catch (error) {
        console.error('Error updating paper:', error);
        alert('Error updating paper: ' + error.message);
      }
    },
    async removePaper(paperId) {
      if (confirm('Are you sure you want to remove this paper?')) {
        try {
          // Use paperService instead of direct fetch
          await paperService.deletePaper(paperId);
          
          // Update the local list
          this.importedPapers = this.importedPapers.filter(paper => paper.id !== paperId);
          this.selectedPaperIds = this.selectedPaperIds.filter(id => id !== paperId);
          
          alert('Paper removed successfully.');
        } catch (error) {
          console.error('Error removing paper:', error);
          alert('Error removing paper: ' + error.message);
        }
      }
    },
    async removeSelectedPapers() {
      if (this.selectedPaperIds.length === 0) return;
      
      if (confirm(`Are you sure you want to remove ${this.selectedPaperIds.length} selected papers?`)) {
        try {
          // Use paperService batch delete instead of multiple API calls
          await paperService.batchDeletePapers(this.selectedPaperIds);
          
          // Update the local list
          this.importedPapers = this.importedPapers.filter(paper => !this.selectedPaperIds.includes(paper.id));
          this.selectedPaperIds = [];
          
          alert('Selected papers removed successfully.');
        } catch (error) {
          console.error('Error removing selected papers:', error);
          alert('Error removing papers: ' + error.message);
          // Refresh list to show current state
          this.fetchImportedPapers();
        }
      }
    },
    toggleSelectAll() {
      if (this.isAllSelected) {
        this.selectedPaperIds = [];
      } else {
        this.selectedPaperIds = this.importedPapers.map(paper => paper.id);
      }
    },
    togglePaperSelection(paperId) {
      const index = this.selectedPaperIds.indexOf(paperId);
      if (index > -1) {
        this.selectedPaperIds.splice(index, 1);
      } else {
        this.selectedPaperIds.push(paperId);
      }
    },
    isSelected(paperId) {
      return this.selectedPaperIds.includes(paperId);
    },
    formatFileSize(size) {
      if (size < 1024) {
        return `${size} B`;
      } else if (size < 1024 * 1024) {
        return `${(size / 1024).toFixed(1)} KB`;
      } else {
        return `${(size / (1024 * 1024)).toFixed(1)} MB`;
      }
    },
    formatAuthors(authors) {
      if (!authors) return 'Unknown Authors';
      
      if (typeof authors === 'string') {
        return authors;
      }
      
      if (!Array.isArray(authors) || authors.length === 0) {
        return 'Unknown Authors';
      }
      
      // Handle different author formats
      const getAuthorName = (author) => {
        if (typeof author === 'string') return author;
        if (typeof author === 'object' && author !== null) {
          if (author.name) return author.name;
          if (author.firstName && author.lastName) return `${author.firstName} ${author.lastName}`;
          if (author.given && author.family) return `${author.given} ${author.family}`;
        }
        return 'Unknown';
      };
      
      if (authors.length <= 3) {
        return authors.map(getAuthorName).join(', ');
      } else {
        return `${getAuthorName(authors[0])}, et al.`;
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 'imported':
        case 'complete':
          return 'bg-green-100 text-green-800';
        case 'processing':
          return 'bg-yellow-100 text-yellow-800';
        case 'error':
          return 'bg-red-100 text-red-800';
        default:
          return 'bg-gray-100 text-gray-800';
      }
    },
    getStatusText(status) {
      switch (status) {
        case 'imported':
        case 'complete':
          return 'Imported';
        case 'processing':
          return 'Processing...';
        case 'error':
          return 'Error';
        default:
          return status || 'Unknown';
      }
    }
  }
};
</script>

<style scoped>
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #6366f1;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>