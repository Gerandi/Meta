<template>
  <div class="bg-white rounded-lg shadow">
    <div class="p-4 border-b flex justify-between items-center">
      <div class="font-medium">Imported Papers ({{ papers.length || 0 }})</div>
      <div class="flex items-center">
        <button class="flex items-center px-3 py-2 text-sm border rounded-lg mr-2 hover:bg-gray-50">
          <Filter class="mr-1" size="16" /> Filter
        </button>
        <button 
          class="flex items-center px-3 py-2 text-sm border rounded-lg hover:bg-gray-50"
          @click="$emit('add-to-project')"
          :disabled="selectedPapers.length === 0"
          :class="{'opacity-50 cursor-not-allowed': selectedPapers.length === 0}"
        >
          <PlusCircle class="mr-1" size="16" /> Add to Project
        </button>
      </div>
    </div>

    <div class="divide-y">
      <div v-if="loading" class="text-center py-8">
        <div class="spinner mb-4"></div>
        <p class="text-gray-500">Loading papers...</p>
      </div>
      
      <template v-else>
        <ImportedPaperItem 
          v-for="paper in papers" 
          :key="paper.id" 
          :paper="paper"
          :selected="isSelected(paper.id)"
          @toggle-selection="toggleSelection(paper.id)"
          @view="$emit('view-paper', paper)"
          @download="$emit('download-pdf', paper)"
          @remove="$emit('remove-paper', paper.id)"
        />
        <div v-if="papers.length === 0" class="p-10 text-center text-gray-500 border-dashed border-gray-300">
          <FileText class="text-gray-300 mx-auto mb-3" size="40" />
          <p class="mb-2">No papers imported yet</p>
          <p class="text-sm">Use the tabs above to search databases or upload PDFs</p>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import ImportedPaperItem from './imported-paper-item.vue';
import { Filter, PlusCircle, FileText } from 'lucide-vue-next';

export default {
  name: 'ImportedPapersList',
  components: {
    ImportedPaperItem,
    Filter,
    PlusCircle,
    FileText
  },
  props: {
    papers: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      selectedPapers: []
    }
  },
  methods: {
    isSelected(paperId) {
      return this.selectedPapers.includes(paperId);
    },
    
    toggleSelection(paperId) {
      if (this.isSelected(paperId)) {
        this.selectedPapers = this.selectedPapers.filter(id => id !== paperId);
      } else {
        this.selectedPapers.push(paperId);
      }
      this.$emit('update:selected', this.selectedPapers);
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
