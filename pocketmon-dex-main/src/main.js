// main.js
// -----------------------------------------------------------------------------
// 앱의 진입점(Entry point). 이 파일이 가장 먼저 실행됩니다.
// 여기서 하는 일:
//  1) Vue 앱 인스턴스 생성
//  2) 상태관리 라이브러리 Pinia 연결 (로그인 상태 등을 저장)
//  3) 라우터(Vue Router) 연결 (로그인 페이지 <-> 도감 페이지 이동)
//  4) 전역 스타일 불러오기
//  5) #app 엘리먼트에 마운트(부착)
// -----------------------------------------------------------------------------
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)

app.use(createPinia()) // 전역 상태 저장소 활성화
app.use(router)        // 페이지 전환(라우팅) 활성화

app.mount('#app')
