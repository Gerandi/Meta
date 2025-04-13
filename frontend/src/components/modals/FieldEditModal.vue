<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md">
      <div class="p-4 border-b flex justify-between items-center">
        <h3 class="font-medium">{{ isEdit ? 'Edit Field' : 'Add Field' }}</h3>
        <button class="text-gray-400 hover:text-gray-600" @click="$emit('close')">
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
              v-model="formData.label"
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
              v-model="formData.type"
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
              v-model="formData.description"
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              rows="2"
              placeholder="e.g., Authors of the paper in citation format"
            ></textarea>
          </div>
          
          <div v-if="formData.type === 'select'" class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Options (one per line)</label>
            <textarea 
              v-model="formData.options" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              rows="4"
              placeholder="Option 1&#10;Option 2&#10;Option 3"
            ></textarea>
          </div>
          
          <div class="flex items-center">
            <input 
              type="checkbox" 
              id="required" 
              v-model="formData.required"
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
                  v-model="formData.autoExtract"
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
                  v-model="formData.regexPattern"
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
          @click="$emit('close')"
        >
          Cancel
        </button>
        <button 
          class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          @click="saveField"
          :disabled="!isFormValid"
        >
          Save Changes
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { X } from 'lucide-vue-next';

export default {
  name: 'FieldEditModal',
  components: {
    X
  },
  props: {
    field: {
      type: Object,
      default: () => ({
        name: '',
        label: '',
        type: 'text',
        description: '',
        required: false,
        options: '',
        autoExtract: true,
        regexPattern: ''
      })
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      formData: { ...this.field }
    };
  },
  computed: {
    isFormValid() {
      return this.formData.label.trim() !== '';
    }
  },
  watch: {
    field: {
      handler(newField) {
        this.formData = { ...newField };
      },
      deep: true
    }
  },
  methods: {
    saveField() {
      if (!this.isFormValid) return;
      
      // Generate a name from the label if not provided
      if (!this.formData.name) {
        this.formData.name = this.formData.label
          .toLowerCase()
          .replace(/[^a-z0-9]/gi, '_');
      }
      
      this.$emit('save', this.formData);
    }
  }
}
</script>
