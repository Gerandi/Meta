<template>
  <div class="flex h-screen bg-gray-100">
    <Sidebar 
      :activeView="activeView" 
      :activeProject="activeProject"
      @change-view="setActiveView" 
      @set-active-project="setActiveProject"
    />
    <div class="flex-1 overflow-auto">
      <div v-if="needsProject && !activeProject" class="p-6 text-center">
        <div class="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md">
          <font-awesome-icon icon="folder-open" class="text-gray-400 text-5xl mb-4" />
          <h2 class="text-xl font-medium mb-4">Please Select a Project</h2>
          <p class="text-gray-600 mb-6">You need to select or create a project before you can access this page.</p>
          <div class="flex justify-center space-x-4">
            <button 
              class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
              @click="setActiveView('projects')"
            >
              Go to Projects
            </button>
          </div>
        </div>
      </div>
      <component 
        v-else
        :is="currentView" 
        v-bind="componentProps"
        @select-paper="handleSelectPaper"
        @view-project="handleViewProject"
        @set-active-project="setActiveProject"
        @clear-active-project="clearActiveProject"
        @change-view="setActiveView"
        @process-papers="handleProcessPapers"
        @add-to-project="showProjectSelectModal"
      />
    </div>
  </div>
  <!-- Add ProjectSelectModal -->
  <ProjectSelectModal
    :show="isProjectModalVisible"
    :papers="paperForProjectModal"
    @close="isProjectModalVisible = false"
    @paper-added="handlePaperAddedToProject"
  />
</template>

<script>
import Sidebar from './components/Sidebar.vue';
import Dashboard from './components/Dashboard.vue';
import PaperSearch from './components/PaperSearch.vue';
import PdfViewer from './components/PdfViewer.vue';
import PaperProcessing from './components/PaperProcessing.vue';
import CodingSheet from './components/CodingSheet.vue';
import ResultsTable from './components/ResultsTable.vue';
import Projects from './components/Projects.vue';
import ProjectDetail from './components/ProjectDetail.vue';
import ProjectSelectModal from './components/ProjectSelectModal.vue';
import { API_ROUTES } from './config.js';

export default {
  name: 'App',
  components: {
    Sidebar,
    Dashboard,
    PaperSearch,
    PdfViewer,
    PaperProcessing,
    CodingSheet,
    ResultsTable,
    Projects,
    ProjectDetail,
    ProjectSelectModal
  },
  data() {
    return {
      activeView: 'dashboard',
      selectedPaper: null,
      selectedProjectId: null,
      selectedPapers: [], // Add selected papers array to store across navigation
      activeProject: null,
      isProjectModalVisible: false,
      paperForProjectModal: null
    }
  },
  computed: {
    currentView() {
      switch(this.activeView) {
        case 'dashboard':
          return Dashboard;
        case 'search':
          return PaperSearch;
        case 'viewer':
          return PdfViewer;
        case 'processing':
          return PaperProcessing;
        case 'codingSheet':
          return CodingSheet;
        case 'resultsTable':
          return ResultsTable;
        case 'projects':
          return Projects;
        case 'projectDetail':
          return ProjectDetail;
        default:
          return Dashboard;
      }
    },
    componentProps() {
      if (this.activeView === 'viewer' && this.selectedPaper) {
        return { paper: this.selectedPaper };
      }
      if (this.activeView === 'projectDetail' && this.selectedProjectId) {
        return { projectId: this.selectedProjectId };
      }
      if (this.activeView === 'processing') {
        return { selectedPapers: this.selectedPapers };
      }
      // Pass activeProject to components that need it
      if (['dashboard', 'search', 'processing', 'viewer', 'codingSheet', 'resultsTable'].includes(this.activeView)) {
        return { activeProject: this.activeProject };
      }
      return {};
    },
    needsProject() {
      const protectedViews = ['dashboard', 'search', 'processing', 'viewer', 'codingSheet', 'resultsTable'];
      return protectedViews.includes(this.activeView);
    }
  },
  methods: {
    setActiveView(view) {
      // Prevent accessing protected views without an active project
      const protectedViews = ['dashboard', 'search', 'processing', 'viewer', 'codingSheet', 'resultsTable'];
      if (!this.activeProject && protectedViews.includes(view)) {
        console.warn(`Cannot navigate to ${view} without an active project.`);
        // Redirect to projects view
        this.activeView = 'projects';
        return;
      }
      this.activeView = view;
    },
    
    handleSelectPaper(paper) {
      this.selectedPaper = paper;
      this.activeView = 'viewer';
    },
    
    handleViewProject(projectId) {
      this.selectedProjectId = projectId;
      this.activeView = 'projectDetail';
    },
    
    setActiveProject(project) {
      this.activeProject = project;
      
      // Save to localStorage for persistence
      localStorage.setItem('activeProjectId', project.id);
      localStorage.setItem('activeProjectName', project.name);
      
      console.log('Active project set:', project.name);
      
      // If user was stuck on project selection prompt, navigate to dashboard
      if (this.needsProject && this.activeView === 'projects') {
        this.activeView = 'dashboard';
      }
    },
    
    clearActiveProject() {
      this.activeProject = null;
      localStorage.removeItem('activeProjectId');
      localStorage.removeItem('activeProjectName');
      
      // If current view requires a project, redirect to projects view
      if (this.needsProject) {
        this.activeView = 'projects';
      }
    },

    handleProcessPapers(papers) {
      // Store the selected papers and navigate to processing page
      this.selectedPapers = papers;
      this.activeView = 'processing';
    },
    
    async loadActiveProject() {
      const projectId = localStorage.getItem('activeProjectId');
      
      if (projectId) {
        try {
          const response = await fetch(API_ROUTES.PROJECTS.GET_BY_ID(projectId));
          
          if (response.ok) {
            const project = await response.json();
            this.activeProject = project;
            console.log('Loaded active project:', project.name);
          } else {
            // If error, clear the stored active project
            this.clearActiveProject();
          }
        } catch (error) {
          console.error('Error loading active project:', error);
          this.clearActiveProject();
        }
      }
    },
    
    // Method to show the project selection modal
    showProjectSelectModal(paper) {
      console.log("App.vue: showProjectSelectModal called with paper:", paper);
      this.paperForProjectModal = paper;
      this.isProjectModalVisible = true;
    },
    
    // Handle successful addition
    handlePaperAddedToProject(event) {
      console.log(`${event.papers.length} paper(s) added to project ${event.projectId}`);
      // Optionally show a success message
      this.isProjectModalVisible = false; // Close modal
    }
  },
  mounted() {
    // Load active project from localStorage if available
    this.loadActiveProject();
  }
}
</script>

<style>
@import './style.css';

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Inter', sans-serif;
}
</style>
