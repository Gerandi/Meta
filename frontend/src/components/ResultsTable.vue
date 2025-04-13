<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Results Table</h1>
      <div class="flex">
        <button class="flex items-center px-3 py-2 rounded-lg border bg-white mr-2 hover:bg-gray-50">
          <Filter class="mr-1" size="16" /> Filter
        </button>
        <button class="flex items-center px-3 py-2 rounded-lg border bg-white hover:bg-gray-50">
          <Download class="mr-1" size="16" /> Export
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="text-center py-12">
      <div class="spinner mb-4"></div>
      <p class="text-gray-500">Loading results...</p>
    </div>
    
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-6">
      <h3 class="font-medium mb-1">Error loading results</h3>
      <p>{{ error }}</p>
    </div>
    
    <div v-else-if="rows.length === 0" class="bg-white rounded-lg shadow p-8 text-center">
      <div class="mb-4 text-gray-400">
        <Table class="mx-auto" size="64" />
      </div>
      <h2 class="text-xl font-medium mb-2">No Results Yet</h2>
      <p class="text-gray-500 mb-4">Start by searching for papers and coding them.</p>
      <button 
        class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
        @click="$emit('change-view', 'search')"
      >
        Find Papers
      </button>
    </div>
    
    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
      <div class="p-4 border-b">
        <div class="flex justify-between items-center">
          <div class="text-lg font-medium">Extracted Data</div>
          <div class="text-sm text-gray-500">{{ rows.length }} Papers • {{ totalDataPoints }} Data Points</div>
        </div>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th v-for="column in columns" :key="column.name"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {{ column.label }}
              </th>
              <th class="relative px-6 py-3">
                <span class="sr-only">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="row in rows" :key="row.paper_id">
              <td v-for="column in columns" :key="column.name"
                class="px-6 py-4 whitespace-nowrap text-sm"
                :class="column.name === 'authors' ? 'font-medium text-gray-900' : 'text-gray-500'"
              >
                {{ getCellValue(row, column.name) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button class="text-indigo-600 hover:text-indigo-900"
                  @click="editPaper(row.paper_id)"
                >
                  Edit
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div class="px-6 py-4 border-t flex justify-between items-center">
        <div class="text-sm text-gray-500">
          Showing {{ rows.length }} entries
        </div>
        <div class="flex">
          <button 
            class="px-3 py-1 border rounded-md hover:bg-gray-50 mr-2"
            :disabled="currentPage === 1"
            @click="prevPage"
          >Previous</button>
          <button 
            class="px-3 py-1 border rounded-md hover:bg-gray-50"
            :disabled="currentPage === totalPages"
            @click="nextPage"
          >Next</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { resultsService, paperService } from '../services/api';
import { Filter, Download, Table } from 'lucide-vue-next';

export default {
  name: 'ResultsTable',
  components: {
    Filter,
    Download,
    Table
  },
  props: {
    projectId: {
      type: Number,
      required: false,
      default: null
    }
  },
  data() {
    return {
      loading: true,
      error: null,
      columns: [],
      rows: [],
      currentPage: 1,
      totalPages: 1,
      totalDataPoints: 0
    }
  },
  mounted() {
    // Fetch data
    this.fetchResults();
  },
  watch: {
    projectId: {
      handler() {
        this.fetchResults();
      }
    }
  },
  methods: {
    async fetchResults() {
      this.loading = true;
      this.error = null;
      
      try {
        if (!this.projectId) {
          console.warn("ResultsTable: projectId is missing. Cannot fetch results.");
          this.rows = [];
          this.columns = [];
          this.totalDataPoints = 0;
          this.error = "No project selected.";
          this.loading = false;
          return;
        }
        
        // Get results table data from API
        const resultsTable = await resultsService.getResultsTable(this.projectId);
        
        // Update component data
        this.columns = resultsTable.columns;
        this.rows = resultsTable.rows;
        this.totalPages = Math.ceil(resultsTable.total_rows / resultsTable.page_size);
        
        // Calculate total data points
        this.calculateTotalDataPoints();
        
        this.loading = false;
      } catch (err) {
        console.error('Error fetching results:', err);
        
        // Check for specific "No coding sheet found" error
        if (err.message && err.message.toLowerCase().includes('no coding sheet found')) {
          this.error = 'No coding sheet has been configured for this project yet.';
          this.rows = []; // Ensure table is empty
          this.columns = [];
        } else {
          this.error = 'Failed to load results. Please try again: ' + err.message;
        }
        this.loading = false;
      }
    },
    
    calculateTotalDataPoints() {
      let total = 0;
      
      this.rows.forEach(row => {
        if (row.values) {
          // Count each field that has a value
          total += Object.values(row.values).filter(value => {
            return value !== null && value !== undefined && value !== '';
          }).length;
        }
      });
      
      this.totalDataPoints = total;
    },
    
    getCellValue(row, column) {
      if (!row.values) return 'N/A';
      
      const value = row.values[column];
      
      if (value === null || value === undefined) {
        return 'N/A';
      }
      
      return value;
    },
    
    editPaper(paperId) {
      // First, get the paper details
      this.getPaperAndNavigate(paperId);
    },
    
    async getPaperAndNavigate(paperId) {
      try {
        const paper = await paperService.getPaper(paperId);
        this.$emit('select-paper', paper, this.projectId);
      } catch (error) {
        console.error('Error getting paper details:', error);
        alert('Error loading paper details: ' + error.message);
      }
    },
    
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchResults();
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.fetchResults();
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
