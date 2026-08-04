// api/fakeAuth.js
// -----------------------------------------------------------------------------
// "Fake API" 모듈: 실제 백엔드 서버가 없기 때문에, 로그인 요청을
// 실제 네트워크 통신처럼 보이게 흉내(mock)냅니다.
//
// - setTimeout으로 네트워크 지연(latency)을 흉내냄
// - 실제 API처럼 Promise를 반환하고, 성공/실패 시 각각 resolve / reject 함
// - 이후 실제 백엔드가 준비되면, 이 함수 내부만 fetch/axios 호출로
//   교체하면 되므로 나머지 코드(store, view)는 수정할 필요가 없음
// -----------------------------------------------------------------------------

// 데모용으로 허용되는 계정 목록 (실제 서비스에서는 절대 이렇게 하지 않음! 서버 검증 필요)
const FAKE_USER_DB = [
  { username: 'ash', password: 'pikachu' },
  { username: 'trainer', password: '1234' },
]

/**
 * 가짜 로그인 API 호출
 * @param {string} username
 * @param {string} password
 * @returns {Promise<{token: string, username: string}>}
 */
export function fakeLogin(username, password) {
  return new Promise((resolve, reject) => {
    // 700ms 정도의 지연을 줘서 "서버에 요청 중"인 느낌을 살림
    setTimeout(() => {
      const found = FAKE_USER_DB.find(
        (u) => u.username === username && u.password === password
      )

      if (found) {
        // 실제 API라면 서버가 JWT 토큰을 발급해주는 상황을 흉내냄
        resolve({
          token: `fake-token-${btoa(username)}-${Date.now()}`,
          username: found.username,
        })
      } else {
        reject(new Error('아이디 또는 비밀번호가 올바르지 않습니다.'))
      }
    }, 700)
  })
}
