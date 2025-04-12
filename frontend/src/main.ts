import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

// Import FontAwesome core
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Import icons individually
import { 
  faSearch, 
  faUpload, 
  faPlusCircle, 
  faFilter, 
  faDownload, 
  faBook, 
  faFileAlt, 
  faThLarge, 
  faEdit, 
  faTable, 
  faCog, 
  faTrash, 
  faSave, 
  faCheck, 
  faTimes, 
  faPlus, 
  faMinus,
  faFolder,
  faFolderOpen,
  faEllipsisV,
  faArrowLeft,
  faFileUpload,
  faExchangeAlt,
  faArrowRight,
  faTasks
} from '@fortawesome/free-solid-svg-icons'

// Add icons to the library
library.add(
  faSearch, 
  faUpload, 
  faPlusCircle, 
  faFilter, 
  faDownload, 
  faBook, 
  faFileAlt, 
  faThLarge, 
  faEdit, 
  faTable, 
  faCog, 
  faTrash, 
  faSave, 
  faCheck, 
  faTimes, 
  faPlus, 
  faMinus,
  faFolder,
  faFolderOpen,
  faEllipsisV,
  faArrowLeft,
  faFileUpload,
  faExchangeAlt,
  faArrowRight,
  faTasks
)

// Create Vue app
const app = createApp(App)

// Register FontAwesome component
app.component('font-awesome-icon', FontAwesomeIcon)

// Mount app
app.mount('#app')
