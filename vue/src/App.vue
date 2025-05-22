<script setup>
import { RouterLink, RouterView } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import BookListView from '@/views/BookListView.vue'

</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Home</RouterLink> |
      <!-- <RouterLink :to="{name: 'SignupView'}">Signup</RouterLink> | -->
      <RouterLink :to="{name: 'Login'}">로그인</RouterLink> |
      <RouterLink :to="{name: 'BookList'}">책 리스트</RouterLink>

    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
</style>
