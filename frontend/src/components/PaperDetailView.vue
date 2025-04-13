<template>
  <div class="flex h-screen">
    <!-- Metadata Panel -->
    <div class="w-1/3 border-r p-4 overflow-y-auto bg-white">
      <button @click="$emit('change-view', 'search')" class="mb-4 text-indigo-600 hover:text-indigo-800 flex items-center">
         <ArrowLeft size="16" class="mr-1"/> Back to Search
      </button>
      <h2 class="text-lg font-semibold mb-2">{{ paper.title }}</h2>
      <p class="text-sm text-gray-600 mb-1"><strong>Authors:</strong> {{ formatAuthors(paper.authors) }}</p>
      <p class="text-sm text-gray-600 mb-1"><strong>Journal:</strong> {{ paper.journal || 'N/A' }}</p>
      <p class="text-sm text-gray-600 mb-1"><strong>Year:</strong> {{ getYear(paper.publication_date) }}</p>
      <p class="text-sm text-gray-600 mb-1"><strong>DOI:</strong> {{ paper.doi || 'N/A' }}</p>
      <p class="text-sm text-gray-600 mb-3"><strong>Source:</strong> {{ paper.source || 'N/A' }}</p>

      <button
        class="w-full flex items-center justify-center px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 mb-4"
        @click="handleImport"
        :disabled="isImporting || isImported"
        :class="{'opacity-50 cursor-not-allowed': isImported}"
      >
        <component :is="isImported ? 'CheckCircle' : 'PlusCircle'" class="mr-1" size="16" />
        {{ isImported ? 'Imported' : (isImporting ? 'Importing...' : 'Import Paper') }}
      </button>

      <h3 class="font-semibold mb-1 mt-4">Abstract</h3>
      <p class="text-sm text-gray-700">{{ paper.abstract || 'No abstract available.' }}</p>

      <h3 class="font-semibold mb-1 mt-4">Keywords</h3>
      <div v-if="paper.keywords && paper.keywords.length" class="flex flex-wrap gap-1">
         <span v-for="kw in paper.keywords" :key="kw" class="text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded-full">{{ kw }}</span>
      </div>
      <p v-else class="text-sm text-gray-500">No keywords available.</p>
    </div>

    <!-- PDF Viewer -->
    <div class="w-2/3 flex-grow">
      <PdfViewer :paper="paper" :showCodingPanel="false" />
    </div>
  </div>
</template>

<script>
import PdfViewer from './PdfViewer.vue';
import { ArrowLeft, PlusCircle, CheckCircle } from 'lucide-vue-next';
import { paperService, projectService } from '../services/api.js'; // Import services
import { useProjectStore } from '../stores/project'; // Import Pinia store
import { mapState } from 'pinia';

export default {
  name: 'PaperDetailView',
  components: { PdfViewer, ArrowLeft, PlusCircle, CheckCircle },
  props: {
    paper: { type: Object, required: true }
  },
  data() {
    return {
      isImporting: false,
      isImported: false // Add state to track if imported
    };
  },
  computed: {
     ...mapState(useProjectStore, ['activeProject', 'hasActiveProject']),
  },
  methods: {
    formatAuthors(authors) {
      if (!authors || authors.length === 0) return 'Unknown Authors';
      
      // Handle different author formats from various providers
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
    getYear(dateString) {
      if (!dateString) return 'Unknown Year';
      
      // Handle different date formats
      try {
        // Try to parse as ISO date
        const year = new Date(dateString).getFullYear();
        if (!isNaN(year)) return year;
        
        // Check if the string itself is just a year
        if (/^\d{4}$/.test(dateString)) return dateString;
        
        // Try to extract year from a date string
        const yearMatch = dateString.match(/\b(19|20)\d{2}\b/);
        if (yearMatch) return yearMatch[0];
      } catch (err) {
        console.warn('Error parsing date:', dateString, err);
      }
      
      return 'Unknown Year';
    },
    async handleImport() {
      this.isImporting = true;
      try {
        // Reuse the formatting logic from PaperSearch.vue
        const formattedPaper = this.formatPaperForImport(this.paper);

        if (this.hasActiveProject) {
          // Import directly to project
          formattedPaper.status = 'processing';
          await projectService.importAndAddPaperToProject(this.activeProject.id, formattedPaper);
          alert(`Paper "${this.paper.title}" added directly to project "${this.activeProject.name}".`);
          this.isImported = true; // Mark as imported
          this.$emit('refresh-project', this.activeProject.id); // Notify App.vue if needed
        } else {
          // Import to staging
          formattedPaper.status = 'imported';
          const result = await paperService.importPapersBatch([formattedPaper]);
          if (result.imported_count > 0) {
            alert(`Paper "${this.paper.title}" imported to staging area.`);
            this.isImported = true; // Mark as imported
            // Optionally notify App.vue to refresh imported list in PaperSearch
            this.$emit('refresh-imported-list');
          } else {
             throw new Error(result.errors?.[0]?.error || 'Import failed');
          }
        }
      } catch (error) {
        console.error('Error importing paper from detail view:', error);
        alert(`Failed to import paper: ${error.message}`);
      } finally {
        this.isImporting = false;
      }
    },
    // Copy formatPaperForImport from PaperSearch.vue here
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
         // Status will be set by handleImport
       };
    }
  }
}
</script>
