<script setup>
import { computed } from 'vue'

// 부모가 전달한 도시 객체
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

// 카드 선택과 상세보기 동작을 부모에게 알릴 이벤트
const emit = defineEmits(['select-card', 'click-detail'])

// 날씨 상태에 맞는 아이콘과 배경 테마를 고른다.
const weatherView = computed(() => {
  const weatherMap = {
    맑음: { icon: '☀️', theme: 'sunny' },
    비: { icon: '🌧️', theme: 'rainy' },
    구름: { icon: '☁️', theme: 'cloudy' },
    비바람: { icon: '⛈️', theme: 'stormy' },
  }

  return weatherMap[props.city.status] ?? { icon: '🌤️', theme: 'default' }
})

// 날씨와 기온에 맞는 짧은 메시지를 만든다.
const weatherMessage = computed(() => {
  if (props.city.status === '비바람') return '튼튼한 우산을 꼭 챙겨요! ☂️'
  if (props.city.status === '비') return '빗소리와 따뜻한 차는 어때요? ☕'
  if (props.city.temp >= 26) return '아이스크림이 필요한 날이에요! 🍦'
  if (props.city.temp >= 21) return '산책하기 좋은 날씨예요! 🐕'
  return '포근한 겉옷을 챙기세요! 🧣'
})

// 카드가 선택되면 도시 객체를 부모에게 보낸다.
const selectCard = () => {
  emit('select-card', props.city)
}

// 상세보기 요청도 도시 객체와 함께 부모에게 보낸다.
const clickDetail = () => {
  emit('click-detail', {
    city: props.city,
    message: weatherMessage.value,
  })
}
</script>

<template>
  <!-- 클릭하거나 Enter를 누르면 카드 선택 이벤트가 발생한다. -->
  <article
    class="weather-card"
    :class="`weather-${weatherView.theme}`"
    tabindex="0"
    @click="selectCard"
    @keyup.enter="selectCard"
  >
    <div class="weather-main">
      <span class="weather-icon" aria-hidden="true">{{ weatherView.icon }}</span>

      <div class="weather-info">
        <h3>
          {{ props.city.name }} <span>({{ props.city.status }})</span>
          <small v-if="props.isMyCity" class="my-city-label">📍 내 지역</small>
        </h3>
        <p>현재 기온: {{ props.city.temp }}°C</p>

        <!-- 26도를 기준으로 서로 다른 라벨을 표시한다. -->
        <span v-if="props.city.temp >= 26" class="temperature-label hot">
          🔥 더움 (26도 이상)
        </span>
        <span v-else-if="props.city.temp >= 21" class="temperature-label normal">
          ☁️ 보통 (21도 이상 26도 미만)
        </span>
        <span v-else class="temperature-label cool">❄️ 선선함 (21도 미만)</span>

      </div>
    </div>

    <!-- .stop으로 상세보기 클릭이 카드 선택으로 전파되지 않게 한다. -->
    <button type="button" @click.stop="clickDetail">상세보기</button>
  </article>
</template>

<style scoped>
/* 도시별 날씨 카드 레이아웃 */
.weather-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  min-height: 128px;
  padding: 20px;
  border: 1px solid #d8dfe6;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 1px 3px rgb(27 43 65 / 5%);
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}

/* 날씨별로 카드의 배경 분위기를 바꾼다. */
.weather-card.weather-sunny {
  border-color: #f2d882;
  background: linear-gradient(135deg, #fffef8 0%, #fff5c9 100%);
}

.weather-card.weather-rainy {
  border-color: #a7cbe8;
  background: linear-gradient(135deg, #f8fcff 0%, #dceeff 100%);
}

.weather-card.weather-cloudy {
  border-color: #c9c4e5;
  background: linear-gradient(135deg, #fbfaff 0%, #ece9f8 100%);
}

.weather-card.weather-stormy {
  border-color: #aab9cc;
  background: linear-gradient(135deg, #f6f8fb 0%, #d9e2ec 100%);
}

.weather-main {
  display: flex;
  align-items: center;
  gap: 18px;
  min-width: 0;
}

.weather-icon {
  flex: 0 0 auto;
  font-size: 44px;
  filter: drop-shadow(0 4px 5px rgb(45 72 100 / 14%));
}

/* 마우스나 키보드로 선택했을 때 카드 강조 */
.weather-card:hover,
.weather-card:focus-visible {
  border-color: #7db7e8;
  box-shadow: 0 7px 18px rgb(46 108 160 / 12%);
  outline: none;
  transform: translateY(-2px);
}

.weather-info h3,
.weather-info p {
  margin: 0;
}

.weather-info h3 {
  margin-bottom: 6px;
  color: #2d4864;
  font-size: 19px;
  font-weight: 600;
}

.weather-info h3 span {
  font-weight: 500;
}

.weather-info p {
  margin-bottom: 9px;
  font-size: 17px;
}

/* 기온 상태 라벨 공통 디자인 */
.temperature-label {
  display: inline-block;
  padding: 7px 12px;
  border-radius: 5px;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
}

/* 더움과 선선함 상태별 색상 */
.temperature-label.hot {
  color: #994f58;
  background: #ffd3d8;
}

.temperature-label.normal {
  color: #645985;
  background: #e3dcf7;
}

.temperature-label.cool {
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
  font-weight: 700;
  vertical-align: middle;
}

/* 상세보기 버튼 */
.weather-card button {
  flex: 0 0 auto;
  padding: 9px 14px;
  border: 1px solid #c6b9e5;
  border-radius: 4px;
  color: #625387;
  background: #f0ebfc;
  font-weight: 700;
  cursor: pointer;
  transition: color 0.2s, background 0.2s;
}

.weather-card button:hover,
.weather-card button:focus-visible {
  color: #514276;
  background: #e1d8f7;
  box-shadow: 0 3px 8px rgb(98 83 135 / 18%);
  outline: none;
}

/* 작은 화면에서 카드와 버튼의 여백을 줄인다. */
@media (max-width: 560px) {
  .weather-card {
    align-items: flex-start;
    gap: 12px;
    padding: 16px;
  }

  .weather-card button {
    padding: 8px 10px;
  }

  .weather-main {
    align-items: flex-start;
    gap: 12px;
  }

  .weather-icon {
    font-size: 34px;
  }
}
</style>
