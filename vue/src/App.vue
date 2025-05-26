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
  localStorage.removeItem('userId')
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
        <RouterLink to="/">Starbooks</RouterLink>
      </div>
      <div class="nav-right">
        <template v-if="userStore.isLoggedIn">
          <span class="namename">{{ userStore.username }}님, 환영합니다!</span>
          <RouterLink :to="{ name: 'BookList' }">책마루</RouterLink>
          <RouterLink :to="{ name: 'Report' }">감상문</RouterLink>
          <RouterLink :to="{ name: 'UserProfile', params: { userId: userStore.userId } }">나의 책갈피</RouterLink>
          <span @click="logout" class="logout">떠나기</span>
        </template>
        <template v-else>
          <RouterLink :to="{ name: 'Login' }">들르기</RouterLink>
          <RouterLink :to="{ name: 'BookList' }">책마루</RouterLink>
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

.namename {
  color: rgb(0, 105, 0);
  text-decoration: none;
  cursor: pointer;
  font-size: smaller;
}

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

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #f9f6f2;
  min-height: 100vh;
}

body {
  margin: 0;
  padding: 0;
  background-color: #f9f6f2;
}
