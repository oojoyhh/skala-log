<script setup>
import { computed, ref, watch } from 'vue'
import southKoreaMap from '@svg-maps/south-korea'
import { Location, Right } from '@element-plus/icons-vue'

import { useConfigStore } from '@/stores/configStore'
import { convertTemperature } from '@/domain/weather'

const props = defineProps({
  cities: {
    type: Array,
    required: true,
  },
  myCityId: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['select-region', 'view-detail'])
const configStore = useConfigStore()
const selectedRegionId = ref('seoul')

const preferredRegionByCityId = {
  city_01: 'seoul',
  city_03: 'busan',
  city_04: 'gangwon',
  city_05: 'north-chungcheong',
  city_06: 'daejeon',
  city_07: 'north-jeolla',
  city_08: 'gwangju',
  city_09: 'daegu',
  city_10: 'jeju',
}

const regionNames = {
  busan: '부산광역시',
  daegu: '대구광역시',
  daejeon: '대전광역시',
  gangwon: '강원특별자치도',
  gwangju: '광주광역시',
  gyeonggi: '경기도',
  incheon: '인천광역시',
  jeju: '제주특별자치도',
  'north-chungcheong': '충청북도',
  'north-gyeongsang': '경상북도',
  'north-jeolla': '전북특별자치도',
  sejong: '세종특별자치시',
  seoul: '서울특별시',
  'south-chungcheong': '충청남도',
  'south-gyeongsang': '경상남도',
  'south-jeolla': '전라남도',
  ulsan: '울산광역시',
}

// 현재 제공 중인 주요 도시를 각 시·도의 대표 관측 지점으로 연결함
const representativeCities = {
  busan: '부산',
  daegu: '대구',
  daejeon: '대전',
  gangwon: '속초',
  gwangju: '광주',
  gyeonggi: '서울',
  incheon: '서울',
  jeju: '제주',
  'north-chungcheong': '청주',
  'north-gyeongsang': '대구',
  'north-jeolla': '전주',
  sejong: '대전',
  seoul: '서울',
  'south-chungcheong': '대전',
  'south-gyeongsang': '부산',
  'south-jeolla': '광주',
  ulsan: '부산',
}

const regions = computed(() =>
  southKoreaMap.locations.map((location) => ({
    ...location,
    label: regionNames[location.id] ?? location.name,
    city: props.cities.find((city) => city.name === representativeCities[location.id]) ?? null,
  })),
)

const selectedRegion = computed(
  () => regions.value.find((region) => region.id === selectedRegionId.value) ?? regions.value[0],
)

const displayTemp = (temp) => convertTemperature(temp, configStore.unit)

const selectRegion = (region) => {
  selectedRegionId.value = region.id
  emit('select-region', {
    regionId: region.id,
    regionName: region.label,
    city: region.city,
  })
}

watch(
  () => props.myCityId,
  (cityId) => {
    selectedRegionId.value = preferredRegionByCityId[cityId] ?? 'seoul'
  },
  { immediate: true },
)
</script>

<template>
  <el-card class="korea-map-card" shadow="hover">
    <template #header>
      <header>
        <div>
          <span class="section-kicker">CLICKABLE PROVINCE MAP</span>
          <h2>전국 시·도 날씨</h2>
          <p>행정구역을 누르면 연결된 대표 도시의 날씨 카드가 표시됩니다.</p>
        </div>
        <el-tag type="primary" effect="light" round>17개 시·도</el-tag>
      </header>
    </template>

    <div class="map-layout">
      <svg
        class="province-map"
        :viewBox="southKoreaMap.viewBox"
        role="img"
        aria-label="대한민국 17개 시도 선택 지도"
      >
        <path
          v-for="region in regions"
          :key="region.id"
          :d="region.path"
          class="province"
          :class="{
            'is-selected': region.id === selectedRegionId,
            'is-my-region': region.city?.id === myCityId,
          }"
          tabindex="0"
          role="button"
          :aria-label="`${region.label} 선택`"
          @click="selectRegion(region)"
          @keyup.enter="selectRegion(region)"
        >
          <title>{{ region.label }}</title>
        </path>
      </svg>

      <aside v-if="selectedRegion" class="region-preview" aria-live="polite">
        <span class="preview-icon" aria-hidden="true"><el-icon><Location /></el-icon></span>
        <div class="preview-heading">
          <small>선택 지역</small>
          <h3>{{ selectedRegion.label }}</h3>
        </div>

        <template v-if="selectedRegion.city">
          <div class="preview-weather">
            <span>대표 관측 · {{ selectedRegion.city.name }}</span>
            <strong>
              {{ displayTemp(selectedRegion.city.temp) }}{{ configStore.unitSymbol }}
            </strong>
            <small>{{ selectedRegion.city.status }}</small>
          </div>
          <el-button type="primary" @click="emit('view-detail', selectedRegion.city)">
            상세 날씨 보기 <el-icon class="el-icon--right"><Right /></el-icon>
          </el-button>
        </template>
      </aside>
    </div>

    <footer>
      지도: @svg-maps/south-korea · MapSVG · CC BY 4.0
    </footer>
  </el-card>
