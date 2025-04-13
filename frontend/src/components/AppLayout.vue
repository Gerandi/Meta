<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Debug message to confirm AppLayout is loaded -->
    <div class="fixed top-0 left-0 bg-red-500 text-white p-2 z-50">
      AppLayout is loaded - User: {{ currentUser?.email }}
    </div>
    
    <Sidebar
      :activeView="activeRouteName"
      @change-view="navigateToView"
      @set-active-project="handleSetActiveProject"
      ref="sidebar"
    />
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Top Bar for Active Project -->
      <div v-if="activeProject" class="bg-indigo-100 text-indigo-800 px-4 py-1.5 text-sm border-b border-indigo-200">
        <span>Active Project: <strong>{{ activeProject.name }}</strong></span>
         <button @click="logout" class="float-right text-indigo-600 hover:underline text-xs">Logout</button>
         <span class="float-right mx-2 text-indigo-400">|</span>
         <span class="float-right text-xs text-indigo-500">Logged in as: {{ currentUser?.email }}</span>
      </div>
       <div v-else class="bg-gray-100 text-gray-600 px-4 py-1.5 text-sm border-b border-gray-200">
         <span>No active project selected.</span>
         <button @click="logout" class="float-right text-indigo-600 hover:underline text-xs">Logout</button>
         <span class="float-right mx-2 text-gray-400">|</span>
         <span class="float-right text-xs text-gray-500">Logged in as: {{ currentUser?.email }}</span>
      </div>

      <div class="flex-1 overflow-auto">
         <!-- Router view renders the matched child component -->
        <router-view
          v-slot="{ Component }"
          :key="$route.fullPath"
          @select-paper="handleSelectPaper"
          @view-details="handleViewDetails"
          @view-project="handleViewProject"
          @set-active-project="handleSetActiveProject"
          @clear-active-project="handleClearActiveProject"
          @change-view="navigateToView"
          @process-papers="handleProcessPapers"
          @add-to-project="showProjectSelectModal"
          @request-confirmation="showConfirmation"
          @project-list-changed="refreshProjectList"
          @configure-coding-sheet="configureCodingSheet"
          @configure-sheet="handleConfigureSheet"
          @start-coding="handleStartCoding"
          @back-to-project="handleBackToProject"
          @coding-saved="refreshResultsTable"
        >
           <component :is="Component" :active-project="activeProject" /> <!-- Bind activeProject -->
        </router-view>
      </div>
    </div>
     <!-- Modals remain here -->
     <ProjectSelectModal
        v-if="isProjectModalVisible"
        :show="isProjectModalVisible"
        :papers="paperForProjectModal"
        @close="isProjectModalVisible = false"
        @paper-added="handlePaperAddedToProject"
      />
      <ConfirmationModal
        v-if="confirmationState.show"
        :show="confirmationState.show"
        :title="confirmationState.title"
        :message="confirmationState.message"
        :confirmText="confirmationState.confirmText"
        :cancelText="confirmationState.cancelText"
        @confirm="handleConfirmationConfirm"
        @cancel="handleConfirmationCancel"
      />
  </div>
</template>

