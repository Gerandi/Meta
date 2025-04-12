<template>
  <div 
    class="flex items-center p-2 my-1 rounded"
    :class="{
      'bg-indigo-700': active,
      'hover:bg-indigo-700': !disabled && !active,
      'cursor-pointer': !disabled,
      'opacity-50 cursor-default': disabled
    }"
    @click="!disabled && $emit('click')"
  >
    <div class="mr-3">
      <component :is="icon" size="18" />
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
    },
    disabled: {
      type: Boolean,
      default: false
    }
  }
}
</script>
