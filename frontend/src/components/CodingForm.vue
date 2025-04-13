<template>
  <div class="bg-white flex flex-col h-full">
    <div class="p-4 border-b">
      <h2 class="font-medium mb-2">Coding Sheet</h2>
      <p class="text-sm text-gray-500">Extract data from the paper using the form below</p>
    </div>
    
    <div class="flex-1 p-4 overflow-auto">
      <template v-if="codingSheet && codingSheet.sections">
        <!-- Dynamic form based on coding sheet -->
        <div v-for="(section, sectionIndex) in codingSheet.sections" :key="sectionIndex" class="mb-6">
          <h3 class="font-medium mb-3">{{ section.title }}</h3>
          
          <div v-for="(field, fieldIndex) in section.fields" :key="fieldIndex" class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ field.label }}
              <span v-if="field.required" class="text-red-500">*</span>
            </label>
            
            <!-- Text input -->
            <input 
              v-if="field.type === 'text'"
              v-model="codingData[field.name]"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              :placeholder="field.description"
            />
            
            <!-- Number input -->
            <input 
              v-else-if="field.type === 'number'"
              v-model.number="codingData[field.name]"
              type="number" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              :placeholder="field.description"
            />
            
            <!-- Date input -->
            <input 
              v-else-if="field.type === 'date'"
              v-model="codingData[field.name]"
              type="date" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
            
            <!-- Select dropdown -->
            <select 
              v-else-if="field.type === 'select'"
              v-model="codingData[field.name]"
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            >
              <option value="">-- Select an option --</option>
              <option 
                v-for="(option, optionIndex) in getFieldOptions(field)" 
                :key="optionIndex" 
                :value="option"
              >
                {{ option }}
              </option>
            </select>
            
            <!-- Checkbox (boolean) -->
            <div v-else-if="field.type === 'boolean'" class="flex items-center">
              <input 
                type="checkbox" 
                :id="`field-${field.name}`" 
                v-model="codingData[field.name]"
                class="mr-2"
              />
              <label :for="`field-${field.name}`" class="text-sm text-gray-700">
                {{ field.description || 'Yes' }}
              </label>
            </div>
            
            <!-- Textarea -->
            <textarea 
              v-else-if="field.type === 'textarea'"
              v-model="codingData[field.name]"
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              rows="3"
              :placeholder="field.description"
            ></textarea>
          </div>
        </div>
      </template>
      
      <!-- Default form if no coding sheet is available -->
      <template v-else>
        <div class="mb-6">
          <h3 class="font-medium mb-3">Study Information</h3>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Authors
            </label>
            <input 
              v-model="codingData.authors"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Publication Year
            </label>
            <input 
              v-model="codingData.publicationYear"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Journal
            </label>
            <input 
              v-model="codingData.journal"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
        </div>
        
        <div class="mb-6">
          <h3 class="font-medium mb-3">Methodology</h3>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Study Design
            </label>
            <select 
              v-model="codingData.studyDesign"
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            >
              <option value="">-- Select an option --</option>
              <option value="meta-analysis">Meta-Analysis</option>
              <option value="rct">RCT</option>
              <option value="cohort">Cohort Study</option>
              <option value="case-control">Case-Control</option>
              <option value="systematic-review">Systematic Review</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Number of Studies
            </label>
            <input 
              v-model.number="codingData.numberOfStudies"
              type="number" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Total Sample Size
            </label>
            <input 
              v-model.number="codingData.sampleSize"
              type="number" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
        </div>
        
        <div class="mb-6">
          <h3 class="font-medium mb-3">Study Findings</h3>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Overall Effect Size
            </label>
            <input 
              v-model="codingData.effectSize"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              placeholder="e.g., g = 0.82"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Confidence Interval
            </label>
            <input 
              v-model="codingData.confidenceInterval"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              placeholder="e.g., 95% CI [0.71, 0.93]"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Statistical Significance
            </label>
            <input 
              v-model="codingData.pValue"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              placeholder="e.g., p < .001"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Moderators Identified
            </label>
            <textarea 
              v-model="codingData.moderators"
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              rows="3"
            ></textarea>
          </div>
        </div>
      </template>
    </div>
    
    <div class="p-4 border-t flex justify-end">
      <button 
        class="px-4 py-2 rounded-lg bg-gray-200 text-gray-800 mr-2 hover:bg-gray-300"
        @click="resetForm"
      >
        Reset
      </button>
      <button 
        class="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 flex items-center"
        @click="saveData"
        :disabled="saving"
      >
        <Save class="mr-1" size="18" /> {{ saving ? 'Saving...' : 'Save Data' }}
      </button>
    </div>
  </div>
</template>

<script>
import { API_ROUTES } from '../config.js';
import { Save } from 'lucide-vue-next';

