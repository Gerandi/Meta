<template>
  <div class="p-6">
    <div class="flex items-center mb-6">
      <button 
        class="text-indigo-600 hover:text-indigo-800 mr-4"
        @click="goBackToProjects"
      >
        <ArrowLeft class="mr-1" size="18" /> Back to Projects
      </button>
      <h1 class="text-2xl font-bold flex-grow">{{ project.name }}</h1>
      <div class="flex space-x-2">
        <button 
          class="flex items-center bg-white border text-indigo-600 px-4 py-2 rounded-lg hover:bg-indigo-50"
          @click="configureCodingSheet"
        >
          <ClipboardList class="mr-1" size="18" /> Configure Coding Sheet
        </button>
        <button 
          class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
          @click="showEditModal = true"
        >
          <Edit class="mr-1" size="18" /> Edit
        </button>
      </div>
    </div>
    
    <div v-if="project.description" class="bg-gray-50 p-4 rounded-lg mb-6">
      <p class="text-gray-700">{{ project.description }}</p>
    </div>
    
    <div v-if="isLoading" class="text-center py-12">
      <div class="spinner mb-4"></div>
      <p class="text-gray-500">Loading papers...</p>
    </div>
    
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-6">
      <h3 class="font-medium mb-1">Error loading papers</h3>
      <p>{{ error }}</p>
    </div>
    
    <div v-else-if="papers.length === 0" class="bg-white rounded-lg p-8 text-center shadow">
      <FileText class="text-gray-400 mx-auto" size="48" />
      <h3 class="text-xl font-medium mb-2">No Papers in This Project</h3>
      <p class="text-gray-600 mb-4">Add papers by searching and selecting "Add to Project".</p>
      <button 
        class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
        @click="goToSearch"
      >
        Find Papers
      </button>
    </div>
    
    <div v-else class="bg-white rounded-lg shadow">
      <div class="p-4 border-b flex justify-between items-center">
        <div class="font-medium">{{ papers.length }} {{ papers.length === 1 ? 'Paper' : 'Papers' }}</div>
        <div class="flex items-center">
          <button 
            class="text-indigo-600 mr-4 hover:text-indigo-800"
            @click="exportPapers"
          >
            <Download class="mr-1" size="18" /> Export
          </button>
        </div>
      </div>
      
      <div>
        <div 
          v-for="paper in papers" 
          :key="paper.id"
          class="p-4 border-b hover:bg-gray-50"
        >
          <div class="flex justify-between">
            <div class="flex-grow">
              <div class="font-medium text-indigo-600 mb-1">{{ paper.title }}</div>
              <div class="text-sm text-gray-700 mb-1">
                {{ formatAuthors(paper.authors) }}
              </div>
              <div class="text-sm text-gray-500 mb-2">
                {{ paper.journal }} • {{ getYear(paper.publication_date) }}
              </div>
              <div class="text-sm text-gray-600">
                {{ paper.abstract ? (paper.abstract.substring(0, 200) + '...') : 'No abstract available' }}
              </div>
            </div>
            <div class="ml-4 flex flex-col justify-between">
              <button 
                class="text-red-600 hover:text-red-800"
                @click="confirmRemove(paper)"
              >
                <X size="18" />
              </button>
              <button 
                class="mt-auto text-indigo-600 hover:text-indigo-800"
                @click="viewPaper(paper)"
              >
                View
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Edit Project Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">Edit Project</h2>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
          <input 
            v-model="editForm.name"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Project name"
          />
        </div>
        
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">Description (optional)</label>
          <textarea 
            v-model="editForm.description"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Brief description of this project"
            rows="3"
          ></textarea>
        </div>
        
        <div class="flex justify-end">
          <button 
            class="text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 mr-2"
            @click="showEditModal = false"
          >
            Cancel
          </button>
          <button 
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
            @click="updateProject"
            :disabled="!editForm.name"
          >
            Update
          </button>
        </div>
      </div>
    </div>
    
    <!-- Remove Paper Confirmation Modal -->
    <div v-if="showRemoveModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">Remove Paper</h2>
        <p class="mb-6">Are you sure you want to remove this paper from the project? The paper will remain in the database but will no longer be part of this project.</p>
        
        <div class="flex justify-end">
          <button 
            class="text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 mr-2"
            @click="showRemoveModal = false"
          >
            Cancel
          </button>
          <button 
            class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
            @click="removePaper"
          >
            Remove
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { API_ROUTES } from '../config.js';
import { ArrowLeft, ClipboardList, Edit, FileText, Download, X } from 'lucide-vue-next';
import { projectService, paperService } from '../services/api.js';

