<template>
  <div class="p-4 hover:bg-gray-50 flex justify-between">
    <div>
      <div class="font-medium text-indigo-600 mb-1">{{ paper.title || 'Unknown Title' }}</div>
      <div class="text-sm text-gray-700 mb-1">{{ formatAuthors(paper.authors) }}</div>
      <div class="text-sm text-gray-500">{{ paper.journal || 'Unknown Journal' }} • {{ paper.year || 'Unknown Year' }}</div>
    </div>
    <div class="flex items-center">
      <span 
        class="text-xs px-2 py-1 rounded-full"
        :class="paper.status === 'imported' || paper.status === 'complete' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'"
      >
        {{ paper.status === 'imported' || paper.status === 'complete' ? 'Imported' : 'Processing...' }}
      </span>
      <div class="ml-4 flex">
        <button 
          class="p-1 text-gray-400 hover:text-indigo-600 mr-1"
          @click="$emit('view')"
        >
          <font-awesome-icon icon="book" />
        </button>
        <button 
          class="p-1 text-gray-400 hover:text-red-600"
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
  name: 'ImportedPaperItem',
  props: {
    paper: {
      type: Object,
      required: true
    },
    selected: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    formatAuthors(authors) {
      if (!authors) return 'Unknown Authors';
      
      if (typeof authors === 'string') {
        return authors;
      }
      
      if (!Array.isArray(authors) || authors.length === 0) {
        return 'Unknown Authors';
      }
      
      // Handle different author formats
      const getAuthorName = (author) => {
        if (typeof author === 'string') return author;
        if (typeof author === 'object' && author !== null) {
          if (author.name) return author.name;
          if (author.firstName && author.lastName) return `${author.firstName} ${author.lastName}`;
          if (author.given && author.family) return `${author.given} ${author.family}`;
        }
        return 'Unknown';
      };
      
      if (authors.length <= 3) {
        return authors.map(getAuthorName).join(', ');
      } else {
        return `${getAuthorName(authors[0])}, et al.`;
      }
    },
    
    getStatusClass(status) {
      switch (status) {
        case 'imported':
        case 'complete':
          return 'bg-green-100 text-green-800';
        case 'processing':
          return 'bg-yellow-100 text-yellow-800';
        case 'error':
          return 'bg-red-100 text-red-800';
        default:
          return 'bg-gray-100 text-gray-800';
      }
    },
    
    getStatusIcon(status) {
      switch (status) {
        case 'imported':
        case 'complete':
          return 'check-circle';
        case 'processing':
          return 'spinner';
        case 'error':
          return 'exclamation-circle';
        default:
          return 'circle';
      }
    },
    
    getStatusText(status) {
      switch (status) {
        case 'imported':
        case 'complete':
          return 'Imported';
        case 'processing':
          return 'Processing...';
        case 'error':
          return 'Error';
        default:
          return status || 'Unknown';
      }
    }
  }
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
