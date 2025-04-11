<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
      <h2 class="text-xl font-bold mb-4">
        {{ isMultiplePapers ? `Add ${papers.length} Papers to Collection` : 'Add to Collection' }}
      </h2>
      
      <div v-if="collections.length === 0" class="mb-4 p-4 bg-gray-50 rounded text-center">
        <p class="text-gray-500 mb-2">You don't have any collections yet.</p>
        <button 
          class="text-indigo-600 hover:text-indigo-800 font-medium"
          @click="createNewCollection"
        >
          Create a new collection
        </button>
      </div>
      
      <div v-else class="mb-6">
        <div class="mb-2 text-sm font-medium text-gray-700">Select a collection</div>
        <div class="max-h-60 overflow-y-auto border rounded-lg divide-y">
          <div 
            v-for="collection in collections" 
            :key="collection.id"
            class="p-3 hover:bg-gray-50 cursor-pointer"
            @click="selectedCollectionId = collection.id"
          >
            <div class="flex items-center">
              <div class="mr-2">
                <input 
                  type="radio" 
                  :checked="selectedCollectionId === collection.id"
                  class="form-radio h-4 w-4 text-indigo-600"
                />
              </div>
              <div>
                <div class="font-medium">{{ collection.name }}</div>
                <div v-if="collection.description" class="text-sm text-gray-500">
                  {{ collection.description }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="showCreateForm" class="mb-6 border-t pt-4">
        <h3 class="text-lg font-medium mb-2">Create New Collection</h3>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
          <input 
            v-model="newCollection.name"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Collection name"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Description (optional)</label>
          <textarea 
            v-model="newCollection.description"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Brief description of this collection"
            rows="2"
          ></textarea>
        </div>
      </div>
      
      <div class="flex justify-between">
        <button 
          v-if="!showCreateForm && collections.length > 0"
          class="text-indigo-600 hover:text-indigo-800"
          @click="showCreateForm = true"
        >
          <font-awesome-icon icon="plus" class="mr-1" /> New Collection
        </button>
        <div v-else></div>
        
        <div>
          <button 
            class="text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 mr-2"
            @click="closeModal"
          >
            Cancel
          </button>
          <button 
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
            @click="addToCollection"
            :disabled="!isFormValid"
          >
            Add to Collection
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { API_ROUTES } from '../config.js';

export default {
  name: 'CollectionSelectModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    paper: {
      type: [Object, Array],
      default: null
    }
  },
  data() {
    return {
      collections: [],
      selectedCollectionId: null,
      showCreateForm: false,
      newCollection: {
        name: '',
        description: ''
      },
      isLoading: false,
      error: null
    }
  },
  computed: {
    isFormValid() {
      if (this.showCreateForm) {
        return this.newCollection.name.trim() !== '';
      } else {
        return this.selectedCollectionId !== null;
      }
    },
    isMultiplePapers() {
      return Array.isArray(this.paper) && this.paper.length > 1;
    },
    papers() {
      return Array.isArray(this.paper) ? this.paper : [this.paper];
    }
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.fetchCollections();
      }
    }
  },
  methods: {
    async fetchCollections() {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await fetch(API_ROUTES.COLLECTIONS.LIST);
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to load collections');
        }
        
        this.collections = await response.json();
        
        // If there are collections, select the first one by default
        if (this.collections.length > 0) {
          this.selectedCollectionId = this.collections[0].id;
        } else {
          // If no collections, show the create form
          this.showCreateForm = true;
        }
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching collections:', err);
      } finally {
        this.isLoading = false;
      }
    },
    
    createNewCollection() {
      this.showCreateForm = true;
    },
    
    async addToCollection() {
      try {
        let collectionId = this.selectedCollectionId;
        
        // If we're creating a new collection, do that first
        if (this.showCreateForm) {
          const createResponse = await fetch(API_ROUTES.COLLECTIONS.CREATE, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.newCollection)
          });
          
          if (!createResponse.ok) {
            const errorData = await createResponse.json();
            throw new Error(errorData.detail || 'Failed to create collection');
          }
          
          const createdCollection = await createResponse.json();
          collectionId = createdCollection.id;
        }
        
        // Process each paper
        for (const paper of this.papers) {
          // Skip if paper is null
          if (!paper) continue;
          
          // Save the paper
          const saveResponse = await fetch(API_ROUTES.PAPERS.CREATE, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(paper)
          });
          
          if (!saveResponse.ok) {
            const errorData = await saveResponse.json();
            throw new Error(errorData.detail || 'Failed to save paper');
          }
          
          const savedPaper = await saveResponse.json();
          
          // Add the paper to the collection
          const addResponse = await fetch(API_ROUTES.COLLECTIONS.ADD_PAPER(collectionId, savedPaper.id), {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            }
          });
          
          if (!addResponse.ok) {
            const errorData = await addResponse.json();
            throw new Error(errorData.detail || 'Failed to add paper to collection');
          }
        }
        
        // Close the modal and emit success event
        this.$emit('paper-added', {
          papers: this.papers,
          collectionId: collectionId
        });
        
        this.closeModal();
      } catch (err) {
        console.error('Error adding papers to collection:', err);
        alert('Error: ' + err.message);
      }
    },
    
    closeModal() {
      this.selectedCollectionId = null;
      this.showCreateForm = false;
      this.newCollection = { name: '', description: '' };
      this.$emit('close');
    }
  }
}
</script>
