import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from './stores/auth';
import Login from './components/Login.vue';
import Register from './components/Register.vue';
import Dashboard from './components/Dashboard.vue';
import Projects from './components/Projects.vue';
import PaperSearch from './components/PaperSearch.vue';
import ProjectDetail from './components/ProjectDetail.vue';
import PaperDetailView from './components/PaperDetailView.vue';
import CodingView from './components/CodingView.vue';
import CodingSheet from './components/CodingSheet.vue';
import CodingListView from './components/CodingListView.vue';
import ResultsTable from './components/ResultsTable.vue';
import PaperProcessing from './components/PaperProcessing.vue';

// Create routes configuration
const routes = [
  {
    path: '/',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    component: Login,
    meta: { guest: true }
  },
  {
    path: '/register',
    component: Register,
    meta: { guest: true }
  },
  {
    path: '/projects',
    component: Projects,
    meta: { requiresAuth: true }
  },
  {
    path: '/projects/:id',
    component: ProjectDetail,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/search',
    component: PaperSearch,
    meta: { requiresAuth: true }
  },
  {
    path: '/papers/:id',
    component: PaperDetailView,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/coding/:paperId',
    component: CodingView,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/coding-sheet/:projectId',
    component: CodingSheet,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/coding-list/:projectId',
    component: CodingListView,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/results/:projectId',
    component: ResultsTable,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/processing',
    component: PaperProcessing,
    meta: { requiresAuth: true }
  }
];

// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation guard to check authentication
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  
  // If auth store hasn't been initialized yet, initialize it
  if (authStore.status === 'idle' && authStore.token) {
    await authStore.initializeAuth();
  }
  
  // Check if the route requires authentication
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isGuestOnly = to.matched.some(record => record.meta.guest);
  
  if (requiresAuth && !authStore.isAuthenticated) {
    // If route requires auth but user is not authenticated
    next('/login');
  } else if (isGuestOnly && authStore.isAuthenticated) {
    // If route is for guests only (like login) but user is authenticated
    next('/');
  } else {
    // Otherwise proceed as normal
    next();
  }
});

export default router;
