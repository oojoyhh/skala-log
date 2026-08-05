import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // State: 로그인 토큰 및 사용자 정보
  const token = ref(localStorage.getItem('accessToken') || null)
  const user = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  // Getters: 로그인 여부 확인 및 사용자 이름
  const isLoggedIn = computed(() => !!token.value)
  const username = computed(() => user.value?.name || '게스트')

  // Actions: 로그인 / 로그아웃 로직
  function login(userData, authToken) {
    user.value = userData
    token.value = authToken

    // 브라우저 재접속 시 유지용
    localStorage.setItem('accessToken', authToken)
    localStorage.setItem('userInfo', JSON.stringify(userData))
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('userInfo')
  }

  return { token, user, isLoggedIn, username, login, logout }
})
