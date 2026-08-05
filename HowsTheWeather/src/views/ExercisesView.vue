<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import ServiceIntroduction from '@/Components/exercise/ServiceIntroduction.vue'
import PracticeDayHeader from '@/Components/exercise/PracticeDayHeader.vue'
import UnitToggler from '@/Components/exercise/UnitToggler.vue'
import WeatherComposition from '@/Components/exercise/WeatherComposition.vue'
import WeatherMockup from '@/Components/exercise/WeatherMockup.vue'
import WeatherParent from '@/Components/exercise/WeatherParent.vue'
import AxiosJson from '@/Components/practices/library/AxiosJson.vue'
import AxiosWeather from '@/Components/practices/library/AxiosWeather.vue'
import ElementPlusPractice from '@/Components/practices/library/ElementPlusPractice.vue'
import ModernJavaScriptChallenge from '@/Components/practices/library/ModernJavaScriptChallenge.vue'
import StoreCounter from '@/Components/practices/library/StoreCounter.vue'
import WeatherHomeView from '@/views/WeatherHomeView.vue'

const tabs = [
  { id: 'mockup', label: 'Mockup', icon: '🧱', subtitle: '과제 1 · 정적 마크업' },
  { id: 'composition', label: 'Composition', icon: '🧩', subtitle: '과제 2 · Composition API' },
  { id: 'component', label: 'Component', icon: '🏗️', subtitle: '과제 3 · 컴포넌트 분리' },
  { id: 'router', label: 'Router', icon: '🧭', subtitle: '과제 4 · Vue Router' },
  { id: 'store-route', label: 'Store 적용', icon: '🗂️', subtitle: '과제 5 · 전역 상태 적용' },
  { id: 'store', label: 'Store', icon: '📦', subtitle: '과제 6 · Pinia' },
  { id: 'axios', label: 'Axios', icon: '🔌', subtitle: '과제 7 · API 통신' },
  { id: 'element-plus', label: 'Element Plus', icon: '🎨', subtitle: '과제 8 · UI 라이브러리' },
  { id: 'modern-js', label: 'Modern JavaScript', icon: '⚡', subtitle: '과제 9 · MODERN JAVASCRIPT' },
]

const route = useRoute()
const tabIds = tabs.map((tab) => tab.id)

const activeTab = computed(() => {
  const requestedTab = route.query.exercise
  return typeof requestedTab === 'string' && tabIds.includes(requestedTab)
    ? requestedTab
    : tabs[0].id
})

const demoPage = computed(() => (route.query.demo === 'about' ? 'about' : 'dashboard'))

const exerciseRoute = (exercise, demo) => ({
  name: 'Exercises',
  query: {
    exercise,
    ...(demo ? { demo } : {}),
  },
  hash: demo ? `#${exercise}-demo` : '#exercises',
})
</script>

