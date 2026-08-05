<script setup>
defineProps({
  day: {
    type: String,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <header class="practice-day-header">
    <el-tag type="primary" effect="light">{{ day }} · {{ name }}</el-tag>
    <h2>{{ title }}</h2>
    <p>{{ description }}</p>
  </header>
</template>

<style scoped>
.practice-day-header {
  margin-bottom: 1.25rem;
}

.practice-day-header h2 {
  margin: 0.55rem 0 0;
  color: #303133;
  font-size: clamp(1.45rem, 3vw, 1.85rem);
  font-weight: 750;
}

.practice-day-header p {
  margin: 0.35rem 0 0;
  color: #909399;
}
</style>
