<template>
  <div class="p-6">
    <!-- Announcement Banner -->
    <div class="bg-indigo-50 border border-indigo-200 text-indigo-700 p-4 rounded-lg mb-6">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2h-1V9z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium">New Search Engine!</h3>
          <div class="text-sm">
            We've upgraded our search to use OpenAlex, providing better results and faster performance. <a href="https://openalex.org/" target="_blank" class="font-medium underline">Learn more</a>
          </div>
        </div>
        <div class="ml-auto pl-3">
          <button @click="$el.querySelector('.bg-indigo-50').style.display = 'none'" class="inline-flex text-indigo-500 focus:outline-none">
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>
    <!-- CSV Upload Modal -->
    <div v-if="showCsvUploadModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 w-1/2 max-w-xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">Upload Papers from CSV</h2>
          <button @click="showCsvUploadModal = false" class="text-gray-500 hover:text-gray-700">
            <font-awesome-icon icon="times" />
          </button>
        </div>
        <p class="mb-4 text-gray-600">Upload a CSV file containing paper details. The file must include columns for <strong>title</strong>, <strong>authors</strong>, and <strong>year</strong>.</p>
        
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">Select CSV File</label>
          <input 
            type="file" 
            ref="csvFileInput"
            accept=".csv"
            class="block w-full text-gray-700 border border-gray-300 rounded py-2 px-3"
          />
        </div>
        
        <div class="flex justify-end">
          <button 
            @click="showCsvUploadModal = false" 
            class="mr-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >Cancel</button>
          <button 
            @click="uploadCsvFile" 
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            :disabled="csvUploading"
          >
            {{ csvUploading ? 'Uploading...' : 'Upload & Process' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- DOI Lookup Modal -->
    <div v-if="showDoiLookupModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 w-1/2 max-w-xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">Paper DOI Lookup</h2>
          <button @click="showDoiLookupModal = false" class="text-gray-500 hover:text-gray-700">
            <font-awesome-icon icon="times" />
          </button>
        </div>
        <p class="mb-4 text-gray-600">Enter paper details to find its DOI.</p>
        
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">Paper Title</label>
          <input 
            v-model="doiLookup.title"
            type="text" 
            placeholder="Enter paper title"
            class="block w-full text-gray-700 border border-gray-300 rounded py-2 px-3"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">First Author</label>
          <input 
            v-model="doiLookup.author"
            type="text" 
            placeholder="Enter first author (last name or full name)"
            class="block w-full text-gray-700 border border-gray-300 rounded py-2 px-3"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">Publication Year</label>
          <input 
            v-model="doiLookup.year"
            type="number" 
            placeholder="Enter publication year"
            class="block w-full text-gray-700 border border-gray-300 rounded py-2 px-3"
          />
        </div>
        
        <div v-if="doiLookupResult" class="mb-4 p-4 rounded" :class="doiLookupResult.status === 'success' ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'">
          <div v-if="doiLookupResult.status === 'success'">
            <p class="text-green-700 font-medium">DOI Found!</p>
            <p class="text-gray-700">{{ doiLookupResult.doi }}</p>
            <p v-if="doiLookupResult.pdf_url" class="mt-2">
              <a :href="doiLookupResult.pdf_url" target="_blank" class="text-indigo-600 hover:text-indigo-800">
                <font-awesome-icon icon="download" class="mr-1" /> Download PDF
              </a>
            </p>
          </div>
          <div v-else>
            <p class="text-red-700 font-medium">DOI Not Found</p>
            <p class="text-gray-700">{{ doiLookupResult.message }}</p>
          </div>
        </div>
        
        <div class="flex justify-end">
          <button 
            @click="showDoiLookupModal = false" 
            class="mr-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >Close</button>
          <button 
            @click="lookupDoi" 
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            :disabled="doiLookupLoading || !doiLookup.title || !doiLookup.author || !doiLookup.year"
          >
            {{ doiLookupLoading ? 'Searching...' : 'Find DOI' }}
          </button>
        </div>
      </div>
    </div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Find Papers</h1>
      <div>
        <button 
          @click="showDoiLookupModal = true"
          class="mr-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          <font-awesome-icon icon="search" class="mr-1" /> DOI Lookup
        </button>
        <button 
          @click="showCsvUploadModal = true"
          class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          <font-awesome-icon icon="file-upload" class="mr-1" /> Upload CSV
        </button>
      </div>
    </div>
    
    <div class="bg-white rounded-lg p-6 shadow mb-6">
      <div class="flex mb-4">
        <div class="relative flex-1 mr-4">
          <font-awesome-icon icon="search" class="absolute left-3 top-3 text-gray-400" />
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Search by title, author, keywords..."
            class="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            @keyup.enter="searchPapers"
          />
        </div>
        <button 
          class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
          @click="searchPapers"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Searching...' : 'Search' }}
        </button>
      </div>
      
      <div class="flex flex-wrap -mx-2">
        <div class="px-2 w-1/4">
          <div class="mb-2 text-sm font-medium">Database</div>
          <select 
            v-model="filters.database"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            disabled
          >
            <option value="openalex">OpenAlex</option>
          </select>
        </div>
        <div class="px-2 w-1/4">
          <div class="mb-2 text-sm font-medium">Year Range</div>
          <div class="flex">
            <input 
              v-model="filters.yearFrom"
              type="number" 
              placeholder="From"
              class="w-1/2 mr-2 border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
            <input 
              v-model="filters.yearTo"
              type="number" 
              placeholder="To" 
              class="w-1/2 border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
        </div>
        <div class="px-2 w-1/4">
          <div class="mb-2 text-sm font-medium">Study Type</div>
          <select 
            v-model="filters.studyType"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          >
            <option value="">All Types</option>
            <option value="rct">RCT</option>
            <option value="cohort">Cohort</option>
            <option value="case-control">Case Control</option>
            <option value="meta-analysis">Meta-Analysis</option>
          </select>
        </div>
        <div class="px-2 w-1/4">
          <div class="mb-2 text-sm font-medium">Sort By</div>
          <select 
            v-model="filters.sortBy"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          >
            <option value="relevance">Relevance</option>
            <option value="date">Most Recent</option>
            <option value="cited">Most Cited</option>
            <option value="title">Title (A-Z)</option>
          </select>
        </div>
      </div>
      
      <div class="flex justify-end mt-4">
        <button 
          class="flex items-center text-indigo-600 mr-4 hover:text-indigo-800"
          @click="showMoreFilters = !showMoreFilters"
        >
          <font-awesome-icon :icon="showMoreFilters ? 'minus' : 'plus'" class="mr-1" /> 
          {{ showMoreFilters ? 'Fewer Filters' : 'More Filters' }}
        </button>
        <button 
          class="flex items-center text-gray-600 hover:text-gray-800"
          @click="clearFilters"
        >
          Clear All
        </button>
      </div>
      
      <div v-if="showMoreFilters" class="mt-4 pt-4 border-t">
        <div class="flex flex-wrap -mx-2">
          <div class="px-2 w-1/3 mb-4">
            <div class="mb-2 text-sm font-medium">Journal</div>
            <input 
              v-model="filters.journal"
              type="text" 
              placeholder="Journal name..."
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div class="px-2 w-1/3 mb-4">
            <div class="mb-2 text-sm font-medium">Author</div>
            <input 
              v-model="filters.author"
              type="text" 
              placeholder="Author name..."
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div class="px-2 w-1/3 mb-4">
            <div class="mb-2 text-sm font-medium">Open Access Only</div>
            <div class="pt-2">
              <label class="inline-flex items-center">
                <input 
                  v-model="filters.openAccessOnly" 
                  type="checkbox" 
                  class="form-checkbox h-5 w-5 text-indigo-600"
                >
                <span class="ml-2 text-gray-700">Show only Open Access papers</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="isLoading" class="text-center py-12">
      <div class="spinner mb-4"></div>
      <p class="text-gray-500">Searching for papers in OpenAlex...</p>
    </div>
    
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-6">
      <h3 class="font-medium mb-1">Error searching for papers</h3>
      <p>{{ error }}</p>
    </div>
    
    <div v-else-if="results.length > 0" class="bg-white rounded-lg shadow">
      <div class="p-4 border-b flex justify-between items-center">
        <div class="flex items-center">
          <label class="inline-flex items-center mr-4">
            <input 
              type="checkbox" 
              class="form-checkbox h-5 w-5 text-indigo-600"
              :checked="allSelected"
              @change="toggleSelectAll"
            >
            <span class="ml-2 text-gray-700">Select All</span>
          </label>
          <div class="font-medium">{{ totalResults }} Results</div>
          <button 
            v-if="selectedPapers.length > 0"
            class="ml-4 px-3 py-1 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
            @click="addSelectedToCollection"
          >
            Add {{ selectedPapers.length }} Selected Papers to Collection
          </button>
        </div>
        <div class="flex items-center text-sm">
          <span>Page {{ currentPage }} of {{ totalPages }}</span>
          <button 
            class="ml-4 px-2 py-1 border rounded-md hover:bg-gray-50"
            :disabled="currentPage === 1"
            @click="prevPage"
          >Previous</button>
          <button 
            class="ml-2 px-2 py-1 border rounded-md hover:bg-gray-50"
            :disabled="currentPage === totalPages"
            @click="nextPage"
          >Next</button>
        </div>
      </div>
      
      <div>
        <div 
          v-for="paper in results" 
          :key="paper.id || paper.doi || paper.title"
          class="p-4 border-b hover:bg-gray-50"
          style="min-height: 200px; display: flex;"
        >
          <div class="flex w-full">
            <div class="mr-3 pt-1">
              <input 
                type="checkbox"
                class="form-checkbox h-5 w-5 text-indigo-600"
                :checked="isSelected(paper)"
                @change="toggleSelection(paper)"
                @click.stop
              >
            </div>
            <div class="flex-1 cursor-pointer flex flex-col justify-between" @click="viewPaper(paper)">
              <div>
                <div class="font-medium text-indigo-600 mb-1 line-clamp-2 text-lg" style="max-height: 3rem; overflow: hidden;">
                  {{ paper.title }}
                </div>
                <div class="text-sm text-gray-700 mb-1 line-clamp-1">
                  {{ formatAuthors(paper.authors) }}
                </div>
                <div class="text-sm text-gray-500 mb-2 flex items-center">
                  <span class="truncate max-w-xs">{{ paper.journal || 'Unknown Journal' }}</span>
                  <span class="mx-1">•</span>
                  <span>{{ getYear(paper.publication_date) }}</span>
                  <span v-if="paper.citation_count" class="ml-2 text-xs font-medium">
                    <span class="px-2 py-0.5 bg-blue-100 text-blue-800 rounded-full">{{ paper.citation_count }} citations</span>
                  </span>
                  <span v-if="paper.source" class="ml-2 px-2 py-0.5 bg-gray-100 rounded-full text-xs">{{ paper.source }}</span>
                </div>
                <div class="text-sm text-gray-600 mb-3 line-clamp-3" style="max-height: 4.5rem; overflow: hidden;">
                  {{ paper.abstract }}
                </div>
              </div>
              <div class="flex mt-2 text-sm">
                <button 
                  v-if="paper.doi" 
                  class="flex items-center text-indigo-600 mr-4 hover:text-indigo-800"
                  @click.stop="downloadPdf(paper)"
                >
                  <font-awesome-icon icon="download" class="mr-1" /> Get PDF
                </button>
                <button 
                  class="flex items-center text-indigo-600 mr-4 hover:text-indigo-800"
                  @click.stop="addToCollection(paper)"
                >
                  <font-awesome-icon icon="plus-circle" class="mr-1" /> Add to Collection
                </button>
                <button 
                  class="flex items-center text-indigo-600 hover:text-indigo-800"
                  @click.stop="viewDetails(paper)"
                >
                  <font-awesome-icon icon="book" class="mr-1" /> View Details
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="results.length === 0" class="p-8 text-center">
        <p class="text-gray-500">No results found. Try adjusting your search criteria.</p>
      </div>
    </div>
    
    <!-- Collection Select Modal -->
    <CollectionSelectModal
      :show="showCollectionModal"
      :paper="selectedPaperForCollection"
      @close="showCollectionModal = false"
      @paper-added="handlePaperAdded"
    />
  </div>
</template>

<script>
import CollectionSelectModal from './CollectionSelectModal.vue';
import { API_ROUTES, APP_CONFIG } from '../config.js';

export default {
  name: 'PaperSearch',
  components: {
    CollectionSelectModal
  },
  data() {
    return {
      searchQuery: '',
      filters: {
        database: 'openalex',
        yearFrom: null,
        yearTo: null,
        studyType: '',
        sortBy: 'relevance',
        journal: '',
        author: '',
        openAccessOnly: false,
        providers: ['openalex']
      },
      selectedPapers: [],
      allSelected: false,
      showMoreFilters: false,
      isLoading: false,
      error: null,
      results: [],
      totalResults: 0,
      currentPage: 1,
      totalPages: 1,
      itemsPerPage: APP_CONFIG.ITEMS_PER_PAGE,
      showCollectionModal: false,
      selectedPaperForCollection: null,
      
      // Caching for local pagination
      cachedResults: null,
      cachedTotalResults: 0,
      cachedMetadata: null,
      
      // CSV Upload Modal
      showCsvUploadModal: false,
      csvUploading: false,
      csvResults: [],
      
      // DOI Lookup Modal
      showDoiLookupModal: false,
      doiLookup: {
        title: '',
        author: '',
        year: null
      },
      doiLookupLoading: false,
      doiLookupResult: null
    }
  },
  methods: {
    isSelected(paper) {
      return this.selectedPapers.some(p => this.isSamePaper(p, paper));
    },
    
    isSamePaper(paper1, paper2) {
      // Compare by DOI if available
      if (paper1.doi && paper2.doi) {
        return paper1.doi === paper2.doi;
      }
      // Otherwise compare by title
      return paper1.title === paper2.title;
    },
    
    toggleSelection(paper) {
      if (this.isSelected(paper)) {
        this.selectedPapers = this.selectedPapers.filter(p => !this.isSamePaper(p, paper));
      } else {
        this.selectedPapers.push(paper);
      }
      this.updateAllSelected();
    },
    
    toggleSelectAll() {
      if (this.allSelected) {
        this.selectedPapers = [];
      } else {
        this.selectedPapers = [...this.results];
      }
      this.allSelected = !this.allSelected;
    },
    
    updateAllSelected() {
      this.allSelected = this.results.length > 0 && 
        this.results.every(paper => this.isSelected(paper));
    },
    
    addSelectedToCollection() {
      if (this.selectedPapers.length === 0) {
        return;
      }
      
      // Show the collection modal with multiple papers
      this.selectedPaperForCollection = this.selectedPapers;
      this.showCollectionModal = true;
    },
    
    async uploadCsvFile() {
      const fileInput = this.$refs.csvFileInput;
      if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
        alert('Please select a CSV file to upload');
        return;
      }
      
      const file = fileInput.files[0];
      if (!file.name.endsWith('.csv')) {
        alert('Please select a CSV file');
        return;
      }
      
      this.csvUploading = true;
      
      try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${API_ROUTES.PAPERS.BATCH_FIND_DOI}`, {
          method: 'POST',
          body: formData,
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Error processing CSV file');
        }
        
        const data = await response.json();
        this.csvResults = data;
        
        // Show summary
        const doisFound = data.filter(item => item.doi && item.doi !== 'Not found').length;
        const total = data.length;
        
        alert(`Processed ${total} papers. Found DOIs for ${doisFound} papers (${Math.round(doisFound/total*100)}%)`);
        
        // Close modal after success
        this.showCsvUploadModal = false;
      } catch (err) {
        alert(`Error: ${err.message}`);
        console.error('Error uploading CSV:', err);
      } finally {
        this.csvUploading = false;
      }
    },
    
    async lookupDoi() {
      if (!this.doiLookup.title || !this.doiLookup.author || !this.doiLookup.year) {
        return;
      }
      
      this.doiLookupLoading = true;
      this.doiLookupResult = null;
      
      try {
        const formData = new FormData();
        formData.append('title', this.doiLookup.title);
        formData.append('author', this.doiLookup.author);
        formData.append('year', this.doiLookup.year);
        
        const response = await fetch(`${API_ROUTES.PAPERS.FIND_DOI}`, {
          method: 'POST',
          body: formData,
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Error finding DOI');
        }
        
        this.doiLookupResult = await response.json();
      } catch (err) {
        this.doiLookupResult = {
          status: 'error',
          message: `Error: ${err.message}`
        };
        console.error('Error looking up DOI:', err);
      } finally {
        this.doiLookupLoading = false;
      }
    },
    
    async searchPapers() {
      if (!this.searchQuery.trim()) return;
      
      this.isLoading = true;
      this.error = null;
      
      try {
        // Build query parameters for enhanced results
        const params = new URLSearchParams();
        params.append('query', this.searchQuery);
        params.append('limit', "100");
        params.append('offset', "0");
        params.append('client_pagination', "true");
        
        // Add filters if provided
        if (this.filters.yearFrom) params.append('year_from', this.filters.yearFrom.toString());
        if (this.filters.yearTo) params.append('year_to', this.filters.yearTo.toString());
        if (this.filters.journal) params.append('journal', this.filters.journal);
        if (this.filters.author) params.append('author', this.filters.author);
        if (this.filters.openAccessOnly) params.append('open_access_only', 'true');
        
        // Add sort parameter
        params.append('sort_by', this.filters.sortBy);
        
        // Use simple search endpoint
        const endpoint = API_ROUTES.PAPERS.SIMPLE_SEARCH;
        
        const response = await fetch(`${endpoint}?query=${encodeURIComponent(this.searchQuery)}&limit=100`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          let errorDetail = 'Failed to search papers';
          try {
            const errorData = await response.json();
            if (errorData.detail) {
              errorDetail = errorData.detail;
            }
          } catch (e) {
            console.error('Error parsing error response:', e);
          }
          throw new Error(errorDetail);
        }
        
        const data = await response.json();
        // Store all results in cached results for local pagination
        this.cachedResults = data.results || [];
        this.cachedTotalResults = data.totalResults || data.results.length;
        this.cachedMetadata = data.metadata;
          
        // Process results to have uniform appearance
        this.cachedResults = this.processResultsForUniformAppearance(data.results || []);
        this.cachedTotalResults = data.totalResults || this.cachedResults.length;
        
        // Handle pagination locally
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        this.results = this.cachedResults.slice(startIndex, endIndex);
        this.totalResults = this.cachedTotalResults;
        this.totalPages = Math.ceil(this.totalResults / this.itemsPerPage);
        
        // Reset selection
        this.selectedPapers = [];
        this.allSelected = false;
        
        // Store search metadata if available
        if (this.cachedMetadata) {
          console.log('Search metadata:', this.cachedMetadata);
        }
      } catch (err) {
        this.error = err.message;
        console.error('Error searching papers:', err);
      } finally {
        this.isLoading = false;
      }
    },
    
    formatAuthors(authors) {
      if (!authors || authors.length === 0) return 'Unknown Authors';
      
      // Handle different author formats from various providers
      const getAuthorName = (author) => {
        if (typeof author === 'string') return author;
        if (typeof author === 'object' && author !== null) {
          if (author.name) return author.name;
          // Handle possible alternative formats
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
    
    clearFilters() {
      this.filters = {
        database: 'openalex',
        yearFrom: null,
        yearTo: null,
        studyType: '',
        sortBy: 'relevance',
        journal: '',
        author: '',
        openAccessOnly: false,
        providers: ['openalex']
      };
      
      // Clear cached results when filters are reset
      this.cachedResults = null;
      this.cachedTotalResults = 0;
      this.cachedMetadata = null;
      
      // Reset pagination
      this.currentPage = 1;
      
      // If there was a search query, perform a new search with cleared filters
      if (this.searchQuery.trim()) {
        this.searchPapers();
      }
    },
    
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.updateLocalPagination();
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.updateLocalPagination();
      }
    },
    
    updateLocalPagination() {
      if (this.cachedResults && this.cachedResults.length > 0) {
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        this.results = this.cachedResults.slice(startIndex, endIndex);
        
        // Reset selection when changing pages
        this.selectedPapers = [];
        this.allSelected = false;
        
        // Scroll to top of results
        window.scrollTo({
          top: document.querySelector('.bg-white.rounded-lg.shadow').offsetTop - 20,
          behavior: 'smooth'
        });
      }
    },
    
    viewPaper(paper) {
      // Navigate to PDF viewer with the selected paper
      this.$emit('select-paper', paper);
    },
    
    async downloadPdf(paper) {
      this.isLoading = true;
      try {
        // Always fetch the PDF URL from the backend when requested
        // This ensures we're not using stale data and only fetch when needed
        if (paper.doi) {
          const response = await fetch(`${API_ROUTES.PAPERS.GET_PDF}/${encodeURIComponent(paper.doi)}`);
          if (response.ok) {
            const data = await response.json();
            if (data.pdf_url) {
              window.open(data.pdf_url, '_blank');
              this.isLoading = false;
              return;
            }
          }
          // If backend request failed but we have a cached URL, try that
          if (paper.open_access_url) {
            window.open(paper.open_access_url, '_blank');
            this.isLoading = false;
            return;
          }
          
          throw new Error('Could not retrieve PDF URL');
        } else if (paper.open_access_url) {
          // If we somehow already have a URL but no DOI
          window.open(paper.open_access_url, '_blank');
          this.isLoading = false;
          return;
        } else {
          throw new Error('No DOI or PDF URL available');
        }
      } catch (err) {
        console.error('Error fetching PDF URL:', err);
        alert('The PDF could not be retrieved. It may not be publicly accessible.');
      } finally {
        this.isLoading = false;
      }
    },
    
    addToCollection(paper) {
      this.selectedPaperForCollection = paper;
      this.showCollectionModal = true;
    },
    
    handlePaperAdded({ papers, collectionId }) {
      const count = Array.isArray(papers) ? papers.length : 1;
      // Show success message
      alert(`${count} paper${count > 1 ? 's' : ''} added to collection successfully`);
      
      // Clear selections if multiple papers were added
      if (count > 1) {
        this.selectedPapers = [];
        this.allSelected = false;
      }
    },
    
    viewDetails(paper) {
      // View paper details (implement later)
      console.log('View details:', paper);
    },
    
    processResultsForUniformAppearance(results) {
      // Process each result to have uniform appearance
      const ABSTRACT_LENGTH = 300; // Max length for abstracts
      
      return results.map(paper => {
        // Truncate abstract to consistent length
        let abstract = paper.abstract || 'No abstract available';
        if (abstract.length > ABSTRACT_LENGTH) {
          abstract = abstract.substring(0, ABSTRACT_LENGTH) + '...';
        }
        
        // Ensure all papers have same structure
        return {
          ...paper,
          abstract: abstract,
          // Ensure other fields exist
          authors: paper.authors || [],
          journal: paper.journal || 'Unknown Journal',
          publication_date: paper.publication_date || 'Unknown Date',
          doi: paper.doi || null,
          url: paper.url || null,
          citation_count: paper.citation_count || 0,
          source: paper.source || 'Unknown Source'
        };
      });
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