<template>
  <div id="exercises" class="exercises-container">
    <header class="exercises-heading">
      <el-tag type="primary" effect="light" round>SKALA PRACTICE LAB</el-tag>
      <h1>🧪 실습 내비게이션</h1>
      <p>각 실습을 선택하면 해당 내용만 표시됩니다.</p>
    </header>

    <nav class="exercises-nav" aria-label="실습 목록">
      <RouterLink
        v-for="tab in tabs"
        :key="tab.id"
        :to="exerciseRoute(tab.id)"
        class="tab-link"
        :class="{ 'is-active': activeTab === tab.id }"
      >
        <span class="tab-icon" aria-hidden="true">{{ tab.icon }}</span>
        <span>
          <strong>{{ tab.label }}</strong>
          <small>{{ tab.subtitle }}</small>
        </span>
      </RouterLink>
    </nav>

    <section v-if="activeTab === 'mockup'" class="assignment-section">
      <PracticeDayHeader
        day="과제 1"
        name="MOCKUP"
        title="날씨 Mockup"
        description="단일 컴포넌트에서 날씨 목록과 선택 상태를 구성합니다."
      />
      <el-card class="assignment-card" shadow="never">
        <WeatherMockup />
      </el-card>
    </section>

    <section v-else-if="activeTab === 'composition'" class="assignment-section">
      <PracticeDayHeader
        day="과제 2"
        name="COMPOSITION"
        title="Composition API 날씨"
        description="computed, watch, watchEffect로 검색과 선택 상태를 관리합니다."
      />
      <el-card class="assignment-card" shadow="never">
        <WeatherComposition />
      </el-card>
    </section>

    <section v-else-if="activeTab === 'component'" class="assignment-section">
      <PracticeDayHeader
        day="과제 3"
        name="COMPONENT"
        title="컴포넌트 기반 날씨"
        description="검색, 카드, 레이아웃을 독립 컴포넌트로 분리합니다."
      />
      <el-card class="assignment-card" shadow="never">
        <WeatherParent />
      </el-card>
    </section>

    <section v-else-if="activeTab === 'router'" id="router-demo" class="assignment-section">
      <PracticeDayHeader
        day="과제 4"
        name="ROUTER"
        title="Vue Router 날씨"
        description="대시보드와 서비스 소개를 URL 상태로 전환합니다."
      />
      <el-card class="assignment-card exercise-demo" shadow="never">
        <nav class="navigation-bar" aria-label="과제 4 화면">
          <RouterLink
            :to="exerciseRoute('router', 'dashboard')"
            class="nav-item"
            :class="{ 'is-active': demoPage === 'dashboard' }"
          >
            🌦️ 날씨 대시보드
          </RouterLink>
          <span class="divider">|</span>
          <RouterLink
            :to="exerciseRoute('router', 'about')"
            class="nav-item"
            :class="{ 'is-active': demoPage === 'about' }"
          >
            ℹ️ 서비스 소개
          </RouterLink>
        </nav>

        <ServiceIntroduction
          v-if="demoPage === 'about'"
          :home-to="exerciseRoute('router', 'dashboard')"
        />
        <WeatherHomeView v-else />
      </el-card>
    </section>

    <section
      v-else-if="activeTab === 'store-route'"
      id="store-route-demo"
      class="assignment-section"
    >
      <PracticeDayHeader
        day="과제 5"
        name="STORE"
        title="Pinia Store 날씨"
        description="전역 온도 단위 상태를 여러 날씨 컴포넌트에서 공유합니다."
      />
      <el-card class="assignment-card exercise-demo" shadow="never">
        <nav class="navigation-bar" aria-label="과제 5 화면">
          <RouterLink
            :to="exerciseRoute('store-route', 'dashboard')"
            class="nav-item"
            :class="{ 'is-active': demoPage === 'dashboard' }"
          >
            🌦️ 날씨 대시보드
          </RouterLink>
          <span class="divider">|</span>
          <RouterLink
            :to="exerciseRoute('store-route', 'about')"
            class="nav-item"
            :class="{ 'is-active': demoPage === 'about' }"
          >
            ℹ️ 서비스 소개
          </RouterLink>
          <UnitToggler />
        </nav>

        <ServiceIntroduction
          v-if="demoPage === 'about'"
          :home-to="exerciseRoute('store-route', 'dashboard')"
        />
        <WeatherHomeView v-else />
      </el-card>
    </section>

    <section v-else-if="activeTab === 'store'" class="library-section">
      <StoreCounter />
    </section>

    <section v-else-if="activeTab === 'axios'" class="library-section">
      <AxiosWeather />
      <AxiosJson />
    </section>

    <section v-else-if="activeTab === 'element-plus'" class="library-section">
      <ElementPlusPractice />
    </section>

    <section v-else class="library-section">
      <ModernJavaScriptChallenge />
    </section>
  </div>
</template>

<style scoped>
.exercises-container {
  scroll-margin-top: 1rem;
}

.exercises-heading {
  padding: 8px 4px 0;
  margin-bottom: 1.5rem;
}

.exercises-heading h1 {
  margin: 10px 0 4px;
  color: #303133;
  font-size: clamp(1.75rem, 5vw, 2.45rem);
  letter-spacing: -0.04em;
}

.exercises-heading p {
  margin: 0;
  color: #909399;
}

.exercises-nav {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 12px;
  margin-bottom: 2rem;
}

.tab-link {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
  padding: 14px 16px;
  border: 1px solid #e4e7ed;
  border-radius: 12px;
  color: #606266;
  text-decoration: none;
  background: #fff;
  transition:
    border-color 0.2s ease,
    color 0.2s ease,
    background 0.2s ease;
}

.tab-link:hover {
  border-color: #a0cfff;
  color: #337ecc;
  background: #ecf5ff;
}

.tab-link.is-active {
  border-color: #409eff;
  color: #337ecc;
  background: #ecf5ff;
  box-shadow: 0 4px 14px rgb(64 158 255 / 12%);
}

.tab-icon {
  display: grid;
  flex: 0 0 40px;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #f4f4f5;
  font-size: 1.1rem;
  place-items: center;
}

.tab-link.is-active .tab-icon {
  background: #d9ecff;
}

.tab-link strong,
.tab-link small {
  display: block;
}

.tab-link strong {
  color: #303133;
  font-size: 0.95rem;
  font-weight: 750;
}

.tab-link small {
  margin-top: 2px;
  color: #909399;
  font-size: 0.72rem;
}

.exercise-demo .nav-item.router-link-active,
.exercise-demo .nav-item.router-link-exact-active {
  padding-bottom: 4px;
  border-bottom: 0;
  color: #7f8c8d;
}

.exercise-demo .nav-item.is-active {
  padding-bottom: 2px;
  border-bottom: 2px solid var(--weather-blue);
  color: var(--weather-blue);
}

.exercise-demo {
  scroll-margin-top: 1rem;
}

.library-section {
  display: grid;
  gap: 1.25rem;
  min-width: 0;
}

.assignment-section {
  padding: clamp(1.25rem, 3vw, 2rem);
  border: 1px solid #e4e7ed;
  border-radius: 18px;
  background:
    radial-gradient(circle at 0 0, rgb(64 158 255 / 8%), transparent 32%),
    #f8fafc;
}

.assignment-card {
  border-radius: 12px;
}

.assignment-card :deep(.el-card__body) {
  padding: clamp(1rem, 3vw, 1.5rem);
}
</style>
