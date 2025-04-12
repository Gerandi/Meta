<template>
  <div class="p-4 flex items-center hover:bg-gray-50">
    <div class="flex-1">
      <div class="flex justify-between items-center mb-2">
        <div class="font-medium flex items-center">
          <font-awesome-icon icon="file-pdf" class="text-red-500 mr-2" />
          {{ item.name }}
        </div>
        <div class="text-sm text-gray-500">{{ formatFileSize(item.size) }}</div>
      </div>
      
      <div v-if="item.status === 'uploading'" class="mb-1">
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div 
            class="h-2 rounded-full bg-indigo-600"
            :style="{ width: `${item.progress}%` }"
          ></div>
        </div>
      </div>
      
      <div class="flex justify-between items-center">
        <div class="text-sm">
          <span 
            :class="{
              'text-gray-500': item.status === 'queued',
              'text-indigo-600': item.status === 'uploading',
              'text-green-600': item.status === 'complete',
              'text-red-600': item.status === 'error'
            }"
          >
            {{ getStatusText() }}
          </span>
          <span v-if="item.error" class="text-red-600 ml-2">({{ item.error }})</span>
        </div>
        <button 
          v-if="item.status !== 'uploading'"
          class="text-gray-400 hover:text-red-600"
          @click="$emit('remove')"
        >
          <font-awesome-icon icon="times" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UploadItem',
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
