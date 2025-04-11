<template>
  <div class="flex h-screen bg-gray-100">
    <Sidebar :activeView="activeView" @change-view="setActiveView" />
    <div class="flex-1 overflow-auto">
      <component 
        :is="currentView" 
        v-bind="componentProps"
        @select-paper="handleSelectPaper"
        @view-collection="handleViewCollection"
        @change-view="setActiveView"
      />
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue';
import Dashboard from './components/Dashboard.vue';
import PaperSearch from './components/PaperSearch.vue';
import PdfViewer from './components/PdfViewer.vue';
import CodingSheet from './components/CodingSheet.vue';
import ResultsTable from './components/ResultsTable.vue';
import Collections from './components/Collections.vue';
import CollectionDetail from './components/CollectionDetail.vue';

export default {
  name: 'App',
  components: {
    Sidebar,
    Dashboard,
    PaperSearch,
    PdfViewer,
    CodingSheet,
    ResultsTable,
    Collections,
    CollectionDetail
  },
  data() {
    return {
      activeView: 'dashboard',
      selectedPaper: null,
      selectedCollectionId: null
    }
  },
  computed: {
    currentView() {
      switch(this.activeView) {
        case 'dashboard':
          return Dashboard;
        case 'search':
          return PaperSearch;
        case 'viewer':
          return PdfViewer;
        case 'codingSheet':
          return CodingSheet;
        case 'resultsTable':
          return ResultsTable;
        case 'collections':
          return Collections;
        case 'collectionDetail':
          return CollectionDetail;
        default:
          return Dashboard;
      }
    },
    componentProps() {
      if (this.activeView === 'viewer' && this.selectedPaper) {
        return { paper: this.selectedPaper };
      }
      if (this.activeView === 'collectionDetail' && this.selectedCollectionId) {
        return { collectionId: this.selectedCollectionId };
      }
      return {};
    }
  },
  methods: {
    setActiveView(view) {
      this.activeView = view;
    },
    handleSelectPaper(paper) {
      this.selectedPaper = paper;
      this.activeView = 'viewer';
    },
    
    handleViewCollection(collectionId) {
      this.selectedCollectionId = collectionId;
      this.activeView = 'collectionDetail';
    }
  }
}
</script>

<style>
@import './style.css';

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Inter', sans-serif;
}
</style>
