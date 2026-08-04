// composables/usePokemonList.js
// -----------------------------------------------------------------------------
// "포켓몬 목록 + 페이지네이션"에 관한 비즈니스 로직만 담은 Composable.
// PokedexView.vue(UI)는 이 함수가 반환하는 상태/함수만 템플릿에 연결하고,
// 실제 fetch 호출, 페이지 계산 같은 로직은 전부 여기서 처리합니다.
//
// 이렇게 분리하면 얻는 것:
//  - PokedexView.vue는 "어떻게 그릴지"만 신경 쓰면 됨 (관심사 분리)
//  - 이 로직을 다른 화면에서도 재사용 가능
//  - API 호출 로직만 따로 테스트하기 쉬움 (컴포넌트 마운트 없이 테스트 가능)
// -----------------------------------------------------------------------------
import { ref } from 'vue'
import { fetchPokemonList } from '../api/pokeApi'

const PAGE_SIZE = 20 // 한 페이지에 보여줄 포켓몬 수

export function usePokemonList() {
  const pokemonList = ref([])   // 현재 페이지에 표시할 포켓몬 배열
  const totalCount = ref(0)     // PokeAPI가 가진 전체 포켓몬 수
  const offset = ref(0)         // 몇 번째부터 가져올지 (페이지네이션 커서)
  const isLoading = ref(true)
  const errorMsg = ref('')

  // 목록을 서버(PokeAPI)에서 가져오는 함수 (실제 데이터 요청 = 비즈니스 로직)
  async function loadList() {
    isLoading.value = true
    errorMsg.value = ''

    try {
      const { results, count } = await fetchPokemonList(PAGE_SIZE, offset.value)
      pokemonList.value = results
      totalCount.value = count
    } catch (err) {
      errorMsg.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  function goPrev() {
    if (offset.value === 0) return
    offset.value = Math.max(0, offset.value - PAGE_SIZE)
    loadList()
  }

  function goNext() {
    if (offset.value + PAGE_SIZE >= totalCount.value) return
    offset.value += PAGE_SIZE
    loadList()
  }

  // UI 컴포넌트가 v-if 등으로 바로 쓸 수 있도록 계산된 값도 함께 제공
  const hasPrev = () => offset.value > 0
  const hasNext = () => offset.value + PAGE_SIZE < totalCount.value

  return {
    // 상태 (state)
    pokemonList,
    totalCount,
    offset,
    isLoading,
    errorMsg,
    PAGE_SIZE,
    // 동작 (actions)
    loadList,
    goPrev,
    goNext,
    hasPrev,
    hasNext,
  }
}
