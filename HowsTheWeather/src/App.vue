<script setup>
import { ref } from 'vue'

const weatherList = ref([
  { id: 'city_01', name: '서울', temp: 28, status: '맑음' },
  { id: 'city_02', name: '수원', temp: 24, status: '비' },
  { id: 'city_03', name: '부산', temp: 26, status: '구름' },
])

const searchCity = ref('')
const selectMessage = ref('도시를 선택해 주세요.')
const handleInput = (event) => {
  searchCity.value = event.target.value
}
const selectCity = (cityName) => {
  selectMessage.value = `${cityName}이 선택되었습니다.`
}
const showDetail = (cityName, status) => {
    window.alert(`${cityName}의 현재 날씨는 [${status}] 상태입니다.`)
}
</script>

<template>
  <div class="status-bar">
  {{ selectedMessage }}
  </div>

  <input type="text"
  placeholder="도시 이름을 입력하세요"
  :value="searchCity"
  @input="handleInput"/>

  <p>입력한 도시명: {{ searchCity }}</p>

  <div v-for="city in weatherList"
  :key="city.id"
  class="weather-card"
  @click="selectCity(city.name)">

  <h2>{{ city.name }}</h2>
  <p>기온: {{ city.temp }}도</p>
  <p>날씨: {{ city.status }}</p>

  <p v-if="city.temp >=25">더움(25도 이상)</p>
  <p v-else>선선함(25도 미만)</p>

  <button @click.stop="showDetail(city.name, city.status)">상세보기</button>
  </div>
</template>

<style scoped></style>
