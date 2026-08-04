// router/index.js
// -----------------------------------------------------------------------------
// URL 경로(path)와 화면 컴포넌트를 연결하는 라우터 설정 파일입니다.
// 또한 "네비게이션 가드(beforeEach)"를 사용해서
//   - 로그인하지 않은 사용자가 도감 페이지에 접근하면 -> 로그인 페이지로 강제 이동
//   - 이미 로그인한 사용자가 로그인 페이지에 접근하면 -> 도감 페이지로 이동
// 하도록 처리합니다.
// -----------------------------------------------------------------------------
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const routes = [
  {
    path: '/',
    redirect: '/dex', // 루트 경로 접속 시 도감 페이지로 리다이렉트 (가드가 로그인 여부를 다시 판단함)
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'), // 지연 로딩(lazy load)으로 초기 로딩 속도 개선
  },
  {
    path: '/dex',
    name: 'dex',
    component: () => import('../views/PokedexView.vue'),
    meta: { requiresAuth: true }, // 이 라우트는 로그인이 필요함을 표시
  },
  {
    path: '/dex/:id',
    name: 'pokemon-detail',
    component: () => import('../views/PokemonDetailView.vue'),
    meta: { requiresAuth: true },
    props: true, // :id 파라미터를 컴포넌트의 props로 그대로 전달
  },
]

const router = createRouter({
  history: createWebHistory(), // 브라우저의 History API를 사용한 깔끔한 URL (해시 없음)
  routes,
})

// 모든 라우트 이동 전에 실행되는 전역 가드
router.beforeEach((to) => {
  const auth = useAuthStore()

  // 로그인이 필요한 페이지인데 로그인 상태가 아니라면 로그인 화면으로 보냄
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  // 이미 로그인한 상태에서 로그인 페이지로 다시 가려고 하면 도감으로 보냄
  if (to.name === 'login' && auth.isLoggedIn) {
    return { name: 'dex' }
  }

  return true // 그 외의 경우는 정상적으로 이동 허용
})

export default router
