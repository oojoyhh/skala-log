// stores/auth.js
// -----------------------------------------------------------------------------
// Pinia를 사용한 "인증 상태 저장소(Store)".
// 로그인 여부(token), 로그인한 사용자 이름을 앱 어디서든 꺼내 쓸 수 있게 관리합니다.
//
// localStorage에 토큰을 저장해두면, 브라우저를 새로고침해도
// 로그인 상태가 유지됩니다 (진짜 서비스의 "로그인 유지"와 동일한 원리).
// -----------------------------------------------------------------------------
import { defineStore } from 'pinia'
import { fakeLogin } from '../api/fakeAuth'

export const useAuthStore = defineStore('auth', {
  // state: 이 스토어가 들고 있는 실제 데이터
  state: () => ({
    token: localStorage.getItem('pokedex_token') || null,
    username: localStorage.getItem('pokedex_username') || '',
    loginError: '', // 로그인 실패 시 사용자에게 보여줄 에러 메시지
    isLoggingIn: false, // 로그인 요청이 진행 중인지 여부 (버튼 로딩 표시용)
  }),

  // getters: state로부터 계산되는 파생 값 (computed와 비슷한 역할)
  getters: {
    isLoggedIn: (state) => !!state.token,
  },

  // actions: state를 변경하는 함수들 (여기서 비동기 로직도 처리 가능)
  actions: {
    /**
     * 로그인 시도
     * @param {string} username
     * @param {string} password
     * @returns {Promise<boolean>} 성공 여부
     */
    async login(username, password) {
      this.isLoggingIn = true
      this.loginError = ''

      try {
        // 가짜 API 호출 (api/fakeAuth.js)
        const { token, username: name } = await fakeLogin(username, password)

        // 성공하면 state와 localStorage 둘 다 갱신
        this.token = token
        this.username = name
        localStorage.setItem('pokedex_token', token)
        localStorage.setItem('pokedex_username', name)

        return true
      } catch (err) {
        this.loginError = err.message
        return false
      } finally {
        this.isLoggingIn = false
      }
    },

    /** 로그아웃: 저장된 인증 정보를 모두 제거 */
    logout() {
      this.token = null
      this.username = ''
      localStorage.removeItem('pokedex_token')
      localStorage.removeItem('pokedex_username')
    },
  },
})
