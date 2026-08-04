// api/httpClient.js
// -----------------------------------------------------------------------------
// PokeAPI 호출에 사용할 axios 인스턴스를 하나 만들어서 공유합니다.
// fetch 대신 axios를 쓰면 좋은 점:
//  - baseURL을 한 번만 설정하면 매번 전체 URL을 안 적어도 됨
//  - 응답이 4xx/5xx면 자동으로 reject 되어 res.ok 체크가 필요 없음
//  - 인터셉터(interceptors)로 공통 에러 처리/로깅을 한 곳에서 관리 가능
//  - 타임아웃, 요청 취소(AbortController 대체) 설정이 내장돼 있음
// -----------------------------------------------------------------------------
import axios from 'axios'

export const pokeApiClient = axios.create({
  baseURL: 'https://pokeapi.co/api/v2',
  timeout: 8000, // 8초 안에 응답이 없으면 타임아웃 에러로 처리
})

// 응답 인터셉터: 모든 API 응답이 여기를 한 번 거쳐감
pokeApiClient.interceptors.response.use(
  (response) => response, // 정상 응답은 그대로 통과
  (error) => {
    // 서버가 에러 응답을 준 경우 (예: 404 - 존재하지 않는 포켓몬)
    if (error.response) {
      return Promise.reject(
        new Error(
          error.response.status === 404
            ? '해당 포켓몬을 찾을 수 없습니다.'
            : `요청 처리 중 오류가 발생했습니다. (${error.response.status})`
        )
      )
    }
    // 응답 자체를 못 받은 경우 (네트워크 끊김, 타임아웃 등)
    return Promise.reject(new Error('네트워크 연결을 확인해주세요.'))
  }
)
