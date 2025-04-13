<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <h1 class="text-2xl font-bold mb-6">Dashboard</h1>
    
    <div class="grid grid-cols-3 gap-6 mb-8">
      <StatCard title="Papers Collected" :value="stats.papersCollected" />
      <StatCard title="Papers Coded" :value="stats.papersCoded" />
      <StatCard title="Data Points Extracted" :value="stats.dataPointsExtracted" />
    </div>
    
    <div class="grid grid-cols-2 gap-6">
      <div class="bg-white rounded-lg p-6 shadow">
        <h2 class="text-lg font-semibold mb-4">Recent Projects</h2>
        <div v-if="projects.length > 0" class="space-y-3">
          <ProjectItem 
            v-for="project in projects"
            :key="project.id"
            :title="project.name" 
            :papers="project.paperCount" 
            :lastUpdated="formatLastUpdated(project.updated_at)" 
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
          <PlusCircle class="mr-1" size="18" /> New Project
        </button>
      </div>
      
      <div class="bg-white rounded-lg p-6 shadow">
        <h2 class="text-lg font-semibold mb-4">Quick Actions</h2>
        <div class="grid grid-cols-2 gap-4">
          <ActionCard 
            icon="Search" 
            title="Find Papers" 
            description="Search databases for relevant papers" 
            @click="$emit('change-view', 'search')"
          />
          <ActionCard 
            icon="Upload" 
            title="Import PDFs" 
            description="Upload PDFs from your computer" 
            @click="importPdfs"
          />
          <ActionCard 
            icon="PenLine" 
            title="Edit Coding Sheet" 
            description="Configure your data extraction variables" 
            @click="$emit('change-view', 'codingSheet')"
          />
          <ActionCard 
            icon="Table" 
            title="View Results" 
            description="See your extracted data" 
            @click="$emit('change-view', 'resultsTable')"
          />
        </div>
      </div>
    </div>

    <div class="mt-6 grid grid-cols-2 gap-6">
      <div class="bg-white rounded-lg p-6 shadow">
        <h2 class="text-lg font-semibold mb-4">Recent Activity</h2>
        <div v-if="activities.length > 0" class="space-y-3">
          <ActivityItem 
            v-for="(activity, index) in activities" 
            :key="index"
            :action="activity.action" 
            :project="activity.project" 
            :time="activity.time"
            :user="activity.user"
          />
        </div>
        <div v-else class="text-gray-500 py-6 text-center">
          No recent activities to display.
        </div>
      </div>
      
      <div class="bg-white rounded-lg p-6 shadow">
        <h2 class="text-lg font-semibold mb-4">Project Progress</h2>
        <div v-if="projectProgress.length > 0" class="space-y-6">
          <ProgressItem 
            v-for="progress in projectProgress" 
            :key="progress.id"
            :title="progress.title"
            :searchComplete="progress.searchComplete"
            :screeningComplete="progress.screeningComplete"
            :dataExtractionComplete="progress.dataExtractionComplete"
            :analysisComplete="progress.analysisComplete"
            :percent="progress.percent"
          />
        </div>
        <div v-else class="text-gray-500 py-6 text-center">
          No projects to display progress for.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import StatCard from './StatCard.vue';
import ProjectItem from './ProjectItem.vue';
import ActionCard from './ActionCard.vue';
import { API_ROUTES } from '../config.js';
import { PlusCircle } from 'lucide-vue-next';
import { projectService, paperService } from '../services/api';
import { useAuthStore } from '../stores/auth';

// Define the ActivityItem component
const ActivityItem = {
  name: 'ActivityItem',
  props: {
    action: {
      type: String,
      required: true
    },
    project: {
      type: String,
      required: true
    },
    time: {
      type: String,
      required: true
    },
    user: {
      type: String,
      required: true
    }
  },
  template: `
    <div class="border-b border-gray-100 pb-3">
      <div class="font-medium text-gray-800">{{ action }}</div>
      <div class="text-sm text-indigo-600 mb-1">{{ project }}</div>
      <div class="flex text-sm text-gray-500">
        <span>{{ time }}</span>
        <span class="mx-2">•</span>
        <span>{{ user }}</span>
      </div>
    </div>
  `
};

// Define the StepItem component
const StepItem = {
  name: 'StepItem',
  props: {
    label: {
      type: String,
      required: true
    },
    complete: {
      type: Boolean,
      required: true
    }
  },
  template: `
    <div :class="['text-center text-xs py-1 rounded', complete ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500']">
      {{ label }}
    </div>
  `
};

// Define the ProgressItem component
const ProgressItem = {
  name: 'ProgressItem',
  components: {
    StepItem
  },
  props: {
    title: {
      type: String,
      required: true
    },
    searchComplete: {
      type: Boolean,
      required: true
    },
    screeningComplete: {
      type: Boolean,
      required: true
    },
    dataExtractionComplete: {
      type: Boolean,
      required: true
    },
    analysisComplete: {
      type: Boolean,
      required: true
    },
    percent: {
      type: Number,
      required: true
    }
  },
  template: `
    <div>
      <div class="flex justify-between items-center mb-2">
        <div class="font-medium text-gray-800">{{ title }}</div>
        <div class="text-sm text-gray-500">{{ percent }}% Complete</div>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2.5 mb-3">
        <div class="bg-indigo-600 h-2.5 rounded-full" :style="{ width: percent + '%' }"></div>
      </div>
      <div class="grid grid-cols-4 gap-2">
        <StepItem label="Search" :complete="searchComplete" />
        <StepItem label="Screening" :complete="screeningComplete" />
        <StepItem label="Extraction" :complete="dataExtractionComplete" />
        <StepItem label="Analysis" :complete="analysisComplete" />
      </div>
    </div>
  `
};

