<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold">Code Papers</h1>
        <p class="text-gray-600">Review and code papers in your collection</p>
      </div>
      <div class="flex">
        <button 
          class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center"
          @click="configureSheet"
        >
          <Settings class="mr-1" size="16" /> Configure Coding Sheet
        </button>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-lg mb-6 p-6">
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6 flex">
        <div class="text-blue-500 mr-3 mt-0.5">
          <HelpCircle size="24" />
        </div>
        <div>
          <h3 class="font-medium text-blue-800 mb-1">Coding Papers</h3>
          <p class="text-blue-700 text-sm">
            This page shows all papers that are ready to be coded. Click "Start Coding" to begin coding a paper.
            Make sure to configure your coding sheet first if you haven't already.
          </p>
        </div>
      </div>
      
      <div class="flex justify-between items-center mb-4">
        <div class="flex">
          <div class="relative mr-2">
            <Search class="absolute left-3 top-2.5 text-gray-400" size="18" />
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search papers..."
              class="pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none w-64"
              @keyup.enter="fetchPapers"
            />
          </div>
          <select 
            v-model="sortBy"
            class="border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            @change="fetchPapers"
          >
            <option value="title">Sort by Title</option>
            <option value="authors">Sort by Author</option>
            <option value="year">Sort by Year</option>
            <option value="journal">Sort by Journal</option>
          </select>
        </div>
      </div>

      <div v-if="isLoading" class="text-center py-12">
        <div class="spinner mb-4"></div>
        <p class="text-gray-500">Loading papers...</p>
      </div>
      
      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-6">
        <h3 class="font-medium mb-1">Error loading papers</h3>
        <p>{{ error }}</p>
      </div>
      
      <div v-else-if="papers.length === 0" class="text-center py-12">
        <FolderOpen class="text-gray-400 mx-auto mb-4" size="48" />
        <h3 class="text-xl font-medium mb-2">No Papers Ready for Coding</h3>
        <p class="text-gray-600 mb-4">
          There are no papers ready to be coded. Process your papers in the Processing view first.
        </p>
        <button 
          class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          @click="goToProcessing"
        >
          Go to Processing
        </button>
      </div>
      
      <div v-else class="bg-white border rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
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
            <tr v-for="paper in papers" :key="paper.id" class="hover:bg-gray-50">
              <td class="px-4 py-4">
                <div class="font-medium text-gray-900">{{ paper.title }}</div>
                <div class="text-sm text-gray-500">{{ formatAuthors(paper.authors) }}</div>
              </td>
              <td class="px-4 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ paper.journal || "—" }}</div>
                <div class="text-sm text-gray-500">{{ paper.publication_date ? new Date(paper.publication_date).getFullYear() : "Unknown Year" }}</div>
              </td>
              <td class="px-4 py-4 whitespace-nowrap text-sm">
                <div class="flex items-center">
                  <span class="h-2 w-2 bg-green-500 rounded-full mr-2"></span>
                  Ready to Code
                </div>
              </td>
              <td class="px-4 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button 
                  class="px-3 py-1 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center ml-auto"
                  @click="startCoding(paper)"
                >
                  <Edit2 class="mr-1" size="14" /> Start Coding
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        
        <div class="px-6 py-4 border-t flex justify-between items-center bg-gray-50">
          <div class="text-sm text-gray-700">
            Showing {{ papers.length }} of {{ totalPapers }} papers
          </div>
          <div class="flex">
            <button 
              class="px-3 py-1 border rounded-md hover:bg-gray-100 mr-2"
              :disabled="currentPage === 1"
              @click="prevPage"
            >Previous</button>
            <button 
              class="px-3 py-1 border rounded-md hover:bg-gray-100"
              :disabled="currentPage === totalPages"
              @click="nextPage"
            >Next</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { paperService } from '../services/api.js';
import { 
  Search, 
  HelpCircle, 
  FolderOpen, 
  Settings, 
  Edit2
} from 'lucide-vue-next';

export default {
  name: 'CodingListView',
  components: {
    Search, 
    HelpCircle, 
    FolderOpen, 
    Settings, 
    Edit2
  },
  props: {
    activeProject: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      papers: [],
      totalPapers: 0,
      currentPage: 1,
      itemsPerPage: 10,
      totalPages: 1,
      searchQuery: '',
      sortBy: 'title',
      isLoading: false,
      error: null
    };
  },
  watch: {
    activeProject: {
      immediate: true,
      handler(newProject) {
        if (newProject && newProject.id) {
          this.fetchPapers();
        }
      }
    }
  },
  mounted() {
    this.fetchPapers();
  },
  methods: {
    async fetchPapers() {
      if (!this.activeProject || !this.activeProject.id) {
        this.error = "No active project selected.";
        return;
      }

      this.isLoading = true;
      this.error = null;
      
      try {
        // Build filters to get papers with status=ready_to_code for this project
        const filters = {
          project_id: this.activeProject.id,
          status: 'READY_TO_CODE',
          skip: (this.currentPage - 1) * this.itemsPerPage,
          limit: this.itemsPerPage
        };
        
        if (this.searchQuery) {
          filters.search = this.searchQuery;
        }
        
        if (this.sortBy) {
          filters.sort_by = this.sortBy;
        }
        
        const response = await paperService.listPapers(
          (this.currentPage - 1) * this.itemsPerPage,
          this.itemsPerPage,
          filters
        );
        
        this.papers = response;
        this.totalPapers = response.length; // This should be improved if API returns total count
        this.totalPages = Math.ceil(this.totalPapers / this.itemsPerPage);
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching papers for coding:', err);
      } finally {
        this.isLoading = false;
      }
    },
    
    formatAuthors(authors) {
      if (!authors || authors.length === 0) {
        return 'Unknown Authors';
      }
      
      if (typeof authors === 'string') {
        return authors;
      }
      
      if (authors.length <= 3) {
        return authors.map(a => typeof a === 'object' ? a.name : a).join(', ');
      } else {
        const firstAuthor = typeof authors[0] === 'object' ? authors[0].name : authors[0];
        return `${firstAuthor}, et al.`;
      }
    },
    
    configureSheet() {
      this.$emit('configure-sheet');
    },
    
    startCoding(paper) {
      this.$emit('start-coding', paper);
    },
    
    goToProcessing() {
      this.$emit('change-view', 'processing', this.activeProject.id);
    },
    
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchPapers();
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.fetchPapers();
      }
    }
  }
};
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