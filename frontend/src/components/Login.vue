<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="p-8 bg-white rounded-lg shadow-md w-full max-w-md">
      <h2 class="text-2xl font-bold text-center mb-6">Login to MetaReview</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input type="email" id="email" v-model="email" required
                 class="w-full border rounded-lg p-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none" />
        </div>
        <div class="mb-6">
          <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input type="password" id="password" v-model="password" required
                 class="w-full border rounded-lg p-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none" />
        </div>
        <div v-if="error" class="mb-4 text-red-600 text-sm">
          {{ error }}
        </div>
        <button type="submit" :disabled="status === 'loading'"
                class="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition duration-200 disabled:opacity-50">
          {{ status === 'loading' ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      <p class="text-center text-sm text-gray-600 mt-4">
        Don't have an account? <router-link to="/register" class="text-indigo-600 hover:underline">Register here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth';

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
    };
  },
  computed: {
    status() {
      return useAuthStore().status;
    },
    error() {
      return useAuthStore().error;
    }
  },
  methods: {
    async handleLogin() {
      const authStore = useAuthStore();
      const success = await authStore.login({ email: this.email, password: this.password });
      
      if (success) {
        // Navigate to the dashboard or home page
        this.$router.push('/');
      }
    },
  },
};
</script>
