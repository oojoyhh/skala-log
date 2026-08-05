<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Grid, Refresh, Search } from '@element-plus/icons-vue'

import { cities } from '@/api/weatherApi'
import { fetchWeatherList } from '@/services/weatherService'
import KoreaMap from '@/Components/tuned/KoreaMap.vue'
import TunedWeatherCard from '@/Components/tuned/TunedWeatherCard.vue'

const route = useRoute()
const router = useRouter()

const weatherList = ref([])
const searchQuery = ref('')
const selectedCityInfo = ref(null)
const myCityId = ref(cities[0].id)
const isLoading = ref(false)
const errorMessage = ref('')
const updatedAt = ref('')
const selectedRegionName = ref('')

const loadWeather = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    weatherList.value = await fetchWeatherList()
    updatedAt.value = new Date().toLocaleTimeString('ko-KR', {
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch (error) {
    errorMessage.value = error.message || '날씨 데이터를 불러오지 못했습니다.'
  } finally {
    isLoading.value = false
  }
}

// 검색어가 포함된 도시만 반환한다.
const filteredWeatherList = computed(() => {
  const query = searchQuery.value.trim()

  if (!query) {
    return weatherList.value
  }

  return weatherList.value.filter((city) => city.name.includes(query))
})

const displayedWeatherList = computed(() => {
  return filteredWeatherList.value
})

// 마지막 글자의 받침 여부에 따라 '이' 또는 '가'를 붙인다.
const selectedCityMessage = computed(() => {
  if (!selectedCityInfo.value) {
    return '카드를 클릭하거나 검색해 보세요.'
  }

  const cityName = selectedCityInfo.value.name
  const lastCharacterCode = cityName.charCodeAt(cityName.length - 1)
  const isHangul = lastCharacterCode >= 0xac00 && lastCharacterCode <= 0xd7a3
  const hasFinalConsonant = isHangul && (lastCharacterCode - 0xac00) % 28 !== 0
  const particle = hasFinalConsonant ? '이' : '가'

  return `${cityName}${particle} 선택되었습니다.`
})

const updateMyCity = (cityId) => {
  myCityId.value = cityId
}

const selectCity = (city) => {
  selectedCityInfo.value = city
}

// 실습 4·5에서 만든 동적 경로를 그대로 활용한다.
const goToWeatherDetail = (city) => {
  router.push(`/weather/${city.id}`)
}

const showAllCities = () => {
  searchQuery.value = ''
  selectedRegionName.value = ''
  selectedCityInfo.value = null
}

const selectRegion = ({ regionName, city }) => {
  selectedRegionName.value = regionName

  if (city) {
    searchQuery.value = city.name
    selectedCityInfo.value = city
  }
}

// 저장된 내 위치와 공유 가능한 검색어(URL 쿼리)를 화면이 열릴 때 불러온다.
onMounted(() => {
  const savedCityId = localStorage.getItem('tunedMyCityId')
  const isValidCity = cities.some((city) => city.id === savedCityId)

  if (isValidCity) {
    myCityId.value = savedCityId
  }

  if (route.query.search) {
    searchQuery.value = route.query.search
  }

  loadWeather()
})

// 내 위치가 바뀔 때마다 다음 방문을 위해 저장한다.
watch(myCityId, (cityId) => {
  localStorage.setItem('tunedMyCityId', cityId)
})

// 검색어를 URL 쿼리에 반영해 검색 상태를 공유/새로고침해도 유지되게 한다.
watch(searchQuery, (newQuery) => {
  router.push({
    path: route.path,
    query: { search: newQuery || undefined },
  })
})
</script>

<template>
  <div class="city-search">
    <header class="search-heading">
      <el-tag type="primary" effect="light" round>REGIONAL SEARCH</el-tag>
      <h1>지역별 날씨 검색</h1>
      <p>전국 주요 도시의 실시간 날씨를 검색하고, 원하는 지역을 내 지역으로 고정하세요.</p>
    </header>

    <KoreaMap
      v-if="weatherList.length"
      :cities="weatherList"
      :my-city-id="myCityId"
      @select-region="selectRegion"
      @view-detail="goToWeatherDetail"
    />
    <el-skeleton v-else-if="isLoading" animated>
      <template #template>
        <el-skeleton-item variant="rect" class="loading-map" />
      </template>
    </el-skeleton>

    <el-card class="search-panel" shadow="hover">
      <template #header>
        <div class="search-panel-header">
          <div>
            <small class="search-panel-kicker">MAJOR CITY WEATHER</small>
            <span>주요 지역별 날씨</span>
            <small v-if="updatedAt" class="updated-at">마지막 업데이트 {{ updatedAt }}</small>
          </div>
          <div class="search-panel-actions">
            <el-button :disabled="!searchQuery" @click="showAllCities">
              <el-icon><Grid /></el-icon> 전체 지역 보기
            </el-button>
            <el-button type="primary" plain :loading="isLoading" @click="loadWeather">
              <el-icon><Refresh /></el-icon> 새로고침
            </el-button>
          </div>
        </div>
      </template>

      <el-input
        v-model="searchQuery"
        class="search-input"
        size="large"
        clearable
        placeholder="도시 이름을 입력하세요 (예: 서울, 부산)"
      >
        <template #prefix><el-icon><Search /></el-icon></template>
      </el-input>

      <div class="pin-hint">
        <el-tag type="info" effect="plain" round>TIP</el-tag>
        <span>카드의 핀 아이콘을 누르면 내 지역으로 고정됩니다.</span>
      </div>

      <el-alert
        v-if="errorMessage"
        class="api-message"
        :title="errorMessage"
        type="error"
        show-icon
        :closable="false"
      />
      <el-skeleton v-if="isLoading && !weatherList.length" class="search-loading" animated>
        <template #template>
          <div class="loading-cards">
            <el-skeleton-item v-for="n in 6" :key="n" variant="rect" class="loading-card" />
          </div>
        </template>
      </el-skeleton>

      <TransitionGroup
        v-else-if="displayedWeatherList.length"
        name="weather-list"
        tag="div"
        class="weather-list"
      >
        <TunedWeatherCard
          v-for="city in displayedWeatherList"
          :key="city.id"
          :city="city"
          :is-my-city="city.id === myCityId"
          compact
          @select-card="selectCity"
          @click-detail="goToWeatherDetail"
          @set-my-city="updateMyCity"
        />
      </TransitionGroup>

      <el-empty v-else-if="!errorMessage" description="검색 결과와 일치하는 도시가 없습니다." />
    </el-card>

    <el-alert
      class="status-bar"
      :title="selectedRegionName ? `${selectedRegionName} · ${selectedCityMessage}` : selectedCityMessage"
      type="info"
      show-icon
      :closable="false"
    />
  </div>
</template>

<style scoped>
.city-search {
  display: grid;
  gap: 22px;
  width: min(100%, 820px);
  margin: 0 auto;
}

.search-heading {
  padding: 8px 4px 0;
}

.search-heading h1 {
  margin: 16px 0 6px;
  color: #303133;
  font-size: clamp(1.75rem, 5vw, 2.45rem);
  letter-spacing: -0.04em;
}

.search-heading p {
  margin: 0;
  color: #909399;
}

.search-panel {
  overflow: hidden;
  border-color: #d9ecff;
  border-radius: 16px;
  background: #fff;
}

.search-panel :deep(.el-card__header) {
  padding: 20px 24px;
  background: linear-gradient(135deg, #fff, #f5f9ff);
}

.search-panel :deep(.el-card__body) {
  padding: 24px;
}

.search-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.search-panel-header .updated-at {
  display: block;
  margin-top: 3px;
  color: #7a8795;
}

.search-panel-kicker {
  display: block;
  margin-bottom: 4px;
  color: #409eff;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.1em;
}

.search-panel-header span {
  color: #303133;
  font-weight: 800;
}

.search-panel-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 10px;
}

.pin-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 10px 2px 0;
  color: #606266;
  font-size: 0.82rem;
}

.api-message {
  margin-top: 16px;
}

.search-loading {
  margin-top: 24px;
}

.loading-map {
  display: block;
  height: 420px;
  border-radius: 20px;
}

.loading-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(228px, 1fr));
  gap: 10px;
}

.loading-card {
  height: 158px;
  border-radius: 16px;
}

.weather-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(228px, 1fr));
  gap: 10px;
  margin-top: 16px;
}

.weather-list-move,
.weather-list-enter-active,
.weather-list-leave-active {
  transition:
    opacity 0.35s ease,
    transform 0.35s ease;
}

.weather-list-enter-from,
.weather-list-leave-to {
  opacity: 0;
  transform: translateY(14px) scale(0.98);
}

.status-bar {
  border-radius: 10px;
}

@media (max-width: 560px) {
  .search-panel :deep(.el-card__header),
  .search-panel :deep(.el-card__body) {
    padding: 16px;
  }

  .search-panel-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .search-panel-actions {
    width: 100%;
  }

  .search-panel-actions :deep(.el-button) {
    flex: 1;
    margin: 0;
  }

  .weather-list {
    grid-template-columns: 1fr;
  }
}
</style>
