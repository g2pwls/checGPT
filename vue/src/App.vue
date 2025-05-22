<script setup>
import { RouterLink, RouterView } from 'vue-router'
import LoginView from '@/views/LoginView.vue'

</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Home</RouterLink> |
      <!-- <RouterLink :to="{name: 'SignupView'}">Signup</RouterLink> | -->
      <RouterLink :to="{name: 'Login'}">로그인</RouterLink> |

    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
</style>
