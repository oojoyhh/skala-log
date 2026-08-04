<script setup>
// components/icons/IconSearch.vue
// -----------------------------------------------------------------------------
// 검색(조회) 버튼에 쓰는 돋보기 아이콘.
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
    stroke-width="2.2"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
  >
    <circle cx="11" cy="11" r="7" />
    <line x1="21" y1="21" x2="16.2" y2="16.2" />
  </svg>
</template>
