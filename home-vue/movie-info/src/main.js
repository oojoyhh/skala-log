import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Vue 앱 생성
const app = createApp(App)

// 플러그인 등록
app.use(createPinia())
app.use(router)

// 앱 연결
app.mount('#app')
