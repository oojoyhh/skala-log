# HowsTheWeather 과제 파일 안내

## 가장 최신 튜닝 화면

- `src/Components/tuned/TunedWeatherDashboard.vue`
- `src/Components/tuned/TunedWeatherCard.vue`

실습 5의 라우터와 Pinia 단위 설정을 사용하면서 내 위치(카드 핀 고정), 검색(URL 쿼리 반영), 정렬, 온도 라벨을 추가한 화면이다.

## 실습 1~5

### 실습 1: 기본 렌더링

- `src/Components/exercise/WeatherMockup.vue`

### 실습 2: Composition API

- `src/Components/exercise/WeatherComposition.vue`

### 실습 3: 컴포넌트 분리

- `src/Components/exercise/WeatherParent.vue`
- `src/Components/exercise/BaseDashboardCard.vue`
- `src/Components/exercise/SearchBar.vue`
- `src/Components/exercise/WeatherCard.vue`

### 실습 4: Vue Router

- `src/router/index.js`
- `src/views/WeatherHomeView.vue`
- `src/views/WeatherDetailView.vue`
- `src/views/WeatherAboutView.vue`
- `src/views/NotFoundView.vue`

### 실습 5: Pinia 단위 설정

- `src/stores/configStore.js`
- `src/Components/exercise/UnitToggler.vue`

## Pinia 및 Axios 라이브러리 실습

- `src/stores/counter.js`
- `src/Components/practices/library/StoreCounter.vue`
- `src/Components/practices/library/AxiosWeather.vue`
- `src/Components/practices/library/AxiosJson.vue`

OpenWeather API 키는 Git에 포함되지 않는 `.env.local` 파일에 입력한다.

```env
VITE_OPENWEATHER_API_KEY=여기에_새로_발급한_API_KEY_입력
```

`.env.example`은 변수 이름만 공유하는 예시 파일이며 실제 키는 입력하지 않는다.

## 앱 진입점

- `src/main.js`: Vue, Pinia, Router 등록
- `src/App.vue`: 최신 튜닝 화면과 실습 화면 배치

## 기타

- `src/assets/exercise.css`: 교수님 교안 과제 공통 스타일
- `src/stores/authStore.js`: 현재 별도로 작성 중인 인증 실습
