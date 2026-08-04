import { createRouter, createWebHistory } from 'vue-router'
import WeatherHomeView from '../views/WeatherHomeView.vue'
import { useAuthStore } from '@/stores/authStore.js'

const routes = [
  {
    path: '/',
    name: 'WeatherHome',
    component: WeatherHomeView,
  },
  {
    path: '/about',
    name: 'WeatherAbout',
    component: () => import('../views/WeatherAboutView.vue'),
  },
  {
    path: '/weather/:cityId',
    name: 'WeatherDetail',
    component: () => import('../views/WeatherDetailView.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFoundView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Navigation Guard 연동
router.beforeEach((to, from) => {
  // Guard 내부에서 authStore 호출
  const authStore = useAuthStore()

  // 인증이 필요한 페이지 접근 시 로그인 여부 체크
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    alert('로그인이 필요한 서비스입니다.')
    return { name: 'Login', query: { redirect: to.fullPath }} // 로그인 후 돌아올 위치 전달

  // 이미 로그인한 사용자가 로그인 페이지 접근 시 메인으로 이동
  if (to.name === 'Login' && authStore.isLoggedIn) {
    return { name: 'Dashboard'}
  }
  }
})
export default router
