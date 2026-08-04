<script setup>
// components/icons/IconSpeaker.vue
// -----------------------------------------------------------------------------
// "울음소리 재생" 버튼에 쓰는 스피커 아이콘. 기본 이모지(🔊) 대신 SVG로 그려서
// 어떤 기기/폰트에서도 동일한 모양으로 보이게 함.
// -----------------------------------------------------------------------------
defineProps({
  size: { type: [Number, String], default: 16 },
})
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
  >
    <polygon points="4 8 8 8 12 4 12 20 8 16 4 16 4 8" />
    <path d="M16.5 8.5a5 5 0 0 1 0 7" />
    <path d="M19.5 5.5a9 9 0 0 1 0 13" />
  </svg>
</template>
