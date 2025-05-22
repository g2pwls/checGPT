<template>
    <div>
        <h1>로그인</h1>
        <form @submit.prevent="login">
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

</style>