<template>
  <div class="p-6">
    <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6">
      <div class="mx-auto w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
        <UploadCloud class="text-indigo-600" size="32" />
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
        @dragover.prevent
        @drop.prevent="handleDrop"
      >
        Select Files
      </button>
    </div>

    <div class="bg-gray-50 rounded-lg p-4 mb-6">
      <h3 class="font-medium mb-2">Upload Queue ({{ uploadQueue.length || 3 }})</h3>
      <div class="space-y-3">
        <UploadItem 
          v-for="(item, index) in uploadQueue.length ? uploadQueue : mockUploadItems" 
          :key="index"
          :item="item"
          @remove="$emit('remove-from-queue', index)"
        />
      </div>
    </div>

    <div>
      <h3 class="font-medium mb-2">Extraction Options</h3>
      <div class="space-y-3">
        <div class="flex items-center">
          <input 
            :checked="extractionOptions.extractMetadata"
            @change="updateExtractionOption('extractMetadata', $event.target.checked)"
            type="checkbox" 
            id="extract-metadata"
            class="mr-2"
          />
          <label for="extract-metadata">Automatically extract metadata (title, authors, journal, etc.)</label>
        </div>
        <div class="flex items-center">
          <input 
            :checked="extractionOptions.applyCodingSheet"
            @change="updateExtractionOption('applyCodingSheet', $event.target.checked)"
            type="checkbox" 
            id="apply-coding"
            class="mr-2"
          />
          <label for="apply-coding">Apply coding sheet for automated data extraction</label>
        </div>
        <div class="flex items-center">
          <input 
            :checked="extractionOptions.addToProject"
            @change="updateExtractionOption('addToProject', $event.target.checked)"
            type="checkbox" 
            id="add-project"
            class="mr-2"
          />
          <label for="add-project">Add to current project</label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UploadItem from './upload-item.vue';
import { UploadCloud } from 'lucide-vue-next';

export default {
  name: 'UploadTab',
  components: {
    UploadItem,
    UploadCloud
  },
  data() {
    return {
      mockUploadItems: [
        {
          name: "Smith_et_al_2023_CBT_Meta_Analysis.pdf",
          size: 2.4 * 1024 * 1024, // 2.4 MB
          progress: 100,
          status: "complete"
        },
        {
          name: "Garcia_et_al_2022_Remote_Work.pdf",
          size: 1.8 * 1024 * 1024, // 1.8 MB
          progress: 65,
          status: "uploading"
        },
        {
          name: "Chen_et_al_2022_Vaccines.pdf",
          size: 3.2 * 1024 * 1024, // 3.2 MB
          progress: 0,
          status: "queued"
        }
      ]
    };
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
