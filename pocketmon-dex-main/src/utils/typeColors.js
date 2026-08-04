// utils/typeColors.js
// -----------------------------------------------------------------------------
// 포켓몬 타입(불꽃, 물, 풀 등) 별로 배지 색상을 지정하는 매핑 테이블.
// 여러 컴포넌트(카드, 상세페이지)에서 공통으로 재사용하기 위해 별도 파일로 분리했습니다.
// -----------------------------------------------------------------------------
export const TYPE_COLORS = {
  normal: '#a8a878',
  fire: '#f08030',
  water: '#6890f0',
  electric: '#f8d030',
  grass: '#78c850',
  ice: '#98d8d8',
  fighting: '#c03028',
  poison: '#a040a0',
  ground: '#e0c068',
  flying: '#a890f0',
  psychic: '#f85888',
  bug: '#a8b820',
  rock: '#b8a038',
  ghost: '#705898',
  dragon: '#7038f8',
  dark: '#705848',
  steel: '#b8b8d0',
  fairy: '#ee99ac',
}

/** 타입 이름 -> 색상 코드. 매핑에 없으면 기본 회색 반환 */
export function getTypeColor(typeName) {
  return TYPE_COLORS[typeName] || '#777777'
}
