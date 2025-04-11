<template>
  <div class="bg-white rounded-lg p-6 shadow">
    <div class="text-sm text-gray-500 mb-1">{{ title }}</div>
    <div class="text-3xl font-bold">{{ value }}</div>
  </div>
</template>

<script>
export default {
  name: 'StatCard',
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: [String, Number],
      required: true
    }
  }
}
</script>
