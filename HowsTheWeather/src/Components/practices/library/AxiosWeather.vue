<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const weatherData = ref(null)
const isLoading = ref(false)

const handleFetchWeather = async () => {
  const API_KEY = import.meta.env.VITE_OPENWEATHER_API_KEY

  if (!API_KEY) {
    ElMessage.warning('.env.local 파일에 OpenWeather API 키를 입력하세요.')
    return
  }

  isLoading.value = true

  const URL = `https://api.openweathermap.org/data/2.5/weather?lat=35.158582&lon=126.804975&appid=${API_KEY}&units=metric&lang=kr`

  try {
    const response = await axios.get(URL)

    console.log('Axios 통신 응답 전체 객체:', response)
    console.log('백엔드가 준 핵심 날씨 데이터(JSON):', response.data)
    weatherData.value = response.data
    ElMessage.success('실시간 날씨 데이터를 불러왔습니다.')
  } catch (error) {
    console.error('통신 중 에러가 발생했습니다:', error)
    ElMessage.error('데이터를 가져오지 못했습니다. API 키와 주소를 확인하세요.')
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <section class="library-practice" aria-labelledby="axios-weather-title">
    <div class="section-heading">
      <el-tag type="primary" effect="light">과제 7 · AXIOS GET</el-tag>
      <h2 id="axios-weather-title">실시간 날씨 통신 검증</h2>
      <p>외부 API 요청과 로딩·성공·실패 상태를 확인합니다.</p>
    </div>

    <el-card class="practice-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <strong>OpenWeather API</strong>
          <el-button type="primary" :loading="isLoading" @click="handleFetchWeather">
            {{ isLoading ? '데이터 로딩 중...' : '날씨 데이터 불러오기' }}
          </el-button>
        </div>
      </template>

      <div class="result-panel" aria-live="polite">
        <span>RESULT</span>
        <code v-if="weatherData">
          위치: {{ weatherData.name }} / 현재 기온: {{ weatherData.main.temp }}°C / 날씨 상태:
          {{ weatherData.weather[0].description }} / 습도: {{ weatherData.main.humidity }}%
        </code>
        <code v-else>버튼을 눌러 실시간 날씨 데이터를 불러오세요.</code>
      </div>
    </el-card>
  </section>
</template>

<style scoped>
.library-practice {
  padding: clamp(1.25rem, 3vw, 2.25rem);
  border: 1px solid #e7eaf0;
  border-radius: 20px;
  background:
    radial-gradient(circle at 0 0, rgb(64 158 255 / 10%), transparent 34%),
    #f8fafc;
}

.section-heading {
  margin-bottom: 1.5rem;
}

.section-heading h2 {
  margin: 0.55rem 0 0;
  color: #182230;
  font-size: clamp(1.55rem, 3vw, 2rem);
  font-weight: 800;
}

.section-heading p {
  margin: 0.4rem 0 0;
  color: #667085;
}

.practice-card {
  border-radius: 12px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.result-panel {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: start;
  gap: 12px;
  padding: 0.9rem 1rem;
  border: 1px solid #d9ecff;
  border-radius: 9px;
  color: #337ecc;
  background: #ecf5ff;
}

.result-panel span {
  color: #409eff;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.06em;
}

.result-panel code {
  min-width: 0;
  color: #606266;
  font-size: 0.82rem;
  overflow-wrap: anywhere;
}

@media (max-width: 560px) {
  .card-header {
    align-items: stretch;
    flex-direction: column;
  }

  .result-panel {
    grid-template-columns: 1fr;
  }
}
</style>
