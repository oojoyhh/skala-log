<script setup>
// components/icons/IconWarning.vue
// -----------------------------------------------------------------------------
// 경고/에러 메시지 앞에 붙는 아이콘. 기본 이모지(⚠) 대신 선(stroke) 기반의
// SVG로 그려서, 폰트나 OS에 따라 모양이 달라지지 않고 항상 동일하게 보이도록 함.
// currentColor를 사용해서 부모 요소의 text color(예: --accent-red)를 그대로 물려받음.
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
    <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z" />
    <line x1="12" y1="9" x2="12" y2="13" />
    <line x1="12" y1="17" x2="12.01" y2="17" />
  </svg>
</template>
