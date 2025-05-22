<template>
  <div class="signupwrapper">
  <form @submit.prevent="submitForm" enctype="multipart/form-data" class="signupcard">
    <input v-model="form.username" placeholder="아이디" />
    <input v-model="form.email" placeholder="이메일" type="email" />
    <input v-model="form.password1" placeholder="비밀번호" type="password" />
    <input v-model="form.password2" placeholder="비밀번호 확인" type="password" />
    <input v-model="form.full_name" placeholder="이름" />
    <input @change="onFileChange" type="file" />

    <div>
      <label v-for="(label, value) in genreChoices" :key="value">
        <input type="checkbox" :value="value" v-model="form.interests" />
        {{ label }}
      </label>
    </div>
    <button type="submit">회원가입</button>
  </form>
</div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({
  username: '',
  email: '',
  password1: '',
  password2: '',
  full_name: '',
  profile_image: null,
  interests: [],
})

const genreChoices = {
  '소설': '소설/시/희곡',
  '경제': '경제/경영',
  '자기계발': '자기계발',
  '인문': '인문/교양',
  '과학': '과학',
  '취미': '취미/실용',
  '어린이': '어린이/청소년',
}

function onFileChange(event) {
  form.value.profile_image = event.target.files[0]
}

async function submitForm() {
  const formData = new FormData()
  for (const key in form.value) {
    if (key === 'interests') {
      form.value.interests.forEach(i => formData.append('interests', i))
    } else {
      formData.append(key, form.value[key])
    }
  }

  try {
    const res = await axios.post('http://localhost:8000/api/register/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    alert('회원가입 성공')
  } catch (err) {
    console.error(err)
    alert('회원가입 실패')
  }
}
</script>

<style>
body {
    height: 100%;
    margin: 0;
    /* overflow: hidden; */
}
</style>


<style scoped>
.signupwrapper {
  height: 100vh;
  background-color: #000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.signupcard {
  background-color: #1e1e1e;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}


.signupcard input,
.signupcard label,
.signupcard button {
  color: white;
}


.signupcard button {
  background-color: #333;
  border: none;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
}

.signupcard button:hover {
  background-color: #444;
}

</style>