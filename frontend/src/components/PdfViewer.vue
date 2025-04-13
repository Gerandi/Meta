<template>
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
          v-if="showCodingPanelButton"
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
        <!-- PDF Viewer -->
        <template v-if="pdfUrl">
          <vue-pdf-embed
            class="h-full"
            :source="pdfUrl"
            :style="{ height: 'calc(100vh - 180px)' }"
            @rendered="onPdfRendered"
            @error="onPdfError"
          />
        </template>
        
        <!-- Fallback when no PDF is available -->
        <template v-else>
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
              <p class="text-gray-500">PDF not available for this paper</p>
              <p class="text-sm text-gray-400">The paper doesn't have an accessible PDF link</p>
              <button 
                v-if="paper.open_access_url"
                class="mt-3 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                @click="downloadPdf"
              >
                Download PDF
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { API_ROUTES } from '../config.js';
import { Download, Edit, X, FileText } from 'lucide-vue-next';
import VuePdfEmbed from 'vue-pdf-embed';

export default {
  name: 'PdfViewer',
  components: {
    Download,
    Edit,
    X,
    FileText,
    VuePdfEmbed
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
    },
    showCodingPanel: {
      type: Boolean,
      default: true
    },
    showCodingPanelButton: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      loading: true,
      error: null,
      pdfUrl: null
    }
  },
  mounted() {
    this.loadPdf();
  },
  watch: {
    paper: {
      handler() {
        this.loadPdf();
      },
      deep: true
    }
  },
  methods: {
    async loadPdf() {
      this.loading = true;
      this.error = null;
      
      try {
        // First check if the paper already has a direct PDF URL
        if (this.paper.open_access_url) {
          this.pdfUrl = this.paper.open_access_url;
          this.loading = false;
          return;
        }
        
        // If not, try to get the PDF URL from the API
        if (this.paper.doi) {
          const response = await fetch(`${API_ROUTES.PAPERS.GET_PDF}/${encodeURIComponent(this.paper.doi)}`);
          if (response.ok) {
            const data = await response.json();
            if (data.pdf_url) {
              this.pdfUrl = data.pdf_url;
              this.loading = false;
              return;
            }
          }
        }
        
        // If we still don't have a PDF URL, check if the paper has a local file path
        if (this.paper.file_path) {
          // In a real implementation, we would have an API endpoint to serve local files
          // For now, we'll simulate this with a placeholder
          this.pdfUrl = `/api/papers/${this.paper.id}/pdf-content`;
          this.loading = false;
          return;
        }
        
        // If we reach here, there's no PDF available
        this.pdfUrl = null;
        this.loading = false;
      } catch (err) {
        console.error('Error loading PDF:', err);
        this.error = 'Failed to load PDF: ' + err.message;
        this.loading = false;
      }
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
      try {
        return new Date(dateString).getFullYear();
      } catch (e) {
        return 'Unknown Year';
      }
    },
    
    toggleCodingPanel() {
      this.$emit('toggle-coding-panel');
    },
    
    onPdfRendered() {
      this.loading = false;
    },
    
    onPdfError(error) {
      console.error('PDF loading error:', error);
      this.error = 'Failed to render PDF. The file might be corrupted or inaccessible.';
      this.loading = false;
    },
    
    downloadPdf() {
      if (this.paper.open_access_url) {
        window.open(this.paper.open_access_url, '_blank');
      }
    },
    
    retryLoad() {
      this.loadPdf();
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
