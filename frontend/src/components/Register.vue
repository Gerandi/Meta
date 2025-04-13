<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="p-8 bg-white rounded-lg shadow-md w-full max-w-md">
      <h2 class="text-2xl font-bold text-center mb-6">Register for MetaReview</h2>
      <form @submit.prevent="handleRegister">
        <div class="mb-4">
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input type="email" id="email" v-model="email" required
                 class="w-full border rounded-lg p-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none" />
        </div>
        <div class="mb-4">
          <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input type="password" id="password" v-model="password" required
                 class="w-full border rounded-lg p-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none" />
        </div>
         <div class="mb-6">
          <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
          <input type="password" id="confirmPassword" v-model="confirmPassword" required
                 class="w-full border rounded-lg p-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none" />
           <p v-if="password !== confirmPassword && confirmPassword" class="text-red-500 text-xs mt-1">Passwords do not match.</p>
        </div>
        <div v-if="error" class="mb-4 text-red-600 text-sm">
          {{ error }}
        </div>
        <button type="submit" :disabled="status === 'loading' || password !== confirmPassword"
                class="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition duration-200 disabled:opacity-50">
          {{ status === 'loading' ? 'Registering...' : 'Register' }}
        </button>
      </form>
      <p class="text-center text-sm text-gray-600 mt-4">
        Already have an account? <router-link to="/login" class="text-indigo-600 hover:underline">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth';

export default {
  name: 'Register',
  data() {
    return {
      email: '',
      password: '',
      confirmPassword: '',
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
    async handleRegister() {
      if (this.password !== this.confirmPassword) {
        return; // Button should be disabled, but extra check
      }
      
      const authStore = useAuthStore();
      const success = await authStore.register({ email: this.email, password: this.password });
      
      if (success) {
        alert('Registration successful! Please log in.');
        this.$router.push('/login');
      }
    },
  },
};
</script>
