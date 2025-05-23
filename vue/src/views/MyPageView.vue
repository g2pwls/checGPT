<template>
<div>
    <section>
        <img :src="user.profile_image" alt="프로필 사진" />
        <h2>{{ user.name }}</h2>
    </section>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const user = ref({})

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/accounts/mypage/', {
      withCredentials: true // 세션 기반이면 이 옵션 유지
    })
    user.value = res.data
  } catch (error) {
    console.error(error)
  }
})
</script>

<style scoped>

</style>