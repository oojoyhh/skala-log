import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig(() => ({
  // GitHub Pages는 https://<user>.github.io/skala-log/ 처럼 하위 경로로 서빙되지만,
  // Vercel은 루트 경로(/)로 서빙되므로 GITHUB_PAGES 환경변수가 있을 때만 base를 바꾼다.
  base: process.env.GITHUB_PAGES ? '/skala-log/' : '/',
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/kma-api': {
        target: 'https://apihub.kma.go.kr',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/kma-api/, ''),
      },
    },
  },
}))
