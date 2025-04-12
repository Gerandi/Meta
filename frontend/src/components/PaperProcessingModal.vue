<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-xl">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">
          {{ isMultiplePapers ? `Process ${papers.length} Papers` : 'Process Paper' }}
        </h2>
        <button 
          class="text-gray-500 hover:text-gray-700"
          @click="closeModal"
        >
          <X size="18" />
        </button>
      </div>
      
      <div class="mb-4">
        <div class="mb-2 text-sm font-medium text-gray-700">Selected Papers</div>
        <div class="max-h-60 overflow-y-auto border rounded-lg divide-y mb-4">
          <div 
            v-for="(paper, index) in papers" 
            :key="index"
            class="p-3 hover:bg-gray-50"
          >
            <div class="font-medium">{{ paper.title }}</div>
            <div v-if="paper.authors && paper.authors.length" class="text-sm text-gray-500 mt-1">
              {{ formatAuthors(paper.authors) }}
            </div>
            <div class="text-xs text-gray-400 mt-1">
              {{ paper.journal }} {{ paper.publication_date ? `(${getYear(paper.publication_date)})` : '' }}
            </div>
          </div>
        </div>
      </div>
      
      <div class="mb-6 border-t pt-4">
        <h3 class="text-lg font-medium mb-4">Processing Options</h3>
        
        <div class="mb-4">
          <label class="flex items-center text-sm font-medium text-gray-700 mb-1">
            <input 
              type="checkbox"
              v-model="processingOptions.extractKeywords"
              class="form-checkbox h-4 w-4 text-indigo-600 mr-2"
            />
            Extract Keywords
          </label>
        </div>
        
        <div class="mb-4">
          <label class="flex items-center text-sm font-medium text-gray-700 mb-1">
            <input 
              type="checkbox"
              v-model="processingOptions.summarize"
              class="form-checkbox h-4 w-4 text-indigo-600 mr-2"
            />
            Generate Summary
          </label>
        </div>
        
        <div class="mb-4">
          <label class="flex items-center text-sm font-medium text-gray-700 mb-1">
            <input 
              type="checkbox"
              v-model="processingOptions.extractData"
              class="form-checkbox h-4 w-4 text-indigo-600 mr-2"
            />
            Extract Data Tables
          </label>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Analysis Type</label>
          <select 
            v-model="processingOptions.analysisType"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          >
            <option value="basic">Basic Analysis</option>
            <option value="statistical">Statistical Analysis</option>
            <option value="qualitative">Qualitative Analysis</option>
            <option value="comprehensive">Comprehensive Analysis</option>
          </select>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Processing Name (optional)</label>
          <input 
            v-model="processingName"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Enter a name for this processing batch"
          />
        </div>
      </div>
      
      <div class="flex justify-end">
        <button 
          class="text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 mr-2"
          @click="closeModal"
        >
          Cancel
        </button>
        <button 
          class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
          @click="processPapers"
          :disabled="isProcessing"
        >
          {{ isProcessing ? 'Processing...' : 'Process' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { X } from 'lucide-vue-next';

export default {
  name: 'PaperProcessingModal',
  components: {
    X
  },
  props: {
    show: {
      type: Boolean,
      required: true
    },
    papers: {
      type: Array,
      required: true
    },
    isMultiplePapers: {
      type: Boolean,
      required: true
    },
    processingOptions: {
      type: Object,
      required: true
    },
    processingName: {
      type: String,
      default: ''
    },
    isProcessing: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    processPapers() {
      this.$emit('confirm');
    },
    formatAuthors(authors) {
      return authors.join(', ');
    },
    getYear(date) {
      return new Date(date).getFullYear();
    }
  }
};
</script>