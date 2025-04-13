<template>
  <div class="p-4 border-b hover:bg-gray-50">
    <div class="flex justify-between">
      <div class="font-medium text-indigo-600 mb-1">{{ paper.title }}</div>
      <div class="flex items-center">
        <div class="text-xs px-2 py-1 rounded-full mr-2" :class="paper.open_access ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'">
          {{ paper.open_access ? 'Open Access' : 'Subscription' }}
        </div>
        <div class="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600 flex items-center">
          <Database class="mr-1" size="12" />
          {{ paper.source || 'Unknown' }}
        </div>
      </div>
    </div>
    <div class="text-sm text-gray-700 mb-1">{{ formatAuthors(paper.authors) }}</div>
    <div class="text-sm text-gray-500 mb-2">{{ paper.journal || 'Unknown Journal' }} • {{ getYear(paper.publication_date) }}</div>
    <div class="text-sm text-gray-600 mb-3 line-clamp-3">{{ paper.abstract || 'No abstract available for this paper.' }}</div>
    <div class="flex">
      <button 
        v-if="paper.doi || paper.open_access_url" 
        class="flex items-center text-indigo-600 mr-4 hover:text-indigo-800"
        @click.stop="$emit('download')"
      >
        <Download class="mr-1" size="16" /> Download PDF
      </button>
      <button 
        class="flex items-center mr-4"
        :class="isImported ? 'text-green-600 cursor-default' : 'text-indigo-600 hover:text-indigo-800'"
        @click.stop="!isImported && handleImportAction()"
        :disabled="isImported"
      >
        <component :is="isImported ? 'CheckCircle' : 'PlusCircle'" class="mr-1" size="16" />
        {{ isImported ? 'Imported' : 'Import' }}
      </button>
      <button 
        class="flex items-center text-indigo-600 hover:text-indigo-800"
        @click.stop="$emit('view-details')"
      >
        <Book class="mr-1" size="16" /> View Details
      </button>
    </div>
  </div>
</template>

<script>
import { Database, Download, PlusCircle, Book, CheckCircle } from 'lucide-vue-next';
import { useProjectStore } from '../../../stores/project';
import { mapState } from 'pinia';

export default {
  name: 'SearchResultItem',
  components: {
    Database,
    Download,
    PlusCircle,
    Book
  },
  props: {
    paper: {
      type: Object,
      required: true
    },
    selected: {
      type: Boolean,
      default: false
    },
    importedPaperIds: {
      type: Set,
      required: true
    }
    // activeProject prop removed - now using Pinia store
  },
  computed: {
    ...mapState(useProjectStore, ['activeProject', 'hasActiveProject']),
    isImported() {
      // Check if the paper's DOI or title exists in the imported set
      return this.importedPaperIds.has(this.paper.id) || // Check if backend returns ID now
             (this.paper.doi && this.importedPaperIds.has(this.paper.doi)) || // Fallback check
             this.importedPaperIds.has(this.paper.title); // Least reliable fallback
    }
  },
  emits: ['download', 'view-details', 'import-to-project', 'import-to-staging'],
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
    
    handleImportAction() {
      if (this.hasActiveProject) {
        // If project is active, emit event to add directly to project
        console.log(`Emitting import-to-project for paper: ${this.paper.title} to project ${this.activeProject.id}`);
        this.$emit('import-to-project', this.paper);
      } else {
        // If no project active, emit event to add to staging (imported list)
        console.log(`Emitting import-to-staging for paper: ${this.paper.title}`);
        this.$emit('import-to-staging', this.paper);
      }
    }
  }
};
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
