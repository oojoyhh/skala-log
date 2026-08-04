// composables/usePokemonDetail.js
// -----------------------------------------------------------------------------
// "포켓몬 한 마리의 상세 정보"에 관한 비즈니스 로직만 담은 Composable.
// PokemonDetailView.vue(UI)는 여기서 반환하는 pokemon/koreanName 등을
// 템플릿에 그대로 뿌리기만 하고, fetch/에러 처리/재조회 로직은 신경 쓰지 않습니다.
// -----------------------------------------------------------------------------
import { ref, watch, onMounted } from 'vue'
import { fetchPokemonDetail, fetchPokemonKoreanName } from '../api/pokeApi'

/**
 * @param {import('vue').Ref<string> | (() => string)} idSource
 *        조회할 포켓몬의 id/이름. ref 또는 getter 함수를 받아서,
 *        값이 바뀌면 자동으로 다시 조회합니다 (라우트 파라미터가 바뀌는 경우 대응).
 */
export function usePokemonDetail(idSource) {
  const pokemon = ref(null)
  const koreanName = ref(null)
  const isLoading = ref(true)
  const errorMsg = ref('')

  // 실제 데이터 요청 (비즈니스 로직)
  async function loadDetail(targetId) {
    isLoading.value = true
    errorMsg.value = ''
    pokemon.value = null
    koreanName.value = null

    try {
      // 상세 정보와 한글 이름을 동시에(병렬로) 요청해서 대기 시간을 줄임
      const [detail, ko] = await Promise.all([
        fetchPokemonDetail(targetId),
        fetchPokemonKoreanName(targetId),
      ])
      pokemon.value = detail
      koreanName.value = ko
    } catch (err) {
      errorMsg.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  // 울음소리 재생도 pokemon 데이터(cries URL)에 의존하는 "동작"이므로
  // UI 컴포넌트가 아니라 여기(로직 계층)에 둡니다.
  function playCry() {
    if (pokemon.value?.cries) {
      new Audio(pokemon.value.cries).play()
    }
  }

  // 최초 마운트 시 1회 로드
  onMounted(() => loadDetail(typeof idSource === 'function' ? idSource() : idSource.value))

  // idSource가 바뀌면(예: 목록에서 다른 포켓몬 클릭) 다시 로드
  watch(
    () => (typeof idSource === 'function' ? idSource() : idSource.value),
    (newId) => loadDetail(newId)
  )

  return {
    pokemon,
    koreanName,
    isLoading,
    errorMsg,
    playCry,
  }
}
