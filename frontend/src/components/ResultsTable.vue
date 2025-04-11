<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Results Table</h1>
      <div class="flex">
        <button class="flex items-center px-3 py-2 rounded-lg border bg-white mr-2 hover:bg-gray-50">
          <font-awesome-icon icon="filter" class="mr-1" /> Filter
        </button>
        <button class="flex items-center px-3 py-2 rounded-lg border bg-white hover:bg-gray-50">
          <font-awesome-icon icon="download" class="mr-1" /> Export
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
        <font-awesome-icon icon="table" size="4x" />
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
export default {
  name: 'ResultsTable',
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
      currentPage: 1,
      totalPages: 1,
      totalDataPoints: 0
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
        // Mock data for now
        setTimeout(() => {
          // For MVP, just show empty state
          this.papers = [];
          this.totalDataPoints = 0;
          this.loading = false;
        }, 1000);
      } catch (err) {
        console.error('Error fetching results:', err);
        this.error = 'Failed to load results. Please try again.';
        this.loading = false;
      }
    },
    
    getCellValue(paper, column) {
      switch (column) {
        case 'authors':
          return paper.authors || 'Unknown';
        case 'year':
          return paper.year || 'N/A';
        case 'journal':
          return paper.journal || 'N/A';
        // Add other column handling here
        default:
          return paper[column] || 'N/A';
      }
    },
    
    editPaper(paper) {
      // Navigate to coding view for this paper
      console.log('Edit paper:', paper);
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
