<script setup>
// views/PokemonDetailView.vue
// -----------------------------------------------------------------------------
// [UI 전용] 포켓몬 상세 화면.
// API 호출, 로딩/에러 상태, 재조회(watch) 같은 비즈니스 로직은 전부
// composables/usePokemonDetail.js 로 옮겼습니다. 이 컴포넌트는 그 결과를
// 받아서 화면에 그리는 것과, 화면에서만 필요한 값(라벨 매핑, 그래프 최대값)만 다룹니다.
// -----------------------------------------------------------------------------
import { usePokemonDetail } from '../composables/usePokemonDetail'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { getTypeColor } from '../utils/typeColors'
import IconWarning from '../components/icons/IconWarning.vue'
import IconSpeaker from '../components/icons/IconSpeaker.vue'
import IconChevronLeft from '../components/icons/IconChevronLeft.vue'

const props = defineProps({
  id: { type: String, required: true }, // 라우트 파라미터 (router/index.js에서 props: true로 전달)
})

// 비즈니스 로직(조회 + 재조회 + 울음소리 재생)은 composable에서 가져다 쓰기만 함
// props.id가 바뀌면 composable 내부의 watch가 자동으로 다시 조회함
const { pokemon, koreanName, isLoading, errorMsg, playCry } = usePokemonDetail(() => props.id)

// 능력치(stat) 이름을 한글로 보여주기 위한 매핑 (화면 표시 전용 -> UI 계층에 둠)
const STAT_LABELS = {
  hp: 'HP',
  attack: '공격',
  defense: '방어',
  'special-attack': '특수공격',
  'special-defense': '특수방어',
  speed: '스피드',
}

// 능력치 막대 그래프의 최대값 기준 (화면 표시 전용 -> UI 계층에 둠)
const STAT_MAX = 255
</script>

<template>
  <main class="detail">
    <router-link to="/dex" class="detail__back">
      <IconChevronLeft :size="14" />
      도감 목록
    </router-link>

    <LoadingSpinner v-if="isLoading" label="개체 정보 스캔 중..." />

    <p v-else-if="errorMsg" class="detail__hint detail__hint--error">
      <IconWarning :size="14" />
      {{ errorMsg }}
    </p>

    <article v-else-if="pokemon" class="detail__card">
      <header class="detail__header">
        <span class="detail__id">#{{ String(pokemon.id).padStart(4, '0') }}</span>
        <button class="detail__cry" @click="playCry" :disabled="!pokemon.cries">
          <IconSpeaker :size="14" />
          울음소리
        </button>
      </header>

      <img
        class="detail__sprite"
        :src="pokemon.sprite"
        :alt="pokemon.name"
        width="180"
        height="180"
      />

      <h1 class="detail__name">
        {{ pokemon.name }}
        <span v-if="koreanName" class="detail__name-ko">({{ koreanName }})</span>
      </h1>

      <div class="detail__types">
        <span
          v-for="t in pokemon.types"
          :key="t"
          class="type-badge"
          :style="{ background: getTypeColor(t) }"
        >
          {{ t }}
        </span>
      </div>

      <div class="detail__meta">
        <div class="meta-box">
          <span class="meta-box__label">키</span>
          <span class="meta-box__value">{{ (pokemon.height / 10).toFixed(1) }} m</span>
        </div>
        <div class="meta-box">
          <span class="meta-box__label">몸무게</span>
          <span class="meta-box__value">{{ (pokemon.weight / 10).toFixed(1) }} kg</span>
        </div>
      </div>

      <section class="detail__section">
        <h2 class="detail__section-title">특성</h2>
        <div class="detail__abilities">
          <span v-for="a in pokemon.abilities" :key="a" class="ability-chip">{{ a }}</span>
        </div>
      </section>

      <section class="detail__section">
        <h2 class="detail__section-title">기본 능력치</h2>
        <ul class="stat-list">
          <li v-for="s in pokemon.stats" :key="s.name" class="stat-row">
            <span class="stat-row__label">{{ STAT_LABELS[s.name] || s.name }}</span>
            <div class="stat-row__bar-track">
              <div
                class="stat-row__bar-fill"
                :style="{ width: `${Math.min(100, (s.value / STAT_MAX) * 100)}%` }"
              ></div>
            </div>
            <span class="stat-row__value">{{ s.value }}</span>
          </li>
        </ul>
      </section>
    </article>
  </main>
</template>

<style scoped>
.detail {
  flex: 1;
  padding: 24px;
  max-width: 480px;
  margin: 0 auto;
  width: 100%;
}

.detail__back {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 16px;
  font-family: var(--font-display);
  font-size: 12px;
  color: var(--text-dim);
}

.detail__back:hover {
  color: var(--accent-scan);
}

.detail__hint--error {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--accent-red);
  font-size: 13px;
}

.detail__card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
}

.detail__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail__id {
  font-family: var(--font-display);
  color: var(--text-dim);
  font-size: 13px;
}

.detail__cry {
  display: flex;
  align-items: center;
  gap: 5px;
  background: var(--surface-alt);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 12px;
  color: var(--text);
  cursor: pointer;
}

.detail__cry:hover:not(:disabled) {
  border-color: var(--accent-scan);
  color: var(--accent-scan);
}

.detail__cry:disabled {
  opacity: 0.4;
  cursor: default;
}

.detail__sprite {
  width: 180px;
  height: 180px;
  object-fit: contain;
  margin: 8px auto;
  filter: drop-shadow(0 8px 20px #000a);
}

.detail__name {
  text-transform: capitalize;
  font-size: 22px;
  margin: 4px 0 12px;
}

.detail__name-ko {
  font-size: 15px;
  color: var(--text-dim);
  font-weight: 400;
}

.detail__types {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 20px;
}

.type-badge {
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  color: #1a1a1a;
  text-transform: capitalize;
}

.detail__meta {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-bottom: 24px;
}

.meta-box {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.meta-box__label {
  font-size: 11px;
  color: var(--text-dim);
}

.meta-box__value {
  font-family: var(--font-display);
  font-size: 15px;
}

.detail__section {
  text-align: left;
  margin-top: 20px;
}

.detail__section-title {
  font-size: 12px;
  letter-spacing: 0.06em;
  color: var(--text-dim);
  border-bottom: 1px solid var(--border);
  padding-bottom: 6px;
  margin-bottom: 12px;
}

.detail__abilities {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ability-chip {
  background: var(--surface-alt);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 12px;
  text-transform: capitalize;
}

.stat-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-row {
  display: grid;
  grid-template-columns: 64px 1fr 32px;
  align-items: center;
  gap: 8px;
}

.stat-row__label {
  font-size: 12px;
  color: var(--text-dim);
}

.stat-row__bar-track {
  height: 6px;
  border-radius: 3px;
  background: var(--surface-alt);
  overflow: hidden;
}

.stat-row__bar-fill {
  height: 100%;
  background: var(--accent-scan);
}

.stat-row__value {
  font-family: var(--font-display);
  font-size: 12px;
  text-align: right;
}
</style>
