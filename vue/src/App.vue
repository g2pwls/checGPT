<script setup>
import { RouterLink, RouterView } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import BookListView from '@/views/BookListView.vue'

</script>

<template>
  <header class="custom-navbar">
    <nav class="nav-container">
      <div class="nav-left">
        <RouterLink to="/">Home</RouterLink>
      </div>
      <div class="nav-right">
        <!-- <RouterLink :to="{name: 'SignupView'}">회원가입</RouterLink> | -->
        <span class="divider">|</span>
        <RouterLink :to="{name: 'Login'}">로그인</RouterLink>
        <span class="divider">|</span>
        <RouterLink :to="{name: 'BookList'}">책 리스트</RouterLink>
        <span class="divider">|</span>
        <!-- <RouterLink :to="{name: 'ThreadListView'}">커뮤니티</RouterLink> | -->

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

.nav-left a,
.nav-right a {
  color: rgb(0, 105, 0);
  text-decoration: none;
  font-weight: bold;
}

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

