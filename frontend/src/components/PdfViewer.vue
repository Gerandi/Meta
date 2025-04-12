<template>
  <div class="flex h-full">
    <div :class="`${showCodingPanel ? 'w-2/3' : 'w-full'} bg-gray-100 border-r flex flex-col h-full`">
      <div class="p-4 bg-white border-b flex justify-between items-center">
        <div>
          <h2 class="font-medium">{{ paper.title }}</h2>
          <div class="text-sm text-gray-500">{{ formatAuthors(paper.authors) }} • {{ paper.journal }} • {{ getYear(paper.publication_date) }}</div>
        </div>
        <div class="flex">
          <button 
            class="px-3 py-1 rounded border mr-2 hover:bg-gray-50"
            @click="downloadPdf"
            :disabled="!paper.open_access_url"
          >
            <Download size="18" />
          </button>
          <button 
            class="px-3 py-1 rounded border hover:bg-gray-50"
            @click="toggleCodingPanel"
          >
            <component :is="showCodingPanel ? 'X' : 'Edit'" size="18" />
          </button>
        </div>
      </div>
      
      <div class="flex-1 p-6 overflow-auto">
        <div v-if="loading" class="flex justify-center items-center h-full">
          <div class="spinner"></div>
        </div>
        <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg">
          <h3 class="font-medium mb-1">Error loading PDF</h3>
          <p>{{ error }}</p>
          <button 
            class="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            @click="retryLoad"
          >
            Try again
          </button>
        </div>
        <div v-else class="bg-white rounded-lg shadow p-6 h-full">
          <!-- PDF Placeholder for MVP -->
          <div class="border-b pb-4 mb-4">
            <h1 class="text-xl font-bold mb-2">{{ paper.title }}</h1>
            <p class="text-sm text-gray-700 mb-4">{{ formatAuthors(paper.authors) }} • {{ paper.journal }} • {{ getYear(paper.publication_date) }}</p>
            <p class="font-medium mb-1">Abstract</p>
            <p class="text-gray-700">
              {{ paper.abstract || 'No abstract available for this paper.' }}
            </p>
          </div>
          
          <div class="flex justify-center items-center h-64 bg-gray-100 rounded-lg border border-dashed border-gray-300 mb-4">
            <div class="text-center">
              <FileText class="text-gray-400 mx-auto mb-2" size="48" />
              <p class="text-gray-500">PDF viewer will be available in the next version</p>
              <p class="text-sm text-gray-400">For now, you can download the PDF if available</p>
              <button 
                v-if="paper.open_access_url"
                class="mt-3 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                @click="downloadPdf"
              >
                Download PDF
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="showCodingPanel" class="w-1/3 bg-white flex flex-col h-full">
      <div class="p-4 border-b">
        <h2 class="font-medium mb-2">Coding Sheet</h2>
        <p class="text-sm text-gray-500">Extract data from the paper using the form below</p>
      </div>
      
      <div class="flex-1 p-4 overflow-auto">
        <div class="mb-6">
          <h3 class="font-medium mb-3">Study Information</h3>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Authors
            </label>
            <input 
              v-model="codingData.authors"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Publication Year
            </label>
            <input 
              v-model="codingData.publicationYear"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Journal
            </label>
            <input 
              v-model="codingData.journal"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
        </div>
        
        <div class="mb-6">
          <h3 class="font-medium mb-3">Methodology</h3>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Study Design
            </label>
            <select 
              v-model="codingData.studyDesign"
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            >
              <option value="meta-analysis">Meta-Analysis</option>
              <option value="rct">RCT</option>
              <option value="cohort">Cohort Study</option>
              <option value="case-control">Case-Control</option>
              <option value="systematic-review">Systematic Review</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Number of Studies
            </label>
            <input 
              v-model="codingData.numberOfStudies"
              type="number" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Total Sample Size
            </label>
            <input 
              v-model="codingData.sampleSize"
              type="number" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
        </div>
        
        <div class="mb-6">
          <h3 class="font-medium mb-3">Study Findings</h3>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Overall Effect Size
            </label>
            <input 
              v-model="codingData.effectSize"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              placeholder="e.g., g = 0.82"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Confidence Interval
            </label>
            <input 
              v-model="codingData.confidenceInterval"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              placeholder="e.g., 95% CI [0.71, 0.93]"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Statistical Significance
            </label>
            <input 
              v-model="codingData.pValue"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              placeholder="e.g., p < .001"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Moderators Identified
            </label>
            <textarea 
              v-model="codingData.moderators"
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              rows="3"
            ></textarea>
          </div>
        </div>
      </div>
      
      <div class="p-4 border-t flex justify-end">
        <button 
          class="px-4 py-2 rounded-lg bg-gray-200 text-gray-800 mr-2 hover:bg-gray-300"
          @click="resetForm"
        >
          Reset
        </button>
        <button 
          class="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 flex items-center"
          @click="saveData"
          :disabled="saving"
        >
          <Save class="mr-1" size="18" /> {{ saving ? 'Saving...' : 'Save Data' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { API_ROUTES } from '../config.js';
import { Download, Edit, X, FileText, Save } from 'lucide-vue-next';

export default {
  name: 'PdfViewer',
  components: {
    Download,
    Edit,
    X,
    FileText,
    Save
  },
  props: {
    paper: {
      type: Object,
      required: true
    },
    projectId: {
      type: Number,
      required: false,
      default: null
    }
  },
  data() {
    return {
      showCodingPanel: true,
      loading: false,
      error: null,
      saving: false,
      codingSheet: null,
      codingData: {},
      savedCoding: null,
      defaultCodingData: {
        authors: '',
        publicationYear: '',
        journal: '',
        studyDesign: '',
        numberOfStudies: null,
        sampleSize: null,
        effectSize: '',
        confidenceInterval: '',
        pValue: '',
        moderators: '',
        riskOfBias: 'low',
        prismaAdherence: 'not-reported',
        qualityNotes: ''
      }
    }
  },
  mounted() {
    // Load the coding sheet for this project (if project ID is provided)
    this.loadCodingSheet();
    // Check if this paper already has coding data saved
    this.loadExistingCoding();
  },
  methods: {
    async loadCodingSheet() {
      if (!this.projectId) return;
      
      try {
        const response = await fetch(API_ROUTES.CODING.GET_BY_PROJECT_ID(this.projectId));
        
        if (response.ok) {
          this.codingSheet = await response.json();
          console.log('Loaded coding sheet:', this.codingSheet);
          
          // Initialize coding data object with fields from the coding sheet
          this.initializeCodingData();
        } else {
          console.warn('No coding sheet found for this project. Using default form.');
          // Use default form
          this.codingData = { ...this.defaultCodingData };
          this.prefillForm();
        }
      } catch (err) {
        console.error('Error loading coding sheet:', err);
        // Use default form on error
        this.codingData = { ...this.defaultCodingData };
        this.prefillForm();
      }
    },
    
    async loadExistingCoding() {
      if (!this.paper.id) return;
      
      try {
        const response = await fetch(API_ROUTES.CODING.GET_FOR_PAPER(this.paper.id));
        
        if (response.ok) {
          this.savedCoding = await response.json();
          console.log('Loaded existing coding:', this.savedCoding);
          
          // Merge existing coding data with our coding data object
          if (this.savedCoding.data) {
            this.codingData = { ...this.codingData, ...this.savedCoding.data };
          }
        } else {
          console.log('No existing coding found for this paper.');
        }
      } catch (err) {
        console.error('Error loading existing coding:', err);
      }
    },
    
    initializeCodingData() {
      // Initialize coding data with empty values
      if (!this.codingSheet) {
        this.codingData = { ...this.defaultCodingData };
        return;
      }
      
      // Initialize from coding sheet sections and fields
      const newCodingData = {};
      
      this.codingSheet.sections.forEach(section => {
        section.fields.forEach(field => {
          // Initialize with empty value based on field type
          switch (field.type) {
            case 'number':
              newCodingData[field.name] = null;
              break;
            case 'boolean':
              newCodingData[field.name] = false;
              break;
            case 'select':
              // Get first option as default
              const options = (field.options || '').split('\n');
              newCodingData[field.name] = options.length > 0 ? options[0] : '';
              break;
            default:
              newCodingData[field.name] = '';
          }
        });
      });
      
      this.codingData = newCodingData;
      this.prefillForm();
    },
    formatAuthors(authors) {
      if (!authors || authors.length === 0) return 'Unknown Authors';
      
      if (authors.length <= 3) {
        return authors.map(a => a.name).join(', ');
      } else {
        return `${authors[0].name}, et al.`;
      }
    },
    
    getYear(dateString) {
      if (!dateString) return 'Unknown Year';
      return new Date(dateString).getFullYear();
    },
    
    toggleCodingPanel() {
      this.showCodingPanel = !this.showCodingPanel;
    },
    
    prefillForm() {
      // Prefill form with paper metadata
      if (this.paper) {
        this.codingData.authors = this.formatAuthors(this.paper.authors);
        this.codingData.publicationYear = this.getYear(this.paper.publication_date);
        this.codingData.journal = this.paper.journal || '';
        
        // Try to auto-detect study design from title or abstract
        const titleLower = this.paper.title?.toLowerCase() || '';
        if (titleLower.includes('meta-analysis')) {
          this.codingData.studyDesign = 'meta-analysis';
        } else if (titleLower.includes('systematic review')) {
          this.codingData.studyDesign = 'systematic-review';
        } else if (titleLower.includes('randomized') || titleLower.includes('rct')) {
          this.codingData.studyDesign = 'rct';
        }
      }
    },
    
    downloadPdf() {
      if (this.paper.open_access_url) {
        window.open(this.paper.open_access_url, '_blank');
      }
    },
    
    retryLoad() {
      this.error = null;
      // For MVP, we're not actually loading a PDF
    },
    
    resetForm() {
      this.prefillForm();
    },
    
    async saveData() {
      this.saving = true;
      
      try {
        // Prepare the data to save
        const payload = {
          paperId: this.paper.id,
          projectId: this.projectId,
          data: this.codingData
        };
        
        // If we already have saved coding, update it
        let url = API_ROUTES.CODING.SAVE_PAPER_CODING;
        let method = 'POST';
        
        if (this.savedCoding && this.savedCoding.id) {
          url = `${API_ROUTES.CODING.GET_BY_ID(this.savedCoding.id)}`;
          method = 'PUT';
          payload.id = this.savedCoding.id;
        }
        
        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to save coding data');
        }
        
        const savedData = await response.json();
        this.savedCoding = savedData;
        
        // Show success message
        alert('Coding data saved successfully!');
      } catch (err) {
        console.error('Error saving coding data:', err);
        alert('Failed to save coding data: ' + err.message);
      } finally {
        this.saving = false;
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
