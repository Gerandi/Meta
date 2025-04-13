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
        icon="LayoutGrid" 
        text="Dashboard" 
        :active="activeView === 'dashboard'" 
        @click="changeView('dashboard')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="Search" 
        text="Find Papers" 
        :active="activeView === 'search'" 
        @click="changeView('search')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="ClipboardList" 
        text="Process Papers" 
        :active="activeView === 'processing'" 
        @click="changeView('processing')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="FileText" 
        text="PDF Viewer" 
        :active="activeView === 'viewer'" 
        @click="changeView('viewer')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="PenLine" 
        text="Coding" 
        :active="activeView === 'codingList' || activeView === 'codingSheet'" 
        @click="changeView('coding')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="Table" 
        text="Results Table" 
        :active="activeView === 'resultsTable'" 
        @click="changeView('resultsTable')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="Folder" 
        text="Projects" 
        :active="activeView === 'projects'" 
        @click="changeView('projects')" 
      />
      <SidebarItem 
        icon="Settings" 
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
import { useProjectStore } from '../stores/project';
import { mapState, mapActions } from 'pinia';

export default {
  name: 'Sidebar',
  components: {
    SidebarItem
  },
  props: {
    activeView: {
      type: String,
      required: true
    }
    // activeProject prop removed - now using Pinia store
  },
  computed: {
    ...mapState(useProjectStore, ['activeProject', 'hasActiveProject', 'projects', 'isLoading', 'error'])
  },
  data() {
    return {
      selectedProjectId: null,
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
    ...mapActions(useProjectStore, ['setActiveProject', 'clearActiveProject', 'fetchProjects']),
    changeView(view) {
      // If no active project and trying to access a protected view, show project selector
      const protectedViews = ['dashboard', 'search', 'processing', 'viewer', 'codingSheet', 'codingList', 'resultsTable'];
      if (!this.activeProject && protectedViews.includes(view)) {
         console.warn("Cannot navigate: No active project selected.");
         return;
      }
      
      // Special handling for coding navigation
      if (view === 'coding') {
        this.$emit('change-view', 'codingList');
      } else {
        this.$emit('change-view', view);
      }
    },

    // fetchProjects now comes from Pinia store

    handleProjectChange() {
      if (this.selectedProjectId === 'manage') {
        return; // This is handled by the watcher
      }
      
      const selectedProject = this.projects.find(p => p.id === this.selectedProjectId);
      if (selectedProject) {
        this.setActiveProject(selectedProject);
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
