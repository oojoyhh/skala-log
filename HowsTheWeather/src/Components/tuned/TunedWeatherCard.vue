<script setup>
import { computed } from 'vue'
import { ArrowRight, Location } from '@element-plus/icons-vue'

import { useConfigStore } from '@/stores/configStore'
import { convertTemperature } from '@/domain/weather'

const props = defineProps({
  city: {
    type: Object,
    required: true,
  },
  isMyCity: {
    type: Boolean,
    default: false,
  },
  compact: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['select-card', 'click-detail', 'set-my-city'])
const configStore = useConfigStore()

const displayTemp = computed(() => convertTemperature(props.city.temp, configStore.unit))
const displayMin = computed(() => convertTemperature(props.city.minTemp, configStore.unit))
const displayMax = computed(() => convertTemperature(props.city.maxTemp, configStore.unit))
</script>

<template>
  <el-card
    class="tuned-weather-card"
    :class="{ 'is-my-city': isMyCity, 'is-compact': compact }"
    shadow="never"
    :body-style="{ padding: '0' }"
    tabindex="0"
    @click="emit('select-card', city)"
    @keyup.enter="emit('select-card', city)"
  >
    <article class="card-content">
      <header class="card-header">
        <button
          class="location-mark"
          :class="{ 'is-my-city': isMyCity }"
          :aria-pressed="isMyCity"
          :disabled="isMyCity"
          :title="isMyCity ? '내 지역' : '내 지역으로 설정'"
          :aria-label="isMyCity ? '내 지역' : `내 지역으로 설정: ${city.name}`"
          @click.stop="emit('set-my-city', city.id)"
        >
          <el-icon><Location /></el-icon>
        </button>

        <div class="city-heading">
          <h3>{{ city.name }}</h3>
          <span class="weather-status"><i aria-hidden="true"></i>{{ city.status }}</span>
        </div>

        <strong class="card-temp">{{ displayTemp }}{{ configStore.unitSymbol }}</strong>
      </header>

      <footer class="card-footer">
        <span>최저 {{ displayMin }}° · 최고 {{ displayMax }}°</span>
        <el-button
          class="detail-link"
          type="primary"
          link
          @click.stop="emit('click-detail', city)"
        >
          상세 날씨 <el-icon class="el-icon--right"><ArrowRight /></el-icon>
        </el-button>
      </footer>
    </article>
  </el-card>
</template>

<style scoped>
.tuned-weather-card {
  min-width: 0;
  overflow: hidden;
  border: 1px solid #dfe7ef;
  border-radius: 16px;
  background: #fff;
  cursor: pointer;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    transform 0.2s ease;
}

.tuned-weather-card :deep(.el-card__body) {
  padding: 0;
}

.tuned-weather-card:hover,
.tuned-weather-card:focus-visible {
  border-color: #9bc7eb;
  box-shadow: 0 10px 24px rgb(46 108 160 / 11%);
  outline: none;
  transform: translateY(-2px);
}

.tuned-weather-card.is-my-city {
  border-color: #79bbff;
  background: linear-gradient(145deg, #fff, #f4f9ff);
}

.card-content {
  padding: 18px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 14px;
}

.location-mark {
  display: grid;
  flex: 0 0 auto;
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 11px;
  color: #3b82c4;
  background: #eaf4fc;
  font-size: 17px;
  cursor: pointer;
  place-items: center;
  transition:
    background 0.15s ease,
    color 0.15s ease,
    transform 0.15s ease;
}

.location-mark:hover:not(:disabled) {
  background: #d9ecff;
  transform: scale(1.06);
}

.location-mark.is-my-city {
  color: #fff;
  background: #3b82c4;
  cursor: default;
}

.location-mark:disabled {
  opacity: 1;
}

.city-heading {
  display: grid;
  flex: 1 1 auto;
  gap: 3px;
  min-width: 0;
}

.city-heading h3 {
  margin: 0;
  overflow: hidden;
  color: #2d4864;
  font-size: 19px;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.15;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.weather-status {
  display: flex;
  align-items: center;
  min-width: 0;
  overflow: hidden;
  color: #60778e;
  font-size: 12.5px;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.weather-status i {
  flex: 0 0 auto;
  width: 6px;
  height: 6px;
  margin-right: 6px;
  border-radius: 50%;
  background: #79bbff;
  box-shadow: 0 0 0 3px #ecf5ff;
}

.card-temp {
  flex: 0 0 auto;
  color: #203b56;
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 1;
  white-space: nowrap;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding-top: 11px;
  border-top: 1px solid #edf1f5;
}

.card-footer > span {
  color: #8493a3;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.detail-link {
  flex: 0 0 auto;
  height: auto;
  padding: 2px 0;
  font-size: 12px;
  font-weight: 800;
}

.tuned-weather-card.is-compact .card-content {
  padding: 16px;
}

.tuned-weather-card.is-compact .card-temp {
  font-size: 24px;
}

@media (max-width: 560px) {
  .card-content,
  .tuned-weather-card.is-compact .card-content {
    padding: 16px;
  }
}
</style>
