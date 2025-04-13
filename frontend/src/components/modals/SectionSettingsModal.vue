<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md">
      <div class="p-4 border-b flex justify-between items-center">
        <h3 class="font-medium">Section Settings</h3>
        <button class="text-gray-400 hover:text-gray-600" @click="$emit('close')">
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
              v-model="formData.title"
              type="text" 
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea 
              v-model="formData.description"
              class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              rows="2"
            ></textarea>
          </div>
          
          <div class="flex items-center">
            <input 
              type="checkbox" 
              id="section-required" 
              v-model="formData.required"
              class="mr-2"
            />
            <label for="section-required" class="text-sm text-gray-700">
              Required section
            </label>
          </div>

          <div v-if="formData.fields && formData.fields.length > 0" class="flex justify-between pt-4 border-t">
            <span class="text-sm font-medium text-gray-700">
              Contains {{ formData.fields.length }} field(s)
            </span>
          </div>
        </div>
      </div>
      
      <div class="p-4 border-t flex justify-end">
        <button 
          class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 mr-auto"
          @click="$emit('delete')"
        >
          Delete Section
        </button>
        <button 
          class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 mr-2"
          @click="$emit('close')"
        >
          Cancel
        </button>
        <button 
          class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          @click="saveSection"
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
  name: 'SectionSettingsModal',
  components: {
    X
  },
  props: {
    section: {
      type: Object,
      default: () => ({
        name: '',
        title: '',
        description: '',
        required: false,
        fields: []
      })
    }
  },
  data() {
    return {
      formData: { ...this.section }
    };
  },
  computed: {
    isFormValid() {
      return this.formData.title.trim() !== '';
    }
  },
  watch: {
    section: {
      handler(newSection) {
        this.formData = { ...newSection };
      },
      deep: true
    }
  },
  methods: {
    saveSection() {
      if (!this.isFormValid) return;
      
      // Generate a name from the title if not provided
      if (!this.formData.name) {
        this.formData.name = this.formData.title
          .toLowerCase()
          .replace(/[^a-z0-9]/gi, '_');
      }
      
      this.$emit('save', this.formData);
    }
  }
}
</script>
