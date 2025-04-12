<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
      <h2 class="text-xl font-bold mb-4">{{ title }}</h2>
      <p class="mb-6 text-gray-700">{{ message }}</p>

      <div class="flex justify-end">
        <button
          class="text-gray-700 px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-100 mr-2"
          @click="cancel"
        >
          {{ cancelText }}
        </button>
        <button
          class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
          @click="confirm"
        >
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmationModal',
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      default: 'Confirm Action',
    },
    message: {
      type: String,
      required: true,
    },
    confirmText: {
      type: String,
      default: 'Confirm',
    },
    cancelText: {
      type: String,
      default: 'Cancel',
    },
  },
  emits: ['confirm', 'cancel'],
  methods: {
    confirm() {
      this.$emit('confirm');
    },
    cancel() {
      this.$emit('cancel');
    },
  },
};
</script>