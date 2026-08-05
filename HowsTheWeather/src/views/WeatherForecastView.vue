<script setup>
import { computed, onMounted, ref } from 'vue'
import { Bell, LocationFilled } from '@element-plus/icons-vue'

import { fetchCurrentWarnings, fetchWarningRegions } from '@/api/kmaWarningApi'
import { cities } from '@/api/weatherApi'
import { getActionGuide, getCityWarnings } from '@/domain/weatherWarning'

const warnings = ref([])
const isWarningLoading = ref(false)
const warningError = ref('')
const checkedAt = ref('')
const selectedType = ref('')
const myCityId = ref(cities[0].id)

const myCity = computed(() => cities.find((city) => city.id === myCityId.value) ?? cities[0])

const warningTypeCounts = computed(() => {
  const counts = new Map()
  warnings.value.forEach((warning) => counts.set(warning.type, (counts.get(warning.type) ?? 0) + 1))

  return [
    { type: '', label: '전체', count: warnings.value.length },
    ...[...counts.entries()].map(([type, count]) => ({ type, label: type, count })),
  ]
})

const filteredWarnings = computed(() =>
  selectedType.value
    ? warnings.value.filter((warning) => warning.type === selectedType.value)
    : warnings.value,
)

const myRegionWarnings = computed(() =>
  filteredWarnings.value.filter((warning) => warning.isMyRegion),
)

const otherRegionWarnings = computed(() =>
  filteredWarnings.value.filter((warning) => !warning.isMyRegion),
)

// 특보 등급(주의보 < 경보 < 중대경보) 순서로 배지 색을 진하게 올린다.
const warningBadgeClass = (warning) => {
  if (warning.level.includes('중대')) return 'is-critical'
  if (warning.level.includes('경보')) return 'is-warning'
  if (warning.level.includes('주의')) return 'is-advisory'
  return 'is-neutral'
}

const badgeSeverityRank = { 'is-advisory': 1, 'is-warning': 2, 'is-critical': 3, 'is-neutral': 0 }

// 특보 종류별로 가장 심각한 등급의 배지 색을 골라 행동 요령 카드에도 같이 입힌다.
const activeGuides = computed(() => {
  const bestByType = new Map()

  filteredWarnings.value.forEach((warning) => {
    const badgeClass = warningBadgeClass(warning)
    const existing = bestByType.get(warning.type)

    if (!existing || badgeSeverityRank[badgeClass] > badgeSeverityRank[existing.badgeClass]) {
      bestByType.set(warning.type, { badgeClass })
    }
  })

  return [...bestByType.entries()].map(([type, { badgeClass }]) => ({
    type,
    badgeClass,
    tips: getActionGuide(type),
  }))
})

