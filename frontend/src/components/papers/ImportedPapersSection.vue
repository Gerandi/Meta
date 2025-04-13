<template>
  <div class="bg-white rounded-lg shadow">
    <div class="p-4 border-b flex justify-between items-center">
      <div class="font-medium">Imported Papers ({{ importedPapers.length || 0 }})</div>
      <div class="flex items-center">
        <button class="flex items-center px-3 py-2 text-sm border rounded-lg mr-2 hover:bg-gray-50">
          <Filter class="mr-1" size="16" /> Filter
        </button>
        <button 
          class="flex items-center px-3 py-2 text-sm border rounded-lg hover:bg-gray-50"
          @click="addSelectedImportedToProject"
          :disabled="selectedImportedPapers.length === 0"
        >
          <PlusCircle class="mr-1" size="16" /> Add to Project
        </button>
      </div>
    </div>

    <div class="divide-y">
      <div v-if="isLoading" class="text-center py-8">
        <div class="spinner mb-4"></div>
        <p class="text-gray-500">Loading papers...</p>
      </div>
      
      <template v-else>
        <div class="p-3 border-b flex items-center">
          <input 
            type="checkbox" 
            :checked="allImportedSelected"
            @change="toggleSelectAllImported"
            class="h-4 w-4 text-indigo-600 mr-2 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <span class="text-sm text-gray-600">Select All</span>
          <span class="ml-2 text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full">
            {{ selectedImportedPapers.length }} selected
          </span>
        </div>
        <ImportedPaperItem 
          v-for="paper in importedPapers" 
          :key="paper.id" 
          :paper="paper"
          :selected="isImportedSelected(paper.id)"
          @toggle-selection="toggleImportedSelection(paper.id)"
          @view="$emit('view-paper', paper)"
          @download="$emit('download-pdf', paper)"
          @remove="removePaper(paper.id)"
        />
        <div v-if="importedPapers.length === 0" class="p-10 text-center text-gray-500 border-dashed border-gray-300">
          <FileText class="text-gray-300 mx-auto mb-3" size="40" />
          <p class="mb-2">No papers imported yet</p>
          <p class="text-sm">Use the tabs above to search databases or upload PDFs</p>
        </div>
      </template>
    </div>

    <!-- Project Select Modal -->
    <div v-if="showProjectModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 w-full max-w-xl shadow-xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold">Add to Project</h2>
          <button @click="showProjectModal = false" class="text-gray-500 hover:text-gray-700 p-1 rounded-full hover:bg-gray-100">
            <X size="18" />
          </button>
        </div>
        
        <div class="mb-6">
          <label class="block text-gray-700 mb-2 font-medium">Select Project</label>
          <select 
            v-model="selectedProjectId"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          >
            <option value="">-- Select a Project --</option>
            <option v-for="project in projects" :key="project.id" :value="project.id">{{ project.name }}</option>
          </select>
          
          <div class="mt-4">
            <button 
              @click="showCreateProjectForm = !showCreateProjectForm"
              class="text-indigo-600 text-sm flex items-center hover:text-indigo-800"
            >
              <Plus class="mr-1" size="16" /> Create New Project
            </button>
          </div>
          
          <div v-if="showCreateProjectForm" class="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Project Name*</label>
              <input 
                v-model="newProject.name"
                type="text" 
                class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                placeholder="Enter project name"
              />
            </div>
            
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Description (optional)</label>
              <textarea 
                v-model="newProject.description"
                class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                placeholder="Brief description of this project"
                rows="3"
              ></textarea>
            </div>
            
            <div class="flex justify-end">
              <button 
                @click="createProject"
                class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                :disabled="!newProject.name"
              >
                Create Project
              </button>
            </div>
          </div>
        </div>
        
        <div class="flex justify-end">
          <button 
            @click="showProjectModal = false" 
            class="mr-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >Cancel</button>
          <button 
            @click="addPapersToProject" 
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            :disabled="!selectedProjectId"
          >
            Add to Project
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ImportedPaperItem from './find-papers/imported-paper-item.vue';
import { paperService, projectService } from '../../services/api.js';
import { 
  Filter, 
  PlusCircle, 
  FileText, 
  X, 
  Plus 
} from 'lucide-vue-next';

