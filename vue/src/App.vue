<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from './stores/user'

const userStore = useUserStore()
const router = useRouter()

onMounted(() => {
  userStore.initializeFromStorage()
})

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('name')
  userStore.logout()
  router.push('/').then(() => {
    window.location.reload()
  })
}
</script>


<template>
  <header class="custom-navbar">
    <nav class="nav-container">
      <div class="nav-left">
        <RouterLink to="/">Home</RouterLink>
      </div>
      <div class="nav-right">
        <template v-if="userStore.isLoggedIn">
          <span class="namename">{{ userStore.username }}님</span>
          <RouterLink :to="{ name: 'BookList' }">책 리스트</RouterLink>
          <RouterLink :to="{ name: 'MyPageView' }">마이페이지</RouterLink>
          <span @click="logout" class="logout">로그아웃</span>
        </template>
        <template v-else>
          <RouterLink :to="{ name: 'Login' }">로그인</RouterLink>
          <RouterLink :to="{ name: 'BookList' }">책 리스트</RouterLink>
        </template>
      </div>
    </nav>
  </header>
  <RouterView />
</template>



<style scoped>
.custom-navbar {
  background-color: #D4CCC3;
  padding: 1rem 2rem;
  height: 26px;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.namename,
.logout,
.nav-left a,
.nav-right a {
  color: rgb(0, 105, 0);
  text-decoration: none;
  font-weight: bold;
  cursor: pointer;
}

.logout:hover,
.nav-left a:hover,
.nav-right a:hover {
  color: lightgreen;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.divider {
  color: green;
  margin: 0 0.5rem;
}
</style>
