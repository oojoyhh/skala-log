<script setup>
// App.vue
// -----------------------------------------------------------------------------
// 모든 페이지에서 공통으로 보여지는 최상위 컴포넌트입니다.
// <router-view> 위치에 현재 URL 경로에 맞는 페이지 컴포넌트가 렌더링됩니다.
//   예) /login       -> LoginView.vue
//       /dex         -> PokedexView.vue
//       /dex/:id     -> PokemonDetailView.vue
// -----------------------------------------------------------------------------
import { useAuthStore } from './stores/auth'
import { useRouter, useRoute } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

// 로그아웃 버튼 클릭 시: 인증 상태를 비우고 로그인 화면으로 이동
function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="shell">
    <!-- 로그인 화면(/login)에서는 상단 바를 숨김: 로그인 전에는 도감 메뉴가 필요 없기 때문 -->
    <header v-if="route.name !== 'login'" class="topbar">
      <div class="topbar__brand">
        <span class="topbar__dot" aria-hidden="true"></span>
        POKÉDEX <span class="topbar__ver">v2.6</span>
      </div>

      <div v-if="auth.isLoggedIn" class="topbar__user">
        <span class="topbar__trainer">TRAINER · {{ auth.username }}</span>
        <button class="btn btn--ghost" @click="handleLogout">로그아웃</button>
      </div>
    </header>

    <!-- 실제 페이지 콘텐츠가 이 위치에 표시됨 -->
    <router-view />
  </div>
</template>

<style scoped>
.shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(to bottom, var(--surface), transparent);
  position: sticky;
  top: 0;
  z-index: 10;
  backdrop-filter: blur(6px);
}

.topbar__brand {
  font-family: var(--font-display);
  font-weight: 700;
  letter-spacing: 0.08em;
  font-size: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.topbar__dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--accent-scan);
  box-shadow: 0 0 8px var(--accent-scan);
}

.topbar__ver {
  color: var(--text-dim);
  font-weight: 400;
  font-size: 12px;
}

.topbar__user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.topbar__trainer {
  font-family: var(--font-display);
  font-size: 12px;
  color: var(--text-dim);
  letter-spacing: 0.04em;
}

.btn {
  font-family: var(--font-display);
  font-size: 12px;
  letter-spacing: 0.04em;
  padding: 8px 14px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface-alt);
  color: var(--text);
  cursor: pointer;
  transition: border-color 0.15s ease, color 0.15s ease;
}

.btn:hover {
  border-color: var(--accent-scan);
  color: var(--accent-scan);
}

.btn--ghost {
  border-color: var(--accent-red-dim);
  color: var(--accent-red);
}

.btn--ghost:hover {
  border-color: var(--accent-red);
  color: var(--accent-red);
}
</style>
