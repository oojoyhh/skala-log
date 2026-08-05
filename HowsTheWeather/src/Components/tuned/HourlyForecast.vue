<script setup>
import { computed } from 'vue'
import { useConfigStore } from '@/stores/configStore'
import { convertTemperature } from '@/domain/weather'

const props = defineProps({
  hourly: {
    type: Array,
    required: true,
  },
})

const configStore = useConfigStore()
const displayTemp = (temp) => convertTemperature(temp, configStore.unit)

const GRAPH_HEIGHT = 72
const GRAPH_PAD = 16

// 시간대별 기온을 그래프 좌표(0~100%, px)로 변환함
const graphCoords = computed(() => {
  const temps = props.hourly.map((item) => displayTemp(item.temp))
  if (!temps.length) return []

  const min = Math.min(...temps)
  const max = Math.max(...temps)
  const range = max - min || 1

  return temps.map((temp, index) => ({
    leftPct: ((index + 0.5) / temps.length) * 100,
    top: GRAPH_PAD + (1 - (temp - min) / range) * (GRAPH_HEIGHT - GRAPH_PAD * 2),
    temp,
  }))
})

// leftPct(0~100)는 viewBox 너비가 1000이라 10 곱해서 좌표로 변환함
const linePoints = computed(() =>
  graphCoords.value.map((point) => `${point.leftPct * 10},${point.top}`).join(' '),
)

const areaPoints = computed(() => {
  if (!graphCoords.value.length) return ''
  return `0,${GRAPH_HEIGHT} ${linePoints.value} 1000,${GRAPH_HEIGHT}`
})
</script>

<template>
  <el-card class="hourly-forecast" shadow="never">
    <template #header>
      <header>
        <h3>24시간 예보</h3>
        <el-tag type="info" effect="plain" size="small" round>3시간 간격</el-tag>
      </header>
    </template>

    <div class="hourly-scroll">
      <div class="hourly-track">
        <div class="hourly-graph-wrap">
          <svg
            class="hourly-graph-svg"
            viewBox="0 0 1000 72"
            preserveAspectRatio="none"
            aria-hidden="true"
          >
            <defs>
              <linearGradient id="hourlyAreaGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#409eff" stop-opacity="0.32" />
                <stop offset="100%" stop-color="#409eff" stop-opacity="0" />
              </linearGradient>
            </defs>
            <polyline class="hourly-graph-area" :points="areaPoints" fill="url(#hourlyAreaGradient)" />
            <polyline class="hourly-graph-line" :points="linePoints" />
          </svg>

          <div
            v-for="(point, index) in graphCoords"
            :key="index"
            class="hourly-graph-point"
            :style="{ left: `${point.leftPct}%`, top: `${point.top}px` }"
          >
            <span class="hourly-graph-value">{{ point.temp }}°</span>
            <span class="hourly-graph-dot" aria-hidden="true"></span>
          </div>
        </div>

        <div
          class="hourly-list"
          :style="{ gridTemplateColumns: `repeat(${hourly.length}, minmax(76px, 1fr))` }"
        >
          <div v-for="item in hourly" :key="item.timestamp" class="hourly-slot">
            <img :src="`https://openweathermap.org/img/wn/${item.icon}@2x.png`" :alt="item.status" />
            <small>강수 {{ item.rainChance }}%</small>
            <time>{{ item.time }}</time>
          </div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<style scoped>
.hourly-forecast {
  min-width: 0;
  border: 1px solid rgb(104 159 205 / 22%);
  border-radius: 14px;
  background: rgb(255 255 255 / 72%);
}

.hourly-forecast :deep(.el-card__header) {
  padding: 14px 18px;
}

.hourly-forecast :deep(.el-card__body) {
  padding: 14px 18px 10px;
}

.hourly-forecast header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.hourly-forecast h3 {
  margin: 0;
  color: #294963;
  font-size: 17px;
}

.hourly-scroll {
  overflow-x: auto;
  scrollbar-color: #b7cfe2 transparent;
  scrollbar-width: thin;
}

.hourly-track {
  display: inline-block;
  min-width: 100%;
}

.hourly-graph-wrap {
  position: relative;
  height: 72px;
  margin: 6px 0 14px;
}

.hourly-graph-svg {
  display: block;
  width: 100%;
  height: 100%;
}

.hourly-graph-area {
  stroke: none;
}

.hourly-graph-line {
  fill: none;
  stroke: #409eff;
  stroke-width: 2.5;
  stroke-linecap: round;
  stroke-linejoin: round;
  vector-effect: non-scaling-stroke;
}

.hourly-graph-point {
  position: absolute;
  width: 1px;
  height: 1px;
  pointer-events: none;
  transform: translate(-50%, -50%);
}

.hourly-graph-value {
  position: absolute;
  bottom: 9px;
  left: 50%;
  padding: 1px 6px;
  border-radius: 999px;
  color: #234a6b;
  background: #fff;
  box-shadow: 0 1px 3px rgb(35 74 107 / 15%);
  font-size: 11px;
  font-weight: 800;
  white-space: nowrap;
  transform: translateX(-50%);
}

.hourly-graph-dot {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 8px;
  height: 8px;
  border: 2px solid #409eff;
  border-radius: 50%;
  background: #fff;
  transform: translate(-50%, -50%);
}

.hourly-list {
  display: grid;
}

.hourly-slot {
  display: grid;
  justify-items: center;
  gap: 3px;
  padding: 2px 12px 8px;
  border-right: 1px solid #e2edf5;
}

.hourly-slot:last-child {
  border-right: 0;
}

.hourly-slot time,
.hourly-slot small {
  color: #718096;
  font-size: 12px;
}

.hourly-slot time {
  font-weight: 800;
  color: #3f6483;
  margin-top: 2px;
}

.hourly-slot img {
  width: 52px;
  height: 52px;
}

@media (max-width: 560px) {
  .hourly-forecast :deep(.el-card__header),
  .hourly-forecast :deep(.el-card__body) {
    padding: 16px;
  }
}
</style>
