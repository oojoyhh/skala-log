<script setup>
import AppNavigation from '@/components/AppNavigation.vue'
import RotatingBanner from '@/components/RotatingBanner.vue'

// 공통 배너 문구
const bannerMessages = [
    '좋아하는 마음을 차곡차곡 모으는 중 ♡',
    '오늘의 최애 순간도 아카이브 완료',
    'Keep your favorite moments close'
]
</script>

<template>
    <div class="app-shell">
        <AppNavigation />
        <RotatingBanner :messages="bannerMessages" />
        <RouterView />
    </div>
</template>

<style>
/* 전역 스타일 */
* {
    box-sizing: border-box;
}

:root {
    color: #3f3747;
    background: #fffaf7;
    font-family: "Pretendard", "Noto Sans KR", sans-serif;
}

body {
    min-height: 100vh;
    max-width: 1120px;
    margin: 0 auto;
    padding: 24px;
    background:
        radial-gradient(circle at top left, #ffe7ef 0, transparent 35%),
        radial-gradient(circle at top right, #eee8ff 0, transparent 32%),
        #fffaf7;
}

body::before {
    position: fixed;
    inset: 0;
    z-index: -1;
    background:
        radial-gradient(circle at 10% 0, rgba(255, 218, 232, 0.75), transparent 34%),
        radial-gradient(circle at 92% 8%, rgba(225, 217, 255, 0.78), transparent 32%),
        #fffaf7;
    content: '';
}

.app-shell {
    width: 100%;
}

button {
    cursor: pointer;
    font: inherit;
}

@media (max-width: 640px) {
    body {
        padding: 12px;
    }
}
</style>
