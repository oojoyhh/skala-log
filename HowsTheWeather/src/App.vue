<script setup>
import { useRoute } from 'vue-router'

import TunedWeatherDashboard from './Components/tuned/TunedWeatherDashboard.vue'

import WeatherMockup from './Components/exercise/WeatherMockup.vue'
import WeatherComposition from './Components/exercise/WeatherComposition.vue'
import WeatherParent from './Components/exercise/WeatherParent.vue'
import UnitToggler from './Components/exercise/UnitToggler.vue'
import StoreCounter from './Components/practices/library/StoreCounter.vue'
import AxiosWeather from './Components/practices/library/AxiosWeather.vue'
import AxiosJson from './Components/practices/library/AxiosJson.vue'

const route = useRoute()
</script>

<template>
  <!-- 튜닝 -->
  <div class="app-container">
    <h1>✨ 나만의 날씨 대시보드</h1>
    <hr />

    <div class="dashboard-wrapper">
      <nav class="navigation-bar">
        <RouterLink to="/" class="nav-item">🌦️ 날씨 대시보드</RouterLink>
        <span class="divider">|</span>
        <RouterLink to="/about" class="nav-item">ℹ️ 서비스 소개</RouterLink>
        <UnitToggler />
      </nav>

      <main>
        <TunedWeatherDashboard v-if="route.name === 'WeatherHome'" />
        <RouterView v-else />
      </main>
    </div>
  </div>

  <div class="app-container">
    <h1>⛅ 과제 1: 날씨 (Mockup)</h1>
    <hr />
    <WeatherMockup />
  </div>

  <div class="app-container">
    <h1>⛅ 과제 2: 날씨 (컴포지션)</h1>
    <hr />
    <WeatherComposition />
  </div>

  <div class="app-container">
    <h1>⛅ 과제 3: 날씨 (컴포넌트)</h1>
    <hr />
    <WeatherParent />
  </div>

  <div class="app-container">
    <h1>⛅ 과제 4: 라우터적용</h1>
    <hr />
    <div class="dashboard-wrapper">
      <nav class="navigation-bar">
        <RouterLink to="/" class="nav-item">🌦️ 날씨 대시보드</RouterLink>
        <span class="divider">|</span>
        <RouterLink to="/about" class="nav-item">ℹ️ 서비스 소개</RouterLink>
      </nav>
      <main>
        <RouterView />
      </main>
    </div>
  </div>

  <div class="app-container">
    <h1>⛅ 과제 5: 스토어적용</h1>
    <hr />
    <div class="dashboard-wrapper">
      <nav class="navigation-bar">
        <RouterLink to="/" class="nav-item">🌦️ 날씨 대시보드</RouterLink>
        <span class="divider">|</span>
        <RouterLink to="/about" class="nav-item">ℹ️ 서비스 소개</RouterLink>
        <UnitToggler />
      </nav>
      <main>
        <RouterView />
      </main>
    </div>
  </div>

  <div class="app-container">
    <h1>1. Store</h1>
    <hr />
    <StoreCounter />

    <h1>2. Axios</h1>
    <hr />
    <AxiosWeather />
    <AxiosJson />
  </div>
</template>

<style>
@import '@/assets/exercise.css';
</style>
