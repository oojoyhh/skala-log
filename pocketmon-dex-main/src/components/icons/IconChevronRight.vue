<script setup>
// components/icons/IconChevronRight.vue
// -----------------------------------------------------------------------------
// "다음" 방향을 나타내는 화살표 아이콘 (IconChevronLeft.vue와 좌우 대칭).
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
    stroke-width="2.4"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
  >
    <polyline points="9 5 16 12 9 19" />
  </svg>
</template>
