<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import MyLocationSelector from './MyLocationSelector.vue'
import TunedWeatherCard from './TunedWeatherCard.vue'

const router = useRouter()

const weatherList = ref([
  { id: 'city_01', name: '서울', temp: 28, status: '맑음' },
  { id: 'city_02', name: '수원', temp: 24, status: '비' },
  { id: 'city_03', name: '부산', temp: 26, status: '구름' },
  { id: 'city_04', name: '속초', temp: 20, status: '비바람' },
])

const searchQuery = ref('')
const selectedCityInfo = ref(null)
const myCityId = ref('city_02')

// 선택한 내 위치의 도시 객체를 찾는다.
const myCityInfo = computed(() => {
  return weatherList.value.find((city) => city.id === myCityId.value) ?? null
})

// 검색어가 포함된 도시만 반환한다.
const filteredWeatherList = computed(() => {
  const query = searchQuery.value.trim()

  if (!query) {
    return weatherList.value
  }

  return weatherList.value.filter((city) => city.name.includes(query))
})

// 내 위치를 검색 결과의 맨 위로 정렬한다.
const displayedWeatherList = computed(() => {
  return [...filteredWeatherList.value].sort((cityA, cityB) => {
    const cityAIsMyCity = cityA.id === myCityId.value
    const cityBIsMyCity = cityB.id === myCityId.value

    return Number(cityBIsMyCity) - Number(cityAIsMyCity)
  })
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

// 저장된 내 위치가 있다면 화면이 열릴 때 불러온다.
onMounted(() => {
  const savedCityId = localStorage.getItem('tunedMyCityId')
  const isValidCity = weatherList.value.some((city) => city.id === savedCityId)

  if (isValidCity) {
    myCityId.value = savedCityId
  }
})

// 내 위치가 바뀔 때마다 다음 방문을 위해 저장한다.
watch(myCityId, (cityId) => {
  localStorage.setItem('tunedMyCityId', cityId)
})
</script>

<template>
  <div class="tuned-dashboard">
    <section class="tuned-panel">
      <h2>📍 내 지역 설정</h2>

      <MyLocationSelector
        :cities="weatherList"
        :selected-city-id="myCityId"
        @update-my-city="updateMyCity"
      />

      <div v-if="myCityInfo" class="tuned-my-location-preview">
        <TunedWeatherCard
          :city="myCityInfo"
          is-my-city
          @select-card="selectCity"
          @click-detail="goToWeatherDetail"
        />
      </div>
    </section>

    <section class="tuned-panel">
      <h2>🔍 도시 검색</h2>

      <input
        v-model="searchQuery"
        class="tuned-search-input"
        type="text"
        placeholder="검색할 도시 이름 입력"
      />

      <p class="tuned-search-message">
        검색 중인 도시: <strong>{{ searchQuery }}</strong>
      </p>
    </section>

    <section class="tuned-panel">
      <h2>🏙️ 지역별 날씨 현황</h2>

      <TransitionGroup
        v-if="displayedWeatherList.length > 0"
        name="tuned-weather-list"
        tag="div"
        class="tuned-weather-list"
      >
        <TunedWeatherCard
          v-for="city in displayedWeatherList"
          :key="city.id"
          :city="city"
          :is-my-city="city.id === myCityId"
          @select-card="selectCity"
          @click-detail="goToWeatherDetail"
        />
      </TransitionGroup>

      <p v-else class="tuned-no-results">검색 결과와 일치하는 도시가 없습니다.</p>
    </section>

    <div class="tuned-status-bar" role="status">{{ selectedCityMessage }}</div>
  </div>
</template>

<style scoped>
.tuned-dashboard {
  display: grid;
  gap: 20px;
  width: min(100%, 760px);
  margin: 0 auto;
}

.tuned-panel {
  padding: 24px;
  border: 1px solid #dfe5eb;
  border-radius: 12px;
  background: #f8fafc;
  box-shadow: 0 2px 8px rgb(27 43 65 / 4%);
}

.tuned-panel h2 {
  margin: 0 0 16px;
  color: #334d69;
  font-size: 21px;
}

.tuned-my-location-preview {
  margin-top: 18px;
}

.tuned-search-input {
  width: 100%;
  height: 44px;
  padding: 0 12px;
  border: 1px solid #9ba7b3;
  border-radius: 4px;
  color: #24364b;
  background: #fff;
  font: inherit;
  outline: none;
}

.tuned-search-input:focus {
  border-color: #438fd1;
  box-shadow: 0 0 0 3px rgb(67 143 209 / 18%);
}

.tuned-search-message {
  margin: 8px 0 0;
}

.tuned-weather-list {
  display: grid;
  gap: 14px;
}

.tuned-weather-list-move,
.tuned-weather-list-enter-active,
.tuned-weather-list-leave-active {
  transition:
    opacity 0.35s ease,
    transform 0.35s ease;
}

.tuned-weather-list-enter-from,
.tuned-weather-list-leave-to {
  opacity: 0;
  transform: translateY(14px) scale(0.98);
}

.tuned-no-results {
  padding: 36px 16px;
  margin: 0;
  color: #c0392b;
  text-align: center;
}

.tuned-status-bar {
  padding: 16px 20px;
  border: 1px solid #d8ebd8;
  border-radius: 9px;
  color: #299548;
  background: #ebf7eb;
  text-align: center;
  font-weight: 700;
}

@media (max-width: 560px) {
  .tuned-panel {
    padding: 16px;
  }
}
</style>
