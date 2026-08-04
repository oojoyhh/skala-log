<script setup>
// 부모가 가진 도시 목록과 현재 내 지역을 전달받는다.
const props = defineProps({
  cities: {
    type: Array,
    required: true,
  },
  selectedCityId: {
    type: String,
    required: true,
  },
})

// 선택한 도시 id를 부모에게 전달한다.
const emit = defineEmits(['update-my-city'])

const handleChange = (event) => {
  emit('update-my-city', event.target.value)
}
</script>

<template>
  <div class="location-selector">
    <label for="my-city">내 지역</label>
    <select id="my-city" :value="props.selectedCityId" @change="handleChange">
      <option v-for="city in props.cities" :key="city.id" :value="city.id">
        {{ city.name }}
      </option>
    </select>
    <p>선택한 지역을 위 카드와 전체 날씨 목록에 함께 표시합니다.</p>
  </div>
</template>

<style scoped>
.location-selector {
  display: grid;
  grid-template-columns: auto minmax(160px, 1fr);
  align-items: center;
  gap: 10px 14px;
}

.location-selector label {
  color: #334d69;
  font-weight: 700;
}

.location-selector select {
  height: 44px;
  padding: 0 12px;
  border: 1px solid #9ba7b3;
  border-radius: 4px;
  color: #24364b;
  background: #fff;
  outline: none;
}

.location-selector select:focus {
  border-color: #438fd1;
  box-shadow: 0 0 0 3px rgb(67 143 209 / 18%);
}

.location-selector p {
  grid-column: 1 / -1;
  margin: 0;
  color: #68788a;
  font-size: 14px;
}

@media (max-width: 480px) {
  .location-selector {
    grid-template-columns: 1fr;
  }

  .location-selector p {
    grid-column: auto;
  }
}
</style>
