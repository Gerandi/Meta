<template>
  <!-- App.vue now just renders the router view -->
  <router-view />
</template>
<script>
// Remove most logic from App.vue, it's now handled by AppLayout.vue and router guards
export default {
  name: 'App',
  // No components needed here anymore unless you have global ones outside the router
  // No data, computed, methods needed here anymore
  // mounted hook logic moved to main.ts or auth store initializeAuth
}
</script>
<style>
/* Keep global styles */
@import './style.css';
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Inter', sans-serif;
}
</style>
