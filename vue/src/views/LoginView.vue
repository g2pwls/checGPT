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
      <button class="signup-button" @click="goSignup">회원가입</button>
    </form>
  </div>
</template>

<script setup>
import axios from 'axios'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const password = ref('')

const login = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/accounts/api/login/', {
      username: username.value,
      password: password.value
    })

    const token = response.data.token
    const name = response.data.name
    const userId = response.data.user.id

    axios.defaults.headers.common['Authorization'] = `Token ${token}`

    localStorage.setItem('token', token)
    localStorage.setItem('name', name)
    localStorage.setItem('userId', userId)

    userStore.login(name)
    
    router.push({ name: 'UserProfile', params: { userId: userId } })
  } catch (error) {
    console.error(error)
    alert('로그인에 실패했습니다.')
  }
}

const goSignup = () => {
  router.push('/signup')
}
</script>


<style scoped>
.login-wrapper {
  min-height: 100vh;
  background-color: #fff;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 180px 0 0 0;
}

.login-card {
  background-color: #fff;
  padding: 2.5rem 2rem;
  border-radius: 0px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  width: 350px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  border: 1px solid #eee;
  transition: box-shadow 0.4s cubic-bezier(.4,1.4,.6,1), transform 0.4s cubic-bezier(.4,1.4,.6,1), opacity 0.6s, top 0.6s;
  opacity: 0;
  transform: translateY(30px);
  animation: loginCardFadeIn 0.7s cubic-bezier(.4,1.4,.6,1) forwards;
}


@keyframes loginCardFadeIn {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-card div {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  color: #333;
  font-weight: 500;
  margin-bottom: 0.2rem;
}

input[type="text"],
input[type="password"] {
  padding: 12px 16px;
  border: 1px solid #dadada;
  border-radius: 15px;
  background-color: #fff;
  color: #222;
  font-size: 15px;
  outline: none;
  transition: border-color 0.3s;
}

input[type="text"]:focus,
input[type="password"]:focus {
  border-color: #333;
}

input[type="submit"] {
  padding: 12px;
  background-color: #333;
  border: none;
  border-radius: 15px;
  color: white;
  font-weight: bold;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

input[type="submit"]:hover {
  background-color: #555;
}

.signup-button {
  width: 100%;
  padding: 12px;
  background-color: #f8f8f8;
  border: 1px solid #dadada;
  border-radius: 15px;
  color: #333;
  font-weight: 500;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}
.signup-button:hover {
  background-color: #868686;
  color: #fff;
}
</style>