<script>
// Import necessary components and stores
import Sidebar from './Sidebar.vue';
import ProjectSelectModal from './ProjectSelectModal.vue';
import ConfirmationModal from './ConfirmationModal.vue';
import { useAuthStore } from '../stores/auth';
import { useProjectStore } from '../stores/project';
import { mapState, mapActions } from 'pinia';
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'AppLayout',
  components: {
    Sidebar,
    ProjectSelectModal,
    ConfirmationModal,
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const authStore = useAuthStore();
    const projectStore = useProjectStore();

    const logout = () => {
      authStore.logout();
      router.push('/login');
    };

    return { router, route, logout };
  },
  data() {
     // Keep modal states etc. here
     return {
      isProjectModalVisible: false,
      paperForProjectModal: null,
      resultsTableKey: 0,
      confirmationState: {
        show: false, title: '', message: '', confirmText: 'Confirm', cancelText: 'Cancel', onConfirm: null
      },
      // selectedPaper and selectedProjectId might be needed if passing props directly
      selectedPaper: null,
      selectedProjectId: null,
      selectedPapers: [], // For processing view
    }
  },
  computed: {
    ...mapState(useAuthStore, ['currentUser']),
    ...mapState(useProjectStore, ['activeProject']),
    activeRouteName() {
      // Map route names to sidebar active states
      const name = this.$route.name;
      if (name === 'CodingView' || name === 'CodingList' || name === 'CodingSheet') return 'coding';
      if (name === 'ProjectDetail') return 'projects';
      if (name === 'Dashboard') return 'dashboard';
      if (name === 'Search') return 'search';
      if (name === 'Processing') return 'processing';
      if (name === 'Results') return 'resultsTable';
      // Add more mappings as needed
      return name ? name.toLowerCase() : 'dashboard';
    }
  },
  methods: {
    ...mapActions(useProjectStore, ['setActiveProject', 'clearActiveProject', 'loadActiveProjectFromStorage']), 
    
    navigateToView(viewName) {
      // Map sidebar clicks to route names
      let routeName = viewName;
      if (viewName === 'coding') routeName = 'CodingList'; // Default to list view
      if (viewName === 'viewer') {
          // Need a paper selected to go to viewer/coding view
          if (this.selectedPaper) {
              routeName = 'CodingView';
              this.$router.push({ name: routeName, params: { paperId: this.selectedPaper.id } });
              return;
          } else {
              console.warn("Cannot navigate to viewer without a selected paper.");
              // Optionally navigate to coding list or show a message
              routeName = 'CodingList';
          }
      }
      if (viewName === 'resultsTable') routeName = 'Results';
      if (viewName === 'processing') routeName = 'Processing';
      if (viewName === 'search') routeName = 'Search';
      if (viewName === 'dashboard') routeName = 'Dashboard';
      if (viewName === 'projects') routeName = 'Projects';

      // Navigate using router
      if (this.$route.name !== routeName) {
          this.$router.push({ name: routeName });
      }
    },
    
    handleSelectPaper(paper, projectId) {
      this.selectedPaper = paper;
      // Navigate to the coding view for this paper
      this.$router.push({ name: 'CodingView', params: { paperId: paper.id } });
    },
    
    handleViewProject(projectId) {
       this.selectedProjectId = projectId; 
       this.$router.push({ name: 'ProjectDetail', params: { projectId: projectId } });
    },
    
    configureCodingSheet(projectId) {
       this.$router.push({ name: 'CodingSheet', params: { projectId: projectId || this.activeProject?.id } });
    },
    
    handleBackToProject() {
        const targetProjectId = this.selectedProjectId || this.activeProject?.id;
        if (targetProjectId) {
            this.$router.push({ name: 'ProjectDetail', params: { projectId: targetProjectId } });
        } else {
            this.$router.push({ name: 'Projects' });
        }
    },
    
    handleStartCoding(paper) {
        this.selectedPaper = paper;
        this.$router.push({ name: 'CodingView', params: { paperId: paper.id } });
    },
    
    handleConfigureSheet() {
        if (this.activeProject) {
            this.$router.push({ name: 'CodingSheet', params: { projectId: this.activeProject.id } });
        } else {
            alert("Please select an active project first.");
            this.$router.push({ name: 'Projects' });
        }
    },
    
    handleProcessPapers(papers) {
      this.selectedPapers = papers; 
      this.$router.push({ name: 'Processing' });
    },
    
    handleViewDetails(paper) {
        this.selectedPaper = paper;
        this.$router.push({ name: 'PaperDetail', params: { paperId: paper.id } });
    },

    // Modal and confirmation methods
    showProjectSelectModal(paper) {
      console.log("AppLayout: showProjectSelectModal called with paper:", paper);
      this.paperForProjectModal = paper;
      this.isProjectModalVisible = true;
    },
    
    handlePaperAddedToProject(event) {
      console.log(`${event.papers.length} paper(s) added to project ${event.projectId}`);
      this.isProjectModalVisible = false; 
    },
    
    showConfirmation({ title, message, confirmText = 'Confirm', cancelText = 'Cancel', onConfirm }) {
      this.confirmationState.title = title;
      this.confirmationState.message = message;
      this.confirmationState.confirmText = confirmText;
      this.confirmationState.cancelText = cancelText;
      this.confirmationState.onConfirm = onConfirm;
      this.confirmationState.show = true;
    },
    
    handleConfirmationConfirm() {
      if (typeof this.confirmationState.onConfirm === 'function') {
        this.confirmationState.onConfirm();
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
    
    refreshProjectList() {
      if (this.$refs.sidebar) {
        this.$refs.sidebar.fetchProjects();
      }
    },
    
    refreshResultsTable() {
      this.resultsTableKey++;
    },
    
    handleSetActiveProject(project) {
      this.setActiveProject(project);
    },
    
    handleClearActiveProject() {
      this.clearActiveProject();
    }
  },
  created() {
    console.log('[AppLayout.vue] Created hook executed.'); // Add log here
  },
  mounted() {
    console.log("AppLayout mounted - current user:", this.currentUser?.email);
    console.log("AppLayout mounted - active project:", this.activeProject);
    this.loadActiveProjectFromStorage();
  }
}
</script>
