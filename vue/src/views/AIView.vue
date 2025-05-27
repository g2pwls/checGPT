<template>
  <div class="ai-view">
    <AIMovie />
    <AIMusic />
  </div>
</template>

<script>
import AIMovie from '@/components/AIMovie.vue'
import AIMusic from '@/components/AIMusic.vue'

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