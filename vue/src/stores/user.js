// src/stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    isLoggedIn: false,
    username: ''
  }),
  actions: {
    login(name) {
      this.isLoggedIn = true
      this.username = name
    },
    logout() {
      this.isLoggedIn = false
      this.username = ''
    },
    initializeFromStorage() {
      const token = localStorage.getItem('token')
      const name = localStorage.getItem('name')
      if (token && name) {
        this.login(name)
      }
    }
  }
})
