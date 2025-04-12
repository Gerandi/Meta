<template>
  <div class="bg-white p-3 rounded border">
    <div class="flex justify-between items-center mb-2">
      <div class="font-medium">{{ item.name }}</div>
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
        :class="item.status === 'complete' ? 'bg-green-500' : 'bg-indigo-600'"
        :style="{ width: `${item.progress}%` }"
      ></div>
    </div>
    <div class="text-xs text-gray-500 mt-1">
      {{ item.status === 'complete' ? 'Complete' : item.status === 'uploading' ? `Uploading... ${item.progress}%` : 'Queued' }}
    </div>
  </div>
</template>

<script>
import { X, CheckCircle } from 'lucide-vue-next';

export default {
  name: 'UploadItem',
  components: {
    X,
    CheckCircle
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
        case 'complete':
          return 'Complete';
        case 'error':
          return 'Error';
        default:
          return this.item.status;
      }
    }
  }
};
</script>
