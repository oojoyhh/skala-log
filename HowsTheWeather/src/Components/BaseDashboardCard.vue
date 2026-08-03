<script setup>
// 부모가 전달한 패널 제목
defineProps({
  title: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <section class="dashboard-card">
    <h2>{{ title }}</h2>
    <!-- 부모가 넣은 검색창 또는 날씨 목록이 표시된다. -->
    <slot />
  </section>
</template>

<style scoped>
/* 검색 영역과 목록 영역이 공유하는 패널 디자인 */
.dashboard-card {
  padding: 24px;
  border: 1px solid #dfe5eb;
  border-radius: 12px;
  background: #f8fafc;
  box-shadow: 0 2px 8px rgb(27 43 65 / 4%);
}

/* 연속된 패널 사이의 간격 */
.dashboard-card + .dashboard-card {
  margin-top: 22px;
}

.dashboard-card h2 {
  margin: 0 0 8px;
  color: #334d69;
  font-size: 21px;
  font-weight: 600;
}

/* 작은 화면에서는 내부 여백을 줄인다. */
@media (max-width: 560px) {
  .dashboard-card {
    padding: 16px;
  }
}
</style>
