<template>
  <div class="signupwrapper">
    <form @submit.prevent="submitForm" enctype="multipart/form-data" class="signupcard">
      <div class="form-group">
        <label for="username">아이디</label>
        <input id="username" v-model="form.username" placeholder="ID" />
        <p v-if="errors.username">{{ errors.username[0] }}</p>
      </div>
      <div class="form-group">
        <label for="email">이메일</label>
        <input id="email" v-model="form.email" placeholder="ChecGPT@ssafy.com" type="email" />
      </div>
      <div class="form-group">
        <label for="password1">비밀번호</label>
        <input id="password1" v-model="form.password1" placeholder="password" type="password" />
        <p v-if="errors.password1">{{ errors.password1[0] }}</p>
      </div>
      <div class="form-group">
        <label for="password2">비밀번호 확인</label>
        <input id="password2" v-model="form.password2" placeholder="비밀번호와 일치해야 합니다" type="password" />
      </div>
      <div class="form-group">
        <label for="name">이름</label>
        <input id="name" v-model="form.name" placeholder="이름" />
      </div>
      <div class="form-group">
        <label for="profile_image">프로필 이미지</label>
        <input id="profile_image" @change="onFileChange" type="file" />
      </div>
      <div class="form-group interests-group">
        <span style="font-weight:500; color:#333; margin-bottom:0.2rem;">관심 카테고리</span>
        <div class="checkbox-row">
          <label v-for="(label, value) in genreChoices" :key="value">
            <input type="checkbox" :value="value" v-model="form.interests" />
            {{ label }}
          </label>
        </div>
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
      form.value.interests.forEach(i => formData.append('interests[]', i))
    } else {
      formData.append(key, form.value[key])
    }
  }
  console.log(formData)
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
  min-height: 100vh;
  background-color: #fff;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 0 0 0;
}

.signupcard {
  background-color: #fff;
  color: #222;
  font-weight: 500;
  padding: 2.5rem 2rem;
  border-radius: 0px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  width: 350px;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  border: 1px solid #eee;
  transition: box-shadow 0.4s cubic-bezier(.4,1.4,.6,1), transform 0.4s cubic-bezier(.4,1.4,.6,1), opacity 0.6s, top 0.6s;
  opacity: 0;
  transform: translateY(30px);
  animation: signupCardFadeIn 0.7s cubic-bezier(.4,1.4,.6,1) forwards;
}

@keyframes signupCardFadeIn {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  margin-bottom: 0.2rem;
}
.form-group label {
  color: #333;
  font-weight: 500;
  margin-bottom: 0.1rem;
}

.signupcard input[type="text"],
.signupcard input[type="email"],
.signupcard input[type="password"],
.signupcard input[type="file"],
.signupcard input:not([type="checkbox"]) {
  padding: 12px 16px;
  border: 1px solid #dadada;
  border-radius: 15px;
  background-color: #fff;
  color: #222;
  font-size: 15px;
  outline: none;
  transition: border-color 0.3s;
}
.signupcard input[type="text"]:focus,
.signupcard input[type="email"]:focus,
.signupcard input[type="password"]:focus {
  border-color: #333;
}

.interests-group > .checkbox-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 1rem;
  margin-bottom: 0.5rem;
  margin-top: 0.4rem;
}
.signupcard label {
  color: #333;
  font-weight: 500;
  display: flex;
  align-items: center;
  min-width: 110px;
  margin-right: 0.5rem;
  margin-bottom: 0.4rem;
  cursor: pointer;
  user-select: none;
}
.signupcard input[type="checkbox"] {
  cursor: pointer;
  margin-right: 0.3em;
}

.signupcard button {
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
.signupcard button:hover {
  background-color: #000000;
}

/* 에러 메시지 스타일 개선 */
.signupcard p {
  color: #e74c3c;
  font-size: 0.95em;
  margin: 0 0 0.5em 0;
}

</style>
