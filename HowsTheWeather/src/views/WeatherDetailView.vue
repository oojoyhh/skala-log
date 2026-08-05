<script setup>
import { computed, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useConfigStore } from '@/stores/configStore'
import { cities, fetchCityAirQuality, fetchCityWeather } from '@/api/weatherApi'
import { fetchCityForecastView } from '@/services/weatherService'
import { convertTemperature } from '@/domain/weather'
import AirQualityCard from '@/Components/tuned/AirQualityCard.vue'
import HourlyForecast from '@/Components/tuned/HourlyForecast.vue'
import DailyForecast from '@/Components/tuned/DailyForecast.vue'
import SunArc from '@/Components/tuned/SunArc.vue'
import WeatherMetrics from '@/Components/tuned/WeatherMetrics.vue'
import WeatherLoadingState from '@/Components/tuned/WeatherLoadingState.vue'

const route = useRoute()
const router = useRouter()
const configStore = useConfigStore()

const cityData = ref(null)
const hourly = ref([])
const daily = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

// route.params만 바뀌는 이동(같은 컴포넌트 재사용)도 감지해야 하므로 onMounted 대신 watch를 쓴다.
watch(
  () => route.params.cityId,
  async (id) => {
    const city = cities.find((item) => item.id === id)
    cityData.value = null
    hourly.value = []
    daily.value = []
    errorMessage.value = ''

    if (!city) {
      errorMessage.value = '해당 지역의 정보가 없습니다.'
      return
    }

    isLoading.value = true
    try {
      const [weather, forecast, airQuality] = await Promise.all([
        fetchCityWeather(city),
        fetchCityForecastView(city),
        fetchCityAirQuality(city),
      ])
      const today = forecast.daily[0]

      cityData.value = {
        ...weather,
        ...airQuality,
        minTemp: Math.min(weather.temp, today?.minTemp ?? weather.temp),
        maxTemp: Math.max(weather.temp, today?.maxTemp ?? weather.temp),
      }
      hourly.value = forecast.hourly
      daily.value = forecast.daily
    } catch (error) {
      errorMessage.value = error.message || '날씨 데이터를 불러오지 못했습니다.'
    } finally {
      isLoading.value = false
    }
  },
  { immediate: true },
)

const displayTemp = computed(() => convertTemperature(cityData.value?.temp ?? 0, configStore.unit))
const displayFeelsLike = computed(() =>
  convertTemperature(cityData.value?.feelsLike ?? 0, configStore.unit),
)
const displayMin = computed(() =>
  convertTemperature(cityData.value?.minTemp ?? 0, configStore.unit),
)
const displayMax = computed(() =>
  convertTemperature(cityData.value?.maxTemp ?? 0, configStore.unit),
)

const metrics = computed(() => {
  if (!cityData.value) return []

  return [
    { label: '체감', value: `${displayFeelsLike.value}°` },
    { label: '습도', value: `${cityData.value.humidity}%` },
    { label: '기압', value: `${cityData.value.pressure}hPa` },
    { label: '풍속', value: `${cityData.value.wind}m/s` },
  ]
})
</script>

<template>
  <el-card class="detail-container" shadow="hover">
    <WeatherLoadingState
      v-if="isLoading"
      title="상세 날씨를 불러오는 중이에요"
      description="시간별·일별 예보와 대기질 정보를 준비하고 있습니다."
    />
    <el-alert
      v-else-if="errorMessage"
      :title="errorMessage"
      type="error"
      show-icon
      :closable="false"
    />

    <template v-else-if="cityData">
      <header class="detail-header">
        <el-button @click="router.push('/')">홈 대시보드</el-button>
        <el-button type="primary" plain @click="router.push('/cities')">지역 목록</el-button>
      </header>

      <div class="detail-main">
        <div class="detail-identity">
          <img
            class="detail-icon"
            :src="`https://openweathermap.org/img/wn/${cityData.icon}@2x.png`"
            :alt="cityData.status"
          />

          <div class="detail-name-col">
            <small>상세 날씨</small>
            <h2>{{ cityData.name }}</h2>
            <p class="detail-status">{{ cityData.status }}</p>
          </div>
        </div>

        <div class="detail-temp">
          <strong>{{ displayTemp }}{{ configStore.unitSymbol }}</strong>
          <small>오늘 최저 {{ displayMin }}° · 최고 {{ displayMax }}°</small>
        </div>
      </div>

      <WeatherMetrics class="detail-metrics" :metrics="metrics" />

      <div class="detail-secondary">
        <AirQualityCard :pm10="cityData.pm10" :pm25="cityData.pm25" />
        <SunArc :sunrise="cityData.sunrise" :sunset="cityData.sunset" />
      </div>

      <section class="detail-forecast">
        <HourlyForecast :hourly="hourly" />
        <DailyForecast :daily="daily" />
      </section>
    </template>
  </el-card>
</template>

<style scoped>
.detail-container {
  border-color: #e4e7ed;
  border-radius: 16px;
  background: #fff;
}

.detail-container :deep(.el-card__body) {
  padding: 24px;
}

.detail-header {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.detail-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-top: 14px;
}

.detail-identity {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  min-width: 0;
}

.detail-icon {
  flex: 0 0 auto;
  width: 94px;
  height: 94px;
  border-radius: 50%;
  background: var(--weather-blue-soft);
}

.detail-status {
  margin: 1px 0 0;
  color: #5c7891;
  font-size: 15px;
  font-weight: 700;
}

.detail-name-col {
  display: grid;
  gap: 4px;
}

.detail-name-col small {
  color: #718096;
  font-weight: 700;
}

.detail-name-col h2 {
  margin: 0;
  color: #2d4864;
  font-size: 38px;
  line-height: 1.08;
}

.detail-temp {
  display: grid;
  flex: 0 0 auto;
  justify-items: end;
  gap: 5px;
  text-align: right;
}

.detail-temp strong {
  color: #1f354b;
  font-size: 48px;
  line-height: 1;
}

.detail-temp small {
  color: #71879a;
  font-weight: 700;
  white-space: nowrap;
}

.detail-metrics {
  margin-top: 20px;
}

.detail-metrics :deep(div) {
  background: #fff;
}

.detail-secondary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
  margin-top: 12px;
}

.detail-forecast {
  display: grid;
  gap: 16px;
  margin-top: 20px;
}

@media (max-width: 560px) {
  .detail-container :deep(.el-card__body) {
    padding: 18px;
  }

  .detail-main {
    flex-direction: column;
    align-items: flex-start;
  }

  .detail-temp {
    justify-items: start;
    text-align: left;
  }

  .detail-temp strong {
    font-size: 40px;
  }

  .detail-name-col h2 {
    font-size: 32px;
    white-space: nowrap;
  }

  .detail-icon {
    width: 82px;
    height: 82px;
  }
}
</style>
