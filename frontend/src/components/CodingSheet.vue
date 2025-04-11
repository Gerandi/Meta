<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">Coding Sheet Configuration</h1>
    
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex justify-between items-center mb-4">
        <div>
          <h2 class="font-medium">Basic Information</h2>
          <p class="text-sm text-gray-500">Configure fields for study identification and basic metadata</p>
        </div>
      </div>
      
      <div class="space-y-4">
        <div v-for="(field, index) in sections.basic" :key="index" class="flex items-center p-3 border rounded-lg">
          <div class="flex-1">
            <div class="font-medium">{{ field.label }}</div>
            <div class="text-sm text-gray-500">{{ field.description }}</div>
          </div>
          <div class="flex">
            <button class="p-1 text-gray-400 hover:text-gray-600 mr-1" @click="editField('basic', index)">
              <font-awesome-icon icon="edit" />
            </button>
            <button class="p-1 text-gray-400 hover:text-red-600" @click="deleteField('basic', index)">
              <font-awesome-icon icon="trash" />
            </button>
          </div>
        </div>
        
        <button class="flex items-center text-indigo-600 hover:text-indigo-800 mt-2" @click="addField('basic')">
          <font-awesome-icon icon="plus-circle" class="mr-1" /> Add Field
        </button>
      </div>
    </div>
    
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex justify-between items-center mb-4">
        <div>
          <h2 class="font-medium">Methodology Fields</h2>
          <p class="text-sm text-gray-500">Configure fields for methodological information</p>
        </div>
      </div>
      
      <div class="space-y-4">
        <div v-for="(field, index) in sections.methodology" :key="index" class="flex items-center p-3 border rounded-lg">
          <div class="flex-1">
            <div class="font-medium">{{ field.label }}</div>
            <div class="text-sm text-gray-500">{{ field.description }}</div>
          </div>
          <div class="flex">
            <button class="p-1 text-gray-400 hover:text-gray-600 mr-1" @click="editField('methodology', index)">
              <font-awesome-icon icon="edit" />
            </button>
            <button class="p-1 text-gray-400 hover:text-red-600" @click="deleteField('methodology', index)">
              <font-awesome-icon icon="trash" />
            </button>
          </div>
        </div>
        
        <button class="flex items-center text-indigo-600 hover:text-indigo-800 mt-2" @click="addField('methodology')">
          <font-awesome-icon icon="plus-circle" class="mr-1" /> Add Field
        </button>
      </div>
    </div>
    
    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex justify-between items-center mb-4">
        <div>
          <h2 class="font-medium">Results Fields</h2>
          <p class="text-sm text-gray-500">Configure fields for study findings and results</p>
        </div>
      </div>
      
      <div class="space-y-4">
        <div v-for="(field, index) in sections.results" :key="index" class="flex items-center p-3 border rounded-lg">
          <div class="flex-1">
            <div class="font-medium">{{ field.label }}</div>
            <div class="text-sm text-gray-500">{{ field.description }}</div>
          </div>
          <div class="flex">
            <button class="p-1 text-gray-400 hover:text-gray-600 mr-1" @click="editField('results', index)">
              <font-awesome-icon icon="edit" />
            </button>
            <button class="p-1 text-gray-400 hover:text-red-600" @click="deleteField('results', index)">
              <font-awesome-icon icon="trash" />
            </button>
          </div>
        </div>
        
        <button class="flex items-center text-indigo-600 hover:text-indigo-800 mt-2" @click="addField('results')">
          <font-awesome-icon icon="plus-circle" class="mr-1" /> Add Field
        </button>
      </div>
    </div>
    
    <div class="mt-6 flex justify-end">
      <button 
        class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
        @click="saveConfiguration"
        :disabled="saving"
      >
        {{ saving ? 'Saving...' : 'Save Configuration' }}
      </button>
    </div>
    
    <!-- Field Edit Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-1/2 max-w-lg">
        <h3 class="text-lg font-medium mb-4">{{ editingField ? 'Edit Field' : 'Add Field' }}</h3>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Field Name</label>
          <input 
            v-model="fieldForm.name" 
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="e.g., authors"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Display Label</label>
          <input 
            v-model="fieldForm.label" 
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="e.g., Authors"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Field Type</label>
          <select 
            v-model="fieldForm.type" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          >
            <option value="text">Text</option>
            <option value="number">Number</option>
            <option value="select">Dropdown</option>
            <option value="textarea">Text Area</option>
            <option value="date">Date</option>
            <option value="boolean">Yes/No</option>
          </select>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <input 
            v-model="fieldForm.description" 
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="e.g., Text field for paper authors"
          />
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
        
        <div class="mb-4">
          <label class="flex items-center">
            <input type="checkbox" v-model="fieldForm.required" class="mr-2">
            <span class="text-sm text-gray-700">Required field</span>
          </label>
        </div>
        
        <div class="flex justify-end">
          <button 
            class="px-4 py-2 rounded-lg bg-gray-200 text-gray-800 mr-2 hover:bg-gray-300"
            @click="closeEditModal"
          >
            Cancel
          </button>
          <button 
            class="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700"
            @click="saveField"
          >
            Save Field
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CodingSheet',
  data() {
    return {
      sections: {
        basic: [
          { name: 'authors', label: 'Authors', type: 'text', description: 'Text field for paper authors', required: true },
          { name: 'publicationYear', label: 'Publication Year', type: 'number', description: 'Numeric field for publication year', required: true },
          { name: 'journal', label: 'Journal', type: 'text', description: 'Text field for journal name', required: true }
        ],
        methodology: [
          { name: 'studyDesign', label: 'Study Design', type: 'select', description: 'Dropdown with study design options', required: true, options: 'Meta-Analysis\nRCT\nCohort Study\nCase-Control\nSystematic Review' },
          { name: 'numberOfStudies', label: 'Number of Studies', type: 'number', description: 'Numeric field for number of included studies', required: false },
          { name: 'sampleSize', label: 'Total Sample Size', type: 'number', description: 'Numeric field for total participants', required: false }
        ],
        results: [
          { name: 'effectSize', label: 'Overall Effect Size', type: 'text', description: 'Text field for effect size measures', required: false },
          { name: 'confidenceInterval', label: 'Confidence Interval', type: 'text', description: 'Text field for confidence intervals', required: false },
          { name: 'pValue', label: 'Statistical Significance', type: 'text', description: 'Text field for p-values', required: false },
          { name: 'moderators', label: 'Moderators Identified', type: 'textarea', description: 'Text area for moderating variables', required: false }
        ]
      },
      showEditModal: false,
      editingSection: null,
      editingIndex: null,
      fieldForm: {
        name: '',
        label: '',
        type: 'text',
        description: '',
        required: false,
        options: ''
      },
      saving: false
    }
  },
  methods: {
    addField(section) {
      this.editingSection = section;
      this.editingIndex = null;
      this.fieldForm = {
        name: '',
        label: '',
        type: 'text',
        description: '',
        required: false,
        options: ''
      };
      this.showEditModal = true;
    },
    
    editField(section, index) {
      this.editingSection = section;
      this.editingIndex = index;
      
      const field = this.sections[section][index];
      this.fieldForm = {
        name: field.name,
        label: field.label,
        type: field.type,
        description: field.description,
        required: field.required,
        options: field.options || ''
      };
      
      this.showEditModal = true;
    },
    
    deleteField(section, index) {
      if (confirm('Are you sure you want to delete this field?')) {
        this.sections[section].splice(index, 1);
      }
    },
    
    closeEditModal() {
      this.showEditModal = false;
      this.editingSection = null;
      this.editingIndex = null;
    },
    
    saveField() {
      const field = {
        name: this.fieldForm.name,
        label: this.fieldForm.label,
        type: this.fieldForm.type,
        description: this.fieldForm.description,
        required: this.fieldForm.required
      };
      
      if (field.type === 'select' && this.fieldForm.options) {
        field.options = this.fieldForm.options;
      }
      
      if (this.editingIndex !== null) {
        // Update existing field
        this.sections[this.editingSection][this.editingIndex] = field;
      } else {
        // Add new field
        this.sections[this.editingSection].push(field);
      }
      
      this.closeEditModal();
    },
    
    async saveConfiguration() {
      this.saving = true;
      
      try {
        // Format the data for API
        const codingSheet = {
          name: "Default Coding Sheet",
          description: "Default coding sheet for meta-analysis",
          sections: [
            {
              name: "basic",
              title: "Basic Information",
              description: "Study identification and basic metadata",
              fields: this.sections.basic
            },
            {
              name: "methodology",
              title: "Methodology",
              description: "Methodological information",
              fields: this.sections.methodology
            },
            {
              name: "results",
              title: "Results",
              description: "Study findings and results",
              fields: this.sections.results
            }
          ]
        };
        
        // Call to backend API
        // For now, just console log
        console.log('Saving coding sheet:', codingSheet);
        
        // Show success message
        alert('Configuration saved successfully!');
      } catch (err) {
        console.error('Error saving coding sheet:', err);
        alert('Failed to save configuration. Please try again.');
      } finally {
        this.saving = false;
      }
    }
  }
}
</script>
