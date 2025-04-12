<template>
  <div class="w-64 bg-indigo-800 text-white p-4 flex flex-col h-full">
    <div class="text-xl font-bold mb-4 pl-2">MetaReview</div>
    
    <!-- Active Project Dropdown Selector -->
    <div class="mb-6 px-2">
      <div class="relative">
        <select
          id="project-select"
          v-model="selectedProjectId"
          @change="handleProjectChange"
          class="w-full bg-white border border-gray-300 text-black rounded p-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-400 focus:border-indigo-400 appearance-none"
        >
          <option :value="null" disabled>Select a Project</option>
          <option v-for="project in projects" :key="project.id" :value="project.id">
            {{ project.name }}
          </option>
          <option value="manage" class="font-medium">⚙️ Manage Projects</option>
        </select>
      </div>
      <div v-if="isLoading" class="text-xs text-indigo-300 mt-1">Loading projects...</div>
      <div v-if="error" class="text-xs text-red-400 mt-1">Error loading projects</div>
    </div>
    
    <nav class="flex-grow">
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
    
    <div class="mt-auto pt-4 border-t border-indigo-700">
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
      projects: [],
      selectedProjectId: null,
      isLoading: false,
      error: null,
      previousSelectedId: null // To store previous selection
    }
  },
  watch: {
    // Update local selection when prop changes
    activeProject(newVal) {
      this.selectedProjectId = newVal ? newVal.id : null;
      // Store as previous selection too
      if (newVal) {
        this.previousSelectedId = newVal.id;
      }
    },
    
    // Handle special "manage" option
    selectedProjectId(newVal) {
      if (newVal === 'manage') {
        this.goToProjects();
        // Restore previous selection to avoid the dropdown staying on "Manage Projects"
        this.$nextTick(() => {
          this.selectedProjectId = this.previousSelectedId || null;
        });
      } else if (newVal !== null) {
        this.previousSelectedId = newVal;
      }
    }
  },
  mounted() {
    this.selectedProjectId = this.activeProject ? this.activeProject.id : null;
    if (this.selectedProjectId) {
      this.previousSelectedId = this.selectedProjectId;
    }
    this.fetchProjects();
  },
  methods: {
    changeView(view) {
      // If no active project and trying to access a protected view, show project selector
      const protectedViews = ['dashboard', 'search', 'processing', 'viewer', 'codingSheet', 'resultsTable'];
      if (!this.activeProject && protectedViews.includes(view)) {
         console.warn("Cannot navigate: No active project selected.");
         return;
      }
      this.$emit('change-view', view);
    },

    async fetchProjects() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await fetch(API_ROUTES.PROJECTS.LIST);
        if (!response.ok) throw new Error('Failed to load projects');
        this.projects = await response.json();
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching projects for sidebar:', err);
      } finally {
        this.isLoading = false;
      }
    },

    handleProjectChange() {
      if (this.selectedProjectId === 'manage') {
        return; // This is handled by the watcher
      }
      
      const selectedProject = this.projects.find(p => p.id === this.selectedProjectId);
      if (selectedProject) {
        this.$emit('set-active-project', selectedProject);
      }
    },

    goToProjects() {
      this.$emit('change-view', 'projects');
    }
  }
}
</script>

<style scoped>
/* Add custom styles for the select dropdown arrow */
select {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23000000' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem; /* Make space for the arrow */
}
/* Hide default arrow in Firefox */
select::-moz-focus-inner {
  border: 0;
}
/* Hide default arrow in IE/Edge */
select::-ms-expand {
  display: none;
}

/* Option styling */
select option {
  padding: 10px;
  background-color: white;
  color: black;
}
</style>
