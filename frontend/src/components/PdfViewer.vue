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
            <font-awesome-icon icon="download" />
          </button>
          <button 
            class="px-3 py-1 rounded border hover:bg-gray-50"
            @click="toggleCodingPanel"
          >
            <font-awesome-icon :icon="showCodingPanel ? 'times' : 'edit'" />
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
              <font-awesome-icon icon="file-alt" class="text-gray-400 text-4xl mb-2" />
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
          <font-awesome-icon icon="save" class="mr-1" /> {{ saving ? 'Saving...' : 'Save Data' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PdfViewer',
  props: {
    paper: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      showCodingPanel: true,
      loading: false,
      error: null,
      saving: false,
      codingData: {
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
    // Pre-fill form with paper metadata
    this.prefillForm();
  },
  methods: {
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
        // Add paper ID to coding data
        const codingDataToSave = {
          ...this.codingData,
          paperId: this.paper.id
        };
        
        // For MVP, just log the data that would be saved
        console.log('Saving coding data:', codingDataToSave);
        
        // Show success message
        alert('Coding data saved successfully! (This is a mock action for the MVP)');
      } catch (err) {
        console.error('Error saving coding data:', err);
        alert('Failed to save coding data. Please try again.');
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
