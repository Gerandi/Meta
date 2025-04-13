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
        console.log('[Auth Store] Fetching user data...'); // Add log
        const userData = await apiCall(API_ROUTES.AUTH.GET_ME, { // Make sure GET_ME route exists
          headers: { Authorization: `Bearer ${this.token}` },
        });
        this.user = userData;
        this.status = 'success';
        console.log('[Auth Store] User data fetched successfully:', this.user); // Add log
      } catch (error) {
        console.error('[Auth Store] Fetch user error:', error.message); // Log specific message
        // --- MODIFIED CATCH BLOCK ---
        // Check for typical authentication error indicators
        const errorMsg = error.message.toLowerCase();
        if (errorMsg.includes('401') || errorMsg.includes('unauthorized') || errorMsg.includes('could not validate credentials') || errorMsg.includes('authentication failed')) {
           console.warn("[Auth Store] Authentication failed while fetching user. Logging out.");
           this.logout(); // Call logout to clear invalid state
        } else {
           // Keep token but mark state as error for other issues
           this.status = 'error';
           this.error = 'Failed to fetch user data: ' + error.message;
           this.user = null; // Ensure user data is cleared on any fetch error
        }
        // --- END MODIFIED CATCH BLOCK ---
      }
    },
    logout() {
      console.log('[Auth Store] Logging out user.'); // Add log
      this.token = null;
      this.user = null;
      this.status = 'idle';
      this.error = null;
      localStorage.removeItem('authToken');
      // In a real app, you'd likely use the router injected into the store or emit an event
      // For now, the router guard will handle redirecting to login on next navigation attempt.
    },
    // Call this when the app loads
    async initializeAuth() {
        console.log('[Auth Store] Initializing auth...'); // Add log
        const token = localStorage.getItem('authToken');
        if (token) {
            console.log('[Auth Store] Found token in storage.'); // Add log
            this.token = token;
            await this.fetchUser(); // Validate token and get user info
        } else {
            console.log('[Auth Store] No token found in storage.'); // Add log
            this.status = 'idle'; // Ensure status is idle if no token
            this.token = null;
            this.user = null;
        }
    },
  },
});
