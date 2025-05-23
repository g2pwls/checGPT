import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import BookListView from '../views/BookListView.vue'
import BookDetailView from '../views/BookDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
    },
    {
      path: '/booklist',
      name: 'BookList',
      component: BookListView,
    },
    {
      path: '/books/:bookId',
      name: 'BookDetail',
      component: BookDetailView,
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    // 항상 페이지 상단으로 이동
    return { left: 0, top: 0 }
  },
})

export default router
