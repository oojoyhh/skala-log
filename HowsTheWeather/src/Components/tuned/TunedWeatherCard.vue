<script setup>
import { computed } from 'vue'
import { useConfigStore } from '@/stores/configStore'

const props = defineProps({
  city: {
    type: Object,
    required: true,
  },
  isMyCity: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['select-card', 'click-detail'])
const configStore = useConfigStore()

// 실습 5의 단위 설정을 이어받아 표시 온도를 계산한다.
const displayTemp = computed(() => {
  const rawTemp = props.city.temp

  if (configStore.unit === 'fahrenheit') {
    return Math.round((rawTemp * 9) / 5 + 32)
  }

  return rawTemp
})

const temperatureView = computed(() => {
  if (props.city.temp >= 26) {
    return {
      label: '🔥 더움 (26도 이상)',
      className: 'hot',
    }
  }

  if (props.city.temp >= 21) {
    return {
      label: '☁️ 보통 (21도 이상 26도 미만)',
      className: 'normal',
    }
  }

  return {
    label: '❄️ 선선함 (21도 미만)',
    className: 'cool',
  }
})
</script>

<template>
  <article
    class="tuned-weather-card"
    tabindex="0"
    @click="emit('select-card', city)"
    @keyup.enter="emit('select-card', city)"
  >
    <div class="tuned-weather-info">
      <h3>
        {{ city.name }} <span>({{ city.status }})</span>
        <small v-if="isMyCity" class="my-city-label">📍 내 지역</small>
      </h3>

      <p>현재 기온: {{ displayTemp }}{{ configStore.unitSymbol }}</p>

      <span class="temperature-label" :class="temperatureView.className">
        {{ temperatureView.label }}
      </span>
    </div>

    <button type="button" @click.stop="emit('click-detail', city)">상세보기</button>
  </article>
</template>

<style scoped>
.tuned-weather-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  min-height: 128px;
  padding: 20px;
  border: 1px solid #d8dfe6;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition:
    border-color 0.2s,
    box-shadow 0.2s,
    transform 0.2s;
}

.tuned-weather-card:hover,
.tuned-weather-card:focus-visible {
  border-color: #7db7e8;
  box-shadow: 0 7px 18px rgb(46 108 160 / 12%);
  outline: none;
  transform: translateY(-2px);
}

.tuned-weather-info h3,
.tuned-weather-info p {
  margin: 0;
}

.tuned-weather-info h3 {
  margin-bottom: 7px;
  color: #2d4864;
}

.tuned-weather-info h3 span {
  font-weight: 500;
}

.tuned-weather-info p {
  margin-bottom: 10px;
}

.temperature-label {
  display: inline-block;
  padding: 7px 12px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 700;
}

.hot {
  color: #994f58;
  background: #ffd3d8;
}

.normal {
  color: #645985;
  background: #e3dcf7;
}

.cool {
  color: #477394;
  background: #d5edff;
}

.my-city-label {
  display: inline-block;
  padding: 3px 7px;
  margin-left: 6px;
  border-radius: 999px;
  color: #26743b;
  background: #e5f5e8;
  font-size: 12px;
  vertical-align: middle;
}

.tuned-weather-card button {
  flex: 0 0 auto;
  padding: 9px 14px;
  border: 1px solid #c6b9e5;
  border-radius: 4px;
  color: #625387;
  background: #f0ebfc;
  font-weight: 700;
  cursor: pointer;
}

@media (max-width: 560px) {
  .tuned-weather-card {
    align-items: flex-start;
    gap: 12px;
    padding: 16px;
  }
}
</style>
