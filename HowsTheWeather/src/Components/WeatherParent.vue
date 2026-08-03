<script setup>
// 반응형 상태, 계산값, 상태 감시에 사용할 Vue 함수
import { computed, onMounted, ref, watch, watchEffect } from 'vue'

// 화면을 구성하는 자식 컴포넌트
import BaseDashboardCard from './BaseDashboardCard.vue'
import MyLocationSelector from './MyLocationSelector.vue'
import SearchBar from './SearchBar.vue'
import WeatherCard from './WeatherCard.vue'

// 원본 날씨 데이터
const weatherList = ref([
  { id: 'city_01', name: '서울', temp: 28, status: '맑음' },
  { id: 'city_02', name: '수원', temp: 24, status: '비' },
  { id: 'city_03', name: '부산', temp: 26, status: '구름' },
  { id: 'city_04', name: '속초', temp: 20, status: '비바람' },
])

// 검색어, 선택된 도시, 내 지역 상태
const searchQuery = ref('')
const selectedCityInfo = ref(null)
const myCityId = ref('city_02')

// 검색어가 포함된 도시만 반환한다.
const filteredWeatherList = computed(() => {
  const query = searchQuery.value.trim()

  if (query === '') {
    return weatherList.value
  }

  return weatherList.value.filter((city) => city.name.includes(query))
})

// 검색 결과 안에서 내 지역을 맨 앞으로 정렬한다.
const displayedWeatherList = computed(() => {
  return [...filteredWeatherList.value].sort((cityA, cityB) => {
    return Number(cityB.id === myCityId.value) - Number(cityA.id === myCityId.value)
  })
})

// 내 지역 id에 해당하는 도시 객체를 찾는다.
const myCityInfo = computed(() => {
  return weatherList.value.find((city) => city.id === myCityId.value) ?? null
})

// 마지막 글자의 받침 여부에 따라 도시 이름 뒤에 '이' 또는 '가'를 붙인다.
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

// SearchBar가 전달한 검색어를 저장한다.
const updateQuery = (query) => {
  searchQuery.value = query
}

// MyLocationSelector가 전달한 도시를 내 지역으로 저장한다.
const updateMyCity = (cityId) => {
  myCityId.value = cityId
}

// WeatherCard가 전달한 도시를 선택 상태로 저장한다.
const selectCity = (city) => {
  selectedCityInfo.value = city
}

// 상세보기 이벤트를 받아 날씨를 알림으로 표시한다.
const showDetail = ({ city, message }) => {
  window.alert(`${city.name}의 현재 날씨는 [${city.status}] 상태입니다.\n${message}`)
}

// 선택 도시가 바뀔 때마다 이전 값과 새 값을 기록한다.
watch(selectedCityInfo, (newCity, oldCity) => {
  console.log(
    `[선택 도시 변경] ${oldCity?.name ?? '없음'} → ${newCity?.name ?? '없음'}`,
  )
})

// 검색어를 사용하는 효과이므로 검색어 변경 때마다 다시 실행된다.
watchEffect(() => {
  console.log(`[검색어 변경] ${searchQuery.value}`)
})

// 저장된 내 지역이 있으면 처음 화면이 열릴 때 불러온다.
onMounted(() => {
  const savedCityId = localStorage.getItem('myCityId')
  const isValidCity = weatherList.value.some((city) => city.id === savedCityId)

  if (isValidCity) {
    myCityId.value = savedCityId
  }
})

// 내 지역이 바뀔 때마다 다음 방문을 위해 저장한다.
watch(myCityId, (cityId) => {
  localStorage.setItem('myCityId', cityId)
})
</script>

