<script setup>
import { useConfigStore } from '@/stores/configStore'
import { convertTemperature } from '@/domain/weather'

defineProps({
  daily: {
    type: Array,
    required: true,
  },
})

const configStore = useConfigStore()
const displayTemp = (temp) => convertTemperature(temp, configStore.unit)
</script>

<template>
  <el-card class="daily-forecast" shadow="never">
    <template #header>
      <header>
        <h3>5일 예보</h3>
        <el-tag type="info" effect="plain" size="small" round>일 단위</el-tag>
      </header>
    </template>

    <div class="daily-list">
      <div v-for="item in daily" :key="item.date" class="daily-slot">
        <b>{{ item.date }}</b>
        <img :src="`https://openweathermap.org/img/wn/${item.icon}@2x.png`" :alt="item.status" />
        <span class="daily-range"
          ><em>{{ displayTemp(item.minTemp) }}°</em> / {{ displayTemp(item.maxTemp) }}°</span
        >
      </div>
    </div>
  </el-card>
</template>

<style scoped>
.daily-forecast {
  min-width: 0;
  border: 1px solid rgb(104 159 205 / 22%);
  border-radius: 14px;
  background: rgb(255 255 255 / 72%);
}

.daily-forecast :deep(.el-card__header) {
  padding: 14px 18px;
}

.daily-forecast :deep(.el-card__body) {
  padding: 14px 18px 10px;
}

.daily-forecast header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.daily-forecast h3 {
  margin: 0;
  color: #294963;
  font-size: 17px;
}

.daily-list {
  display: grid;
  grid-template-columns: repeat(5, minmax(64px, 1fr));
  overflow-x: auto;
  scrollbar-color: #b7cfe2 transparent;
  scrollbar-width: thin;
}

.daily-slot {
  display: grid;
  justify-items: center;
  gap: 4px;
  padding: 2px 8px 8px;
  border-right: 1px solid #e2edf5;
}

.daily-slot:last-child {
  border-right: 0;
}

.daily-slot b {
  color: #718096;
  font-size: 12px;
}

.daily-slot img {
  width: 44px;
  height: 44px;
}

.daily-range {
  color: #233f59;
  font-size: 13px;
  font-weight: 700;
  white-space: nowrap;
}

.daily-range em {
  color: #5685ad;
  font-style: normal;
}

@media (max-width: 560px) {
  .daily-forecast :deep(.el-card__header),
  .daily-forecast :deep(.el-card__body) {
    padding: 16px;
  }
}
</style>
