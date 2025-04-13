<template>
  <div class="bg-white p-3 rounded border">
    <div class="flex justify-between items-center mb-2">
      <div class="font-medium flex items-center">
        <FileText class="mr-2 text-gray-500" size="16" />
        {{ item.name }}
      </div>
      <div class="flex items-center">
        <span class="text-sm text-gray-500 mr-2">{{ formatFileSize(item.size) }}</span>
        <button v-if="item.status !== 'complete'" 
          class="text-gray-400 hover:text-gray-600"
          @click="$emit('remove')"
        >
          <X size="16" />
        </button>
        <CheckCircle v-else class="text-green-500" size="16" />
      </div>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2.5">
      <div 
        class="h-2.5 rounded-full" 
        :class="getProgressBarClass()"
        :style="{ width: `${item.progress}%` }"
      ></div>
    </div>
    <div class="flex justify-between items-center text-xs mt-1">
      <div :class="item.status === 'error' ? 'text-red-500' : 'text-gray-500'">
        {{ getStatusText() }}
      </div>
      <div v-if="item.status === 'complete' && item.paper" class="text-indigo-600">
        <a href="#" @click.prevent="viewPaper">View</a>
      </div>
    </div>
    <div v-if="item.status === 'error'" class="mt-1 text-xs text-red-500">
      {{ item.error || 'Upload failed' }}
    </div>
  </div>
</template>

<script>
import { X, CheckCircle, FileText } from 'lucide-vue-next';

export default {
  name: 'UploadItem',
  components: {
    X,
    CheckCircle,
    FileText
  },
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(1024));
      return parseFloat((bytes / Math.pow(1024, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    getStatusText() {
      switch (this.item.status) {
        case 'queued':
          return 'Queued';
        case 'uploading':
          return `Uploading... ${this.item.progress}%`;
        case 'extracting':
          return 'Extracting metadata...';
        case 'complete':
          return 'Upload complete';
        case 'error':
          return 'Error';
        default:
          return this.item.status;
      }
    },
    
    getProgressBarClass() {
      if (this.item.status === 'complete') {
        return 'bg-green-500';
      } else if (this.item.status === 'error') {
        return 'bg-red-500';
      } else {
        return 'bg-indigo-600';
      }
    },
    
    viewPaper() {
      if (this.item.paper) {
        this.$emit('view-paper', this.item.paper);
      }
    }
  }
};
</script>
