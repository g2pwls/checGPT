<template>
  <div class="ai-view">
    <AIMovie />
    <AIMusic />
  </div>
</template>

<script>
import AIMusic from '@/components/AIMusic.vue'
import AIMovie from '@/components/AIMovie.vue'

export default {
  components: {
    AIMovie,
    AIMusic,
  },
}
</script>

<style scoped>
.ai-view {
  padding: 1rem;
}
</style>