export default {
  name: 'CodingForm',
  components: {
    Save
  },
  props: {
    paper: {
      type: Object,
      required: true
    },
    projectId: {
      type: Number,
      required: false,
      default: null
    }
  },
  data() {
    return {
      saving: false,
      codingSheet: null,
      codingData: {},
      savedCoding: null,
      defaultCodingData: {
        authors: '',
        publicationYear: '',
        journal: '',
        studyDesign: '',
        numberOfStudies: null,
        sampleSize: null,
        effectSize: '',
        confidenceInterval: '',
        pValue: '',
        moderators: '',
        riskOfBias: 'low',
        prismaAdherence: 'not-reported',
        qualityNotes: ''
      }
    }
  },
  mounted() {
    // Load the coding sheet for this project (if project ID is provided)
    this.loadCodingSheet();
    // Check if this paper already has coding data saved
    this.loadExistingCoding();
  },
  methods: {
    async loadCodingSheet() {
      if (!this.projectId) return;
      
      try {
        const response = await fetch(API_ROUTES.CODING.GET_BY_PROJECT_ID(this.projectId));
        
        if (response.ok) {
          this.codingSheet = await response.json();
          console.log('Loaded coding sheet:', this.codingSheet);
          
          // Initialize coding data object with fields from the coding sheet
          this.initializeCodingData();
        } else {
          console.warn('No coding sheet found for this project. Using default form.');
          // Use default form
          this.codingData = { ...this.defaultCodingData };
          this.prefillForm();
        }
      } catch (err) {
        console.error('Error loading coding sheet:', err);
        // Use default form on error
        this.codingData = { ...this.defaultCodingData };
        this.prefillForm();
      }
    },
    
    async loadExistingCoding() {
      if (!this.paper.id) return;
      
      try {
        const response = await fetch(API_ROUTES.CODING.GET_FOR_PAPER(this.paper.id));
        
        if (response.ok) {
          this.savedCoding = await response.json();
          console.log('Loaded existing coding:', this.savedCoding);
          
          // Merge existing coding data with our coding data object
          if (this.savedCoding.data) {
            this.codingData = { ...this.codingData, ...this.savedCoding.data };
          }
        } else {
          console.log('No existing coding found for this paper.');
        }
      } catch (err) {
        console.error('Error loading existing coding:', err);
      }
    },
    
    initializeCodingData() {
      // Initialize coding data with empty values
      if (!this.codingSheet) {
        this.codingData = { ...this.defaultCodingData };
        return;
      }
      
      // Initialize from coding sheet sections and fields
      const newCodingData = {};
      
      this.codingSheet.sections.forEach(section => {
        section.fields.forEach(field => {
          // Initialize with empty value based on field type
          switch (field.type) {
            case 'number':
              newCodingData[field.name] = null;
              break;
            case 'boolean':
              newCodingData[field.name] = false;
              break;
            case 'select':
              // Get first option as default (if any)
              const options = this.getFieldOptions(field);
              newCodingData[field.name] = options.length > 0 ? options[0] : '';
              break;
            default:
              newCodingData[field.name] = '';
          }
        });
      });
      
      this.codingData = newCodingData;
      this.prefillForm();
    },
    
    getFieldOptions(field) {
      if (!field.options) return [];
      
      // If options is a string, split by newlines
      if (typeof field.options === 'string') {
        return field.options.split('\n').filter(option => option.trim());
      }
      
      // If options is already an array, return it
      if (Array.isArray(field.options)) {
        return field.options;
      }
      
      return [];
    },
    
    formatAuthors(authors) {
      if (!authors || authors.length === 0) return 'Unknown Authors';
      
      if (authors.length <= 3) {
        return authors.map(a => a.name).join(', ');
      } else {
        return `${authors[0].name}, et al.`;
      }
    },
    
    getYear(dateString) {
      if (!dateString) return '';
      try {
        return new Date(dateString).getFullYear().toString();
      } catch (e) {
        return '';
      }
    },
    
    prefillForm() {
      // Prefill form with paper metadata
      if (this.paper) {
        // Set common metadata fields that exist in both default form and coding sheet
        const commonFields = {
          authors: this.paper.authors ? this.formatAuthors(this.paper.authors) : '',
          publicationYear: this.paper.publication_date ? this.getYear(this.paper.publication_date) : '',
          journal: this.paper.journal || '',
        };
        
        // Apply common fields to coding data
        Object.keys(commonFields).forEach(key => {
          if (key in this.codingData) {
            this.codingData[key] = commonFields[key];
          }
        });
        
        // Try to auto-detect study design from title or abstract
        if ('studyDesign' in this.codingData) {
          const titleLower = this.paper.title?.toLowerCase() || '';
          if (titleLower.includes('meta-analysis')) {
            this.codingData.studyDesign = 'meta-analysis';
          } else if (titleLower.includes('systematic review')) {
            this.codingData.studyDesign = 'systematic-review';
          } else if (titleLower.includes('randomized') || titleLower.includes('rct')) {
            this.codingData.studyDesign = 'rct';
          }
        }
      }
    },
    
    resetForm() {
      this.initializeCodingData();
      this.prefillForm();
    },
    
    async saveData() {
      this.saving = true;
      
      try {
        // Prepare the data to save
        const payload = {
          paper_id: this.paper.id,
          sheet_id: this.codingSheet?.id,
          data: this.codingData
        };
        
        // If we already have saved coding, update it
        let url = API_ROUTES.CODING.SAVE_PAPER_CODING;
        let method = 'POST';
        
        if (this.savedCoding && this.savedCoding.id) {
          url = `${API_ROUTES.CODING.UPDATE(this.savedCoding.id)}`;
          method = 'PUT';
          payload.id = this.savedCoding.id;
        }
        
        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || 'Failed to save coding data');
        }
        
        const savedData = await response.json();
        this.savedCoding = savedData;
        
        // Show success message
        alert('Coding data saved successfully!');
        
        // Emit event to notify parent component
        this.$emit('saved');
      } catch (err) {
        console.error('Error saving coding data:', err);
        alert('Failed to save coding data: ' + err.message);
      } finally {
        this.saving = false;
      }
    }
  }
}
</script>
