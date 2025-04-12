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
  methods: {
    continueToProcessing() {
      // Continue to processing logic
    },
    handleFileUpload(event) {
      // Handle file upload logic
    },
    openBulkImportModal() {
      this.showBulkImportModal = true;
    },
    handleBulkFileUpload(event) {
      // Handle bulk file upload logic
    },
    openManualEntryModal() {
      this.showManualEntryModal = true;
    },
    addManualPaper() {
      // Add manual paper logic
    },
    editPaper(paper) {
      this.editingPaper = { ...paper };
      this.showEditModal = true;
    },
    updatePaper() {
      // Update paper logic
    },
    removePaper(paperId) {
      // Remove paper logic
    },
    removeSelectedPapers() {
      // Remove selected papers logic
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
      // Format file size logic
    },
    formatAuthors(authors) {
      // Format authors logic
    },
    getStatusClass(status) {
      // Get status class logic
    },
    getStatusText(status) {
      // Get status text logic
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