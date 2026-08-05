<script setup>
import { DataLine, Drizzling, Odometer, WindPower } from '@element-plus/icons-vue'

defineProps({
  metrics: {
    type: Array,
    required: true,
  },
})

const metricIcons = {
  체감: Odometer,
  습도: Drizzling,
  기압: DataLine,
  풍속: WindPower,
}
</script>

<template>
  <div class="weather-summary">
    <div v-for="metric in metrics" :key="metric.label" class="metric-item">
      <span class="metric-icon" aria-hidden="true">
        <el-icon><component :is="metricIcons[metric.label]" /></el-icon>
      </span>
      <span class="metric-label">{{ metric.label }}</span>
      <strong>{{ metric.value }}</strong>
    </div>
  </div>
</template>

<style scoped>
.weather-summary {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  overflow: hidden;
  border: 1px solid #d9ecff;
  border-radius: 14px;
  background: rgb(255 255 255 / 76%);
}

.metric-item {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 10px;
  min-width: 0;
  padding: 14px 13px;
  border-right: 1px solid #e4edf5;
}

.metric-item:last-child {
  border-right: 0;
}

.metric-icon {
  display: grid;
  flex: 0 0 34px;
  width: 34px;
  height: 34px;
  border-radius: 10px;
  color: #409eff;
  background: #ecf5ff;
  font-size: 18px;
  place-items: center;
}

.metric-label,
.metric-item strong {
  display: block;
}

.metric-label {
  color: #909399;
  font-size: 13px;
  font-weight: 700;
}

.metric-item strong {
  justify-self: end;
  color: #243e59;
  font-size: clamp(15px, 1.8vw, 18px);
  font-weight: 700;
  text-align: right;
  white-space: nowrap;
}

@media (max-width: 660px) {
  .weather-summary {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .metric-item:nth-child(2) {
    border-right: 0;
  }

  .metric-item:nth-child(-n + 2) {
    border-bottom: 1px solid #e4edf5;
  }
}
</style>
