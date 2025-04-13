import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

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
  // Add missing icon components
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
  ChevronDown
} from 'lucide-vue-next'

// Create Vue app
const app = createApp(App)

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

// Mount app
app.mount('#app')
