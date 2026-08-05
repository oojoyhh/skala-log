<script setup>
import { computed } from 'vue'
import { Moon, Sunny } from '@element-plus/icons-vue'
import { formatClockTime } from '@/domain/weather'

const props = defineProps({
  sunrise: {
    type: Number,
    required: true,
  },
  sunset: {
    type: Number,
    required: true,
  },
})

const now = Date.now() / 1000

const progress = computed(() => {
  const span = props.sunset - props.sunrise
  if (span <= 0) return 0
  return Math.min(1, Math.max(0, (now - props.sunrise) / span))
})

const isDaytime = computed(() => now >= props.sunrise && now <= props.sunset)

const sunPosition = computed(() => {
  // progress(0~1)를 반원 각도(π~0)로 바꿔서 호 위 위치를 구함
  const angle = Math.PI * (1 - progress.value)
  return {
    x: 100 + 80 * Math.cos(angle),
    y: 90 - 80 * Math.sin(angle),
  }
})
</script>

<template>
  <el-card class="sun-arc-card" shadow="never">
    <template #header>
      <header>
        <h3>일출 · 일몰</h3>
      </header>
    </template>

    <svg class="sun-arc" viewBox="0 0 200 100" preserveAspectRatio="xMidYMid meet">
      <path d="M20 90 A 80 80 0 0 1 180 90" fill="none" stroke="#e2edf5" stroke-width="3" />
      <line
        x1="10"
        y1="90"
        x2="190"
        y2="90"
        stroke="#edf1f4"
        stroke-width="1"
        stroke-dasharray="2 4"
      />
      <circle
        :cx="sunPosition.x"
        :cy="sunPosition.y"
        r="7"
        :fill="isDaytime ? '#f5a623' : '#c3ccd6'"
      />
    </svg>

    <div class="sun-labels">
      <div class="sun-label">
        <span><el-icon><Sunny /></el-icon> 일출</span>
        <strong>{{ formatClockTime(sunrise) }}</strong>
      </div>
      <div class="sun-label">
        <span><el-icon><Moon /></el-icon> 일몰</span>
        <strong>{{ formatClockTime(sunset) }}</strong>
      </div>
    </div>
  </el-card>
</template>

<style scoped>
.sun-arc-card {
  min-width: 0;
  height: 100%;
  border: 1px solid rgb(104 159 205 / 22%);
  border-radius: 14px;
  background: rgb(255 255 255 / 72%);
}

.sun-arc-card :deep(.el-card__header) {
  padding: 14px 18px;
}

.sun-arc-card :deep(.el-card__body) {
  padding: 0 18px 14px;
}

.sun-arc-card h3 {
  margin: 0;
  color: #294963;
  font-size: 17px;
}

.sun-arc {
  display: block;
  width: 100%;
  height: 96px;
}

.sun-labels {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: -2px;
}

.sun-label {
  display: grid;
  gap: 2px;
}

.sun-label:last-child {
  text-align: right;
}

.sun-label span {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #5c7891;
  font-size: 12px;
  font-weight: 700;
}

.sun-label strong {
  color: #233f59;
  font-size: 16px;
}
</style>