export default {
  name: 'Dashboard',
  components: {
    StatCard,
    ProjectItem,
    ActionCard,
    ActivityItem,
    ProgressItem,
    StepItem,
    PlusCircle
  },
  props: {
    activeProject: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      projects: [],
      stats: {
        papersCollected: 0,
        papersCoded: 0,
        dataPointsExtracted: 0
      },
      activities: [],
      projectProgress: []
    };
  },
  mounted() {
    // Fetch data from the API
    this.fetchProjects();
    this.fetchStats();
    this.fetchActivities();
    this.fetchProjectProgress();
  },
  methods: {
    async fetchProjects() {
      try {
        // Use the projectService instead of direct fetch
        const projects = await projectService.listProjects();
        
        // Get paper counts for each project
        this.projects = await Promise.all(projects.map(async project => {
          try {
            const papers = await projectService.getProjectPapers(project.id);
            return {
              ...project,
              paperCount: papers ? papers.length : 0
            };
          } catch (err) {
            console.error(`Error fetching papers for project ${project.id}:`, err);
            return {
              ...project,
              paperCount: 0
            };
          }
        }));
        
        // Sort by most recently updated
        this.projects.sort((a, b) => new Date(b.updated_at || b.created_at) - new Date(a.updated_at || a.created_at));
        
        // Limit to the most recent 5 projects
        this.projects = this.projects.slice(0, 5);
      } catch (err) {
        console.error('Error fetching projects:', err);
      }
    },
    
    async fetchStats() {
      try {
        // Use default values instead of trying to fetch from an endpoint that doesn't exist
        this.stats = {
          papersCollected: this.projects.reduce((total, project) => total + (project.paperCount || 0), 0),
          papersCoded: 0,
          dataPointsExtracted: 0
        };
        
        // You can implement a proper stats endpoint later and replace this
      } catch (err) {
        console.error('Error calculating stats:', err);
        this.stats = {
          papersCollected: 0,
          papersCoded: 0,
          dataPointsExtracted: 0
        };
      }
    },
    
    async fetchActivities() {
      try {
        // For now, we'll use some mock data for activities since the API endpoint
        // for activity tracking doesn't seem to exist yet
        this.activities = [
          {
            action: 'Added 3 papers',
            project: this.projects.length > 0 ? this.projects[0].name : 'Meta Analysis Project',
            time: '2 hours ago',
            user: 'You'
          },
          {
            action: 'Updated coding sheet',
            project: this.projects.length > 1 ? this.projects[1].name : 'Research Project',
            time: 'Yesterday',
            user: 'You'
          },
          {
            action: 'Exported results to CSV',
            project: this.projects.length > 2 ? this.projects[2].name : 'Analysis Project',
            time: '2 days ago',
            user: 'You'
          }
        ];
      } catch (err) {
        console.error('Error fetching activities:', err);
      }
    },
    
    async fetchProjectProgress() {
      try {
        // Calculate project progress based on papers and coding data
        // This is a placeholder until there's a proper API endpoint for project progress
        this.projectProgress = this.projects.slice(0, 3).map((project, index) => {
          // Simulate different progress states
          const progressMap = [
            { searchComplete: true, screeningComplete: true, dataExtractionComplete: false, analysisComplete: false, percent: 50 },
            { searchComplete: true, screeningComplete: true, dataExtractionComplete: true, analysisComplete: false, percent: 75 },
            { searchComplete: true, screeningComplete: false, dataExtractionComplete: false, analysisComplete: false, percent: 25 }
          ];
          
          return {
            id: project.id,
            title: project.name,
            ...progressMap[index % progressMap.length]
          };
        });
      } catch (err) {
        console.error('Error calculating project progress:', err);
      }
    },
    
    selectProject(project) {
      // Emit event to set this as active project
      this.$emit('set-active-project', project);
      
      // Navigate to project detail view
      this.$emit('view-project', project.id);
    },
    
    createProject() {
      // Navigate to projects page to create a new one
      this.$emit('change-view', 'projects');
    },
    
    importPdfs() {
      // Navigate to the import/upload section
      this.$emit('change-view', 'search');
      // You might want to directly activate the upload tab
      // This would need to be handled in the PaperSearch component
    },
    
    formatLastUpdated(dateString) {
      if (!dateString) return 'Never';
      
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 0) {
        const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
        if (diffHours === 0) {
          const diffMinutes = Math.floor(diffTime / (1000 * 60));
          return diffMinutes === 0 ? 'Just now' : `${diffMinutes} min ago`;
        }
        return `${diffHours} hours ago`;
      } else if (diffDays === 1) {
        return 'Yesterday';
      } else if (diffDays < 7) {
        return `${diffDays} days ago`;
      } else {
        return date.toLocaleDateString();
      }
    }
  }
};
</script>
