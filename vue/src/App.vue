<template>
  <header>
    <nav>
      <RouterLink :to="{name: 'SignUpView'}">Sign Up</RouterLink> | 
      <RouterLink :to="{name: 'MyPageView'}">My Page</RouterLink>
    </nav>
      
  </header>
  <router-view />
</template>

<script setup>
import {RouterView, RouterLink} from 'vue-router'
</script>

<style scoped>

</style>