<template>
  <div class="flex h-screen bg-gray-100">
    <Sidebar 
      :activeView="activeView" 
      :activeProject="activeProject"
      @change-view="setActiveView" 
      @set-active-project="setActiveProject"
      ref="sidebar"
    />
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Top Bar for Active Project -->
      <div v-if="activeProject" class="bg-indigo-100 text-indigo-800 px-4 py-1.5 text-sm border-b border-indigo-200">
        <span>Active Project: <strong>{{ activeProject.name }}</strong></span>
      </div>
      
      <div class="flex-1 overflow-auto">
        <div v-if="needsProject && !activeProject" class="p-6 text-center">
          <div class="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md">
            <FolderOpen class="text-gray-400 mx-auto" size="48" />
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
          @request-confirmation="showConfirmation"
          @project-list-changed="refreshProjectList"
          @configure-coding-sheet="configureCodingSheet"
          @back-to-project="handleBackToProject"
          @coding-saved="refreshResultsTable"
        />
      </div>
    </div>
  </div>
  <!-- Add ProjectSelectModal -->
  <ProjectSelectModal
    :show="isProjectModalVisible"
    :papers="paperForProjectModal"
    @close="isProjectModalVisible = false"
    @paper-added="handlePaperAddedToProject"
  />
  <!-- Add ConfirmationModal -->
  <ConfirmationModal
    :show="confirmationState.show"
    :title="confirmationState.title"
    :message="confirmationState.message"
    :confirmText="confirmationState.confirmText"
    :cancelText="confirmationState.cancelText"
    @confirm="handleConfirmationConfirm"
    @cancel="handleConfirmationCancel"
  />
</template>

<script>
import Sidebar from './components/Sidebar.vue';
import Dashboard from './components/Dashboard.vue';
import PaperSearch from './components/PaperSearch.vue';
import CodingView from './components/CodingView.vue';
import PaperProcessing from './components/PaperProcessing.vue';
import CodingSheet from './components/CodingSheet.vue';
import ResultsTable from './components/ResultsTable.vue';
import Projects from './components/Projects.vue';
import ProjectDetail from './components/ProjectDetail.vue';
import ProjectSelectModal from './components/ProjectSelectModal.vue';
import ConfirmationModal from './components/ConfirmationModal.vue';
import { API_ROUTES } from './config.js';
import { paperService } from './services/api';
import { FolderOpen } from 'lucide-vue-next';

export default {
  name: 'App',
  components: {
    Sidebar,
    Dashboard,
    PaperSearch,
    CodingView,
    PaperProcessing,
    CodingSheet,
    ResultsTable,
    Projects,
    ProjectDetail,
    ProjectSelectModal,
    ConfirmationModal,
    FolderOpen
  },
  data() {
    return {
      activeView: 'dashboard',
      selectedPaper: null,
      selectedProjectId: null,
      selectedPapers: [], // Add selected papers array to store across navigation
      activeProject: null,
      isProjectModalVisible: false,
      paperForProjectModal: null,
      resultsTableKey: 0, // Used to force refresh ResultsTable
      // Confirmation Modal State
      confirmationState: {
        show: false,
        title: '',
        message: '',
        confirmText: 'Confirm',
        cancelText: 'Cancel',
        onConfirm: null // Callback function
      }
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
          return CodingView; // Changed from PdfViewer to CodingView
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
        return { 
          paper: this.selectedPaper,
          projectId: this.activeProject ? this.activeProject.id : null 
        };
      }
      if (this.activeView === 'projectDetail' && this.selectedProjectId) {
        return { projectId: this.selectedProjectId };
      }
      
      if (this.activeView === 'codingSheet' && this.selectedProjectId) {
        return { projectId: this.selectedProjectId };
      }
      
      if (this.activeView === 'resultsTable' && this.activeProject) {
        return { 
          projectId: this.activeProject.id,
          key: this.resultsTableKey // Add key to force refresh when coding is saved
        };
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
    
    handleSelectPaper(paper, projectId) {
      this.selectedPaper = paper;
      if (projectId) {
        // If a project ID was provided, update the selectedProjectId
        this.selectedProjectId = projectId;
      }
      this.activeView = 'viewer';
    },
    
    handleViewProject(projectId) {
      if (!projectId && this.activeProject) {
        // If no projectId is provided but there's an active project, use that
        this.selectedProjectId = this.activeProject.id;
      } else {
        this.selectedProjectId = projectId;
      }
      
      console.log('Setting project detail view with project ID:', this.selectedProjectId);
      this.activeView = 'projectDetail';
    },
    
    configureCodingSheet(projectId) {
      if (!projectId && this.activeProject) {
        // If no projectId provided, use active project
        this.selectedProjectId = this.activeProject.id;
      } else {
        this.selectedProjectId = projectId;
      }
      
      if (!this.selectedProjectId) {
        console.error('No project ID available for coding sheet configuration');
        return;
      }
      
      console.log('Configuring coding sheet for project ID:', this.selectedProjectId);
      this.activeView = 'codingSheet';
    },
    
    handleBackToProject() {
      // Make sure we have a valid project ID
      if (!this.selectedProjectId && this.activeProject) {
        this.selectedProjectId = this.activeProject.id;
      }
      
      if (!this.selectedProjectId) {
        // If no project ID, go to projects list
        this.activeView = 'projects';
      } else {
        // Return to the project detail view
        this.activeView = 'projectDetail';
      }
    },
    
    refreshResultsTable() {
      // Increment the key to force refresh ResultsTable component when data is updated
      this.resultsTableKey++;
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
    },
    
    // Confirmation Modal Methods
    showConfirmation({ title, message, confirmText = 'Confirm', cancelText = 'Cancel', onConfirm }) {
      this.confirmationState.title = title;
      this.confirmationState.message = message;
      this.confirmationState.confirmText = confirmText;
      this.confirmationState.cancelText = cancelText;
      this.confirmationState.onConfirm = onConfirm; // Store the callback
      this.confirmationState.show = true;
    },
    
    handleConfirmationConfirm() {
      if (typeof this.confirmationState.onConfirm === 'function') {
        this.confirmationState.onConfirm(); // Execute the stored callback
      }
      this.resetConfirmationState();
    },
    
    handleConfirmationCancel() {
      this.resetConfirmationState();
    },
    
    resetConfirmationState() {
      this.confirmationState = {
        show: false,
        title: '',
        message: '',
        confirmText: 'Confirm',
        cancelText: 'Cancel',
        onConfirm: null
      };
    },

    // Method to refresh project list in sidebar
    refreshProjectList() {
      console.log('Project list changed, refreshing sidebar...');
      if (this.$refs.sidebar) {
        this.$refs.sidebar.fetchProjects();
      }
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
