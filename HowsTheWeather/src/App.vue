<script setup>
// 실제 화면과 상태를 관리하는 최상위 컴포넌트
import WeatherParent from './Components/WeatherParent.vue'
</script>

<template>
  <!-- 앱 진입점에서는 부모 컴포넌트만 렌더링한다. -->
  <WeatherParent />
</template>
