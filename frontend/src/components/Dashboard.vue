<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">Dashboard</h1>
    
    <div class="grid grid-cols-3 gap-6 mb-8">
      <StatCard title="Papers Collected" value="0" />
      <StatCard title="Papers Coded" value="0" />
      <StatCard title="Data Points Extracted" value="0" />
    </div>
    
    <div class="grid grid-cols-2 gap-6">
      <div class="bg-white rounded-lg p-6 shadow">
        <h2 class="text-lg font-semibold mb-4">Recent Projects</h2>
        <div v-if="projects.length > 0" class="space-y-3">
          <ProjectItem 
            v-for="project in projects"
            :key="project.id"
            :title="project.title" 
            :papers="project.papers" 
            :lastUpdated="project.lastUpdated" 
            @click="selectProject(project)"
          />
        </div>
        <div v-else class="text-gray-500 py-6 text-center">
          No projects yet. Create your first project to get started.
        </div>
        <button 
          class="mt-4 flex items-center text-indigo-600 hover:text-indigo-800"
          @click="createProject"
        >
          <font-awesome-icon icon="plus-circle" class="mr-1" /> New Project
        </button>
      </div>
      
      <div class="bg-white rounded-lg p-6 shadow">
        <h2 class="text-lg font-semibold mb-4">Quick Actions</h2>
        <div class="grid grid-cols-2 gap-4">
          <ActionCard 
            icon="search" 
            title="Find Papers" 
            description="Search databases for relevant papers" 
            @click="$emit('change-view', 'search')"
          />
          <ActionCard 
            icon="upload" 
            title="Import PDFs" 
            description="Upload PDFs from your computer" 
            @click="importPdfs"
          />
          <ActionCard 
            icon="edit" 
            title="Edit Coding Sheet" 
            description="Configure your data extraction variables" 
            @click="$emit('change-view', 'codingSheet')"
          />
          <ActionCard 
            icon="table" 
            title="View Results" 
            description="See your extracted data" 
            @click="$emit('change-view', 'resultsTable')"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import StatCard from './StatCard.vue';
import ProjectItem from './ProjectItem.vue';
import ActionCard from './ActionCard.vue';

export default {
  name: 'Dashboard',
  components: {
    StatCard,
    ProjectItem,
    ActionCard
  },
  data() {
    return {
      projects: [] // Will be populated from API
    }
  },
  mounted() {
    // Fetch projects data
    this.fetchProjects();
  },
  methods: {
    async fetchProjects() {
      try {
        // TODO: Replace with actual API call
        // For now, use mock data
        this.projects = [
          {
            id: 1,
            title: "Effectiveness of CBT for Anxiety Disorders",
            papers: 0,
            lastUpdated: "Just now"
          }
        ];
      } catch (error) {
        console.error('Error fetching projects:', error);
      }
    },
    selectProject(project) {
      // Handle project selection
      console.log('Selected project:', project);
    },
    createProject() {
      // Handle project creation
      console.log('Create new project');
    },
    importPdfs() {
      // Handle PDF import
      console.log('Import PDFs');
    }
  }
}
</script>
