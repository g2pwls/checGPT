<template>
  <div class="ai-view">
    <AIMovie />
  </div>
</template>

<script>
import AIMovie from '@/components/AIMovie.vue'

export default {
  components: {
    AIMovie,
  },
}
</script>

<style scoped>
.ai-view {
  padding: 1rem;
}
</style>
