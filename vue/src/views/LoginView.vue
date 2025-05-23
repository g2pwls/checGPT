<template>
    <div class="login-wrapper">
        <form @submit.prevent="login" class="login-card">
            <div>
                <label for="username">아이디</label>
                <input type="text" id="username" v-model="username">
            </div>
            <div>
                <label for="password">비밀번호</label>
                <input type="password" id="password" v-model="password">
            </div>
            <input type="submit" value="로그인">
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref("")
const password = ref("")
const router = useRouter()

const login = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/accounts/api/login/', {
      username: username.value,
      password: password.value,
    }, {
      withCredentials: true  // 세션 쿠키 저장
    })

    console.log('로그인 성공:', response.data)
    router.push('/mypage')
  } catch (error) {
    console.error('로그인 실패:', error.response.data)
  }
}


</script>

<style scoped>
.login-wrapper {
  height: 100vh;
  background-color: #000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  background-color: #1e1e1e;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.login-card div {
  display: flex;
  flex-direction: column;
}

label {
  color: white;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

input[type="text"],
input[type="password"] {
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: #2a2a2a;
  color: white;
  font-size: 14px;
  outline: none;
}

input[type="submit"] {
  padding: 10px;
  background-color: #f44;
  border: none;
  border-radius: 4px;
  color: white;
  font-weight: bold;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

input[type="submit"]:hover {
  background-color: #d33;
}
</style>
