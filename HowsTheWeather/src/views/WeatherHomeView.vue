<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import BaseDashboardCard from '@/Components/exercise/BaseDashboardCard.vue'
import SearchBar from '@/Components/exercise/SearchBar.vue'
import WeatherCard from '@/Components/exercise/WeatherCard.vue'

const router = useRouter()
const route = useRoute()

const weatherList = ref([
  { id: 'city_01', name: '서울', temp: 28, status: '맑음' },
  { id: 'city_02', name: '수원', temp: 24, status: '비' },
  { id: 'city_03', name: '부산', temp: 26, status: '구름' },
  { id: 'city_04', name: '속초', temp: 20, status: '비바람' },
])

const searchQuery = ref('')
const selectedCityInfo = ref('카드를 클릭하거나 검색해 보세요.')

onMounted(() => {
  if (route.query.search) {
    searchQuery.value = route.query.search
  }
})

// 검색어를 URL 쿼리에 반영해 새로고침/공유해도 유지되게 함
watch(searchQuery, (newQuery) => {
  router.push({
    path: route.path,
    query: {
      ...route.query,
      search: newQuery || undefined,
    },
  })
})

const filteredWeatherList = computed(() => {
  const query = searchQuery.value.trim()

  if (!query) return weatherList.value

  return weatherList.value.filter((item) => item.name.includes(query))
})

const handleDetailJump = (id) => {
  router.push(`/weather/${id}`)
}
</script>

<template>
  <div class="dashboard-wrapper">
    <BaseDashboardCard>
      <SearchBar :current-query="searchQuery" @update-query="(value) => (searchQuery = value)" />
    </BaseDashboardCard>

    <BaseDashboardCard>
      <h3>🏙️ 지역별 날씨 현황</h3>

      <WeatherCard
        v-for="item in filteredWeatherList"
        :key="item.id"
        :city-item="item"
        @select-card="(message) => (selectedCityInfo = message)"
        @click-detail="handleDetailJump(item.id)"
      />

      <p
        v-if="filteredWeatherList.length === 0"
        style="text-align: center; color: #e74c3c; padding: 10px 0"
      >
        😭 검색 결과와 일치하는 도시가 없습니다.
      </p>
    </BaseDashboardCard>

    <div class="status-bar">{{ selectedCityInfo }}</div>
  </div>
</template>

<style scoped>
.status-bar {
  background: #e8f5e9;
  padding: 10px;
  text-align: center;
  color: #2e7d32;
  font-weight: bold;
  border-radius: 6px;
}
</style>
