<template>
  <div class="signupwrapper">
  <form @submit.prevent="submitForm" enctype="multipart/form-data" class="signupcard">
    아이디<input v-model="form.username" placeholder="ID" />
    <p v-if="errors.username" style="color: red;">{{ errors.username[0] }}</p>
    이메일<input v-model="form.email" placeholder="pro@ssafy.com" type="email" />
    비밀번호<input v-model="form.password1" placeholder="password" type="password" />
    <p v-if="errors.password1" style="color: red;">{{ errors.password1[0] }}</p>
    비밀번호 확인<input v-model="form.password2" placeholder="비밀번호와 일치해야 합니다" type="password" />
    이름<input v-model="form.name" placeholder="이름" />
    프로필 이미지<input @change="onFileChange" type="file" />

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
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const form = ref({
  username: '',
  email: '',
  password1: '',
  password2: '',
  name: '',
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

const errors = ref({})

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
  for (const pair of formData.entries()) {
    console.log(pair[0], ':', pair[1])
  }
  
  try {
    const res = await axios.post('http://127.0.0.1:8000/accounts/api/signup/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    console.log('회원가입 성공:', res.data)
    alert('회원가입 성공')
    console.log("라우터 이동 전")
    router.push('/login')
    console.log("라우터 이동 시도함")
  } catch (err) {
  console.error('회원가입 실패:', err.response?.data)
  alert('회원가입 실패: ' + JSON.stringify(err.response?.data))
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
  color: white;
  font-weight: bold;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* 입력창 스타일 - 로그인 input과 동일 */
.signupcard input[type="text"],
.signupcard input[type="email"],
.signupcard input[type="password"],
.signupcard input[type="file"],
.signupcard input:not([type="checkbox"]) {
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: #2a2a2a;
  color: white;
  font-size: 14px;
  outline: none;
}

/* 체크박스 라벨 스타일 */
.signupcard label {
  color: white;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  user-select: none;
}

/* 체크박스 자체는 기본 스타일 유지 (필요시 커스터마이징 가능) */
.signupcard input[type="checkbox"] {
  cursor: pointer;
}

/* 버튼 스타일 - 로그인 submit 스타일과 비슷하게 */
.signupcard button {
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

.signupcard button:hover {
  background-color: #d33;
}

</style>
