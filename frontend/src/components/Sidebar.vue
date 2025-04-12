<template>
  <div class="w-64 bg-indigo-800 text-white p-4">
    <div class="text-xl font-bold mb-4 pl-2">MetaReview</div>
    
    <!-- Active Project Selector -->
    <div class="mb-6 pl-2">
      <div class="text-sm text-indigo-300 mb-1">Active Project:</div>
      <div v-if="activeProject" class="flex items-center justify-between bg-indigo-900 p-2 rounded">
        <div class="text-sm font-medium truncate">{{ activeProject.name }}</div>
        <button 
          class="text-indigo-300 hover:text-white"
          @click="showProjectSelector = true"
        >
          <font-awesome-icon icon="exchange-alt" />
        </button>
      </div>
      <div v-else class="bg-indigo-900 p-2 rounded text-center">
        <button 
          class="text-sm text-indigo-300 hover:text-white"
          @click="showProjectSelector = true"
        >
          Select a project <font-awesome-icon icon="arrow-right" class="ml-1" />
        </button>
      </div>
    </div>
    
    <nav>
      <SidebarItem 
        icon="th-large" 
        text="Dashboard" 
        :active="activeView === 'dashboard'" 
        @click="changeView('dashboard')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="search" 
        text="Find Papers" 
        :active="activeView === 'search'" 
        @click="changeView('search')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="tasks" 
        text="Process Papers" 
        :active="activeView === 'processing'" 
        @click="changeView('processing')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="file-alt" 
        text="PDF Viewer" 
        :active="activeView === 'viewer'" 
        @click="changeView('viewer')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="edit" 
        text="Coding Sheet" 
        :active="activeView === 'codingSheet'" 
        @click="changeView('codingSheet')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="table" 
        text="Results Table" 
        :active="activeView === 'resultsTable'" 
        @click="changeView('resultsTable')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="folder" 
        text="Projects" 
        :active="activeView === 'projects'" 
        @click="changeView('projects')" 
      />
      <SidebarItem 
        icon="cog" 
        text="Settings" 
        :active="activeView === 'settings'" 
        @click="changeView('settings')" 
      />
    </nav>
    
    <!-- Project Selector Modal -->
    <div v-if="showProjectSelector" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md text-gray-800">
        <h2 class="text-xl font-bold mb-4">Select Active Project</h2>
        
        <div v-if="projects.length === 0" class="mb-4 p-4 bg-gray-50 rounded text-center">
          <p class="text-gray-500 mb-2">You don't have any projects yet.</p>
          <button 
            class="text-indigo-600 hover:text-indigo-800 font-medium"
            @click="goToProjects"
          >
            Create your first project
          </button>
        </div>
        
        <div v-else class="mb-6">
          <div class="max-h-60 overflow-y-auto border rounded-lg divide-y">
            <div 
              v-for="project in projects" 
              :key="project.id"
              class="p-3 hover:bg-gray-50 cursor-pointer"
              @click="selectProject(project)"
            >
              <div class="flex items-center">
                <div class="mr-2">
                  <input 
                    type="radio" 
                    :checked="selectedProjectId === project.id"
                    class="form-radio h-4 w-4 text-indigo-600"
                  />
                </div>
                <div>
                  <div class="font-medium">{{ project.name }}</div>
                  <div v-if="project.description" class="text-sm text-gray-500">
                    {{ project.description }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="flex justify-end">
          <button 
            class="text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 mr-2"
            @click="showProjectSelector = false"
          >
            Cancel
          </button>
          <button 
            v-if="projects.length > 0"
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
            @click="applyProjectSelection"
            :disabled="!selectedProjectId"
          >
            Select
          </button>
        </div>
      </div>
    </div>
    
    <div class="mt-auto pt-4 border-t border-indigo-700 mt-8">
      <div class="flex items-center p-2 rounded hover:bg-indigo-700 cursor-pointer">
        <div class="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center mr-2">
          JD
        </div>
        <div>
          <div class="text-sm font-semibold">John Doe</div>
          <div class="text-xs text-indigo-300">Researcher</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SidebarItem from './SidebarItem.vue';
import { API_ROUTES } from '../config.js';

export default {
  name: 'Sidebar',
  components: {
    SidebarItem
  },
  props: {
    activeView: {
      type: String,
      required: true
    },
    activeProject: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      showProjectSelector: false,
      projects: [],
      selectedProjectId: null,
      isLoading: false,
      error: null
    }
  },
  mounted() {
    // If there's an active project, set it as selected
    if (this.activeProject) {
      this.selectedProjectId = this.activeProject.id;
    }
  },
  methods: {
    changeView(view) {
      // If no active project and trying to access a protected view, show project selector
      const protectedViews = ['dashboard', 'search', 'processing', 'viewer', 'codingSheet', 'resultsTable'];
      if (!this.activeProject && protectedViews.includes(view)) {
        this.showProjectSelector = true;
        return;
      }
      
      this.$emit('change-view', view);
    },
    
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
        
        // If there are projects and no selection, select the first one by default
        if (this.projects.length > 0 && !this.selectedProjectId) {
          this.selectedProjectId = this.projects[0].id;
        }
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching projects:', err);
      } finally {
        this.isLoading = false;
      }
    },
    
    selectProject(project) {
      this.selectedProjectId = project.id;
    },
    
    applyProjectSelection() {
      const selectedProject = this.projects.find(p => p.id === this.selectedProjectId);
      if (selectedProject) {
        this.$emit('set-active-project', selectedProject);
        this.showProjectSelector = false;
      }
    },
    
    goToProjects() {
      this.showProjectSelector = false;
      this.$emit('change-view', 'projects');
    }
  },
  watch: {
    showProjectSelector(newVal) {
      if (newVal) {
        this.fetchProjects();
      }
    },
    activeProject(newVal) {
      if (newVal) {
        this.selectedProjectId = newVal.id;
      } else {
        this.selectedProjectId = null;
      }
    }
  }
}
</script>
