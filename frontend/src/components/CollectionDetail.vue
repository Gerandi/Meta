<template>
  <div class="p-6">
    <div class="flex items-center mb-6">
      <button 
        class="text-indigo-600 hover:text-indigo-800 mr-4"
        @click="goBackToCollections"
      >
        <font-awesome-icon icon="arrow-left" class="mr-1" /> Back to Collections
      </button>
      <h1 class="text-2xl font-bold flex-grow">{{ collection.name }}</h1>
      <button 
        class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
        @click="showEditModal = true"
      >
        <font-awesome-icon icon="edit" class="mr-1" /> Edit
      </button>
    </div>
    
    <div v-if="collection.description" class="bg-gray-50 p-4 rounded-lg mb-6">
      <p class="text-gray-700">{{ collection.description }}</p>
    </div>
    
    <div v-if="isLoading" class="text-center py-12">
      <div class="spinner mb-4"></div>
      <p class="text-gray-500">Loading papers...</p>
    </div>
    
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-6">
      <h3 class="font-medium mb-1">Error loading papers</h3>
      <p>{{ error }}</p>
    </div>
    
    <div v-else-if="papers.length === 0" class="bg-white rounded-lg p-8 text-center shadow">
      <font-awesome-icon icon="file-alt" class="text-gray-400 text-5xl mb-4" />
      <h3 class="text-xl font-medium mb-2">No Papers in This Collection</h3>
      <p class="text-gray-600 mb-4">Add papers by searching and selecting "Add to Collection".</p>
      <button 
        class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
        @click="goToSearch"
      >
        Find Papers
      </button>
    </div>
    
    <div v-else class="bg-white rounded-lg shadow">
      <div class="p-4 border-b flex justify-between items-center">
        <div class="font-medium">{{ papers.length }} {{ papers.length === 1 ? 'Paper' : 'Papers' }}</div>
        <div class="flex items-center">
          <button 
            class="text-indigo-600 mr-4 hover:text-indigo-800"
            @click="exportPapers"
          >
            <font-awesome-icon icon="download" class="mr-1" /> Export
          </button>
        </div>
      </div>
      
      <div>
        <div 
          v-for="paper in papers" 
          :key="paper.id"
          class="p-4 border-b hover:bg-gray-50"
        >
          <div class="flex justify-between">
            <div class="flex-grow">
              <div class="font-medium text-indigo-600 mb-1">{{ paper.title }}</div>
              <div class="text-sm text-gray-700 mb-1">
                {{ formatAuthors(paper.authors) }}
              </div>
              <div class="text-sm text-gray-500 mb-2">
                {{ paper.journal }} • {{ getYear(paper.publication_date) }}
              </div>
              <div class="text-sm text-gray-600">
                {{ paper.abstract ? (paper.abstract.substring(0, 200) + '...') : 'No abstract available' }}
              </div>
            </div>
            <div class="ml-4 flex flex-col justify-between">
              <button 
                class="text-red-600 hover:text-red-800"
                @click="confirmRemove(paper)"
              >
                <font-awesome-icon icon="times" />
              </button>
              <button 
                class="mt-auto text-indigo-600 hover:text-indigo-800"
                @click="viewPaper(paper)"
              >
                View
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Edit Collection Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">Edit Collection</h2>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
          <input 
            v-model="editForm.name"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Collection name"
          />
        </div>
        
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">Description (optional)</label>
          <textarea 
            v-model="editForm.description"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Brief description of this collection"
            rows="3"
          ></textarea>
        </div>
        
        <div class="flex justify-end">
          <button 
            class="text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 mr-2"
            @click="showEditModal = false"
          >
            Cancel
          </button>
          <button 
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
            @click="updateCollection"
            :disabled="!editForm.name"
          >
            Update
          </button>
        </div>
      </div>
    </div>
    
    <!-- Remove Paper Confirmation Modal -->
    <div v-if="showRemoveModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">Remove Paper</h2>
        <p class="mb-6">Are you sure you want to remove this paper from the collection? The paper will remain in the database but will no longer be part of this collection.</p>
        
        <div class="flex justify-end">
          <button 
            class="text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 mr-2"
            @click="showRemoveModal = false"
          >
            Cancel
          </button>
          <button 
            class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
            @click="removePaper"
          >
            Remove
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { API_ROUTES } from '../config.js';

export default {
  name: 'CollectionDetail',
  props: {
    collectionId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      collection: {
        id: null,
        name: '',
        description: ''
      },
      papers: [],
      isLoading: false,
      error: null,
      showEditModal: false,
      showRemoveModal: false,
      editForm: {
        name: '',
        description: ''
      },
      paperToRemove: null
    }
  },
  mounted() {
    this.fetchCollection();
    this.fetchPapers();
  },
  methods: {
    async fetchCollection() {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await fetch(API_ROUTES.COLLECTIONS.GET_BY_ID(this.collectionId));
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to load collection');
        }
        
        this.collection = await response.json();
        this.editForm.name = this.collection.name;
        this.editForm.description = this.collection.description || '';
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching collection:', err);
      } finally {
        this.isLoading = false;
      }
    },
    
    async fetchPapers() {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await fetch(API_ROUTES.COLLECTIONS.GET_PAPERS(this.collectionId));
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to load papers');
        }
        
        this.papers = await response.json();
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching papers:', err);
      } finally {
        this.isLoading = false;
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
      return new Date(dateString).getFullYear();
    },
    
    goBackToCollections() {
      this.$emit('change-view', 'collections');
    },
    
    goToSearch() {
      this.$emit('change-view', 'search');
    },
    
    viewPaper(paper) {
      this.$emit('select-paper', paper);
    },
    
    confirmRemove(paper) {
      this.paperToRemove = paper;
      this.showRemoveModal = true;
    },
    
    async removePaper() {
      try {
        const response = await fetch(API_ROUTES.COLLECTIONS.REMOVE_PAPER(this.collectionId, this.paperToRemove.id), {
          method: 'DELETE'
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to remove paper from collection');
        }
        
        // Remove paper from the list
        this.papers = this.papers.filter(p => p.id !== this.paperToRemove.id);
        
        // Close modal
        this.showRemoveModal = false;
        this.paperToRemove = null;
      } catch (err) {
        console.error('Error removing paper:', err);
        alert('Error: ' + err.message);
      }
    },
    
    async updateCollection() {
      try {
        const response = await fetch(API_ROUTES.COLLECTIONS.GET_BY_ID(this.collectionId), {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.editForm)
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to update collection');
        }
        
        // Update local collection data
        this.collection.name = this.editForm.name;
        this.collection.description = this.editForm.description;
        
        // Close modal
        this.showEditModal = false;
      } catch (err) {
        console.error('Error updating collection:', err);
        alert('Error: ' + err.message);
      }
    },
    
    exportPapers() {
      // Prepare data for export
      const data = this.papers.map(paper => {
        return {
          title: paper.title,
          authors: this.formatAuthors(paper.authors),
          journal: paper.journal,
          year: this.getYear(paper.publication_date),
          doi: paper.doi,
          url: paper.url
        };
      });
      
      // Convert to CSV
      const headers = Object.keys(data[0]);
      const csvRows = [];
      
      // Add headers
      csvRows.push(headers.join(','));
      
      // Add rows
      for (const row of data) {
        const values = headers.map(header => {
          const val = row[header];
          return `"${val}"`; // Wrap in quotes to handle commas in values
        });
        csvRows.push(values.join(','));
      }
      
      const csvString = csvRows.join('\n');
      
      // Create download link
      const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `${this.collection.name.replace(/\s+/g, '_')}_papers.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
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
