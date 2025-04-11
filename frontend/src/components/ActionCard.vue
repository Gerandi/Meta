<template>
  <div 
    class="border rounded-lg p-4 hover:bg-gray-50 cursor-pointer transition-colors"
    @click="$emit('click')"
  >
    <div class="text-indigo-600 mb-2">
      <font-awesome-icon :icon="icon" size="lg" />
    </div>
    <div class="font-medium mb-1">{{ title }}</div>
    <div class="text-sm text-gray-500">{{ description }}</div>
  </div>
</template>

<script>
export default {
  name: 'ActionCard',
  props: {
    icon: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    }
  }
}
</script>
