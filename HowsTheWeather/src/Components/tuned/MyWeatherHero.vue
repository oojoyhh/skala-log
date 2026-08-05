<script setup>
import { computed } from 'vue'
import { useConfigStore } from '@/stores/configStore'
import { convertTemperature } from '@/domain/weather'
import AirQualityCard from './AirQualityCard.vue'
import DailyForecast from './DailyForecast.vue'
import HourlyForecast from './HourlyForecast.vue'
import SunArc from './SunArc.vue'
import WeatherMetrics from './WeatherMetrics.vue'

const props = defineProps({
  weather: {
    type: Object,
    required: true,
  },
})

const configStore = useConfigStore()
const displayTemp = computed(() => convertTemperature(props.weather.temp, configStore.unit))
const displayMin = computed(() => convertTemperature(props.weather.minTemp, configStore.unit))
const displayMax = computed(() => convertTemperature(props.weather.maxTemp, configStore.unit))
const displayFeelsLike = computed(() =>
  convertTemperature(props.weather.feelsLike, configStore.unit),
)

const metrics = computed(() => [
  { label: '체감', value: `${displayFeelsLike.value}°` },
  { label: '습도', value: `${props.weather.humidity}%` },
  { label: '기압', value: `${props.weather.pressure}hPa` },
  { label: '풍속', value: `${props.weather.wind}m/s` },
])
</script>

<template>
  <el-card class="my-weather-hero" shadow="hover">
    <template #header>
      <div class="hero-top">
        <div>
          <el-tag type="primary" effect="dark" round>MY LOCATION</el-tag>
          <span>저장된 내 지역 날씨</span>
        </div>
        <RouterLink to="/cities">
          <el-button type="primary" plain>다른 지역 보기 →</el-button>
        </RouterLink>
      </div>
    </template>

    <div class="hero-main">
      <div class="hero-identity">
        <el-avatar
          class="hero-icon"
          :size="94"
          :src="`https://openweathermap.org/img/wn/${weather.icon}@2x.png`"
        />

        <div class="hero-name-col">
          <h2>{{ weather.name }}</h2>
          <p class="hero-status">{{ weather.status }}</p>
        </div>
      </div>

      <div class="hero-temp">
        <strong>{{ displayTemp }}{{ configStore.unitSymbol }}</strong>
        <small>오늘 최저 {{ displayMin }}° · 최고 {{ displayMax }}°</small>
      </div>
    </div>

    <WeatherMetrics class="hero-metrics" :metrics="metrics" />

    <div class="hero-secondary">
      <AirQualityCard :pm10="weather.pm10" :pm25="weather.pm25" />
      <SunArc :sunrise="weather.sunrise" :sunset="weather.sunset" />
    </div>

    <section class="hero-forecast">
      <HourlyForecast :hourly="weather.hourly" />
      <DailyForecast :daily="weather.daily" />
    </section>
  </el-card>
</template>

<style scoped>
.my-weather-hero {
  overflow: hidden;
  border: 1px solid #a0cfff;
  border-radius: 16px;
  background: linear-gradient(135deg, #fff 55%, #ecf5ff);
  box-shadow: 0 8px 22px rgb(46 108 160 / 12%);
}

.my-weather-hero :deep(.el-card__header) {
  padding: 16px 24px;
  border-bottom-color: #d9ecff;
  background: rgb(255 255 255 / 70%);
}

.my-weather-hero :deep(.el-card__body) {
  padding: 24px;
}

.hero-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.hero-top > div {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #606266;
  font-size: 0.85rem;
}

.hero-top a {
  text-decoration: none;
}

.hero-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-top: 14px;
}

.hero-identity {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.hero-icon {
  flex: 0 0 auto;
  border: 1px solid #b3d8ff;
  background: #d9ecff;
}

.hero-status {
  margin: 1px 0 0;
  color: #5c7891;
  font-size: 15px;
  font-weight: 700;
}

.hero-name-col {
  display: grid;
  gap: 4px;
}

.hero-name-col h2 {
  margin: 0;
  color: #243e59;
  font-size: 38px;
  line-height: 1.08;
}

.hero-temp {
  display: grid;
  flex: 0 0 auto;
  justify-items: end;
  gap: 5px;
  text-align: right;
}

.hero-temp strong {
  color: #1f354b;
  font-size: 48px;
  line-height: 1;
}

.hero-temp small {
  color: #71879a;
  font-weight: 700;
  white-space: nowrap;
}

.hero-metrics {
  margin-top: 20px;
}

.hero-secondary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
  margin-top: 12px;
}

.hero-forecast {
  display: grid;
  gap: 16px;
  margin-top: 20px;
}

@media (max-width: 560px) {
  .my-weather-hero :deep(.el-card__header),
  .my-weather-hero :deep(.el-card__body) {
    padding: 18px;
  }

  .hero-top > div span {
    display: none;
  }

  .hero-name-col h2 {
    font-size: 32px;
    white-space: nowrap;
  }

  .hero-main {
    align-items: flex-start;
    flex-direction: column;
  }

  .hero-temp {
    justify-items: start;
    text-align: left;
  }

  .hero-temp strong {
    font-size: 40px;
  }
}
</style>
