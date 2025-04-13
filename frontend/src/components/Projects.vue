<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">My Projects</h1>
    
    <div class="mb-6">
      <button 
        class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
        @click="showCreateModal = true"
      >
        <Plus class="mr-2 inline" size="18" /> Create New Project
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
      <FolderOpen class="text-gray-400 mx-auto" size="48" />
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
        class="bg-white rounded-lg shadow overflow-visible hover:shadow-md transition-shadow duration-200"
      >
        <div class="p-6 min-h-[180px] flex flex-col">
          <div class="flex justify-between items-start">
            <h3 class="text-xl font-semibold mb-2">{{ project.name }}</h3>
            <div class="dropdown relative">
              <button class="text-gray-500 hover:text-gray-700 p-1" @click.stop="toggleDropdown($event)">
                <MoreVertical size="18" />
              </button>
              <div class="dropdown-menu absolute right-0 mt-1 bg-white rounded-lg shadow-lg p-2 z-50 border">
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
                  class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded"
                  @click="confirmDelete(project)"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
          <p v-if="project.description" class="text-gray-600 mb-4 flex-grow">{{ project.description }}</p>
          <p v-else class="text-gray-500 italic mb-4 flex-grow">No description</p>
          <div class="flex justify-between items-center mt-auto">
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
  </div>
</template>

<script>
import { API_ROUTES } from '../config.js';
import { Plus, FolderOpen, MoreVertical } from 'lucide-vue-next';
import { projectService } from '../services/api.js';
import { useAuthStore } from '../stores/auth';

export default {
  name: 'Projects',
  components: {
    Plus,
    FolderOpen,
    MoreVertical
  },
  emits: ['view-project', 'set-active-project', 'clear-active-project', 'request-confirmation', 'project-list-changed'],
  data() {
    return {
      projects: [],
      isLoading: false,
      error: null,
      showCreateModal: false,
      showEditModal: false,
      formData: {
        name: '',
        description: ''
      },
      editingProjectId: null
    }
  },
  mounted() {
    this.fetchProjects();
    
    // Add click handler for dropdown menus
    document.addEventListener('click', (e) => {
      const dropdowns = document.querySelectorAll('.dropdown-menu');
      dropdowns.forEach(menu => {
        menu.classList.remove('active');
      });
    });
  },
  methods: {
    async fetchProjects() {
      this.isLoading = true;
      this.error = null;
      
      try {
        // Use projectService instead of direct fetch
        this.projects = await projectService.listProjects();
        console.log('Fetched projects:', this.projects);
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching projects:', err);
      } finally {
        this.isLoading = false;
      }
    },
    
    toggleDropdown(event) {
      // First close any open dropdowns
      const allMenus = document.querySelectorAll('.dropdown-menu');
      allMenus.forEach(menu => {
        if (menu !== event.currentTarget.nextElementSibling) {
          menu.classList.remove('active');
        }
      });
      
      // Toggle the clicked dropdown
      const menu = event.currentTarget.nextElementSibling;
      menu.classList.toggle('active');
      
      // Prevent event from propagating to document click handler
      event.stopPropagation();
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
      // Use the centralized confirmation modal instead of local one
      this.$emit('request-confirmation', {
        title: 'Delete Project',
        message: `Are you sure you want to delete the project "${project.name}"? This action cannot be undone and will permanently delete all associated papers, coding data, and results within this project.`,
        confirmText: 'Delete Project',
        onConfirm: () => this.deleteProject(project.id)
      });
    },
    
    closeModal() {
      this.showCreateModal = false;
      this.showEditModal = false;
      this.formData = { name: '', description: '' };
      this.editingProjectId = null;
    },
    
    async saveProject() {
      try {
        let savedProject;
        
        if (this.showEditModal) {
          // Use projectService for update
          savedProject = await projectService.updateProject(this.editingProjectId, this.formData);
        } else {
          // Use projectService for create
          savedProject = await projectService.createProject(this.formData);
        }
        
        console.log('Project saved successfully:', savedProject);
        
        // Refresh projects list
        await this.fetchProjects();
        
        // Emit event to notify parent components about project list change
        this.$emit('project-list-changed');
        
        // Close modal
        this.closeModal();
      } catch (err) {
        console.error('Error saving project:', err);
        this.error = err.message || 'Failed to save project.'; // Set error property
        alert('Error: ' + this.error); // Keep alert for immediate feedback
      }
    },
    
    async deleteProject(projectId) {
      try {
        // Use projectService for delete
        await projectService.deleteProject(projectId);
        
        // If this was the active project, clear it
        const activeProjectId = localStorage.getItem('activeProjectId');
        if (activeProjectId && parseInt(activeProjectId) === projectId) {
          localStorage.removeItem('activeProjectId');
          localStorage.removeItem('activeProjectName');
          this.$emit('clear-active-project');
        }
        
        // Refresh projects list
        await this.fetchProjects();
        
        // Emit event to notify parent components about project list change
        this.$emit('project-list-changed');
      } catch (err) {
        console.error('Error deleting project:', err);
        this.error = err.message || 'Failed to delete project.'; // Set error property
        alert('Error: ' + this.error); // Keep alert for immediate feedback
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

.dropdown-menu {
  display: none;
  transform: translateX(0);
  right: 0;
  top: 100%;
  min-width: 140px;
  max-width: 200px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
}

.dropdown {
  position: relative;
  z-index: 30; /* Ensure dropdown container has a higher z-index */
}

.dropdown-menu.active {
  display: block;
}

/* Override any potential overflow hidden settings that might clip the dropdown */
.overflow-visible {
  overflow: visible !important;
}
</style>
