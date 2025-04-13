// frontend/src/stores/project.js
import { defineStore } from 'pinia';
import { projectService } from '../services/api';
import { API_ROUTES } from '../config';

export const useProjectStore = defineStore('project', {
  state: () => ({
    activeProject: null,
    projects: [],
    isLoading: false,
    error: null,
  }),
  getters: {
    hasActiveProject: (state) => !!state.activeProject,
    activeProjectId: (state) => state.activeProject?.id || null,
  },
  actions: {
    async setActiveProject(project) {
      if (project && project.id) {
        this.activeProject = project;
        localStorage.setItem('activeProjectId', project.id);
        // Optionally store name too if needed without full object
        localStorage.setItem('activeProjectName', project.name);
        console.log('Pinia Store: Active project set:', project.name);
      } else {
        console.error('Pinia Store: Attempted to set invalid project', project);
        this.clearActiveProject(); // Clear if invalid project passed
      }
    },
    clearActiveProject() {
      this.activeProject = null;
      localStorage.removeItem('activeProjectId');
      localStorage.removeItem('activeProjectName');
      console.log('Pinia Store: Active project cleared.');
    },
    async loadActiveProjectFromStorage() {
      const projectId = localStorage.getItem('activeProjectId');
      if (projectId && !this.activeProject) { // Load only if not already set
        console.log(`Pinia Store: Found active project ID ${projectId} in storage. Loading...`);
        try {
          // Fetch the full project object using the service
          const project = await projectService.getProject(projectId);
          this.setActiveProject(project); // Use action to set it
        } catch (error) {
          console.error('Pinia Store: Error loading active project from storage:', error);
          this.clearActiveProject(); // Clear invalid stored ID
        }
      } else if (this.activeProject) {
        console.log('Pinia Store: Active project already loaded.');
      } else {
        console.log('Pinia Store: No active project ID found in storage.');
      }
    },
    // Action to fetch the list of projects (can be used by Sidebar/Projects view)
    async fetchProjects() {
      this.isLoading = true;
      this.error = null;
      try {
        this.projects = await projectService.listProjects();
      } catch (err) {
        this.error = err.message;
        console.error('Pinia Store: Error fetching projects:', err);
      } finally {
        this.isLoading = false;
      }
    },
  },
});
