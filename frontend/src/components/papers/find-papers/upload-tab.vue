<template>
  <div>
    <!-- Upload Drop Zone -->
    <div 
      class="border-2 border-dashed border-gray-300 rounded-lg p-10 text-center mb-6 hover:bg-gray-50 transition-colors"
      @dragover.prevent
      @drop.prevent="handleDrop"
      @click="openFileDialog"
    >
      <div class="flex flex-col items-center">
        <div 
          class="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mb-4"
        >
          <font-awesome-icon icon="upload" class="text-indigo-600 text-2xl" />
        </div>
        <h3 class="text-lg font-medium mb-2">Drop PDF files here</h3>
        <p class="text-gray-500 mb-4">or click to browse your computer</p>
        <input 
          ref="fileInput"
          type="file" 
          multiple
          accept=".pdf"
          class="hidden"
          @change="handleFileSelection"
        />
        <button 
          class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
          @click.stop="openFileDialog"
        >
          Select Files
        </button>
      </div>
    </div>

    <!-- Upload Queue -->
    <div v-if="uploadQueue.length > 0" class="mb-8">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-medium">Upload Queue ({{ uploadQueue.length }})</h3>
        <button 
          v-if="hasQueuedFiles"
          class="px-3 py-1.5 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 flex items-center"
          @click="$emit('process-uploads')"
        >
          <font-awesome-icon icon="upload" class="mr-1.5" /> Upload Files
        </button>
      </div>

      <div class="divide-y border rounded-lg bg-white">
        <UploadItem 
          v-for="(item, index) in uploadQueue" 
          :key="index"
          :item="item"
          @remove="$emit('remove-from-queue', index)"
        />
      </div>
    </div>

    <!-- Extraction Options -->
    <div class="bg-white p-6 rounded-lg border mb-6">
      <h3 class="text-lg font-medium mb-4">Extraction Options</h3>
      
      <div class="space-y-4">
        <div>
          <label class="flex items-center">
            <input 
              :checked="extractionOptions.extractMetadata"
              @change="updateExtractionOption('extractMetadata', $event.target.checked)"
              type="checkbox" 
              class="form-checkbox h-5 w-5 text-indigo-600"
            />
            <span class="ml-2 text-gray-700">Automatically extract metadata (title, authors, journal, etc.)</span>
          </label>
        </div>
        
        <div>
          <label class="flex items-center">
            <input 
              :checked="extractionOptions.applyCodingSheet"
              @change="updateExtractionOption('applyCodingSheet', $event.target.checked)"
              type="checkbox" 
              class="form-checkbox h-5 w-5 text-indigo-600"
            />
            <span class="ml-2 text-gray-700">Apply coding sheet for automated data extraction</span>
          </label>
        </div>
        
        <div>
          <label class="flex items-center">
            <input 
              :checked="extractionOptions.addToProject"
              @change="updateExtractionOption('addToProject', $event.target.checked)"
              type="checkbox" 
              class="form-checkbox h-5 w-5 text-indigo-600"
            />
            <span class="ml-2 text-gray-700">Add to current project</span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UploadItem from './upload-item.vue';

export default {
  name: 'UploadTab',
  components: {
    UploadItem
  },
  props: {
    uploadQueue: {
      type: Array,
      default: () => []
    },
    extractionOptions: {
      type: Object,
      default: () => ({
        extractMetadata: true,
        applyCodingSheet: false,
        addToProject: false
      })
    }
  },
  computed: {
    hasQueuedFiles() {
      return this.uploadQueue.some(item => item.status === 'queued');
    }
  },
  methods: {
    openFileDialog() {
      this.$refs.fileInput.click();
    },
    
    handleFileSelection(event) {
      if (event.target.files && event.target.files.length > 0) {
        this.$emit('upload-files', event.target.files);
        // Reset the input so the same file can be selected again
        event.target.value = '';
      }
    },
    
    handleDrop(event) {
      const files = Array.from(event.dataTransfer.files).filter(file => 
        file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
      );
      
      if (files.length > 0) {
        this.$emit('upload-files', files);
      }
    },
    
    updateExtractionOption(key, value) {
      const newOptions = { ...this.extractionOptions };
      newOptions[key] = value;
      this.$emit('update:extractionOptions', newOptions);
    }
  }
};
</script>
