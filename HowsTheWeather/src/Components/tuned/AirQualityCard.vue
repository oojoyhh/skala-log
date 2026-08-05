<script setup>
import { computed } from 'vue'
import { CircleCheckFilled, CircleCloseFilled, InfoFilled, WarningFilled } from '@element-plus/icons-vue'
import { getPm10Level, getPm25Level } from '@/domain/airQuality'

const props = defineProps({
  pm10: {
    type: Number,
    required: true,
  },
  pm25: {
    type: Number,
    required: true,
  },
})

const pm10Level = computed(() => getPm10Level(props.pm10))
const pm25Level = computed(() => getPm25Level(props.pm25))

const levelIcons = {
  success: CircleCheckFilled,
  primary: InfoFilled,
  warning: WarningFilled,
  danger: CircleCloseFilled,
}

const getIcon = (level) => levelIcons[level.type] ?? InfoFilled
</script>

<template>
  <el-card class="air-quality-card" shadow="never">
    <template #header>
      <header>
        <h3>대기질</h3>
      </header>
    </template>

    <div class="air-quality-grid">
      <div class="air-item">
        <span class="air-face" :class="`is-${pm10Level.type}`" aria-hidden="true">
          <el-icon><component :is="getIcon(pm10Level)" /></el-icon>
        </span>
        <div class="air-reading">
          <span class="air-label">미세먼지 <small>PM10</small></span>
          <strong>{{ pm10 }}<small>㎍/㎥</small></strong>
        </div>
        <el-tag :type="pm10Level.type" effect="light" round size="small">
          {{ pm10Level.label }}
        </el-tag>
      </div>

      <div class="air-item">
        <span class="air-face" :class="`is-${pm25Level.type}`" aria-hidden="true">
          <el-icon><component :is="getIcon(pm25Level)" /></el-icon>
        </span>
        <div class="air-reading">
          <span class="air-label">초미세먼지 <small>PM2.5</small></span>
          <strong>{{ pm25 }}<small>㎍/㎥</small></strong>
        </div>
        <el-tag :type="pm25Level.type" effect="light" round size="small">
          {{ pm25Level.label }}
        </el-tag>
      </div>
    </div>
  </el-card>
</template>

<style scoped>
.air-quality-card {
  min-width: 0;
  height: 100%;
  border: 1px solid rgb(104 159 205 / 22%);
  border-radius: 14px;
  background: rgb(255 255 255 / 72%);
}

.air-quality-card :deep(.el-card__header) {
  padding: 14px 18px;
}

.air-quality-card :deep(.el-card__body) {
  padding: 4px 14px 14px;
}

.air-quality-card h3 {
  margin: 0;
  color: #294963;
  font-size: 17px;
}

.air-quality-grid {
  display: grid;
  gap: 8px;
}

.air-item {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 12px;
  padding: 6px;
  border-radius: 12px;
}

.air-face {
  display: grid;
  flex: 0 0 auto;
  width: 56px;
  height: 56px;
  border-radius: 16px;
  font-size: 30px;
  place-items: center;
}

.air-face.is-success {
  color: #529b2e;
  background: #e1f3d8;
}

.air-face.is-primary {
  color: #337ecc;
  background: #d9ecff;
}

.air-face.is-warning {
  color: #b88230;
  background: #faecd8;
}

.air-face.is-danger {
  color: #c45656;
  background: #fde2e2;
}

.air-reading {
  min-width: 0;
}

.air-label {
  display: block;
  color: #5c7891;
  font-size: 13px;
  font-weight: 700;
}

.air-label small {
  color: #a8abb2;
  font-weight: 600;
}

.air-item strong {
  display: block;
  margin-top: 3px;
  color: #233f59;
  font-size: 23px;
}

.air-item strong small {
  margin-left: 3px;
  color: #909399;
  font-size: 11px;
  font-weight: 600;
}
</style>
