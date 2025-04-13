// frontend/src/stores/auth.js
import { defineStore } from 'pinia';
import { API_ROUTES } from '../config'; // Assuming API_ROUTES includes auth endpoints

// Helper to make API calls (could be moved to api.js)
async function apiCall(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    let errorDetail = `HTTP error! status: ${response.status}`;
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || JSON.stringify(errorData);
    } catch (e) { /* Ignore if body isn't JSON */ }
    throw new Error(errorDetail);
  }
  // Handle no content response
  if (response.status === 204 || response.headers.get('content-length') === '0') {
      return null;
  }
  return response.json();
}


export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('authToken') || null,
    user: null, // Store user info like email, id
    status: localStorage.getItem('authToken') ? 'success' : 'idle', // idle, loading, success, error
    error: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    authStatus: (state) => state.status,
    currentUser: (state) => state.user,
  },
  actions: {
    async login(credentials) {
      this.status = 'loading';
      this.error = null;
      try {
        // Use FormData for OAuth2PasswordRequestForm
        const formData = new FormData();
        formData.append('username', credentials.email); // Backend expects 'username'
        formData.append('password', credentials.password);

        const data = await apiCall(API_ROUTES.AUTH.TOKEN, { // Make sure TOKEN route exists in config.js
          method: 'POST',
          body: formData, // Send as form data
          // No 'Content-Type' header needed for FormData, browser sets it
        });

        this.token = data.access_token;
        localStorage.setItem('authToken', data.access_token);
        this.status = 'success';
        await this.fetchUser(); // Fetch user info after login
        return true; // Indicate success
      } catch (error) {
        this.status = 'error';
        this.error = error.message || 'Login failed';
        localStorage.removeItem('authToken');
        this.token = null;
        this.user = null;
        console.error('Login error:', error);
        return false; // Indicate failure
      }
    },
    async register(userInfo) {
      this.status = 'loading';
      this.error = null;
      try {
        await apiCall(API_ROUTES.AUTH.REGISTER, { // Make sure REGISTER route exists
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(userInfo),
        });
        this.status = 'idle'; // Or maybe 'success' but user needs to login
        // Optionally log the user in automatically after registration
        // await this.login({ email: userInfo.email, password: userInfo.password });
        return true;
      } catch (error) {
        this.status = 'error';
        this.error = error.message || 'Registration failed';
        console.error('Registration error:', error);
        return false;
      }
    },
    async fetchUser() {
      if (!this.token) return;
      this.status = 'loading';
      try {
        const userData = await apiCall(API_ROUTES.AUTH.GET_ME, { // Make sure GET_ME route exists
          headers: { Authorization: `Bearer ${this.token}` },
        });
        this.user = userData;
        this.status = 'success';
      } catch (error) {
        console.error('Fetch user error:', error);
        // If token is invalid, log out
        if (error.message.includes('401') || error.message.includes('credentials')) {
          this.logout();
        } else {
          this.status = 'error';
          this.error = 'Failed to fetch user data';
        }
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      this.status = 'idle';
      this.error = null;
      localStorage.removeItem('authToken');
      // Potentially redirect to login page via router action
      console.log('User logged out');
    },
    // Call this when the app loads
    async initializeAuth() {
        const token = localStorage.getItem('authToken');
        if (token) {
            this.token = token;
            await this.fetchUser(); // Validate token and get user info
        } else {
            this.status = 'idle'; // Ensure status is idle if no token
        }
    },
  },
});