<template>
  <div class="flex h-full">
    <PdfViewer 
      :paper="paper" 
      :projectId="projectId" 
      :showCodingPanel="false"
      class="flex-grow"
    />
    <CodingForm 
      :paper="paper" 
      :projectId="projectId"
      class="w-1/3 border-l"
      @saved="onCodingSaved"
    />
  </div>
</template>

<script>
import PdfViewer from './PdfViewer.vue';
import CodingForm from './CodingForm.vue';

export default {
  name: 'CodingView',
  components: {
    PdfViewer,
    CodingForm
  },
  props: {
    paper: {
      type: Object,
      required: true
    },
    projectId: {
      type: Number,
      required: false,
      default: null
    }
  },
  methods: {
    onCodingSaved() {
      // Emit event to parent component when coding is saved
      this.$emit('coding-saved');
    }
  }
}
</script>
