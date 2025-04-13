    getFieldOptionsCount(options) {
      if (!options) return 0;
      
      // If options is a string, count the lines
      if (typeof options === 'string') {
        return options.split('\n').filter(option => option.trim()).length;
      }
      
      // If options is an array, return its length
      if (Array.isArray(options)) {
        return options.length;
      }
      
      return 0;
    },<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <!-- Header with back button, title, and save/duplicate buttons -->
    <div class="flex items-center mb-6">
      <button 
        class="text-indigo-600 hover:text-indigo-800 mr-4"
        @click="goBack"
      >
        <ArrowLeft class="inline mr-1" size="18" /> Back to Project
      </button>
      <h1 class="text-2xl font-bold flex-grow">{{ projectName }} - Coding Sheet Configuration</h1>
      <div class="flex">
        <button class="mr-2 px-4 py-2 bg-white border rounded-lg text-gray-700 hover:bg-gray-50 flex items-center"
          @click="duplicateCodingSheet">
          <Copy class="mr-1" size="18" />
          Duplicate
        </button>
        <button class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center"
          @click="saveConfiguration"
          :disabled="saving">
          <Save class="mr-1" size="18" />
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>
    </div>
    
    <!-- Sections -->
    <div v-for="(sectionData, sectionIndex) in sectionsArray" :key="sectionIndex" class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex justify-between items-center mb-4">
        <div>
          <h2 class="text-lg font-medium flex items-center">
            {{ sectionData.title }}
            <span v-if="sectionData.required" class="ml-2 px-2 py-0.5 bg-blue-100 text-blue-800 text-xs rounded-full">Required</span>
          </h2>
          <p class="text-sm text-gray-500">{{ sectionData.description }}</p>
        </div>
        <div class="flex">
          <button class="text-indigo-600 hover:text-indigo-800 flex items-center text-sm mr-2"
            @click="moveSection(sectionIndex, 'up')"
            :disabled="sectionIndex === 0">
            <ChevronUp class="mr-1" size="16" /> Move Up
          </button>
          <button class="text-indigo-600 hover:text-indigo-800 flex items-center text-sm mr-2"
            @click="moveSection(sectionIndex, 'down')"
            :disabled="sectionIndex === sectionsArray.length - 1">
            <ChevronDown class="mr-1" size="16" /> Move Down
          </button>
          <button class="text-gray-500 hover:text-gray-700"
            @click="openSectionSettings(sectionIndex)">
            <Settings size="16" />
          </button>
        </div>
      </div>
      
      <!-- Fields -->
      <div class="space-y-4 mb-4">
        <div v-for="(field, fieldIndex) in sectionData.fields" :key="fieldIndex"
          class="flex items-center p-3 border rounded-lg group hover:border-indigo-200 hover:bg-indigo-50">
          <div class="flex-1">
            <div class="font-medium flex items-center">
              {{ field.label }}
              <span v-if="field.required" class="ml-2 w-1.5 h-1.5 bg-red-500 rounded-full"></span>
              <HelpCircle class="ml-2 text-gray-400" size="16" :title="field.description" />
            </div>
            <div class="text-sm text-gray-500 flex items-center">
              <span>{{ getFieldTypeName(field.type) }}</span>
              <span v-if="field.options" class="ml-2 text-gray-400">
                ({{ getFieldOptionsCount(field.options) }} options)
              </span>
            </div>
          </div>
          <div class="flex opacity-0 group-hover:opacity-100 transition-opacity">
            <button class="p-1 text-gray-400 hover:text-gray-600 mr-1"
              @click="editField(sectionIndex, fieldIndex)">
              <Edit size="16" />
            </button>
            <button class="p-1 text-gray-400 hover:text-red-600"
              @click="deleteField(sectionIndex, fieldIndex)">
              <Trash2 size="16" />
            </button>
          </div>
        </div>
      </div>
      
      <!-- Add Field Button -->
      <button class="flex items-center text-indigo-600 hover:text-indigo-800 mt-2"
        @click="addField(sectionIndex)">
        <PlusCircle class="mr-1" size="16" /> Add Field
      </button>
    </div>
    
    <!-- Add new section button -->
    <button class="flex items-center text-indigo-600 hover:text-indigo-800 mb-6"
      @click="addSection">
      <PlusCircle class="mr-1" size="16" /> Add New Section
    </button>
    
    <!-- Save and Cancel Buttons -->
    <div class="flex justify-end mt-6">
      <button class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 mr-2"
        @click="goBack">
        Cancel
      </button>
      <button class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
        @click="saveConfiguration"
        :disabled="saving">
        {{ saving ? 'Saving...' : 'Save Coding Sheet' }}
      </button>
    </div>
    
    <!-- Field Edit Modal -->
    <FieldEditModal 
      v-if="showFieldModal"
      :field="fieldForm"
      :isEdit="editingIndex !== null"
      @close="closeFieldModal"
      @save="saveField"
    />
    
    <!-- Section Settings Modal -->
    <SectionSettingsModal 
      v-if="showSectionModal"
      :section="sectionForm"
      @close="closeSectionModal"
      @save="saveSection"
      @delete="confirmDeleteSection"
    />
  </div>
