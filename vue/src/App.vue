<template>
  <header>
    <nav>
      <RouterLink :to="{name: 'SignUpView'}">회원가입</RouterLink> | 
      <RouterLink :to="{name: 'MyPageView'}">마이페이지</RouterLink> | 
      <RouterLink :to="{name: 'LoginView'}">로그인</RouterLink>
    </nav>
      
  </header>
  <router-view />
</template>

<script setup>
import {RouterView, RouterLink} from 'vue-router'
</script>

<style scoped>
</style>