export default {
  name: 'ImportedPapersSection',
  components: {
    ImportedPaperItem,
    Filter,
    PlusCircle,
    FileText,
    X,
    Plus
  },
  props: {
    activeProject: Object,
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  emits: [
    'view-paper',
    'download-pdf',
    'paper-added-to-project'
  ],
  data() {
    return {
      importedPapers: [],
      selectedImportedPapers: [],
      allImportedSelected: false,
      
      // Project management
      showProjectModal: false,
      projects: [],
      selectedProjectId: '',
      showCreateProjectForm: false,
      papersToAddToProject: [], // Stores imported papers with their database IDs
      newProject: {
        name: '',
        description: ''
      }
    };
  },
  mounted() {
    this.fetchProjects();
    this.fetchImportedPapers();
  },
  methods: {
    // Paper selection methods
    isImportedSelected(paperId) {
      return this.selectedImportedPapers.includes(paperId);
    },
    
    toggleImportedSelection(paperId) {
      if (this.isImportedSelected(paperId)) {
        this.selectedImportedPapers = this.selectedImportedPapers.filter(id => id !== paperId);
      } else {
        this.selectedImportedPapers.push(paperId);
      }
      
      // Update allImportedSelected status
      this.updateAllImportedSelected();
    },
    
    toggleSelectAllImported() {
      if (this.allImportedSelected) {
        // Deselect all
        this.selectedImportedPapers = [];
        this.allImportedSelected = false;
      } else {
        // Select all imported papers
        this.selectedImportedPapers = this.importedPapers.map(paper => paper.id);
        this.allImportedSelected = true;
      }
    },
    
    updateAllImportedSelected() {
      this.allImportedSelected = 
        this.importedPapers.length > 0 && 
        this.importedPapers.every(paper => this.selectedImportedPapers.includes(paper.id));
    },
    
    // Project management
    async fetchProjects() {
      try {
        console.log('Fetching projects');
        this.projects = await projectService.listProjects();
        console.log(`Fetched ${this.projects.length} projects`);
      } catch (error) {
        console.error('Error fetching projects:', error);
        this.projects = []; // Empty projects, no mock data
      }
    },
    
    async createProject() {
      try {
        // Create project using the service
        const project = await projectService.createProject(this.newProject);
        
        // Update local data
        this.projects.push(project);
        this.selectedProjectId = project.id;
        
        // Reset form
        this.showCreateProjectForm = false;
        this.newProject = { name: '', description: '' };
      } catch (error) {
        console.error('Error creating project:', error);
        alert('There was a problem creating the project: ' + error.message);
      }
    },
    
    async addPapersToProject() {
      if (!this.selectedProjectId || this.papersToAddToProject.length === 0) {
        alert('Please select a project and papers to add');
        return;
      }
      
      // Extract just the IDs from the papersToAddToProject array
      const paperIds = this.papersToAddToProject.map(paper => paper.id);
      
      try {
        // Use our helper method to add papers to the selected project
        await this.addPapersToSpecificProject(this.selectedProjectId, paperIds);
        
        // Close the modal and clear the stored papers
        this.showProjectModal = false;
        this.papersToAddToProject = [];
      } catch (error) {
        // Error handling is already done in addPapersToSpecificProject
        console.error('Error in addPapersToProject:', error);
      }
    },
    
    // Add selected imported papers to project
    addSelectedImportedToProject() {
      if (this.selectedImportedPapers.length === 0) {
        alert('Please select papers to add to a project');
        return;
      }
      
      // Check if a project is active
      if (this.activeProject && this.activeProject.id) {
        // Directly add to the active project
        console.log(`Adding ${this.selectedImportedPapers.length} papers directly to active project: ${this.activeProject.name} (ID: ${this.activeProject.id})`);
        
        // Call the API to add papers to the active project
        this.addPapersToSpecificProject(this.activeProject.id, this.selectedImportedPapers);
      } else {
        // No active project - show the modal to select one
        console.log('No active project. Showing project selection modal.');
        
        // Store the selected paper IDs directly as papers to add to project
        this.papersToAddToProject = this.selectedImportedPapers.map(id => {
          return { id: id };
        });
        
        // Show project selection modal
        this.showProjectModal = true;
      }
    },
    
    // Helper method to add papers directly to a specific project
    async addPapersToSpecificProject(projectId, paperIds) {
      try {
        console.log(`Adding ${paperIds.length} papers to project ${projectId}`);
        
        // Use the service to add papers to project
        const result = await projectService.addPapersToProject(projectId, paperIds);
        console.log('Project batch API result:', result);
        
        // If papers were added successfully, notify the user
        alert(`${result.added_count || 0} paper(s) added to project successfully. ${result.skipped_count || 0} were already in the project.`);
        
        // Refresh the imported papers list to show updated associations
        // After papers are added to a project, their status changes from IMPORTED to PROCESSING
        // so they should no longer appear in the imported papers list
        await this.fetchImportedPapers();
        
        // Clear selection
        this.selectedImportedPapers = [];

        // Emit event to parent
        this.$emit('paper-added-to-project');
      } catch (error) {
        console.error('Error adding papers to project:', error);
        alert('There was a problem adding papers to the project: ' + error.message);
      }
    },
    
    removePaper(paperId) {
      // Remove a paper from imported list
      this.importedPapers = this.importedPapers.filter(paper => paper.id !== paperId);
      this.selectedImportedPapers = this.selectedImportedPapers.filter(id => id !== paperId);
    },
    
    // Fetch imported papers
    async fetchImportedPapers() {
      try {
        console.log('Fetching imported papers (status=imported)');
        // Use the specific service function for imported papers
        this.importedPapers = await paperService.listImportedPapers();
        console.log(`Fetched ${this.importedPapers.length} imported papers`);
        
        // If papers were removed from the imported list (e.g., added to a project),
        // clean up the selected array to avoid phantom selections
        this.selectedImportedPapers = this.selectedImportedPapers.filter(id => 
          this.importedPapers.some(paper => paper.id === id)
        );
        
        // Update allImportedSelected status
        this.updateAllImportedSelected();
      } catch (error) {
        console.error('Error fetching imported papers:', error);
        // Don't use mock data - show empty state
        this.importedPapers = [];
        this.selectedImportedPapers = [];
        this.allImportedSelected = false;
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
</style>
