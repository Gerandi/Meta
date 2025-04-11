<template>
  <div class="border-b border-gray-100 pb-2 cursor-pointer hover:bg-gray-50 -mx-4 px-4" @click="$emit('click')">
    <div class="font-medium text-gray-800">{{ title }}</div>
    <div class="flex text-sm text-gray-500">
      <span>{{ papers }} papers</span>
      <span class="mx-2">•</span>
      <span>Updated {{ lastUpdated }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProjectItem',
  props: {
    title: {
      type: String,
      required: true
    },
    papers: {
      type: [String, Number],
      required: true
    },
    lastUpdated: {
      type: String,
      required: true
    }
  }
}
</script>
