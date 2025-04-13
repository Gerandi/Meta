<template>
  <div class="p-6">
    <div 
      class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6"
      @dragover.prevent
      @drop.prevent="handleDrop"
    >
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
      >
        Select Files
      </button>
    </div>

    <div v-if="uploadQueue.length > 0" class="bg-gray-50 rounded-lg p-4 mb-6">
      <h3 class="font-medium mb-2">Upload Queue ({{ uploadQueue.length }})</h3>
      <div class="space-y-3">
        <UploadItem 
          v-for="(item, index) in uploadQueue" 
          :key="index"
          :item="item"
          @remove="$emit('remove-from-queue', index)"
          @view-paper="$emit('paper-imported', item.paper)"
        />
      </div>
      
      <div class="mt-4 flex justify-end">
        <button 
          class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          @click="uploadFiles"
          :disabled="!hasQueuedFiles || uploading"
        >
          <span v-if="uploading">Uploading...</span>
          <span v-else>Upload Files</span>
        </button>
      </div>
    </div>

    <div>
      <h3 class="font-medium mb-2">Project Options</h3>
      <div class="space-y-3">
        <div class="flex items-center">
          <input 
            :checked="projectOption"
            @change="updateOption('projectOption', $event.target.checked)"
            type="checkbox" 
            id="add-project"
            class="mr-2"
          />
          <label for="add-project">Add to current project</label>
        </div>
        
        <div v-if="projectOption" class="pl-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Select Project
          </label>
          <select 
            v-model="selectedProjectId"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          >
            <option value="">-- Select a Project --</option>
            <option v-for="project in projects" :key="project.id" :value="project.id">
              {{ project.name }}
            </option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UploadItem from './upload-item.vue';
import { UploadCloud } from 'lucide-vue-next';
import { API_ROUTES } from '../../../config.js';

export default {
  name: 'UploadTab',
  components: {
    UploadItem,
    UploadCloud
  },
  data() {
    return {
      uploadQueue: [],
      uploading: false,
      projectOption: false,
      selectedProjectId: '',
      projects: []
    };
  },
  computed: {
    hasQueuedFiles() {
      return this.uploadQueue.some(item => item.status === 'queued');
    }
  },
  mounted() {
    this.fetchProjects();
  },
  methods: {
    openFileDialog() {
      this.$refs.fileInput.click();
    },
    
    handleFileSelection(event) {
      if (event.target.files && event.target.files.length > 0) {
        this.addFilesToQueue(Array.from(event.target.files));
        // Reset the input so the same file can be selected again
        event.target.value = '';
      }
    },
    
    handleDrop(event) {
      const files = Array.from(event.dataTransfer.files).filter(file => 
        file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
      );
      
      if (files.length > 0) {
        this.addFilesToQueue(files);
      }
    },
    
    addFilesToQueue(files) {
      const newQueue = [...this.uploadQueue];
      
      files.forEach(file => {
        newQueue.push({
          file,
          name: file.name,
          size: file.size,
          progress: 0,
          status: 'queued'
        });
      });
      
      this.uploadQueue = newQueue;
    },
    
    updateOption(key, value) {
      this[key] = value;
    },
    
    async fetchProjects() {
      try {
        const response = await fetch(API_ROUTES.PROJECTS.LIST);
        if (response.ok) {
          this.projects = await response.json();
        }
      } catch (error) {
        console.error('Error fetching projects:', error);
      }
    },
    
    async uploadFiles() {
      this.uploading = true;
      
      for (let i = 0; i < this.uploadQueue.length; i++) {
        const item = this.uploadQueue[i];
        if (item.status === 'queued') {
          try {
            // Update status to uploading - Using Vue 3 direct reactivity (no $set needed)
            this.uploadQueue[i] = { ...item, status: 'uploading' };
            
            // Create form data
            const formData = new FormData();
            formData.append('file', item.file);
            
            // Add project ID if selected
            if (this.projectOption && this.selectedProjectId) {
              formData.append('project_id', this.selectedProjectId);
            }
            
            // Upload using the backend endpoint directly
            const uploadUrl = API_ROUTES.PAPERS.UPLOAD;
            
            // Use XMLHttpRequest for progress tracking
            await new Promise((resolve, reject) => {
              const xhr = new XMLHttpRequest();
              
              xhr.upload.addEventListener('progress', (event) => {
                if (event.lengthComputable) {
                  const percentComplete = Math.round((event.loaded / event.total) * 100);
                  // Use Vue 3 direct reactivity (no $set needed)
                  this.uploadQueue[i] = { ...this.uploadQueue[i], progress: percentComplete };
                }
              });
              
              xhr.addEventListener('load', () => {
                if (xhr.status >= 200 && xhr.status < 300) {
                  try {
                    const response = JSON.parse(xhr.responseText);
                    // Store paper data in item - Use Vue 3 direct reactivity
                    this.uploadQueue[i] = {
                      ...this.uploadQueue[i],
                      status: 'complete',
                      progress: 100,
                      paper: response
                    };
                    resolve(response);
                  } catch (e) {
                    reject(new Error('Invalid response format'));
                  }
                } else {
                  reject(new Error(`Upload failed: ${xhr.statusText}`));
                }
              });
              
              xhr.addEventListener('error', () => {
                reject(new Error('Network error during upload'));
              });
              
              xhr.open('POST', uploadUrl);
              xhr.send(formData);
            });
            
            // Emit event for successful upload
            this.$emit('paper-imported', this.uploadQueue[i].paper);
            
          } catch (error) {
            console.error(`Error uploading ${item.name}:`, error);
            // Use Vue 3 direct reactivity (no $set needed)
            this.uploadQueue[i] = {
              ...this.uploadQueue[i],
              status: 'error',
              error: error.message
            };
          }
        }
      }
      
      this.uploading = false;
      
      // Check if all uploads completed successfully
      const allComplete = this.uploadQueue.every(item => item.status === 'complete');
      if (allComplete) {
        // Clear the queue after a delay to show completion
        setTimeout(() => {
          this.uploadQueue = [];
        }, 2000);
      }
    }
  }
};
</script>
