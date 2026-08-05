<script setup>
import { Loading } from '@element-plus/icons-vue'

defineProps({
  title: {
    type: String,
    default: '날씨 정보를 불러오는 중이에요',
  },
  description: {
    type: String,
    default: '잠시만 기다려 주세요.',
  },
})
</script>

<template>
  <div class="weather-loading-state" role="status" aria-live="polite">
    <span class="loading-icon" aria-hidden="true">
      <el-icon class="is-loading"><Loading /></el-icon>
    </span>
    <div>
      <strong>{{ title }}</strong>
      <small>{{ description }}</small>
    </div>
  </div>
</template>

<style scoped>
.weather-loading-state {
  display: flex;
  align-items: center;
  gap: 14px;
  min-height: 74px;
  padding: 16px 18px;
  border: 1px solid #d9ecff;
  border-radius: 14px;
  color: #315774;
  background: linear-gradient(135deg, #f5f9ff, #fff);
}

.loading-icon {
  display: grid;
  flex: 0 0 auto;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  color: #409eff;
  background: #d9ecff;
  font-size: 22px;
  place-items: center;
}

.weather-loading-state div {
  display: grid;
  gap: 3px;
}

.weather-loading-state strong {
  font-size: 15px;
  font-weight: 800;
}

.weather-loading-state small {
  color: #71879a;
  font-weight: 600;
}
</style>
