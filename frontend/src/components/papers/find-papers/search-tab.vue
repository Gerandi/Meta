<template>
  <div>
    <div class="p-6">
      <div class="flex mb-4">
        <div class="relative flex-1 mr-4">
          <Search class="absolute left-3 top-2.5 text-gray-400" size="18" />
          <input
            :value="searchQuery"
            @input="$emit('update:searchQuery', $event.target.value)"
            type="text"
            placeholder="Search by title, author, keywords..."
            class="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            @keyup.enter="$emit('search')"
          />
        </div>
        <button
          class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
          @click="$emit('search')"
          :disabled="isLoading"
        >
          <span v-if="isLoading">Searching...</span>
          <span v-else>Search</span>
        </button>
      </div>

      <div class="flex flex-wrap -mx-2 mb-4">
        <div class="px-2 w-1/3">
          <div class="mb-2 text-sm font-medium">Year Range</div>
          <div class="flex">
            <input
              :value="filters.yearFrom"
              @input="updateFilter('yearFrom', $event.target.value)"
              type="number"
              placeholder="From"
              class="w-1/2 mr-2 border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
            <input
              :value="filters.yearTo"
              @input="updateFilter('yearTo', $event.target.value)"
              type="number"
              placeholder="To"
              class="w-1/2 border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
        </div>
        <div class="px-2 w-1/3">
          <div class="mb-2 text-sm font-medium">Study Type</div>
          <select
            :value="filters.studyType"
            @input="updateFilter('studyType', $event.target.value)"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          >
            <option value="">All Types</option>
            <option value="rct">RCT</option>
            <option value="cohort">Cohort</option>
            <option value="case-control">Case Control</option>
            <option value="meta-analysis">Meta-Analysis</option>
          </select>
        </div>
        <div class="px-2 w-1/3">
          <div class="mb-2 text-sm font-medium">Sort By</div>
          <select
            :value="filters.sortBy"
            @input="updateFilter('sortBy', $event.target.value)"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          >
            <option value="relevance">Relevance</option>
            <option value="date">Most Recent</option>
            <option value="cited">Most Cited</option>
            <option value="title">Title (A-Z)</option>
          </select>
        </div>
      </div>

      <div class="flex justify-end">
        <button 
          class="flex items-center text-indigo-600 mr-4 hover:text-indigo-800"
          @click="$emit('toggle-more-filters')"
        >
          <FilterIcon class="mr-1" size="16" /> Advanced Filters
        </button>
        <button 
          class="flex items-center text-gray-600 hover:text-gray-800"
          @click="$emit('clear-filters')"
        >
          Reset
        </button>
      </div>

      <!-- Advanced filters section remains hidden but filter toggle button shows -->
      <div v-if="showMoreFilters" class="mt-4 pt-4 border-t">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <div class="mb-2 text-sm font-medium text-gray-700">Journal</div>
            <input
              :value="filters.journal"
              @input="updateFilter('journal', $event.target.value)"
              type="text"
              placeholder="Journal name..."
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div>
            <div class="mb-2 text-sm font-medium text-gray-700">Author</div>
            <input
              :value="filters.author"
              @input="updateFilter('author', $event.target.value)"
              type="text"
              placeholder="Author name..."
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div>
            <div class="mb-2 text-sm font-medium text-gray-700">Open Access Only</div>
            <div class="pt-2">
              <label class="inline-flex items-center">
                <input
                  :checked="filters.openAccessOnly"
                  @change="updateFilter('openAccessOnly', $event.target.checked)"
                  type="checkbox"
                  class="form-checkbox h-5 w-5 text-indigo-600 rounded border-gray-300"
                />
                <span class="ml-2 text-gray-700">Show only Open Access papers</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="border-t">
      <div class="p-4 bg-gray-50 border-b flex justify-between items-center">
        <div class="font-medium">{{ totalResults }} Results</div>
        <div class="flex items-center text-sm">
          <span>Page {{ currentPage }} of {{ totalPages }}</span>
          <button 
            class="ml-4 px-2 py-1 border rounded-md hover:bg-gray-100"
            :disabled="currentPage === 1"
            @click="$emit('prev-page')"
          >Previous</button>
          <button 
            class="ml-2 px-2 py-1 border rounded-md hover:bg-gray-100"
            :disabled="currentPage === totalPages"
            @click="$emit('next-page')"
          >Next</button>
        </div>
      </div>

      <div>
        <!-- Loading state -->
        <div v-if="isLoading" class="text-center py-12">
          <div class="spinner mb-4"></div>
          <p class="text-gray-500">Searching for papers...</p>
        </div>

        <!-- Error message -->
        <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-4 m-4">
          <h3 class="font-medium mb-1 flex items-center">
            <AlertCircle class="mr-2" size="18" />
            Error searching for papers
          </h3>
          <p>{{ error }}</p>
        </div>

        <!-- Results list -->
        <div v-else>
          <div v-for="paper in results" :key="paper.id || paper.doi || paper.title">
            <SearchResultItem
              :paper="paper"
              :selected="isSelected(paper)"
              @toggle-selection="$emit('toggle-selection', paper)"
              @view="$emit('view-paper', paper)"
              @download="$emit('download-pdf', paper)"
              @add-to-project="$emit('add-to-project', paper)"
              @view-details="$emit('view-details', paper)"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Empty results -->
    <div v-if="results.length === 0 && !isLoading && !error" class="p-8 text-center">
      <Search class="text-gray-300 mx-auto mb-3" size="40" />
      <p class="text-gray-500">No results found. Try adjusting your search criteria.</p>
    </div>
  </div>
</template>

<script>
import SearchResultItem from './search-result-item.vue';
import { Search, AlertCircle, Filter as FilterIcon } from 'lucide-vue-next';

export default {
  name: 'SearchTab',
  components: {
    SearchResultItem,
    Search,
    AlertCircle,
    FilterIcon
  },
  data() {
    return {
      searchUpdateTimeout: null
    };
  },
  props: {
    isLoading: {
      type: Boolean,
      default: false
    },
    searchQuery: {
      type: String,
      default: ''
    },
    filters: {
      type: Object,
      required: true
    },
    showMoreFilters: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: null
    },
    results: {
      type: Array,
      default: () => []
    },
    totalResults: {
      type: Number,
      default: 0
    },
    currentPage: {
      type: Number,
      default: 1
    },
    totalPages: {
      type: Number,
      default: 1
    },
    selectedPapers: {
      type: Array,
      default: () => []
    },
    allSelected: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    updateFilter(key, value) {
      // Make sure to update filters in parent component
      console.log(`Updating filter ${key} to:`, value);
      const newFilters = { ...this.filters };
      newFilters[key] = value;
      this.$emit('update:filters', newFilters);
      
      // Perform search with new filters after a short delay
      if (this.searchUpdateTimeout) {
        clearTimeout(this.searchUpdateTimeout);
      }
      
      this.searchUpdateTimeout = setTimeout(() => {
        console.log('Searching with updated filters');
        this.$emit('search');
      }, 800); // 800ms delay to avoid too many API calls
    },
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
