<template>
  <div class="w-64 bg-indigo-800 text-white p-4 flex flex-col h-full">
    <!-- Debug message to confirm Sidebar is loaded -->
    <div class="bg-yellow-500 text-black p-1 mb-2 text-xs">
      Sidebar loaded: {{ user?.email || 'No user' }}
    </div>
    
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
        @click="$emit('change-view', 'dashboard')" 
        :disabled="false" 
      />
      <SidebarItem 
        icon="Search" 
        text="Find Papers" 
        :active="activeView === 'search'" 
        @click="$emit('change-view', 'search')" 
        :disabled="false" 
      />
      <SidebarItem 
        icon="ClipboardList" 
        text="Process Papers" 
        :active="activeView === 'processing'" 
        @click="$emit('change-view', 'processing')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="PenLine" 
        text="Coding" 
        :active="activeView === 'coding' || activeView === 'codingList' || activeView === 'codingSheet'" 
        @click="$emit('change-view', 'coding')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="Table" 
        text="Results Table" 
        :active="activeView === 'resultsTable'" 
        @click="$emit('change-view', 'resultsTable')" 
        :disabled="!activeProject"
      />
      <SidebarItem 
        icon="Folder" 
        text="Projects" 
        :active="activeView === 'projects'" 
        @click="$emit('change-view', 'projects')"
        :disabled="false" 
      />
    </nav>
    
    <div class="mt-auto pt-4 border-t border-indigo-700">
      <div class="flex items-center p-2 rounded hover:bg-indigo-700">
        <div class="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center mr-2">
          <User size="16" />
        </div>
        <div>
          <div class="text-sm font-semibold">{{ user?.email || 'User' }}</div>
          <div class="text-xs flex items-center text-indigo-300 hover:text-white cursor-pointer" @click="handleLogout">
            <LogOut size="14" class="mr-1" /> Logout
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SidebarItem from './SidebarItem.vue';
import { useProjectStore } from '../stores/project';
import { useAuthStore } from '../stores/auth';
import { User, LogOut } from 'lucide-vue-next';
import { mapState, mapActions } from 'pinia';

export default {
  name: 'Sidebar',
  components: {
    SidebarItem,
    User,
    LogOut
  },
  props: {
    activeView: {
      type: String,
      default: 'dashboard'
    }
  },
  computed: {
    ...mapState(useProjectStore, ['activeProject', 'hasActiveProject', 'projects', 'isLoading', 'error']),
    ...mapState(useAuthStore, ['user'])
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
        this.$emit('change-view', 'projects');
        // Restore previous selection to avoid the dropdown staying on "Manage Projects"
        this.$nextTick(() => {
          this.selectedProjectId = this.previousSelectedId || null;
        });
      } else if (newVal !== null) {
        this.previousSelectedId = newVal;
      }
    }
  },
  created() {
    console.log('[Sidebar.vue] Created hook executed.'); // Add log here
  },
  mounted() {
    console.log('[Sidebar.vue] Mounted.'); // Basic mount check
    console.log("Sidebar mounted - current user:", this.user?.email);
    console.log("Sidebar mounted - active project:", this.activeProject);
    console.log("Sidebar mounted - projects length:", this.projects?.length);

    this.selectedProjectId = this.activeProject ? this.activeProject.id : null;
    if (this.selectedProjectId) {
      this.previousSelectedId = this.selectedProjectId;
    }
    this.fetchProjects();
  },
  methods: {
    // Keep existing mapActions
    ...mapActions(useProjectStore, ['setActiveProject', 'clearActiveProject']),
    // Explicitly define fetchProjects to add logging/error handling
    async fetchProjects() {
      console.log('[Sidebar.vue] Attempting to fetch projects via store action...'); // Add log
      const projectStore = useProjectStore(); // Get store instance
      try {
        await projectStore.fetchProjects(); // Call the store action
        console.log('[Sidebar.vue] projectStore.fetchProjects action completed.'); // Log completion
        // State (projects, isLoading, error) is managed by the store and mapped via computed properties
      } catch (err) {
        // Error handling is primarily in the store action, but catch here too for component-specific feedback if needed
        console.error('[Sidebar.vue] Error calling fetchProjects action:', err);
        // Optionally update a local error state if you add one to data()
        // this.localError = err.message || 'Failed to load projects.';
      }
      // isLoading state is handled by the store
    },
    ...mapActions(useAuthStore, ['logout']),

    handleProjectChange() {
      if (this.selectedProjectId === 'manage') {
        return; // This is handled by the watcher
      }
      
      const selectedProject = this.projects.find(p => p.id === this.selectedProjectId);
      if (selectedProject) {
        this.setActiveProject(selectedProject);
        this.$emit('set-active-project', selectedProject);
      }
    },
    
    async handleLogout() {
      await this.logout();
      if (this.$router) {
        this.$router.push('/login');
      }
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
