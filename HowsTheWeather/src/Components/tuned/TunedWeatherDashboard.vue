<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowRight, WarningFilled } from '@element-plus/icons-vue'

import { cities } from '@/api/weatherApi'
import { fetchCityWeatherSummary } from '@/services/weatherService'
import { fetchCityWarnings } from '@/services/warningService'
import MyWeatherHero from './MyWeatherHero.vue'
import WeatherLoadingState from './WeatherLoadingState.vue'

const router = useRouter()

const weatherData = ref(null)
const myCityId = ref(cities[0].id)
const isLoading = ref(false)
const errorMessage = ref('')
const warnings = ref([])

const loadWeather = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const city = cities.find((item) => item.id === myCityId.value) ?? cities[0]
    weatherData.value = await fetchCityWeatherSummary(city)
  } catch (error) {
    errorMessage.value = error.message || '날씨 데이터를 불러오지 못했습니다.'
  } finally {
    isLoading.value = false
  }
}

// 선택한 내 위치의 도시 객체를 찾음
const myCityInfo = computed(() => {
  return weatherData.value
})

const warningSummary = computed(() => {
  if (!warnings.value.length) return ''

  const firstWarning = warnings.value[0]
  const extraCount = warnings.value.length - 1
  return `${firstWarning.region} ${firstWarning.type} ${firstWarning.level}${extraCount ? ` 외 ${extraCount}건` : ''}`
})

const loadWarnings = async () => {
  try {
    const cityName = cities.find((city) => city.id === myCityId.value)?.name ?? cities[0].name
    warnings.value = await fetchCityWarnings(cityName)
  } catch {
    // 대시보드는 특보 API 오류로 막지 않음. 자세한 오류는 특보 화면에서 안내함
    warnings.value = []
  }
}

// 저장된 내 위치를 화면이 열릴 때 불러옴
onMounted(() => {
  const savedCityId = localStorage.getItem('tunedMyCityId')
  const isValidCity = cities.some((city) => city.id === savedCityId)

  if (isValidCity) {
    myCityId.value = savedCityId
  }

  loadWeather()
  loadWarnings()
})
</script>

<template>
  <div class="tuned-dashboard">
    <header class="dashboard-heading">
      <el-tag type="primary" effect="light" round>LIVE WEATHER</el-tag>
      <h1>How's The Weather?</h1>
      <p>내 지역의 현재 날씨와 시간대별 예보를 한눈에 확인하세요.</p>
    </header>

    <el-card v-if="warnings.length" class="warning-banner" shadow="never">
      <div class="warning-banner-body">
        <span class="warning-icon" aria-hidden="true">
          <el-icon><WarningFilled /></el-icon>
        </span>
        <div class="warning-copy">
          <span>WEATHER ALERT</span>
          <strong>{{ warningSummary }}</strong>
          <small>내 지역에 발효 중인 특보가 있습니다. 외출 전 행동 요령을 확인하세요.</small>
        </div>
        <el-button type="danger" plain @click="router.push('/forecast')">
          자세히 보기 <el-icon class="el-icon--right"><ArrowRight /></el-icon>
        </el-button>
      </div>
    </el-card>

    <el-alert
      v-if="errorMessage"
      :title="errorMessage"
      type="error"
      show-icon
      :closable="false"
    />
    <WeatherLoadingState
      v-else-if="isLoading && !weatherData"
      title="내 지역 날씨를 불러오는 중이에요"
      description="현재 날씨와 시간대별 예보를 준비하고 있습니다."
    />
    <MyWeatherHero v-else-if="myCityInfo" :weather="myCityInfo" />
  </div>
</template>

<style scoped>
.tuned-dashboard {
  display: grid;
  gap: 22px;
  width: min(100%, 820px);
  margin: 0 auto;
}

.dashboard-heading {
  display: grid;
  justify-items: start;
  padding: 8px 4px 0;
}

.dashboard-heading > :deep(.el-tag) {
  margin-bottom: 14px;
}

.dashboard-heading h1 {
  margin: 0 0 6px;
  color: #303133;
  font-size: clamp(1.75rem, 5vw, 2.45rem);
  letter-spacing: -0.04em;
}

.dashboard-heading p {
  margin: 0;
  color: #909399;
}

.warning-banner {
  overflow: hidden;
  border-color: #fab6b6;
  border-radius: 16px;
  background: linear-gradient(120deg, #fef0f0, #fff);
}

.warning-banner :deep(.el-card__body) {
  padding: 18px 20px;
}

.warning-banner-body {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 14px;
}

.warning-icon {
  display: grid;
  width: 44px;
  height: 44px;
  border-radius: 13px;
  color: #f56c6c;
  background: #fde2e2;
  font-size: 23px;
  place-items: center;
}

.warning-copy {
  display: grid;
  gap: 2px;
}

.warning-copy > span {
  color: #f56c6c;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.1em;
}

.warning-copy strong {
  color: #713838;
}

.warning-copy small {
  color: #a16c6c;
}

@media (max-width: 560px) {
  .warning-banner-body {
    grid-template-columns: auto minmax(0, 1fr);
    align-items: flex-start;
  }

  .warning-banner-body :deep(.el-button) {
    grid-column: 1 / -1;
    width: 100%;
  }
}
</style>
