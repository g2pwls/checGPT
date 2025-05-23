<template>
    <div class="login-wrapper">
        <form @submit.prevent="login" class="login-card">
            <div>
                <label for="username">아이디</label>
                <input type="text" id="usrename" v-model="username">
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
import {ref} from 'vue'
import axios from 'axios'
import {useRouter} from 'vue-router'

const username = ref("")
const password = ref("")
const router = useRouter()

const login = function () {
    axios({
        url: "http://127.0.0.1:8000/accounts/login/",
        method: "POST",
        data: {
            username: username.value,
            password: password.value,
        }
    }).then((response) => {
        console.log(response)
        router.push({name:'home'})
    }).catch((error) => {
        console.log(error)
    })
}
</script>

<style scoped>
/* 화면 전체 중앙 정렬용 wrapper */
.login-wrapper {
  height: 100vh;
  background-color: #000;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 로그인 카드 UI */
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

/* 입력 그룹 */
.login-card div {
  display: flex;
  flex-direction: column;
}

/* 라벨 */
label {
  color: white;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

/* 입력창 */
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

/* 로그인 버튼 */
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
