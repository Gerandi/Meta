import { createApp } from 'vue'
import { createPinia } from 'pinia' // Import Pinia
import router from './router' // Import the router
import App from './App.vue'
import './style.css'
import { useAuthStore } from './stores/auth' // Import auth store
import { useProjectStore } from './stores/project' // Import project store

// Import Lucide Vue
import {
  Search,
  Upload,
  PlusCircle,
  Filter,
  Download,
  Book,
  FileText,
  LayoutGrid,
  Edit,
  Table,
  Settings,
  Trash2,
  Save,
  Check,
  X,
  Plus,
  Minus,
  Folder,
  FolderOpen,
  MoreVertical,
  ArrowLeft,
  FileUp,
  ArrowUpDown,
  ArrowRight,
  ClipboardList,
  Grid,
  Edit3,
  PenLine,
  CheckCircle,
  HelpCircle,
  RefreshCw,
  RotateCw,
  AlertTriangle,
  Clock,
  Copy,
  Loader2,
  UploadCloud,
  Link,
  ChevronUp,
  ChevronDown,
  LogOut,
  User
} from 'lucide-vue-next'

// Create Vue app
const app = createApp(App)

// Initialize Pinia
const pinia = createPinia()
app.use(pinia)

// Initialize Auth Store (check for existing token) BEFORE mounting router/app
const authStore = useAuthStore();
const projectStore = useProjectStore(); // Initialize project store

console.log('[main.ts] Initializing authentication...'); // Add log

authStore.initializeAuth()
  .then(() => {
    console.log('[main.ts] Authentication initialized successfully. Setting up router and mounting app.'); // Add log
    // Use router AFTER auth is initialized
    app.use(router)

    // Register Lucide icons globally
    app.component('Search', Search)
    app.component('Upload', Upload)
    app.component('PlusCircle', PlusCircle)
    app.component('Filter', Filter)
    app.component('Download', Download)
    app.component('Book', Book)
    app.component('FileText', FileText)
    app.component('LayoutGrid', LayoutGrid)
    app.component('Edit', Edit)
    app.component('Table', Table)
    app.component('Settings', Settings)
    app.component('Trash2', Trash2)
    app.component('Save', Save)
    app.component('Check', Check)
    app.component('X', X)
    app.component('Plus', Plus)
    app.component('Minus', Minus)
    app.component('Folder', Folder)
    app.component('FolderOpen', FolderOpen)
    app.component('MoreVertical', MoreVertical)
    app.component('ArrowLeft', ArrowLeft)
    app.component('FileUp', FileUp)
    app.component('ArrowUpDown', ArrowUpDown)
    app.component('ArrowRight', ArrowRight)
    app.component('ClipboardList', ClipboardList)
    app.component('Grid', Grid)
    app.component('Edit3', Edit3)
    app.component('PenLine', PenLine)
    app.component('CheckCircle', CheckCircle)
    app.component('HelpCircle', HelpCircle)
    app.component('RefreshCw', RefreshCw)
    app.component('RotateCw', RotateCw)
    app.component('AlertTriangle', AlertTriangle)
    app.component('Clock', Clock)
    app.component('Copy', Copy)
    app.component('Loader2', Loader2)
    app.component('UploadCloud', UploadCloud)
    app.component('Link', Link)
    app.component('ChevronUp', ChevronUp)
    app.component('ChevronDown', ChevronDown)
    app.component('LogOut', LogOut)
    app.component('User', User)

    // Mount app
    app.mount('#app')
    console.log('[main.ts] App mounted.'); // Add log
  })
  .catch((error: unknown) => { // Explicitly type error as unknown
    // --- ADDED CATCH BLOCK ---
    console.error("[main.ts] Failed to initialize authentication:", error);
    // Decide recovery strategy: maybe redirect to login, show error message, or still mount the app
    // For now, just log the error. If fetchUser failed due to bad token, logout() should have cleared it.
    // We might still want to mount the router for public routes like login.
    app.use(router) // Mount router even on error to allow access to login page

    // Register Lucide icons globally (needed even if auth fails for login page etc.)
    app.component('Search', Search)
    app.component('Upload', Upload)
    app.component('PlusCircle', PlusCircle)
    app.component('Filter', Filter)
    app.component('Download', Download)
    app.component('Book', Book)
    app.component('FileText', FileText)
    app.component('LayoutGrid', LayoutGrid)
    app.component('Edit', Edit)
    app.component('Table', Table)
    app.component('Settings', Settings)
    app.component('Trash2', Trash2)
    app.component('Save', Save)
    app.component('Check', Check)
    app.component('X', X)
    app.component('Plus', Plus)
    app.component('Minus', Minus)
    app.component('Folder', Folder)
    app.component('FolderOpen', FolderOpen)
    app.component('MoreVertical', MoreVertical)
    app.component('ArrowLeft', ArrowLeft)
    app.component('FileUp', FileUp)
    app.component('ArrowUpDown', ArrowUpDown)
    app.component('ArrowRight', ArrowRight)
    app.component('ClipboardList', ClipboardList)
    app.component('Grid', Grid)
    app.component('Edit3', Edit3)
    app.component('PenLine', PenLine)
    app.component('CheckCircle', CheckCircle)
    app.component('HelpCircle', HelpCircle)
    app.component('RefreshCw', RefreshCw)
    app.component('RotateCw', RotateCw)
    app.component('AlertTriangle', AlertTriangle)
    app.component('Clock', Clock)
    app.component('Copy', Copy)
    app.component('Loader2', Loader2)
    app.component('UploadCloud', UploadCloud)
    app.component('Link', Link)
    app.component('ChevronUp', ChevronUp)
    app.component('ChevronDown', ChevronDown)
    app.component('LogOut', LogOut)
    app.component('User', User)

    app.mount('#app')
    console.warn('[main.ts] App mounted despite auth initialization error.');
    // --- END ADDED CATCH BLOCK ---
  });
