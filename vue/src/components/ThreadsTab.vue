<template>
  <div>
    <h3>애 아 느</h3>
    <p v-if="threads.length === 0">아직 작성한 스레드가 없습니다.</p>
    <ul v-else>
      <li v-for="thread in threads" :key="thread.id">
        <strong>{{ thread.title }}</strong> <br />
        {{ thread.content }}
      </li>
    </ul>
  </div>
</template>

<script setup>

</script>

<style scoped>
h3 {
  margin-bottom: 0.5rem;
}
li {
  margin-bottom: 1rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}
</style>
