<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
      <h2 class="text-xl font-bold mb-4">
        {{ isMultiplePapers ? `Add ${papers.length} Papers to Project` : 'Add to Project' }}
      </h2>
      
      <div v-if="projects.length === 0" class="mb-4 p-4 bg-gray-50 rounded text-center">
        <p class="text-gray-500 mb-2">You don't have any projects yet.</p>
        <button 
          class="text-indigo-600 hover:text-indigo-800 font-medium"
          @click="createNewProject"
        >
          Create a new project
        </button>
      </div>
      
      <div v-else class="mb-6">
        <div class="mb-2 text-sm font-medium text-gray-700">Select a project</div>
        <div class="max-h-60 overflow-y-auto border rounded-lg divide-y">
          <div 
            v-for="project in projects" 
            :key="project.id"
            class="p-3 hover:bg-gray-50 cursor-pointer"
            @click="selectedProjectId = project.id"
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
      
      <div v-if="showCreateForm" class="mb-6 border-t pt-4">
        <h3 class="text-lg font-medium mb-2">Create New Project</h3>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
          <input 
            v-model="newProject.name"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Project name"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Description (optional)</label>
          <textarea 
            v-model="newProject.description"
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Brief description of this project"
            rows="2"
          ></textarea>
        </div>
      </div>
      
      <div class="flex justify-between">
        <button 
          v-if="!showCreateForm && projects.length > 0"
          class="text-indigo-600 hover:text-indigo-800"
          @click="showCreateForm = true"
        >
          <font-awesome-icon icon="plus" class="mr-1" /> New Project
        </button>
        <div v-else></div>
        
        <div>
          <button 
            class="text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 mr-2"
            @click="closeModal"
          >
            Cancel
          </button>
          <button 
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
            @click="addToProject"
            :disabled="!isFormValid"
          >
            Add to Project
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { API_ROUTES } from '../config.js';

export default {
  name: 'ProjectSelectModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    paper: {
      type: [Object, Array],
      default: null
    }
  },
  data() {
    return {
      projects: [],
      selectedProjectId: null,
      showCreateForm: false,
      newProject: {
        name: '',
        description: ''
      },
      isLoading: false,
      error: null
    }
  },
  computed: {
    isFormValid() {
      if (this.showCreateForm) {
        return this.newProject.name.trim() !== '';
      } else {
        return this.selectedProjectId !== null;
      }
    },
    isMultiplePapers() {
      return Array.isArray(this.paper) && this.paper.length > 1;
    },
    papers() {
      return Array.isArray(this.paper) ? this.paper : [this.paper];
    }
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.fetchProjects();
      }
    }
  },
  methods: {
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
        
        // If there are projects, select the first one by default
        if (this.projects.length > 0) {
          this.selectedProjectId = this.projects[0].id;
        } else {
          // If no projects, show the create form
          this.showCreateForm = true;
        }
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching projects:', err);
      } finally {
        this.isLoading = false;
      }
    },
    
    createNewProject() {
      this.showCreateForm = true;
    },
    
    async addToProject() {
      try {
        let projectId = this.selectedProjectId;
        let addedPapers = [];
        
        // If we're creating a new project, do that first
        if (this.showCreateForm) {
          if (!this.newProject.name.trim()) {
            throw new Error('Project name is required');
          }
          
          const createResponse = await fetch(API_ROUTES.PROJECTS.CREATE, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.newProject)
          });
          
          if (!createResponse.ok) {
            const errorData = await createResponse.json();
            throw new Error(errorData.detail || 'Failed to create project');
          }
          
          const createdProject = await createResponse.json();
          projectId = createdProject.id;
          console.log('Created new project:', createdProject.name, 'with ID:', projectId);
        }
        
        if (!projectId) {
          throw new Error('No project selected');
        }
        
        // Process each paper
        for (const paper of this.papers) {
          // Skip if paper is null
          if (!paper) continue;
          
          console.log('Adding paper to project:', paper.title);
          
          // Check and prepare the paper data
          const paperData = {
            title: paper.title,
            doi: paper.doi,
            abstract: paper.abstract || '',
            publication_date: paper.publication_date ? new Date(paper.publication_date).toISOString() : null,
            authors: paper.authors || [],
            journal: paper.journal || '',
            url: paper.url || '',
            open_access_url: paper.open_access_url || ''
          };
          
          // Save the paper
          const saveResponse = await fetch(API_ROUTES.PAPERS.CREATE, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(paperData)
          });
          
          if (!saveResponse.ok) {
            const errorData = await saveResponse.json();
            console.error('Paper data:', paperData);
            console.error('Save response:', errorData);
            throw new Error(errorData.detail || 'Failed to save paper');
          }
          
          const savedPaper = await saveResponse.json();
          addedPapers.push(savedPaper);
          
          // Add the paper to the project
          const addResponse = await fetch(API_ROUTES.PROJECTS.ADD_PAPER(projectId, savedPaper.id), {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            }
          });
          
          if (!addResponse.ok) {
            const errorData = await addResponse.json();
            throw new Error(errorData.detail || 'Failed to add paper to project');
          }
        }
        
        // Close the modal and emit success event
        this.$emit('paper-added', {
          papers: addedPapers,
          projectId: projectId
        });
        
        this.closeModal();
      } catch (err) {
        console.error('Error adding papers to project:', err);
        alert('Error: ' + err.message);
      }
    },
    
    closeModal() {
      this.selectedProjectId = null;
      this.showCreateForm = false;
      this.newProject = { name: '', description: '' };
      this.$emit('close');
    }
  }
}
</script>
