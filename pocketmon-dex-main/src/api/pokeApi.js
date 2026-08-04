// api/pokeApi.js
// -----------------------------------------------------------------------------
// 실제 외부 API인 PokeAPI(https://pokeapi.co/)를 호출하는 함수 모음입니다.
// httpClient.js에서 만든 axios 인스턴스(pokeApiClient)를 사용합니다.
// (참고: axios는 응답 데이터가 이미 res.data에 파싱되어 들어오고,
//  4xx/5xx 에러는 자동으로 reject 되므로 fetch처럼 res.ok를 직접 체크할 필요가 없습니다.)
// -----------------------------------------------------------------------------
import { pokeApiClient } from './httpClient'

/**
 * 포켓몬 목록(이름 + 상세정보 URL)을 페이지네이션으로 가져옵니다.
 * 예: limit=20, offset=0  ->  1~20번 포켓몬
 *     limit=20, offset=20 ->  21~40번 포켓몬
 *
 * @param {number} limit  한 번에 가져올 개수
 * @param {number} offset 몇 번째부터 가져올지
 */
export async function fetchPokemonList(limit = 20, offset = 0) {
  // axios는 두 번째 인자로 { params }를 주면 쿼리스트링(?limit=..&offset=..)을 자동으로 만들어줌
  const { data } = await pokeApiClient.get('/pokemon', {
    params: { limit, offset },
  })

  // data.results 는 [{ name: 'ditto', url: '.../pokemon/132/' }, ...] 형태
  // url 끝의 숫자(id)를 잘라내서 미리 꺼내두면, 목록 화면에서 도감 번호를 바로 표시하기 편함
  const results = data.results.map((item) => {
    const idMatch = item.url.match(/\/pokemon\/(\d+)\//)
    return {
      name: item.name,
      id: idMatch ? Number(idMatch[1]) : null,
    }
  })

  return {
    count: data.count, // 전체 포켓몬 수 (다음 페이지 존재 여부 판단용)
    results,
  }
}

/**
 * 포켓몬 한 마리의 상세 정보를 가져옵니다.
 * id 또는 이름 둘 다 받을 수 있습니다. (예: 132 또는 'ditto')
 */
export async function fetchPokemonDetail(idOrName) {
  const { data } = await pokeApiClient.get(`/pokemon/${idOrName}`)

  // 화면에서 쓰기 좋은 형태로 필요한 값만 가공해서 반환
  return {
    id: data.id,
    name: data.name,
    height: data.height, // 단위: 10cm (예: 3 -> 0.3m)
    weight: data.weight, // 단위: 100g (예: 69 -> 6.9kg)
    types: data.types.map((t) => t.type.name),
    abilities: data.abilities.map((a) => a.ability.name),
    stats: data.stats.map((s) => ({
      name: s.stat.name,
      value: s.base_stat,
    })),
    sprite:
      data.sprites.other?.['official-artwork']?.front_default ||
      data.sprites.front_default,
    cries: data.cries?.latest || null, // 최신 버전 API에는 울음소리 mp3 URL도 포함되어 있음
  }
}

/**
 * 포켓몬의 한글 이름을 species 엔드포인트에서 조회합니다.
 * (PokeAPI는 다국어 이름을 species 데이터의 names 배열에 함께 제공합니다.)
 */
export async function fetchPokemonKoreanName(idOrName) {
  try {
    const { data } = await pokeApiClient.get(`/pokemon-species/${idOrName}`)
    const koEntry = data.names.find((n) => n.language.name === 'ko')
    return koEntry ? koEntry.name : null
  } catch {
    // 한글 이름은 부가 정보이므로, 실패해도 전체 화면이 깨지지 않도록 조용히 null 반환
    return null
  }
}
