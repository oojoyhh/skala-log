<script setup>
// views/PokedexView.vue
// -----------------------------------------------------------------------------
// [UI 전용] 도감 목록 화면.
// 이 컴포넌트는 오직 "어떻게 보여줄지"만 담당합니다.
// 데이터를 어떻게 가져오는지(API), 페이지를 어떻게 계산하는지, 검색어를
// 어떻게 검증하는지는 전부 composables/*.js 에 있고, 여기서는 그 결과값만
// 템플릿에 연결(binding)합니다.
// -----------------------------------------------------------------------------
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePokemonList } from '../composables/usePokemonList'
import { useDexSearch } from '../composables/useDexSearch'
import PokemonCard from '../components/PokemonCard.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import IconWarning from '../components/icons/IconWarning.vue'
import IconSearch from '../components/icons/IconSearch.vue'
import IconChevronLeft from '../components/icons/IconChevronLeft.vue'
import IconChevronRight from '../components/icons/IconChevronRight.vue'

const router = useRouter()

// 비즈니스 로직(목록 조회 + 페이지네이션)은 composable에서 가져다 쓰기만 함
const { pokemonList, totalCount, offset, isLoading, errorMsg, PAGE_SIZE, loadList, goPrev, goNext } =
  usePokemonList()

// 비즈니스 로직(검색어 검증 + 이동)도 composable에서 가져다 쓰기만 함
const { searchTerm, searchError, submitSearch } = useDexSearch(router)

// UI 컴포넌트가 할 일은 "언제 불러올지" 트리거하는 것뿐 (실제 fetch는 composable 내부)
onMounted(loadList)
</script>

<template>
  <main class="dex">
    <section class="dex__search">
      <form @submit.prevent="submitSearch" class="search-form">
        <input
          v-model="searchTerm"
          type="text"
          placeholder="이름 또는 번호로 검색 (예: ditto, 132)"
          aria-label="포켓몬 검색"
        />
        <button type="submit">
          <IconSearch :size="14" />
          조회
        </button>
      </form>
      <p v-if="searchError" class="dex__hint dex__hint--error">
        <IconWarning :size="13" />
        {{ searchError }}
      </p>
    </section>

    <LoadingSpinner v-if="isLoading" label="도감 데이터 불러오는 중..." />

    <p v-else-if="errorMsg" class="dex__hint dex__hint--error">
      <IconWarning :size="13" />
      {{ errorMsg }}
    </p>

    <template v-else>
      <div class="dex__grid">
        <PokemonCard
          v-for="p in pokemonList"
          :key="p.id"
          :id="p.id"
          :name="p.name"
        />
      </div>

      <div class="dex__pager">
        <button :disabled="offset === 0" @click="goPrev">
          <IconChevronLeft :size="14" />
          이전
        </button>
        <span class="dex__page-info">
          {{ offset + 1 }}–{{ Math.min(offset + PAGE_SIZE, totalCount) }} / {{ totalCount }}
        </span>
        <button :disabled="offset + PAGE_SIZE >= totalCount" @click="goNext">
          다음
          <IconChevronRight :size="14" />
        </button>
      </div>
    </template>
  </main>
</template>

<style scoped>
.dex {
  flex: 1;
  padding: 24px;
  max-width: 960px;
  margin: 0 auto;
  width: 100%;
}

.dex__search {
  margin-bottom: 24px;
}

.search-form {
  display: flex;
  gap: 8px;
}

.search-form input {
  flex: 1;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  color: var(--text);
  font-size: 14px;
}

.search-form input:focus {
  border-color: var(--accent-scan);
}

.search-form button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  border-radius: 8px;
  border: 1px solid var(--accent-scan);
  background: transparent;
  color: var(--accent-scan);
  font-family: var(--font-display);
  font-size: 12px;
  letter-spacing: 0.06em;
  cursor: pointer;
}

.search-form button:hover {
  background: var(--accent-scan);
  color: #0b1410;
}

.dex__hint {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 8px 2px 0;
  font-size: 12px;
  color: var(--text-dim);
}

.dex__hint--error {
  color: var(--accent-red);
}

.dex__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 12px;
}

.dex__pager {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 28px;
}

.dex__pager button {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  font-family: var(--font-display);
  font-size: 12px;
  cursor: pointer;
}

.dex__pager button:hover:not(:disabled) {
  border-color: var(--accent-scan);
  color: var(--accent-scan);
}

.dex__pager button:disabled {
  opacity: 0.35;
  cursor: default;
}

.dex__page-info {
  font-family: var(--font-display);
  font-size: 12px;
  color: var(--text-dim);
}
</style>
