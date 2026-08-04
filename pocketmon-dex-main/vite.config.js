// vite.config.js
// -----------------------------------------------------------------------------
// Vite 빌드 도구 설정 파일입니다.
// @vitejs/plugin-vue 플러그인을 등록해서 .vue 파일(SFC, Single File Component)을
// 브라우저가 이해할 수 있는 JS로 변환할 수 있도록 해줍니다.
// -----------------------------------------------------------------------------
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173, // 로컬 개발 서버 포트
  },
})
