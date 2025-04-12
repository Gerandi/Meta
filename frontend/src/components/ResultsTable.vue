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
    
    <div v-else-if="papers.length === 0" class="bg-white rounded-lg shadow p-8 text-center">
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
          <div class="text-sm text-gray-500">{{ papers.length }} Papers • {{ totalDataPoints }} Data Points</div>
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
            <tr v-for="paper in papers" :key="paper.id">
              <td v-for="column in columns" :key="column.name"
                class="px-6 py-4 whitespace-nowrap text-sm"
                :class="column.name === 'authors' ? 'font-medium text-gray-900' : 'text-gray-500'"
              >
                {{ getCellValue(paper, column.name) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button class="text-indigo-600 hover:text-indigo-900"
                  @click="editPaper(paper)"
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
          Showing {{ papers.length }} entries
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
import { API_ROUTES } from '../config.js';
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
      columns: [
        { name: 'authors', label: 'Authors' },
        { name: 'year', label: 'Year' },
        { name: 'journal', label: 'Journal' },
        { name: 'studyDesign', label: 'Study Design' },
        { name: 'sampleSize', label: 'N Studies' },
        { name: 'effectSize', label: 'Effect Size' },
        { name: 'confidenceInterval', label: 'CI' },
        { name: 'pValue', label: 'p-value' }
      ],
      papers: [],
      codedPapers: [],
      currentPage: 1,
      totalPages: 1,
      totalDataPoints: 0,
      codingSheet: null
    }
  },
  mounted() {
    // Fetch data
    this.fetchResults();
  },
  methods: {
    async fetchResults() {
      this.loading = true;
      this.error = null;
      
      try {
        if (!this.projectId) {
          this.papers = [];
          this.totalDataPoints = 0;
          this.loading = false;
          return;
        }
        
        // First, get the project details and coding sheet
        await this.loadCodingSheet();
        
        // Get all papers in the project
        const papersResponse = await fetch(API_ROUTES.PROJECTS.GET_PAPERS(this.projectId));
        if (!papersResponse.ok) {
          throw new Error('Failed to load papers for this project');
        }
        
        const papers = await papersResponse.json();
        this.papers = papers;
        
        // Now get coding data for all papers
        await this.loadCodingData();
        
        // Count data points
        this.calculateTotalDataPoints();
        this.loading = false;
      } catch (err) {
        console.error('Error fetching results:', err);
        this.error = 'Failed to load results. Please try again: ' + err.message;
        this.loading = false;
      }
    },
    
    async loadCodingSheet() {
      try {
        const response = await fetch(API_ROUTES.CODING.GET_BY_PROJECT_ID(this.projectId));
        
        if (response.ok) {
          this.codingSheet = await response.json();
          console.log('Loaded coding sheet:', this.codingSheet);
          
          // Update columns based on coding sheet
          this.updateColumns();
        }
      } catch (err) {
        console.error('Error loading coding sheet:', err);
      }
    },
    
    updateColumns() {
      if (!this.codingSheet) return;
      
      // Start with default columns
      const defaultColumns = [
        { name: 'title', label: 'Title' },
        { name: 'authors', label: 'Authors' }
      ];
      
      // Add columns based on coding sheet fields
      const codingColumns = [];
      
      this.codingSheet.sections.forEach(section => {
        section.fields.forEach(field => {
          codingColumns.push({
            name: field.name,
            label: field.label,
            type: field.type,
            section: section.name
          });
        });
      });
      
      this.columns = [...defaultColumns, ...codingColumns];
    },
    
    async loadCodingData() {
      // Initialize coded papers array
      this.codedPapers = [];
      
      // For each paper, try to get its coding data
      const codingPromises = this.papers.map(async (paper) => {
        try {
          const response = await fetch(API_ROUTES.CODING.GET_FOR_PAPER(paper.id));
          
          if (response.ok) {
            const codingData = await response.json();
            
            // Combine paper metadata with coding data
            return {
              ...paper,
              coding: codingData.data || {}
            };
          }
          
          // If no coding data, just return paper as is
          return paper;
        } catch (err) {
          console.warn(`Error loading coding for paper ${paper.id}:`, err);
          return paper;
        }
      });
      
      // Wait for all coding data to be fetched
      this.codedPapers = await Promise.all(codingPromises);
    },
    
    calculateTotalDataPoints() {
      let total = 0;
      
      this.codedPapers.forEach(paper => {
        if (paper.coding) {
          // Count each field that has a value
          total += Object.values(paper.coding).filter(value => {
            return value !== null && value !== undefined && value !== '';
          }).length;
        }
      });
      
      this.totalDataPoints = total;
    },
    
    getCellValue(paper, column) {
      if (column === 'title') {
        return paper.title || 'Unknown';
      }
      
      if (column === 'authors') {
        if (paper.authors && Array.isArray(paper.authors)) {
          if (paper.authors.length <= 3) {
            return paper.authors.map(a => a.name || a).join(', ');
          } else {
            return `${paper.authors[0].name || paper.authors[0]}, et al.`;
          }
        }
        return paper.authors || 'Unknown';
      }
      
      if (column === 'journal') {
        return paper.journal || 'N/A';
      }
      
      if (column === 'year') {
        if (paper.publication_date) {
          return new Date(paper.publication_date).getFullYear();
        }
        return paper.year || 'N/A';
      }
      
      // Check if it's a coding data field
      if (paper.coding && paper.coding.hasOwnProperty(column)) {
        return paper.coding[column] || 'N/A';
      }
      
      // Default fallback
      return paper[column] || 'N/A';
    },
    
    editPaper(paper) {
      // Navigate to coding view for this paper
      this.$emit('select-paper', paper, this.projectId);
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
