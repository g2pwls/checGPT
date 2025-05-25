// src/stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    isLoggedIn: false,
    username: '',
    userId: null
  }),
  actions: {
    login(name) {
      this.isLoggedIn = true
      this.username = name
      this.userId = localStorage.getItem('userId')
    },
    logout() {
      this.isLoggedIn = false
      this.username = ''
      this.userId = null
      localStorage.removeItem('token')
      localStorage.removeItem('name')
      localStorage.removeItem('userId')
    },
    initializeFromStorage() {
      const token = localStorage.getItem('token')
      const name = localStorage.getItem('name')
      const userId = localStorage.getItem('userId')
      if (token && name && userId) {
        this.isLoggedIn = true
        this.username = name
        this.userId = userId
      }
    }
  }
})
