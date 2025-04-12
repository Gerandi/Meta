<template>
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
                ({{ field.options.split('\n').length }} options)
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
    <div v-if="showFieldModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg w-full max-w-md">
        <div class="p-4 border-b flex justify-between items-center">
          <h3 class="font-medium">{{ editingIndex !== null ? 'Edit Field' : 'Add Field' }}</h3>
          <button class="text-gray-400 hover:text-gray-600" @click="closeFieldModal">
            <X size="18" />
          </button>
        </div>
        
        <div class="p-4">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Field Name
              </label>
              <input 
                v-model="fieldForm.label"
                type="text" 
                class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                placeholder="e.g., Authors"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Field Type
              </label>
              <select 
                v-model="fieldForm.type"
                class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              >
                <option value="text">Text</option>
                <option value="number">Number</option>
                <option value="date">Date</option>
                <option value="select">Dropdown</option>
                <option value="textarea">Text Area</option>
                <option value="boolean">Checkbox</option>
                <option value="radio">Radio Button</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea 
                v-model="fieldForm.description"
                class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                rows="2"
                placeholder="e.g., Authors of the paper in citation format"
              ></textarea>
            </div>
            
            <div v-if="fieldForm.type === 'select'" class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Options (one per line)</label>
              <textarea 
                v-model="fieldForm.options" 
                class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                rows="4"
                placeholder="Option 1&#10;Option 2&#10;Option 3"
              ></textarea>
            </div>
            
            <div class="flex items-center">
              <input 
                type="checkbox" 
                id="required" 
                v-model="fieldForm.required"
                class="mr-2"
              />
              <label for="required" class="text-sm text-gray-700">
                Required field
              </label>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Extraction Settings
              </label>
              <div class="border rounded-lg p-3 bg-gray-50">
                <div class="flex items-center mb-2">
                  <input 
                    type="checkbox" 
                    id="auto-extract" 
                    v-model="fieldForm.autoExtract"
                    class="mr-2"
                  />
                  <label for="auto-extract" class="text-sm text-gray-700">
                    Enable automated extraction
                  </label>
                </div>
                <div class="mb-2">
                  <label class="block text-sm text-gray-700 mb-1">
                    Regular Expression Pattern (optional)
                  </label>
                  <input 
                    type="text" 
                    v-model="fieldForm.regexPattern"
                    class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                    placeholder="e.g., (d|g)\s*=\s*([\d\.]+)"
                  />
                </div>
                <div class="text-xs text-gray-500">
                  Regex pattern to help identify the value in the text. Leave blank to use AI-based extraction.
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="p-4 border-t flex justify-end">
          <button 
            class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 mr-2"
            @click="closeFieldModal"
          >
            Cancel
          </button>
          <button 
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            @click="saveField"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
    
    <!-- Section Settings Modal -->
    <div v-if="showSectionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg w-full max-w-md">
        <div class="p-4 border-b flex justify-between items-center">
          <h3 class="font-medium">Section Settings</h3>
          <button class="text-gray-400 hover:text-gray-600" @click="closeSectionModal">
            <X size="18" />
          </button>
        </div>
        
        <div class="p-4">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Section Title
              </label>
              <input 
                v-model="sectionForm.title"
                type="text" 
                class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea 
                v-model="sectionForm.description"
                class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                rows="2"
              ></textarea>
            </div>
            
            <div class="flex items-center">
              <input 
                type="checkbox" 
                id="section-required" 
                v-model="sectionForm.required"
                class="mr-2"
              />
              <label for="section-required" class="text-sm text-gray-700">
                Required section
              </label>
            </div>

            <div v-if="sectionForm.fields && sectionForm.fields.length > 0" class="flex justify-between pt-4 border-t">
              <span class="text-sm font-medium text-gray-700">
                Contains {{ sectionForm.fields.length }} field(s)
              </span>
            </div>
          </div>
        </div>
        
        <div class="p-4 border-t flex justify-end">
          <button 
            class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 mr-auto"
            @click="confirmDeleteSection"
          >
            Delete Section
          </button>
          <button 
            class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 mr-2"
            @click="closeSectionModal"
          >
            Cancel
          </button>
          <button 
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            @click="saveSection"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { API_ROUTES } from '../config.js';
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
  PlusCircle, 
  X
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
    X
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
          const codingSheetResponse = await fetch(`${API_ROUTES.CODING.GET_BY_PROJECT_ID(this.projectId)}`);
          
          if (codingSheetResponse.ok) {
            // Existing coding sheet found, load it
            const codingSheetData = await codingSheetResponse.json();
            this.codingSheetId = codingSheetData.id;
            
            // Convert sections from object to array format for easier reordering
            if (codingSheetData.sections && Array.isArray(codingSheetData.sections)) {
              this.sectionsArray = codingSheetData.sections;
            } else {
              // Set default sections if no sections or incorrect format
              this.setDefaultSections();
            }
          } else if (codingSheetResponse.status === 404) {
            console.log('No coding sheet found for this project yet. Using default template.');
            this.setDefaultSections();
          } else {
            console.warn(`Error fetching coding sheet: ${codingSheetResponse.status}`);
            this.setDefaultSections();
          }
        } catch (codingSheetError) {
          console.error('Error checking for existing coding sheet:', codingSheetError);
          this.setDefaultSections();
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
    
    saveSection() {
      if (!this.sectionForm.title.trim()) {
        alert('Section title is required');
        return;
      }
      
      if (this.editingSectionIndex !== null) {
        // Update existing section
        const updatedSection = {
          ...this.sectionsArray[this.editingSectionIndex],
          title: this.sectionForm.title,
          description: this.sectionForm.description,
          required: this.sectionForm.required
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
    
    saveField() {
      if (!this.fieldForm.label.trim()) {
        alert('Field label is required');
        return;
      }
      
      // Generate a name from the label if not provided
      if (!this.fieldForm.name) {
        this.fieldForm.name = this.fieldForm.label
          .toLowerCase()
          .replace(/[^a-z0-9]/gi, '_');
      }
      
      const field = {
        name: this.fieldForm.name,
        label: this.fieldForm.label,
        type: this.fieldForm.type,
        description: this.fieldForm.description,
        required: this.fieldForm.required,
        autoExtract: this.fieldForm.autoExtract,
        regexPattern: this.fieldForm.regexPattern
      };
      
      if (field.type === 'select' && this.fieldForm.options) {
        field.options = this.fieldForm.options;
      }
      
      if (this.editingIndex !== null) {
        // Update existing field
        this.$set(this.sectionsArray[this.editingSection].fields, this.editingIndex, field);
      } else {
        // Add new field
        this.sectionsArray[this.editingSection].fields.push(field);
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
          projectId: this.projectId,
          sections: this.sectionsArray
        };
        
        // Determine if we're creating a new coding sheet or updating an existing one
        let apiUrl;
        let method;
        
        if (this.codingSheetId) {
          // Update existing coding sheet
          apiUrl = API_ROUTES.CODING.UPDATE(this.codingSheetId);
          method = 'PUT';
        } else {
          // Create new coding sheet
          apiUrl = API_ROUTES.CODING.CREATE;
          method = 'POST';
        }
        
        console.log(`Saving coding sheet with ${method} to ${apiUrl}`);
        
        const response = await fetch(apiUrl, {
          method: method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(codingSheet)
        });
        
        if (!response.ok) {
          if (response.status === 404) {
            throw new Error('API endpoint not found. The backend service might not be available.');
          }
          
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || `Failed to save coding sheet: ${response.statusText}`);
        }
        
        const savedCodingSheet = await response.json();
        this.codingSheetId = savedCodingSheet.id;
        
        // Mark as no longer having unsaved changes
        this.hasUnsavedChanges = false;
        
        // Show success message
        alert('Coding sheet configuration saved successfully!');
        
        // Go back to project detail
        this.goBack();
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
