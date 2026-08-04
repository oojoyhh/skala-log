# PokéDe

Vue 3 + Vite + Vue Router + Pinia로 만든 로그인 후 포켓몬 도감 보기 앱입니다.

## 구성

- **로그인**: 실제 서버가 없어 `src/api/fakeAuth.js`에서 지연시간(setTimeout)을 흉내낸 **Fake API**로 처리합니다.
  - 데모 계정: `ash` / `pikachu` 또는 `trainer` / `1234`
- **포켓몬 도감**: `src/api/pokeApi.js`에서 실제 [PokeAPI](https://pokeapi.co/api/v2/pokemon/)를 **axios**로 호출합니다 (`src/api/httpClient.js`에 baseURL/timeout/에러 처리를 설정한 axios 인스턴스가 있습니다).
  - 목록: `GET /pokemon?limit=20&offset=0`
  - 상세: `GET /pokemon/{id 또는 이름}` (예: `GET /pokemon/ditto`)
  - 검색창에 `ditto` 처럼 이름/번호를 입력하면 바로 상세 조회로 이동합니다.

## 실행 방법

```bash
npm install
npm run dev
```

브라우저에서 `http://localhost:5173` 접속 → 로그인 → 도감 확인.

## 폴더 구조 (비즈니스 로직 / UI 분리)

API 호출·상태·재조회 같은 **비즈니스 로직**은 `composables/`와 `stores/`에만 있고,
`views/`·`components/`는 그 결과를 받아 그리기만 하는 **순수 UI**로 분리했습니다.

```
src/
  main.js              앱 진입점 (Pinia, Router 연결)
  App.vue              공통 헤더 + 라우터 뷰

  router/index.js      경로 정의 + 로그인 여부 가드

  # ── 비즈니스 로직 계층 ──────────────────────────
  stores/auth.js               Pinia 인증 스토어 (로그인 상태, localStorage 유지)
  composables/
    usePokemonList.js          도감 목록 조회 + 페이지네이션 로직
    usePokemonDetail.js        포켓몬 상세 조회 + 재조회(watch) + 울음소리 재생
    useDexSearch.js            검색어 검증 + 상세 페이지 이동 로직
  api/
    httpClient.js               PokeAPI용 axios 인스턴스 (baseURL, timeout, 공통 에러 처리)
    fakeAuth.js                가짜 로그인 API (지연시간 흉내)
    pokeApi.js                 PokeAPI 실제 호출 함수 (axios 사용)
  utils/typeColors.js          포켓몬 타입별 색상 매핑

  # ── UI 계층 (컴포넌트) ──────────────────────────
  views/
    LoginView.vue               로그인 화면 (auth 스토어의 login()만 호출)
    PokedexView.vue             도감 목록 (usePokemonList/useDexSearch 결과만 렌더링)
    PokemonDetailView.vue       포켓몬 상세 (usePokemonDetail 결과만 렌더링)
  components/
    PokemonCard.vue             목록 카드
    LoadingSpinner.vue          로딩 표시
    icons/                      SVG 아이콘 (Warning, Speaker, ChevronLeft/Right, Search)
```

예를 들어 `PokedexView.vue`는 더 이상 `fetch`를 직접 호출하지 않고, `usePokemonList()`가 반환하는
`pokemonList`, `isLoading`, `goNext()` 같은 값/함수만 템플릿에 연결합니다. 덕분에 같은 로직을
다른 화면에서도 재사용할 수 있고, 컴포넌트를 마운트하지 않고도 로직만 따로 테스트할 수 있습니다.

각 파일 상단과 주요 로직마다 한글 주석으로 동작을 설명해두었습니다.
