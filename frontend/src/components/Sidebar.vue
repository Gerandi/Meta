<template>
  <div class="w-64 bg-indigo-800 text-white p-4">
    <div class="text-xl font-bold mb-8 pl-2">MetaReview</div>
    <nav>
      <SidebarItem 
        icon="th-large" 
        text="Dashboard" 
        :active="activeView === 'dashboard'" 
        @click="changeView('dashboard')" 
      />
      <SidebarItem 
        icon="search" 
        text="Find Papers" 
        :active="activeView === 'search'" 
        @click="changeView('search')" 
      />
      <SidebarItem 
        icon="tasks" 
        text="Process Papers" 
        :active="activeView === 'processing'" 
        @click="changeView('processing')" 
      />
      <SidebarItem 
        icon="file-alt" 
        text="PDF Viewer" 
        :active="activeView === 'viewer'" 
        @click="changeView('viewer')" 
      />
      <SidebarItem 
        icon="edit" 
        text="Coding Sheet" 
        :active="activeView === 'codingSheet'" 
        @click="changeView('codingSheet')" 
      />
      <SidebarItem 
        icon="table" 
        text="Results Table" 
        :active="activeView === 'resultsTable'" 
        @click="changeView('resultsTable')" 
      />
      <SidebarItem 
        icon="folder" 
        text="Collections" 
        :active="activeView === 'collections'" 
        @click="changeView('collections')" 
      />
      <SidebarItem 
        icon="cog" 
        text="Settings" 
        :active="activeView === 'settings'" 
        @click="changeView('settings')" 
      />
    </nav>
    <div class="mt-auto pt-4 border-t border-indigo-700 mt-8">
      <div class="flex items-center p-2 rounded hover:bg-indigo-700 cursor-pointer">
        <div class="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center mr-2">
          JD
        </div>
        <div>
          <div class="text-sm font-semibold">John Doe</div>
          <div class="text-xs text-indigo-300">Researcher</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SidebarItem from './SidebarItem.vue';

export default {
  name: 'Sidebar',
  components: {
    SidebarItem
  },
  props: {
    activeView: {
      type: String,
      required: true
    }
  },
  methods: {
    changeView(view) {
      this.$emit('change-view', view);
    }
  }
}
</script>
