// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import AppLayout from '../components/AppLayout.vue'; // You'll create this wrapper
import Dashboard from '../components/Dashboard.vue';
import PaperSearch from '../components/PaperSearch.vue';
import PaperProcessing from '../components/PaperProcessing.vue';
import CodingView from '../components/CodingView.vue';
import CodingListView from '../components/CodingListView.vue';
import CodingSheet from '../components/CodingSheet.vue';
import ResultsTable from '../components/ResultsTable.vue';
import Projects from '../components/Projects.vue';
import ProjectDetail from '../components/ProjectDetail.vue';
import PaperDetailView from '../components/PaperDetailView.vue';

const routes = [
  { path: '/login', name: 'Login', component: Login, meta: { requiresGuest: true } },
  { path: '/register', name: 'Register', component: Register, meta: { requiresGuest: true } },
  {
    path: '/',
    component: AppLayout, // Use a layout component for authenticated views
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'Dashboard', component: Dashboard },
      { path: 'search', name: 'Search', component: PaperSearch },
      { path: 'processing', name: 'Processing', component: PaperProcessing },
      { path: 'coding', name: 'CodingList', component: CodingListView }, // Main coding list view
      { path: 'coding/:paperId', name: 'CodingView', component: CodingView, props: true }, // View for coding a specific paper
      { path: 'coding-sheet/:projectId?', name: 'CodingSheet', component: CodingSheet, props: true }, // Route for coding sheet config
      { path: 'results', name: 'Results', component: ResultsTable },
      { path: 'projects', name: 'Projects', component: Projects },
      { path: 'projects/:projectId', name: 'ProjectDetail', component: ProjectDetail, props: true },
      { path: 'paper/:paperId', name: 'PaperDetail', component: PaperDetailView, props: true },
    ]
  },
  // Catch-all route
  { path: '/:pathMatch(.*)*', redirect: '/' }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  // --- ADD LOGGING ---
  console.log(`[Router Guard] Navigating to: ${to.path}, IsAuthenticated: ${authStore.isAuthenticated}, AuthStatus: ${authStore.status}`);
  // --- END LOGGING ---
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresGuest = to.matched.some(record => record.meta.requiresGuest);

  // --- ADD LOGGING ---
  console.log(`[Router Guard] Requires Auth: ${requiresAuth}, Requires Guest: ${requiresGuest}`);
  // --- END LOGGING ---

  // REMOVED initializeAuth() call block

  if (requiresAuth && !authStore.isAuthenticated) {
    console.log('[Router Guard] Auth required, not authenticated. Redirecting to Login.'); // Modified log
    next({ name: 'Login' });
  } else if (requiresGuest && authStore.isAuthenticated) {
    console.log('[Router Guard] Guest required, authenticated. Redirecting to Dashboard.'); // Modified log
    next({ name: 'Dashboard' }); // Redirect authenticated users from guest pages
  } else {
    console.log('[Router Guard] Proceeding with next().'); // Add log
    next(); // Proceed as normal
  }
});

export default router;