</template>

<script>
import { API_ROUTES } from '../config.js';
import { codingService } from '../services/api.js';
import FieldEditModal from './modals/FieldEditModal.vue';
import SectionSettingsModal from './modals/SectionSettingsModal.vue';
import { 
  ArrowLeft, 
  Copy, 
  Save, 
  ChevronUp, 
  ChevronDown, 
  Settings, 
  HelpCircle, 
  Edit, 
  Trash2, 
  PlusCircle
} from 'lucide-vue-next';

export default {
  name: 'CodingSheet',
  components: {
    ArrowLeft, 
    Copy, 
    Save, 
    ChevronUp, 
    ChevronDown, 
    Settings, 
    HelpCircle, 
    Edit, 
    Trash2, 
    PlusCircle,
    FieldEditModal,
    SectionSettingsModal
  },
  props: {
    projectId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      projectName: '',
      projectDescription: '',
      codingSheetId: null,
      originalSections: null, // To track changes
      hasUnsavedChanges: false,
      sectionsArray: [], // Array of sections with fields
      
      // Field edit modal
      showFieldModal: false,
      editingSection: null,
      editingIndex: null,
      fieldForm: {
        name: '',
        label: '',
        type: 'text',
        description: '',
        required: false,
        options: '',
        autoExtract: true,
        regexPattern: ''
      },
      
      // Section edit modal
      showSectionModal: false,
      editingSectionIndex: null,
      sectionForm: {
        title: '',
        description: '',
        name: '',
        required: false,
        fields: []
      },
      
      saving: false
    }
  },
  mounted() {
    // Load project details and existing coding sheet if any
    this.loadProjectData();
  },
  watch: {
    sectionsArray: {
      handler() {
        // Mark as having unsaved changes
        this.hasUnsavedChanges = true;
      },
      deep: true
    }
  },
  methods: {
    async loadProjectData() {
      try {
        // Fetch project details
        const projectResponse = await fetch(API_ROUTES.PROJECTS.GET_BY_ID(this.projectId));
        
        if (!projectResponse.ok) {
          if (projectResponse.status === 404) {
            console.warn(`Project with ID ${this.projectId} not found`);
            // Redirect back to projects list
            this.$emit('back-to-project');
            return;
          }
          throw new Error('Failed to load project details');
        }
        
        const projectData = await projectResponse.json();
        this.projectName = projectData.name;
        this.projectDescription = projectData.description;
        
        // Check if a coding sheet already exists for this project
        try {
          const codingSheet = await codingService.getCodingSheetByProject(this.projectId);
          this.codingSheetId = codingSheet.id;
          
          // Convert sections from object to array format for easier reordering
          if (codingSheet.sections && Array.isArray(codingSheet.sections)) {
            this.sectionsArray = codingSheet.sections;
          } else {
            // Set default sections if no sections or incorrect format
            this.setDefaultSections();
          }
        } catch (error) {
          // If 404 Not Found, create a default coding sheet
          if (error.message && error.message.includes('404')) {
            console.log('No coding sheet found for this project yet. Using default template.');
            this.setDefaultSections();
          } else {
            console.error('Error checking for existing coding sheet:', error);
            this.setDefaultSections();
          }
        }
      } catch (error) {
        console.error('Error loading project data:', error);
        alert('There was a problem loading the project data. Please try again.');
      }
    },
    
    setDefaultSections() {
      // Create default sections in array format
      this.sectionsArray = [
        {
          name: "basic",
          title: "Basic Information",
          description: "Study identification and basic metadata",
          required: true,
          fields: [
            { name: 'authors', label: 'Authors', type: 'text', description: 'Authors of the paper in citation format', required: true },
            { name: 'publicationYear', label: 'Publication Year', type: 'number', description: 'Year the paper was published', required: true },
            { name: 'journal', label: 'Journal', type: 'text', description: 'Name of the journal where the paper was published', required: true },
            { name: 'doi', label: 'DOI', type: 'text', description: 'Digital Object Identifier for the paper', required: false }
          ]
        },
        {
          name: "methodology",
          title: "Methodology Fields",
          description: "Study design and methodological characteristics",
          required: false,
          fields: [
            { name: 'studyDesign', label: 'Study Design', type: 'select', description: 'Type of study design', required: true, options: "Meta-Analysis\nRCT\nCohort Study\nCase-Control\nSystematic Review" },
            { name: 'numberOfStudies', label: 'Number of Studies', type: 'number', description: 'Number of studies included in the meta-analysis', required: true },
            { name: 'sampleSize', label: 'Total Sample Size', type: 'number', description: 'Total number of participants across all included studies', required: true },
            { name: 'qualityAssessment', label: 'Quality Assessment Tool', type: 'select', description: 'Tool used to assess the quality of included studies', required: false, options: "Cochrane Risk of Bias\nPRISMA\nROBINS-I\nNewcastle-Ottawa Scale\nOther" }
          ]
        },
        {
          name: "results",
          title: "Results Fields",
          description: "Outcome measures and effect sizes",
          required: false,
          fields: [
            { name: 'effectSize', label: 'Overall Effect Size', type: 'text', description: 'Primary effect size measure (e.g., g = 0.82)', required: true, autoExtract: true, regexPattern: "(g|d|r|η²)\\s*=\\s*([\\d\\.-]+)" },
            { name: 'confidenceInterval', label: 'Confidence Interval', type: 'text', description: 'Confidence interval for the primary effect size', required: true },
            { name: 'pValue', label: 'Statistical Significance', type: 'text', description: 'P-value or significance level', required: true },
            { name: 'heterogeneity', label: 'Heterogeneity (I²)', type: 'text', description: 'I² statistic for heterogeneity assessment', required: false },
            { name: 'moderators', label: 'Moderators Identified', type: 'textarea', description: 'Variables identified as significant moderators', required: false }
          ]
        }
      ];
      
      // Set original state
      this.hasUnsavedChanges = false;
    },
    
    getFieldTypeName(type) {
      const typeMap = {
        'text': 'Text',
        'number': 'Number',
        'date': 'Date',
        'select': 'Dropdown',
        'textarea': 'Text Area',
        'boolean': 'Checkbox',
        'radio': 'Radio Button'
      };
      return typeMap[type] || type;
    },
    
    moveSection(index, direction) {
      if (direction === 'up' && index > 0) {
        // Swap with previous section
        const temp = this.sectionsArray[index];
        this.$set(this.sectionsArray, index, this.sectionsArray[index - 1]);
        this.$set(this.sectionsArray, index - 1, temp);
      } else if (direction === 'down' && index < this.sectionsArray.length - 1) {
        // Swap with next section
        const temp = this.sectionsArray[index];
        this.$set(this.sectionsArray, index, this.sectionsArray[index + 1]);
        this.$set(this.sectionsArray, index + 1, temp);
      }
    },
    
    addSection() {
      const newSectionName = `section_${Date.now()}`;
      const newSection = {
        name: newSectionName,
        title: "New Section",
        description: "Add a description for this section",
        required: false,
        fields: []
      };
      
      this.sectionsArray.push(newSection);
      
      // Open section settings to configure the new section
      this.openSectionSettings(this.sectionsArray.length - 1);
    },
    
    openSectionSettings(sectionIndex) {
      this.editingSectionIndex = sectionIndex;
      const section = this.sectionsArray[sectionIndex];
      
      this.sectionForm = {
        title: section.title,
        description: section.description,
        name: section.name,
        required: section.required,
        fields: section.fields
      };
      
      this.showSectionModal = true;
    },
    
    saveSection(sectionData) {
      if (this.editingSectionIndex !== null) {
        // Update existing section
        const updatedSection = {
          ...this.sectionsArray[this.editingSectionIndex],
          title: sectionData.title,
          description: sectionData.description,
          name: sectionData.name,
          required: sectionData.required
        };
        
        this.$set(this.sectionsArray, this.editingSectionIndex, updatedSection);
      }
      
      this.closeSectionModal();
    },
    
    confirmDeleteSection() {
      this.$emit('request-confirmation', {
        title: 'Delete Section',
        message: 'Are you sure you want to delete this section and all its fields? This action cannot be undone.',
        confirmText: 'Delete',
        cancelText: 'Cancel',
        onConfirm: () => {
          this.deleteSection();
        }
      });
    },
    
    deleteSection() {
      if (this.editingSectionIndex !== null) {
        this.sectionsArray.splice(this.editingSectionIndex, 1);
        this.closeSectionModal();
      }
    },
    
    closeSectionModal() {
      this.showSectionModal = false;
      this.editingSectionIndex = null;
      this.sectionForm = {
        title: '',
        description: '',
        name: '',
        required: false,
        fields: []
      };
    },
    
    addField(sectionIndex) {
      this.editingSection = sectionIndex;
      this.editingIndex = null;
      this.fieldForm = {
        name: '',
        label: '',
        type: 'text',
        description: '',
        required: false,
        options: '',
        autoExtract: true,
        regexPattern: ''
      };
      this.showFieldModal = true;
    },
    
    editField(sectionIndex, fieldIndex) {
      this.editingSection = sectionIndex;
      this.editingIndex = fieldIndex;
      
      const field = this.sectionsArray[sectionIndex].fields[fieldIndex];
      this.fieldForm = {
        name: field.name || '',
        label: field.label || '',
        type: field.type || 'text',
        description: field.description || '',
        required: field.required || false,
        options: field.options || '',
        autoExtract: field.autoExtract !== undefined ? field.autoExtract : true,
        regexPattern: field.regexPattern || ''
      };
      
      this.showFieldModal = true;
    },
    
    deleteField(sectionIndex, fieldIndex) {
      this.$emit('request-confirmation', {
        title: 'Delete Field',
        message: 'Are you sure you want to delete this field? This action cannot be undone.',
        confirmText: 'Delete',
        cancelText: 'Cancel',
        onConfirm: () => {
          this.sectionsArray[sectionIndex].fields.splice(fieldIndex, 1);
        }
      });
    },
    
    closeFieldModal() {
      this.showFieldModal = false;
      this.editingSection = null;
      this.editingIndex = null;
    },
    
    saveField(fieldData) {
      if (this.editingIndex !== null) {
        // Update existing field
        this.$set(this.sectionsArray[this.editingSection].fields, this.editingIndex, fieldData);
      } else {
        // Add new field
        this.sectionsArray[this.editingSection].fields.push(fieldData);
      }
      
      this.closeFieldModal();
    },
    
    goBack() {
      if (this.hasUnsavedChanges) {
        this.$emit('request-confirmation', {
          title: 'Unsaved Changes',
          message: 'You have unsaved changes. Are you sure you want to leave without saving?',
          confirmText: 'Leave',
          cancelText: 'Stay',
          onConfirm: () => {
            this.$emit('back-to-project');
          }
        });
      } else {
        this.$emit('back-to-project');
      }
    },
    
    duplicateCodingSheet() {
      this.$emit('request-confirmation', {
        title: 'Duplicate Coding Sheet',
        message: 'This will create a copy of this coding sheet for a different project. Do you want to continue?',
        confirmText: 'Continue',
        cancelText: 'Cancel',
        onConfirm: () => {
          // To be implemented: open project selection modal and create a copy
          alert('Feature to be implemented. This would allow you to select another project and create a copy of this coding sheet.');
        }
      });
    },
    
    async saveConfiguration() {
      this.saving = true;
      
      try {
        // Format the data for API
        const codingSheet = {
          name: `${this.projectName} Coding Sheet`,
          description: `Coding sheet for project: ${this.projectName}`,
          project_id: this.projectId,
          sections: this.sectionsArray.map(section => ({
            ...section,
            fields: section.fields.map(field => {
              // Convert string options to arrays if present
              const processedField = { ...field };
              if (field.options && typeof field.options === 'string') {
                processedField.options = field.options.split('\n').filter(opt => opt.trim());
              }
              return processedField;
            })
          }))
        };
        
        let response;
        
        if (this.codingSheetId) {
          // Update existing coding sheet
          response = await codingService.updateCodingSheet(this.codingSheetId, codingSheet);
        } else {
          // Create new coding sheet
          response = await codingService.createCodingSheet(codingSheet);
        }
        
        this.codingSheetId = response.id;
        
        // Mark as no longer having unsaved changes
        this.hasUnsavedChanges = false;
        
        // Show success message
        alert('Coding sheet configuration saved successfully!');
        
        // Go back to project detail
        this.$emit('back-to-project');
      } catch (err) {
        console.error('Error saving coding sheet:', err);
        alert('Failed to save configuration. Please try again: ' + err.message);
      } finally {
        this.saving = false;
      }
    }
  }
}
</script>

<style scoped>
.transition-opacity {
  transition: opacity 0.2s ease-in-out;
}
</style>
