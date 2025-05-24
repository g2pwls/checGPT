<template>
  <div>
    <h3>작성한 스레드</h3>
    <ul>
      <li v-for="thread in threads" :key="thread.id">
        <strong>{{ thread.title }}</strong> <br />
        {{ thread.content }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({
  userId: Number
})

const threads = ref([])

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get(`http://127.0.0.1:8000/threads/api/user/${props.userId}/`, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    threads.value = res.data
  } catch (err) {
    console.error('스레드 불러오기 실패:', err)
  }
})
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
