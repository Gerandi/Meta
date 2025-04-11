<template>
  <div 
    class="flex items-center p-2 my-1 rounded cursor-pointer"
    :class="active ? 'bg-indigo-700' : 'hover:bg-indigo-700'"
    @click="$emit('click')"
  >
    <div class="mr-3">
      <font-awesome-icon :icon="icon" size="sm" />
    </div>
    <div>{{ text }}</div>
  </div>
</template>

<script>
export default {
  name: 'SidebarItem',
  props: {
    icon: {
      type: String,
      required: true
    },
    text: {
      type: String,
      required: true
    },
    active: {
      type: Boolean,
      default: false
    }
  }
}
</script>
