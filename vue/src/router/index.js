import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import LoginView from '../views/LoginView.vue'
import BookListView from '../views/BookListView.vue'
import BookDetailView from '../views/BookDetailView.vue'
import ProfileView from '@/views/ProfileView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ThreadDetail from '@/views/ThreadDetail.vue'
import ReportView from '@/views/ReportView.vue'
import CommunityView from '../views/CommunityView.vue'
import CommunityDetailView from '@/views/CommunityDetailView.vue'
import AIView from '../views/AIView.vue'
import StoryView from '@/views/StoryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView
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
      path: '/books/:bookId/ai',
      name: 'book-ai',
      component: AIView,
      props: true
    },
    {
      path: '/users/:userId/profile',
      name: 'UserProfile',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/threads/:threadId',
      name: 'ThreadDetail',
      component: ThreadDetail,
      props: true,
    },
    {
      path: '/report',
      name: 'Report',
      component: ReportView,
      meta: { requiresAuth: true }
    },
    {
      path: '/books/:bookId/community',
      name: 'community',
      component: () => import('@/views/CommunityView.vue'),
      props: true
    },
    {
      path: '/community/:postId',
      name: 'communityDetail',
      component: CommunityDetailView,
      props: true
    },
    {
      path: '/ai/:book',
      name: 'ai',
      component: AIView,
      props: true
    },
    {
      path: '/story',
      name: 'story',
      component: StoryView
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    // 항상 페이지 상단으로 이동
    return { left: 0, top: 0 }
  },
})

export default router