<template>
  <main class="weather-app">
    <!-- 페이지 제목 -->
    <header class="page-header">
      <span class="header-icon" aria-hidden="true">🌤️</span>
      <h1>날씨 <span>(컴포지션)</span></h1>
    </header>

    <!-- 내 지역 선택값은 부모가 관리하고 자식은 이벤트로 전달한다. -->
    <BaseDashboardCard title="📍 내 지역 설정">
      <MyLocationSelector
        :cities="weatherList"
        :selected-city-id="myCityId"
        @update-my-city="updateMyCity"
      />

      <!-- 선택한 내 지역 카드를 상단에도 별도로 보여준다. -->
      <div v-if="myCityInfo" class="my-location-preview">
        <WeatherCard
          :city="myCityInfo"
          is-my-city
          @select-card="selectCity"
          @click-detail="showDetail"
        />
      </div>
    </BaseDashboardCard>

    <!-- slot 안의 SearchBar는 부모 상태와 직접 통신한다. -->
    <BaseDashboardCard title="🔍 도시 검색">
      <SearchBar :query="searchQuery" @update-query="updateQuery" />
    </BaseDashboardCard>

    <!-- 검색 결과를 WeatherCard 목록으로 주입한다. -->
    <BaseDashboardCard title="🏙️ 지역별 날씨 현황">
      <TransitionGroup
        v-if="displayedWeatherList.length > 0"
        name="weather-list"
        tag="div"
        class="weather-list"
      >
        <WeatherCard
          v-for="city in displayedWeatherList"
          :key="city.id"
          :city="city"
          :is-my-city="city.id === myCityId"
          @select-card="selectCity"
          @click-detail="showDetail"
        />
      </TransitionGroup>

      <p v-else class="no-results">검색 결과와 일치하는 도시가 없습니다.</p>
    </BaseDashboardCard>

    <!-- 선택한 도시 정보를 보여주는 상태바 -->
    <div class="status-bar" role="status">
      {{ selectedCityMessage }}
    </div>
  </main>
</template>

<style scoped>
/* 모든 요소의 크기 계산 방식을 통일한다. */
:global(*) {
  box-sizing: border-box;
}

/* 페이지 전체 기본 스타일 */
:global(body) {
  min-width: 320px;
  min-height: 100vh;
  margin: 0;
  color: #24364b;
  background: #f3f6fa;
  font-family:
    Pretendard, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* 폼 요소가 본문 글꼴을 사용하게 한다. */
:global(button),
:global(input) {
  font: inherit;
}

/* 화면 전체 너비와 중앙 정렬 */
.weather-app {
  width: min(100% - 32px, 760px);
  margin: 48px auto;
}

/* 제목 영역 */
.page-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 0 4px 22px;
  margin-bottom: 30px;
  border-bottom: 1px solid #dce3ea;
}

.header-icon {
  font-size: 30px;
}

.page-header h1 {
  margin: 0;
  color: #182c43;
  font-size: clamp(25px, 4vw, 34px);
  line-height: 1.25;
}

.page-header h1 span {
  font-weight: 600;
}

/* 날씨 카드 목록 간격 */
.weather-list {
  display: grid;
  gap: 14px;
}

/* 검색과 내 지역 변경 시 카드를 부드럽게 이동시킨다. */
.weather-list-move,
.weather-list-enter-active,
.weather-list-leave-active {
  transition: opacity 0.35s ease, transform 0.35s ease;
}

.weather-list-enter-from,
.weather-list-leave-to {
  opacity: 0;
  transform: translateY(14px) scale(0.98);
}

/* 내 지역 선택창과 미리보기 카드 사이의 간격 */
.my-location-preview {
  margin-top: 18px;
}

/* 검색 결과가 없을 때 표시하는 안내문 */
.no-results {
  padding: 40px 20px;
  margin: 0;
  border: 1px dashed #c5ced8;
  border-radius: 8px;
  color: #718096;
  background: #fff;
  text-align: center;
}

/* 선택 도시 상태바 */
.status-bar {
  padding: 16px 20px;
  margin-top: 20px;
  border: 1px solid #d8ebd8;
  border-radius: 9px;
  color: #299548;
  background: #ebf7eb;
  text-align: center;
  font-size: 17px;
  font-weight: 700;
}

/* 작은 화면에서 여백을 줄인다. */
@media (max-width: 560px) {
  .weather-app {
    width: min(100% - 20px, 760px);
    margin: 24px auto;
  }
}
</style>