export default {
  name: 'ProjectDetail',
  components: {
    ArrowLeft,
    ClipboardList,
    Edit,
    FileText,
    Download,
    X
  },
  props: {
    projectId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      project: {
        id: null,
        name: '',
        description: '',
        codingSheet: null
      },
      papers: [],
      isLoading: false,
      error: null,
      showEditModal: false,
      showRemoveModal: false,
      editForm: {
        name: '',
        description: ''
      },
      paperToRemove: null
    }
  },
  mounted() {
    this.fetchProject();
    this.fetchPapers();
  },
  methods: {
    async fetchProject() {
      this.isLoading = true;
      this.error = null;
      
      try {
        // Use projectService instead of direct fetch
        this.project = await projectService.getProject(this.projectId);
        this.editForm.name = this.project.name;
        this.editForm.description = this.project.description || '';
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching project:', err);
      } finally {
        this.isLoading = false;
      }
    },
    
    async fetchPapers() {
      this.isLoading = true;
      this.error = null;
      
      try {
        // Use projectService instead of direct fetch
        this.papers = await projectService.getProjectPapers(this.projectId);
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching papers:', err);
      } finally {
        this.isLoading = false;
      }
    },
    
    formatAuthors(authors) {
      if (!authors || authors.length === 0) return 'Unknown Authors';
      
      if (authors.length <= 3) {
        return authors.map(a => a.name).join(', ');
      } else {
        return `${authors[0].name}, et al.`;
      }
    },
    
    getYear(dateString) {
      if (!dateString) return 'Unknown Year';
      return new Date(dateString).getFullYear();
    },
    
    goBackToProjects() {
      this.$emit('change-view', 'projects');
    },
    
    goToSearch() {
      this.$emit('change-view', 'search');
    },
    
    configureCodingSheet() {
      // Emit an event that will be caught by the parent component to navigate to the coding sheet configuration
      // Pass the project ID so we know which project's coding sheet to configure
      this.$emit('configure-coding-sheet', this.project.id);
    },
    
    viewPaper(paper) {
      this.$emit('select-paper', paper);
    },
    
    confirmRemove(paper) {
      this.paperToRemove = paper;
      this.showRemoveModal = true;
    },
    
    async removePaper() {
      try {
        // Use projectService instead of direct fetch
        await projectService.removePaperFromProject(this.projectId, this.paperToRemove.id);
        
        // Remove paper from the list
        this.papers = this.papers.filter(p => p.id !== this.paperToRemove.id);
        
        // Close modal
        this.showRemoveModal = false;
        this.paperToRemove = null;
      } catch (err) {
        console.error('Error removing paper:', err);
        alert('Error: ' + err.message);
      }
    },
    
    async updateProject() {
      try {
        // Use projectService instead of direct fetch
        await projectService.updateProject(this.projectId, this.editForm);
        
        // Update local project data
        this.project.name = this.editForm.name;
        this.project.description = this.editForm.description;
        
        // Close modal
        this.showEditModal = false;
      } catch (err) {
        console.error('Error updating project:', err);
        alert('Error: ' + err.message);
      }
    },
    
    exportPapers() {
      // Prepare data for export
      const data = this.papers.map(paper => {
        return {
          title: paper.title,
          authors: this.formatAuthors(paper.authors),
          journal: paper.journal,
          year: this.getYear(paper.publication_date),
          doi: paper.doi,
          url: paper.url
        };
      });
      
      // Convert to CSV
      const headers = Object.keys(data[0]);
      const csvRows = [];
      
      // Add headers
      csvRows.push(headers.join(','));
      
      // Add rows
      for (const row of data) {
        const values = headers.map(header => {
          const val = row[header];
          return `"${val}"`; // Wrap in quotes to handle commas in values
        });
        csvRows.push(values.join(','));
      }
      
      const csvString = csvRows.join('\n');
      
      // Create download link
      const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `${this.project.name.replace(/\s+/g, '_')}_papers.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
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
