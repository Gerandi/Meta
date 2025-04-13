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
      this.pdfUrl = null; // Reset
      try {
        // 1. Check for local file_path (use /content endpoint)
        if (this.paper.file_path && this.paper.id) {
          const localContentUrl = API_ROUTES.PAPERS.GET_CONTENT(this.paper.id);
          console.log("Trying local file path via endpoint:", localContentUrl);
          // Check if accessible (optional, but good practice)
          try {
              const headResponse = await fetch(localContentUrl, { method: 'HEAD' });
              if (headResponse.ok) {
                  console.log("Local PDF file found via /content endpoint.");
                  this.pdfUrl = localContentUrl;
                  this.loading = false;
                  return; // Use local file
              } else {
                  console.warn(`Local file endpoint check failed: ${headResponse.status}`);
              }
          } catch (headError) {
              console.error("Error checking local file endpoint:", headError);
          }
        }
        // 2. Check for external open_access_url (use /proxy-pdf endpoint)
        if (this.paper.open_access_url && this.paper.id) {
          const proxyUrl = API_ROUTES.PAPERS.PROXY_PDF(this.paper.id);
          console.log("Using backend proxy for external URL:", proxyUrl);
          // Assume proxy works if URL exists, viewer will handle errors
          this.pdfUrl = proxyUrl;
          this.loading = false;
          return; // Use proxied URL
        }
        // 3. Try API lookup via DOI (as fallback, might get external URL again)
        if (this.paper.doi) {
          console.log("Attempting DOI lookup for PDF as fallback:", this.paper.doi);
          const doi = this.paper.doi.split(/[^0-9./\-a-zA-Z]/)[0].trim();
          const response = await fetch(API_ROUTES.PAPERS.GET_PDF(encodeURIComponent(doi)));
          if (response.ok) {
            const data = await response.json();
            if (data.pdf_url && this.paper.id) {
              // If DOI lookup gives an external URL, use the proxy
              console.log("Found external PDF via DOI lookup, using proxy:", data.pdf_url);
              this.pdfUrl = API_ROUTES.PAPERS.PROXY_PDF(this.paper.id); // Use proxy
              this.loading = false;
              return;
            }
          } else {
            console.warn(`DOI lookup failed: ${response.status}`);
          }
        }
        // 4. If none of the above worked
        console.log("No suitable PDF source found for this paper.");
        this.pdfUrl = null; // Explicitly set to null
        this.loading = false;
      } catch (err) {
        console.error('Error loading PDF:', err);
        this.error = 'Failed to load PDF source: ' + err.message;
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
      if (this.paper.id && this.paper.open_access_url) {
        // Use the proxy URL for downloading to avoid CORS issues
        const proxyUrl = API_ROUTES.PAPERS.PROXY_PDF(this.paper.id);
        window.open(proxyUrl, '_blank');
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
