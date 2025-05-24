<template>
  <div>
    <h3>스레드가 뜰 예정</h3>
    <ul>
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
