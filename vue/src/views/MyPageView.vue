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
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/accounts/api/mypage/', {
      headers: {
        Authorization: `Token ${token}`  // 토큰 헤더 필수
      }
    })
    console.log("백엔드에서 받은 데이터:", res.data)
    user.value = res.data
  } catch (error) {
    console.error("마이페이지 요청 실패:", error)
  }
})


</script>

<style scoped>

</style>