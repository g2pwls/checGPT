import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import BookListView from '../views/BookListView.vue'
import BookDetailView from '../views/BookDetailView.vue'
import MyPageView from '@/views/MyPageView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ThreadDetail from '@/views/ThreadDetail.vue'

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
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView,
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
    {
      path: '/mypage',
      name: 'MyPageView',
      component: MyPageView,
    },
    {
      path: '/threads/:threadId',
      name: 'ThreadDetail',
      component: ThreadDetail,
      props: true,  // URL 파라미터를 props로 받기 위함
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    // 항상 페이지 상단으로 이동
    return { left: 0, top: 0 }
  },
})

export default router