</template>

<style scoped>
.korea-map-card {
  overflow: hidden;
  border-color: #d9ecff;
  border-radius: 16px;
}

.korea-map-card :deep(.el-card__header) {
  padding: 20px 24px;
  background: linear-gradient(135deg, #fff, #f5f9ff);
}

.korea-map-card :deep(.el-card__body) {
  padding: 22px 24px 14px;
}

.korea-map-card header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.section-kicker {
  color: #409eff;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.1em;
}

.korea-map-card h2 {
  margin: 4px 0 2px;
  color: #303133;
  font-size: 1.3rem;
}

.korea-map-card header p {
  margin: 0;
  color: #909399;
  font-size: 0.82rem;
}

.map-layout {
  display: grid;
  grid-template-columns: minmax(260px, 1.15fr) minmax(210px, 0.85fr);
  align-items: center;
  gap: clamp(24px, 6vw, 54px);
}

.province-map {
  display: block;
  width: min(100%, 390px);
  max-height: 470px;
  margin: 0 auto;
}

.province {
  fill: #eaf4ff;
  stroke: #fff;
  stroke-linejoin: round;
  stroke-width: 2;
  cursor: pointer;
  transition:
    fill 0.18s ease,
    filter 0.18s ease,
    transform 0.18s ease;
  transform-box: fill-box;
  transform-origin: center;
}

.province:hover,
.province:focus-visible {
  fill: #a0cfff;
  filter: drop-shadow(0 3px 4px rgb(36 95 145 / 18%));
  outline: none;
  transform: scale(1.025);
}

.province.is-selected {
  fill: #409eff;
  filter: drop-shadow(0 4px 5px rgb(36 95 145 / 25%));
}

.province.is-my-region:not(.is-selected) {
  fill: #b3d8ff;
}

.region-preview {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 12px;
  padding: 20px;
  border: 1px solid #d9ecff;
  border-radius: 16px;
  background: #f8fbff;
}

.preview-icon {
  display: grid;
  grid-row: 1;
  width: 42px;
  height: 42px;
  border-radius: 13px;
  color: #409eff;
  background: #d9ecff;
  font-size: 21px;
  place-items: center;
}

.preview-heading small,
.preview-weather small {
  color: #909399;
}

.preview-weather span {
  color: #50677d;
  font-weight: 800;
}

.preview-heading h3 {
  margin: 2px 0 0;
  color: #303133;
  font-size: 1.2rem;
}

.preview-weather {
  display: grid;
  grid-column: 1 / -1;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: end;
  gap: 2px 10px;
  padding: 14px 0;
  border-top: 1px solid #e4edf5;
  border-bottom: 1px solid #e4edf5;
}

.preview-weather strong {
  grid-row: 1 / 3;
  grid-column: 2;
  color: #243e59;
  font-size: 1.8rem;
}

.region-preview :deep(.el-button) {
  grid-column: 1 / -1;
}

.korea-map-card footer {
  margin-top: 10px;
  color: #a8abb2;
  font-size: 10px;
  text-align: right;
}

@media (max-width: 680px) {
  .map-layout {
    grid-template-columns: 1fr;
  }

  .korea-map-card header {
    align-items: flex-start;
    flex-direction: column;
  }

  .korea-map-card :deep(.el-card__header),
  .korea-map-card :deep(.el-card__body) {
    padding: 16px;
  }
}
</style>
