<script setup>
// components/icons/IconChevronLeft.vue
// -----------------------------------------------------------------------------
// "이전" / "뒤로 가기" 방향을 나타내는 화살표 아이콘.
// 유니코드 문자(←) 대신 SVG로 그려서 두께/각도를 디자인 톤에 맞게 통일함.
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
    <polyline points="15 5 8 12 15 19" />
  </svg>
</template>
