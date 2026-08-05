<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Bell, Cloudy, House, InfoFilled, Notebook, Search } from '@element-plus/icons-vue'

import UnitToggler from './Components/exercise/UnitToggler.vue'
import TunedWeatherDashboard from './Components/tuned/TunedWeatherDashboard.vue'

const route = useRoute()
const isExercises = computed(() => route.name === 'Exercises')

// Code Challenge - env: 현재 빌드 모드에 주입된 API 엔드포인트 확인용
console.log('현재 빌드 모드:', import.meta.env.MODE)
console.log('주입된 VITE_API_URL:', import.meta.env.VITE_API_URL)

</script>

<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="header-inner">
        <RouterLink to="/" class="app-brand">
          <span class="brand-icon" aria-hidden="true"
            ><el-icon><Cloudy /></el-icon
          ></span>
          <span>
            <strong>How's The Weather?</strong>
            <small>나만의 날씨 대시보드</small>
          </span>
        </RouterLink>

        <nav class="service-nav" aria-label="날씨 서비스">
          <RouterLink to="/" class="service-link" aria-label="대시보드">
            <el-icon><House /></el-icon><span>대시보드</span>
          </RouterLink>
          <RouterLink to="/cities" class="service-link" aria-label="지역 검색">
            <el-icon><Search /></el-icon><span>지역 검색</span>
          </RouterLink>
          <RouterLink to="/forecast" class="service-link" aria-label="특보">
            <el-icon><Bell /></el-icon><span>특보</span>
          </RouterLink>
          <RouterLink to="/about" class="service-link" aria-label="서비스 소개">
            <el-icon><InfoFilled /></el-icon><span>서비스 소개</span>
          </RouterLink>
        </nav>

        <div class="header-tools">
          <UnitToggler v-if="!isExercises" />
          <RouterLink :to="{ name: 'Exercises' }" class="practice-switch" :class="{ 'is-active': isExercises }">
            <el-icon><Notebook /></el-icon>
            <span>실습</span>
          </RouterLink>
        </div>
      </div>
    </header>

    <div class="app-container">
      <RouterView v-if="isExercises" />

      <div v-else class="dashboard-wrapper">
        <main>
          <TunedWeatherDashboard v-if="route.name === 'WeatherHome'" />
          <RouterView v-else />
        </main>
      </div>
    </div>
  </div>
</template>

<style>
@import '@/assets/exercise.css';

.app-shell {
  min-height: 100vh;
  color: #2c3e50;
  font-family: -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', system-ui, Roboto, sans-serif;
  font-weight: 500;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  --el-font-family: 'Apple SD Gothic Neo', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
}

.app-shell button,
.app-shell input,
.app-shell textarea,
.app-shell select,
.app-shell .el-button,
.app-shell .el-tag,
.app-shell .el-input__inner,
.app-shell .el-select__placeholder {
  font-family: inherit !important;
}

.app-header {
  position: sticky;
  z-index: 20;
  top: 0;
  border-bottom: 1px solid #e4e7ed;
  background: rgb(255 255 255 / 94%);
  box-shadow: 0 4px 18px rgb(31 53 75 / 6%);
  backdrop-filter: blur(14px);
}

.header-inner {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 22px;
  width: min(calc(100% - 32px), 1060px);
  min-height: 72px;
  margin: 0 auto;
}

.app-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #303133;
  text-decoration: none;
}

.brand-icon {
  display: grid;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  color: #409eff;
  background: #ecf5ff;
  font-size: 22px;
  place-items: center;
}

.app-brand strong,
.app-brand small {
  display: block;
}

.app-brand strong {
  font-size: 0.96rem;
  letter-spacing: -0.02em;
  white-space: nowrap;
}

.app-brand small {
  margin-top: 2px;
  color: #909399;
  font-size: 0.7rem;
}

.service-nav {
  display: flex;
  justify-content: center;
  gap: 4px;
}

.service-link,
.practice-switch {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 11px;
  border-radius: 9px;
  color: #606266;
  text-decoration: none;
  font-size: 0.84rem;
  font-weight: 700;
  transition: 0.2s ease;
}

.service-link:hover,
.service-link.router-link-exact-active,
.practice-switch:hover,
.practice-switch.is-active {
  color: #337ecc;
  background: #ecf5ff;
}

.header-tools {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-tools .unit-toggler {
  width: auto;
  margin: 0;
}

.app-shell > .app-container {
  box-sizing: border-box;
  width: min(calc(100% - 32px), 980px);
  max-width: none;
  margin: 24px auto 40px;
  padding: clamp(20px, 4vw, 40px);
  font-family: inherit;
}

.app-shell .dashboard-wrapper {
  width: 100%;
  margin: 0;
}

@media (max-width: 860px) {
  .header-inner {
    grid-template-columns: 1fr auto;
    gap: 10px;
    padding: 10px 0;
  }

  .service-nav {
    grid-column: 1 / -1;
    grid-row: 2;
    justify-content: flex-start;
    overflow-x: auto;
    padding-bottom: 2px;
  }
}

@media (max-width: 560px) {
  .app-brand small,
  .service-link span {
    display: none;
  }

  .service-link {
    padding: 9px 13px;
    font-size: 1rem;
  }

  .app-shell > .app-container {
    width: calc(100% - 20px);
    margin-top: 12px;
    padding: 16px;
  }
}
</style>
