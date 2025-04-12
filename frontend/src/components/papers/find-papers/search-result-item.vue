<template>
  <div class="p-4 border-b hover:bg-gray-50">
    <div class="flex justify-between">
      <div class="font-medium text-indigo-600 mb-1">{{ paper.title }}</div>
      <div class="flex items-center">
        <div class="text-xs px-2 py-1 rounded-full mr-2" :class="paper.open_access ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'">
          {{ paper.open_access ? 'Open Access' : 'Subscription' }}
        </div>
        <div class="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600 flex items-center">
          <font-awesome-icon icon="database" class="mr-1" size="xs" />
          {{ paper.source || 'Unknown' }}
        </div>
      </div>
    </div>
    <div class="text-sm text-gray-700 mb-1">{{ formatAuthors(paper.authors) }}</div>
    <div class="text-sm text-gray-500 mb-2">{{ paper.journal || 'Unknown Journal' }} • {{ getYear(paper.publication_date) }}</div>
    <div class="text-sm text-gray-600 mb-3">{{ paper.abstract || 'No abstract available for this paper.' }}</div>
    <div class="flex">
      <button 
        v-if="paper.doi || paper.open_access_url" 
        class="flex items-center text-indigo-600 mr-4 hover:text-indigo-800"
        @click.stop="$emit('download')"
      >
        <font-awesome-icon icon="download" class="mr-1" /> Download PDF
      </button>
      <button 
        class="flex items-center text-indigo-600 mr-4 hover:text-indigo-800"
        @click.stop="$emit('add-to-project')"
      >
        <font-awesome-icon icon="plus-circle" class="mr-1" /> Import
      </button>
      <button 
        class="flex items-center text-indigo-600 hover:text-indigo-800"
        @click.stop="$emit('view-details')"
      >
        <font-awesome-icon icon="book" class="mr-1" /> View Details
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchResultItem',
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
      if (!authors || authors.length === 0) return 'Unknown Authors';
      
      // Handle different author formats from various providers
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
    
    getYear(dateString) {
      if (!dateString) return 'Unknown Year';
      
      // Handle different date formats
      try {
        // Try to parse as ISO date
        const year = new Date(dateString).getFullYear();
        if (!isNaN(year)) return year;
        
        // Check if the string itself is just a year
        if (/^\d{4}$/.test(dateString)) return dateString;
        
        // Try to extract year from a date string
        const yearMatch = dateString.match(/\b(19|20)\d{2}\b/);
        if (yearMatch) return yearMatch[0];
      } catch (err) {
        console.warn('Error parsing date:', dateString, err);
      }
      
      return 'Unknown Year';
    }
  }
};
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
