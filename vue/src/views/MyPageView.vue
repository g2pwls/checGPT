<template>
  <div>
    <section class="profile-section">
      <img :src="user.profile_image ? `http://127.0.0.1:8000${user.profile_image}` : '/default-profile.png'"
        alt="프로필 사진" />
      <h2>{{ user.name }} 님의 페이지</h2>
      <div>
        <span>팔로잉: {{ user.following_count }}</span>
        <span>팔로워: {{ user.follower_count }}</span>
        <span>작성 쓰레드: {{ user.thread_count }}</span>
        <br>
        <span>관심 장르: {{ user.interests }}</span>
      </div>
    </section>
  </div>

  <!-- ✅ 탭 버튼 -->
  <div class="tabs">
    <span
      :class="{ active: currentTab === 'books' }"
      @click="currentTab = 'books'"
    >
      {{ user.name }} 님의 서재
    </span>
    <span
      :class="{ active: currentTab === 'threads' }"
      @click="currentTab = 'threads'"
    >
      {{ user.name }} 님의 스레드
    </span>
  </div>

  <!-- ✅ 탭에 따라 아래 내용만 바뀜 -->
  <div class="tab-content">
    <BooksTab v-if="currentTab === 'books'" :user="user" />
    <ThreadsTab v-if="currentTab === 'threads'" :user="user" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import BooksTab from '@/components/BooksTab.vue'
import ThreadsTab from '@/components/ThreadsTab.vue'

const user = ref({})
const currentTab = ref('books')

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
.profile-section {
  border-bottom: 1px solid #ccc;
  padding: 1rem;
  margin-bottom: 1rem;
}

.profile-section img {
  width: 200px;       /* 원하는 크기로 조절 */
  height: 200px;      /* 정사각형으로 만들어야 동그랗게 됨 */
  object-fit: cover;  /* 이미지 비율 유지하며 꽉 채우기 */
  border-radius: 50%; /* 둥글게 만들기 */
  /* border: 2px solid #ccc; 선택 사항: 테두리 추가 */
}

.tabs {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
  font-size: 1.1rem;
}

.tabs span {
  cursor: pointer;
  position: relative;
  padding-bottom: 4px;
  color: #555;
  transition: color 0.2s;
}

/* ✅ 마우스 올렸을 때 밑줄 효과 */
.tabs span:hover::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 2px;
  width: 100%;
  background-color: #888;
}

/* ✅ 선택된 탭 강조 */
.tabs span.active {
  font-weight: bold;
  color: #222;
}

/* ✅ 선택된 탭 밑줄 */
.tabs span.active::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 2px;
  width: 100%;
  background-color: #222;
}
</style>