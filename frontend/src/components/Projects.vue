<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">My Projects</h1>
    
    <div class="mb-6">
      <button 
        class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
        @click="showCreateModal = true"
      >
        <font-awesome-icon icon="plus" class="mr-2" /> Create New Project
      </button>
    </div>
    
    <div v-if="isLoading" class="text-center py-12">
      <div class="spinner mb-4"></div>
      <p class="text-gray-500">Loading projects...</p>
    </div>
    
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-6">
      <h3 class="font-medium mb-1">Error loading projects</h3>
      <p>{{ error }}</p>
    </div>
    
    <div v-else-if="projects.length === 0" class="bg-white rounded-lg p-8 text-center shadow">
      <font-awesome-icon icon="folder-open" class="text-gray-400 text-5xl mb-4" />
      <h3 class="text-xl font-medium mb-2">No Projects Yet</h3>
      <p class="text-gray-600 mb-4">Create your first project to organize your papers.</p>
      <button 
        class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
        @click="showCreateModal = true"
      >
        Create Project
      </button>
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="project in projects" 
        :key="project.id"
        class="bg-white rounded-lg shadow overflow-hidden hover:shadow-md transition-shadow duration-200"
      >
        <div class="p-6">
          <div class="flex justify-between items-start">
            <h3 class="text-xl font-semibold mb-2">{{ project.name }}</h3>
            <div class="dropdown relative">
              <button class="text-gray-500 hover:text-gray-700">
                <font-awesome-icon icon="ellipsis-v" />
              </button>
              <div class="dropdown-menu hidden absolute right-0 mt-2 bg-white rounded-lg shadow-lg p-2 z-10">
                <button 
                  class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded"
                  @click="setActiveProject(project)"
                >
                  Set as Active
                </button>
                <button 
                  class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded"
                  @click="editProject(project)"
                >
                  Edit
                </button>
                <button 
                  class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100 rounded"
                  @click="confirmDelete(project)"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
          <p v-if="project.description" class="text-gray-600 mb-4">{{ project.description }}</p>
          <p v-else class="text-gray-500 italic mb-4">No description</p>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-500">
              {{ project.paper_count }} {{ project.paper_count === 1 ? 'paper' : 'papers' }}
            </span>
            <button 
              class="text-indigo-600 hover:text-indigo-800"
              @click="viewProject(project)"
            >
              View Project →
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">
          {{ showEditModal ? 'Edit Project' : 'Create New Project' }}
        </h2>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
          <input 
            v-model="formData.name"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Project name"
          />
        </div>
        
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">Description (optional)</label>
          <textarea 
            v-model="formData.description"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Brief description of this project"
            rows="3"
          ></textarea>
        </div>
        
        <div class="flex justify-end">
          <button 
            class="text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 mr-2"
            @click="closeModal"
          >
            Cancel
          </button>
          <button 
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
            @click="saveProject"
            :disabled="!formData.name"
          >
            {{ showEditModal ? 'Update' : 'Create' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">Confirm Deletion</h2>
        <p class="mb-6">Are you sure you want to delete the project "{{ projectToDelete?.name }}"? This action cannot be undone.</p>
        
        <div class="flex justify-end">
          <button 
            class="text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 mr-2"
            @click="showDeleteModal = false"
          >
            Cancel
          </button>
          <button 
            class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
            @click="deleteProject"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { API_ROUTES } from '../config.js';

export default {
  name: 'Projects',
  data() {
    return {
      projects: [],
      isLoading: false,
      error: null,
      showCreateModal: false,
      showEditModal: false,
      showDeleteModal: false,
      formData: {
        name: '',
        description: ''
      },
      editingProjectId: null,
      projectToDelete: null
    }
  },
  mounted() {
    this.fetchProjects();
    
    // Add click handler for dropdown menus
    document.addEventListener('click', (e) => {
      const dropdowns = document.querySelectorAll('.dropdown');
      dropdowns.forEach(dropdown => {
        if (!dropdown.contains(e.target)) {
          const menu = dropdown.querySelector('.dropdown-menu');
          if (menu) menu.classList.add('hidden');
        }
      });
    });
  },
  methods: {
    async fetchProjects() {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await fetch(API_ROUTES.PROJECTS.LIST);
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to load projects');
        }
        
        this.projects = await response.json();
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching projects:', err);
      } finally {
        this.isLoading = false;
      }
    },
    
    toggleDropdown(event) {
      const menu = event.currentTarget.nextElementSibling;
      menu.classList.toggle('hidden');
    },
    
    viewProject(project) {
      this.$emit('view-project', project.id);
    },
    
    setActiveProject(project) {
      // Store the selected project in localStorage and emit an event
      localStorage.setItem('activeProjectId', project.id);
      localStorage.setItem('activeProjectName', project.name);
      this.$emit('set-active-project', project);
    },
    
    editProject(project) {
      this.formData.name = project.name;
      this.formData.description = project.description || '';
      this.editingProjectId = project.id;
      this.showEditModal = true;
    },
    
    confirmDelete(project) {
      this.projectToDelete = project;
      this.showDeleteModal = true;
    },
    
    closeModal() {
      this.showCreateModal = false;
      this.showEditModal = false;
      this.formData = { name: '', description: '' };
      this.editingProjectId = null;
    },
    
    async saveProject() {
      try {
        let url = API_ROUTES.PROJECTS.CREATE;
        let method = 'POST';
        
        if (this.showEditModal) {
          url = API_ROUTES.PROJECTS.GET_BY_ID(this.editingProjectId);
          method = 'PUT';
        }
        
        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.formData)
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to save project');
        }
        
        // Refresh projects list
        await this.fetchProjects();
        
        // Close modal
        this.closeModal();
      } catch (err) {
        console.error('Error saving project:', err);
        alert('Error: ' + err.message);
      }
    },
    
    async deleteProject() {
      try {
        const response = await fetch(API_ROUTES.PROJECTS.GET_BY_ID(this.projectToDelete.id), {
          method: 'DELETE'
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to delete project');
        }
        
        // If this was the active project, clear it
        const activeProjectId = localStorage.getItem('activeProjectId');
        if (activeProjectId && parseInt(activeProjectId) === this.projectToDelete.id) {
          localStorage.removeItem('activeProjectId');
          localStorage.removeItem('activeProjectName');
          this.$emit('clear-active-project');
        }
        
        // Refresh projects list
        await this.fetchProjects();
        
        // Close modal
        this.showDeleteModal = false;
        this.projectToDelete = null;
      } catch (err) {
        console.error('Error deleting project:', err);
        alert('Error: ' + err.message);
      }
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

.dropdown:hover .dropdown-menu {
  display: block;
}
</style>
