<template>
  <div 
    class="p-4 hover:bg-gray-50 flex items-center" 
    :class="{ 'bg-indigo-50': selected }"
  >
    <div class="mr-3">
      <input 
        type="checkbox" 
        class="form-checkbox h-5 w-5 text-indigo-600"
        :checked="selected"
        @change="$emit('toggle-selection')"
        @click.stop="$emit('toggle-selection')"
      />
    </div>
    <div class="flex-1">
      <h3 class="font-medium text-gray-900 mb-1">{{ paper.title || 'Unknown Title' }}</h3>
      <div class="text-sm text-gray-500 mb-1">{{ formatAuthors(paper.authors) }}</div>
      <div class="text-sm text-gray-600">
        {{ paper.journal || 'Unknown Journal' }} • {{ paper.year || 'Unknown Year' }}
      </div>
    </div>
    
    <div class="flex flex-col items-end ml-4">
      <div class="mb-2">
        <span 
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
          :class="getStatusClass(paper.status)"
        >
          {{ getStatusText(paper.status) }}
        </span>
      </div>
      <div class="flex">
        <button 
          class="text-indigo-600 hover:text-indigo-900 mr-3"
          @click="$emit('view')"
        >
          <font-awesome-icon icon="eye" />
        </button>
        <button 
          v-if="paper.doi || paper.pdf_url"
          class="text-indigo-600 hover:text-indigo-900 mr-3"
          @click="$emit('download')"
        >
          <font-awesome-icon icon="download" />
        </button>
        <button 
          class="text-red-600 hover:text-red-900"
          @click="$emit('remove')"
        >
          <font-awesome-icon icon="trash" />
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
