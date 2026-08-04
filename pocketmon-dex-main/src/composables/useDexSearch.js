// composables/useDexSearch.js
// -----------------------------------------------------------------------------
// 도감 검색창의 "입력값 검증 + 상세 페이지로 이동" 로직.
// 이 자체는 API를 호출하진 않지만(상세 페이지 진입 후 usePokemonDetail이 조회함),
// 화면 렌더링과 무관한 판단 로직이므로 UI 컴포넌트에서 분리해둡니다.
// -----------------------------------------------------------------------------
import { ref } from 'vue'

export function useDexSearch(router) {
  const searchTerm = ref('')
  const searchError = ref('')

  function submitSearch() {
    const term = searchTerm.value.trim().toLowerCase()
    searchError.value = ''

    if (!term) {
      searchError.value = '포켓몬 이름이나 번호를 입력해주세요.'
      return
    }

    router.push(`/dex/${term}`)
  }

  return {
    searchTerm,
    searchError,
    submitSearch,
  }
}
