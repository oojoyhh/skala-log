<script setup>
// components/PokemonCard.vue
// -----------------------------------------------------------------------------
// 도감 목록 화면에서 포켓몬 한 마리를 표시하는 카드.
// 목록 API(fetchPokemonList)는 이름과 id만 주기 때문에, 카드 이미지는
// 매 카드마다 상세 API를 또 호출하지 않고 PokeAPI의 정적 스프라이트 저장소
// (GitHub raw) URL 규칙(id 기반)을 이용해 바로 그립니다. -> 불필요한 API 호출을 줄여 성능 개선
// -----------------------------------------------------------------------------
import { computed } from 'vue'

const props = defineProps({
  id: { type: Number, required: true },
  name: { type: String, required: true },
})

// 도감 번호를 4자리로 맞춰 "#0025" 형태로 표시 (스캐너 단말기 느낌)
const paddedId = computed(() => `#${String(props.id).padStart(4, '0')}`)

// PokeAPI 공식 스프라이트 저장소의 id 기반 이미지 규칙
const spriteUrl = computed(
  () =>
    `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${props.id}.png`
)
</script>

<template>
  <!-- router-link: 클릭하면 /dex/:id 상세 페이지로 이동 -->
  <router-link :to="`/dex/${id}`" class="card">
    <span class="card__id">{{ paddedId }}</span>
    <img
      :src="spriteUrl"
      :alt="name"
      class="card__img"
      loading="lazy"
      width="72"
      height="72"
    />
    <span class="card__name">{{ name }}</span>
  </router-link>
</template>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 16px 8px 12px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  transition: transform 0.15s ease, border-color 0.15s ease, background 0.15s ease;
  position: relative;
}

.card:hover {
  transform: translateY(-3px);
  border-color: var(--accent-scan);
  background: var(--surface-alt);
}

.card__id {
  align-self: flex-start;
  font-family: var(--font-display);
  font-size: 11px;
  color: var(--text-dim);
  padding-left: 4px;
}

.card__img {
  width: 72px;
  height: 72px;
  object-fit: contain;
  image-rendering: pixelated; /* 도트 그래픽 느낌 유지 */
}

.card__name {
  font-size: 13px;
  font-weight: 500;
  text-transform: capitalize;
  color: var(--text);
}
</style>