const scrollToGuide = () => {
  document.getElementById('action-guide')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const warningKey = (warning) =>
  `${warning.regionId}-${warning.type}-${warning.level}-${warning.command}-${warning.effectiveAt}`

const loadWarnings = async () => {
  isWarningLoading.value = true
  warningError.value = ''

  try {
    const [regions, currentWarnings] = await Promise.all([
      fetchWarningRegions(),
      fetchCurrentWarnings(),
    ])
    const warningMap = new Map()

    cities.forEach((city) => {
      getCityWarnings(currentWarnings, regions, city.name).forEach((warning) => {
        const key = warningKey(warning)
        const existingWarning = warningMap.get(key)

        if (existingWarning) {
          if (!existingWarning.mappedCities.includes(city.name)) {
            existingWarning.mappedCities.push(city.name)
          }
          existingWarning.isMyRegion ||= city.id === myCityId.value
          return
        }

        warningMap.set(key, {
          ...warning,
          mappedCities: [city.name],
          isMyRegion: city.id === myCityId.value,
        })
      })
    })

    warnings.value = [...warningMap.values()].sort(
      (a, b) => Number(b.isMyRegion) - Number(a.isMyRegion),
    )
    selectedType.value = ''
    checkedAt.value = new Date().toLocaleTimeString('ko-KR', {
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch (error) {
    warningError.value = error.message
  } finally {
    isWarningLoading.value = false
  }
}

onMounted(() => {
  const savedCityId = localStorage.getItem('tunedMyCityId')

  if (cities.some((city) => city.id === savedCityId)) {
    myCityId.value = savedCityId
  }

  loadWarnings()
})
</script>

<template>
  <div class="tuned-forecast">
    <header class="forecast-heading">
      <div class="forecast-heading-top">
        <el-tag type="danger" effect="light" round>WEATHER WARNINGS</el-tag>
        <el-button v-if="activeGuides.length" text type="primary" @click="scrollToGuide">
          행동요령 확인하기 ↓
        </el-button>
      </div>
      <h1>전체 기상특보</h1>
      <p>지도에 연결된 주요 지역의 특보를 모아보고, 내 지역 특보는 가장 위에서 확인하세요.</p>
    </header>

    <el-card class="warning-panel" shadow="hover">
      <template #header>
        <div class="panel-header">
          <div>
            <span class="section-kicker">MAP REGION ALERTS</span>
            <h2><el-icon><Bell /></el-icon> 지도 지역 특보 {{ warnings.length }}건</h2>
            <small v-if="checkedAt">{{ checkedAt }} 기준 · 대표 지역 {{ cities.length }}곳</small>
          </div>
          <el-button type="danger" plain :loading="isWarningLoading" @click="loadWarnings">
            ↻ 새로고침
          </el-button>
        </div>
      </template>

      <el-alert
        v-if="warningError"
        :title="warningError"
        type="error"
        show-icon
        :closable="false"
        description="APIHub에서 특보구역과 특보현황 조회 활용신청을 확인해주세요."
      />
      <el-skeleton v-else-if="isWarningLoading" animated :rows="3" />
      <el-empty
        v-else-if="!warnings.length"
        description="지도에 연결된 지역에 현재 발효 중인 기상특보가 없습니다."
      >
        <small v-if="checkedAt" class="checked-at">✓ {{ checkedAt }} 기준 확인</small>
      </el-empty>
      <template v-else>
        <div class="warning-filter-pills" aria-label="특보 종류 필터">
          <button
            v-for="item in warningTypeCounts"
            :key="item.type || 'all'"
            type="button"
            class="warning-filter-pill"
            :class="{ 'is-active': selectedType === item.type }"
            :aria-pressed="selectedType === item.type"
            @click="selectedType = item.type"
          >
            {{ item.label }} <strong>{{ item.count }}</strong>건
          </button>
        </div>

        <section v-if="myRegionWarnings.length" class="warning-section my-region-section">
          <header class="warning-section-heading">
            <div class="section-title-with-icon">
              <span><el-icon><LocationFilled /></el-icon></span>
              <div>
                <small>MY REGION</small>
                <h3>{{ myCity.name }} 특보</h3>
              </div>
            </div>
            <b>{{ myRegionWarnings.length }}건</b>
          </header>

          <ul class="warning-list">
            <li
              v-for="warning in myRegionWarnings"
              :key="warningKey(warning)"
              class="is-my-region"
            >
              <div class="warning-row-heading">
                <span class="warning-badge" :class="warningBadgeClass(warning)">
                  {{ warning.type }} {{ warning.level }}
                </span>
                <span>{{ warning.command || '발효' }}</span>
              </div>
              <strong>{{ warning.region }}</strong>
              <time>발효 {{ warning.effectiveAt }}</time>
            </li>
          </ul>
        </section>

        <section class="warning-section other-region-section">
          <header class="warning-section-heading simple">
            <div>
              <small>ALL MAP REGIONS</small>
              <h3>전체 특보</h3>
            </div>
            <b>{{ otherRegionWarnings.length }}건</b>
          </header>

          <ul v-if="otherRegionWarnings.length" class="warning-list">
            <li v-for="warning in otherRegionWarnings" :key="warningKey(warning)">
              <div class="warning-row-heading">
                <span class="warning-badge" :class="warningBadgeClass(warning)">
                  {{ warning.type }} {{ warning.level }}
                </span>
                <span>{{ warning.command || '발효' }}</span>
              </div>
              <strong>{{ warning.region }}</strong>
              <small>{{ warning.upperRegion || warning.mappedCities.join(' · ') }}</small>
              <time>발효 {{ warning.effectiveAt }}</time>
            </li>
          </ul>
          <el-empty v-else description="선택한 종류의 다른 지역 특보가 없습니다." :image-size="72" />
        </section>

        <section v-if="activeGuides.length" id="action-guide" class="warning-section guide-section">
          <header class="warning-section-heading simple">
            <div>
              <small>BEFORE YOU GO OUT</small>
              <h3>외출 전 행동 요령</h3>
            </div>
          </header>

          <div class="guide-list">
            <div
              v-for="guide in activeGuides"
              :key="guide.type"
              class="guide-card"
              :class="guide.badgeClass"
            >
              <strong>{{ guide.type }}</strong>
              <ul>
                <li v-for="tip in guide.tips" :key="tip">{{ tip }}</li>
              </ul>
            </div>
          </div>
        </section>
      </template>
    </el-card>
  </div>
</template>

<style scoped>
.tuned-forecast {
  display: grid;
  gap: 22px;
  width: min(100%, 820px);
  margin: 0 auto;
}

.forecast-heading {
  padding: 8px 4px 0;
}

.forecast-heading-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.forecast-heading h1 {
  margin: 14px 0 5px;
  color: #283f55;
  font-size: clamp(1.75rem, 5vw, 2.45rem);
  letter-spacing: -0.04em;
}

.forecast-heading p {
  margin: 0;
  color: #718096;
  font-weight: 600;
}

.warning-panel {
  overflow: hidden;
  border-color: #e4e7ed;
  border-radius: 18px;
  background: #fff;
}

.warning-panel :deep(.el-card__header) {
  padding: 21px 24px;
  background: #fff;
}

.warning-panel :deep(.el-card__body) {
  padding: 24px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.section-kicker,
.warning-section-heading small {
  color: #e85c5c;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.1em;
}

.panel-header h2 {
  display: flex;
  align-items: center;
  gap: 7px;
  margin: 4px 0 2px;
  color: #384a5c;
  font-size: 1.25rem;
  font-weight: 700;
}

.panel-header small {
  color: #8a98a8;
  font-weight: 600;
}

.checked-at {
  color: #67c23a;
  font-weight: 700;
}

.warning-filter-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding-bottom: 18px;
  border-bottom: 1px solid #eceff3;
}

.warning-filter-pill {
  padding: 7px 12px;
  border: 1px solid #efc7c7;
  border-radius: 999px;
  color: #875f5f;
  background: #fff;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: 0.18s ease;
}

.warning-filter-pill strong {
  color: #c54c4c;
  font-size: 13px;
  font-weight: 800;
}

.warning-filter-pill:hover,
.warning-filter-pill.is-active {
  border-color: #e85c5c;
  color: #fff;
  background: #e85c5c;
}

.warning-filter-pill:hover strong,
.warning-filter-pill.is-active strong {
  color: #fff;
}

.warning-section {
  padding-top: 20px;
}

.warning-section + .warning-section {
  margin-top: 20px;
  border-top: 1px solid #edf0f3;
}

.warning-section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 10px;
}

.section-title-with-icon {
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-title-with-icon > span {
  display: grid;
  width: 36px;
  height: 36px;
  border-radius: 11px;
  color: #e85c5c;
  background: #fef0f0;
  place-items: center;
}

.warning-section-heading h3 {
  margin: 1px 0 0;
  color: #4d5f71;
  font-size: 17px;
  font-weight: 700;
}

.warning-section-heading b {
  padding: 5px 9px;
  border-radius: 999px;
  color: #c45656;
  background: #fef0f0;
  font-size: 12px;
}

.warning-section-heading.simple small {
  color: #8795a4;
}

.warning-list {
  display: grid;
  gap: 9px;
  padding: 0;
  margin: 0;
  list-style: none;
}

.warning-list li {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 4px 16px;
  min-width: 0;
  padding: 14px 16px;
  border: 1px solid #eceff3;
  border-radius: 13px;
  background: #fff;
}

.warning-list li.is-my-region {
  border-color: #f2baba;
  background: linear-gradient(120deg, #fff7f7, #fff);
}

.warning-row-heading {
  display: flex;
  grid-column: 1 / -1;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 4px;
}

.warning-row-heading > span:last-child {
  color: #9b6c6c;
  font-size: 12px;
  font-weight: 700;
}

.warning-badge {
  display: inline-flex;
  align-items: center;
  min-height: 22px;
  padding: 3px 9px;
  border-radius: 999px;
  border: 1px solid currentcolor;
  font-size: 11.5px;
  font-weight: 700;
  line-height: 1.2;
}

/* 주의보 → 경보 → 중대경보 순으로 점점 진해지는 3단계. 경보 색은 앱 전역의 danger 톤(#f56c6c)과 맞췄다. */
.warning-badge.is-advisory {
  color: #a76500;
  background: #fff8e8;
}

.warning-badge.is-warning {
  color: #c45656;
  background: #fef0f0;
}

.warning-badge.is-critical {
  color: #a42e26;
  background: #fde2e2;
}

.warning-badge.is-neutral {
  color: #606266;
  background: #dcdfe6;
}

.warning-list li > strong {
  min-width: 0;
  color: #4f3c3c;
  font-size: 15px;
  font-weight: 700;
  overflow-wrap: anywhere;
}

.warning-list li > small {
  grid-column: 1;
  color: #877a7a;
  font-weight: 600;
  overflow-wrap: anywhere;
}

.warning-list time {
  grid-column: 2;
  grid-row: 2 / 4;
  align-self: end;
  color: #877a7a;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.guide-section {
  padding-top: 20px;
}

.guide-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 10px;
}

.guide-card {
  padding: 14px 16px;
  border: 1px solid #d9ecff;
  border-radius: 13px;
  background: linear-gradient(120deg, #f5f9ff, #fff);
}

.guide-card strong {
  display: inline-block;
  padding: 3px 9px;
  border-radius: 999px;
  color: #fff;
  background: #409eff;
  font-size: 12px;
  font-weight: 700;
}

/* 행동 요령 카드 색을 해당 특보의 최고 등급 배지 색과 맞춘다. */
.guide-card.is-advisory {
  border-color: #f6dba8;
  background: linear-gradient(120deg, #fff8ec, #fff);
}

.guide-card.is-advisory strong {
  background: #f0a020;
}

.guide-card.is-warning {
  border-color: #f5c4c4;
  background: linear-gradient(120deg, #fff5f5, #fff);
}

.guide-card.is-warning strong {
  background: #f56c6c;
}

.guide-card.is-critical {
  border-color: #e3b6b1;
  background: linear-gradient(120deg, #fdf1ef, #fff);
}

.guide-card.is-critical strong {
  background: #922b21;
}

.guide-card ul {
  padding: 0 0 0 18px;
  margin: 10px 0 0;
  color: #475467;
  font-size: 13px;
  line-height: 1.6;
}

.guide-card li + li {
  margin-top: 4px;
}

@media (max-width: 560px) {
  .warning-panel :deep(.el-card__header),
  .warning-panel :deep(.el-card__body) {
    padding: 16px;
  }

  .panel-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .warning-list li {
    grid-template-columns: 1fr;
  }

  .warning-list time {
    grid-column: 1;
    grid-row: auto;
    justify-self: start;
    margin-top: 5px;
  }
}
</style>
