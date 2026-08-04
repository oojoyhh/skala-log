<script setup>
// views/LoginView.vue
// -----------------------------------------------------------------------------
// 로그인 화면.
// 사용자가 아이디/비밀번호를 입력하면 authStore.login()을 호출하고,
// 그 내부에서 api/fakeAuth.js의 fakeLogin()이 실행됩니다(가짜 API 요청).
// 로그인에 성공하면 원래 가려던 페이지(redirect 쿼리) 혹은 /dex로 이동시킵니다.
// -----------------------------------------------------------------------------
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import IconWarning from '../components/icons/IconWarning.vue'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

// v-model로 입력창과 연결되는 반응형 변수
const username = ref('')
const password = ref('')

async function handleSubmit() {
  const success = await auth.login(username.value.trim(), password.value)

  if (success) {
    // 로그인 페이지에 진입하기 전에 가려던 경로가 있으면 그곳으로, 없으면 도감으로 이동
    const target = route.query.redirect || '/dex'
    router.push(target)
  }
  // 실패 시에는 auth.loginError에 메시지가 담기고, 템플릿에서 그대로 보여줌
}

// 데모용 테스트 계정을 빠르게 채워주는 버튼 (데모/QA 편의용)
function fillDemoAccount() {
  username.value = 'ash'
  password.value = 'pikachu'
}
</script>

<template>
  <div class="login">
    <div class="login__panel">
      <!-- 상단 로고 영역: 스캐너 렌즈를 형상화한 원형 아이콘 -->
      <div class="login__lens" aria-hidden="true">
        <div class="login__lens-core"></div>
      </div>

      <h1 class="login__title">POKÉDEX ACCESS</h1>
      <p class="login__subtitle">트레이너 인증이 필요합니다</p>

      <form class="login__form" @submit.prevent="handleSubmit">
        <label class="field">
          <span class="field__label">TRAINER ID</span>
          <input
            v-model="username"
            type="text"
            placeholder="ash"
            autocomplete="username"
            required
          />
        </label>

        <label class="field">
          <span class="field__label">PASSWORD</span>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            autocomplete="current-password"
            required
          />
        </label>

        <!-- 로그인 실패 시에만 에러 메시지 표시 -->
        <p v-if="auth.loginError" class="login__error" role="alert">
          <IconWarning :size="14" />
          {{ auth.loginError }}
        </p>

        <button type="submit" class="login__submit" :disabled="auth.isLoggingIn">
          {{ auth.isLoggingIn ? '인증 중...' : 'ENTER' }}
        </button>
      </form>

      <button class="login__demo" type="button" @click="fillDemoAccount">
        데모 계정 자동입력 (ash / pikachu)
      </button>
    </div>
  </div>
</template>

<style scoped>
.login {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  min-height: 100vh;
}

.login__panel {
  width: 100%;
  max-width: 340px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 32px 28px 24px;
  text-align: center;
  box-shadow: 0 0 0 6px var(--bg), 0 20px 60px -20px #000a;
}

.login__lens {
  width: 56px;
  height: 56px;
  margin: 0 auto 20px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #3a4568, #171b28 70%);
  border: 2px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login__lens-core {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--accent-scan);
  box-shadow: 0 0 14px var(--accent-scan);
}

.login__title {
  font-family: var(--font-display);
  font-size: 18px;
  letter-spacing: 0.08em;
  margin: 0 0 4px;
}

.login__subtitle {
  color: var(--text-dim);
  font-size: 13px;
  margin: 0 0 24px;
}

.login__form {
  display: flex;
  flex-direction: column;
  gap: 14px;
  text-align: left;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field__label {
  font-family: var(--font-display);
  font-size: 11px;
  letter-spacing: 0.08em;
  color: var(--text-dim);
}

.field input {
  background: var(--surface-alt);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 12px;
  color: var(--text);
  font-size: 14px;
}

.field input:focus {
  border-color: var(--accent-scan);
}

.login__error {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--accent-red);
  font-size: 12px;
  margin: 0;
}

.login__submit {
  margin-top: 6px;
  padding: 12px;
  border-radius: 8px;
  border: none;
  background: var(--accent-scan);
  color: #0b1410;
  font-family: var(--font-display);
  font-weight: 700;
  letter-spacing: 0.08em;
  cursor: pointer;
  transition: opacity 0.15s ease;
}

.login__submit:disabled {
  opacity: 0.6;
  cursor: default;
}

.login__demo {
  margin-top: 16px;
  background: none;
  border: none;
  color: var(--text-dim);
  font-size: 12px;
  text-decoration: underline;
  cursor: pointer;
}

.login__demo:hover {
  color: var(--accent-scan);
}
</style>
