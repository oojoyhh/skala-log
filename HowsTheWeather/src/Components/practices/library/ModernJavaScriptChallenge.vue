<script setup>
import { ref } from 'vue'

// 실시간 화면 출력을 위한 Vue 상태값 (수정 금지)
const result1 = ref('')
const result2 = ref('')
const result3 = ref('')


// [과제 1] 회원 명단 가공 및 VIP 추출 핸들러
const runTask1 = () => {
  const members = ['김수원', '이서울', '박부산', '최대전']
  const rawData = { id: 101, grade: 'VIP', details: { score: 95 } }

  const memberContainsPark = members.includes('박부산')
  const {
    grade,
    details: { score },
  } = rawData

  result1.value = `부산 포함 여부: ${memberContainsPark} / 등급: ${grade} / 점수: ${score}점`
}

// [과제 2] 장바구니 상품 추가 및 기본값 방어 시스템
const runTask2 = () => {
  const currentCart = ['Apple', 'Banana']
  const newProduct = { name: 'Orange', stock: 0, preview: null }

  const updatedCart = [...currentCart, newProduct.name]
  const imgStatus = newProduct?.preview ?? '이미지 준비중'
  const finalStock = newProduct.stock ?? 10

  result2.value = `카트: ${updatedCart} / 이미지: ${imgStatus} / 수량: ${finalStock}개`
}


// [과제 3] 서버 연쇄 데이터 요청 및 에러 통합 제어 (Async/Await)
// 가상의 백엔드 API (수정 금지 - Promise 반환형 화살표 함수)
const fetchUserId = () => new Promise((res) => setTimeout(() => res({ uid: 777 }), 400))
const fetchUserProfile = (uid) =>
  new Promise((res) => setTimeout(() => res({ uid, nick: 'Graves' }), 400))

const runTask3 = async () => {
  result3.value = '⏳ 데이터 동기화 중...'

  try {
    const { uid } = await fetchUserId()
    const { nick } = await fetchUserProfile(uid)

    result3.value = `동기화 성공: ${nick}님 환영합니다.`
  } catch {
    result3.value = '통신 실패'
  }
}
</script>

<template>
  <section class="modern-challenge" aria-labelledby="modern-javascript-title">
    <header class="challenge-heading">
      <el-tag type="primary" effect="light">과제 9 · MODERN JAVASCRIPT</el-tag>
      <h2 id="modern-javascript-title">Modern JavaScript</h2>
      <p>ES6+ 문법으로 데이터를 가공하고 비동기 작업을 순서대로 처리합니다.</p>
    </header>

    <div class="challenge-list">
      <el-card class="challenge-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="task-meta">
              <el-tag type="primary" effect="plain">과제 1</el-tag>
              <div>
                <strong>데이터 추출 및 포맷팅</strong>
                <small>includes · 구조 분해 할당 · 템플릿 리터럴</small>
              </div>
            </div>
            <el-button type="primary" @click="runTask1">과제 1 가동</el-button>
          </div>
        </template>

        <div class="result-panel" aria-live="polite">
          <span>RESULT 1</span>
          <code>{{ result1 || '버튼을 눌러 결과를 확인하세요.' }}</code>
        </div>
      </el-card>

      <el-card class="challenge-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="task-meta">
              <el-tag type="primary" effect="plain">과제 2</el-tag>
              <div>
                <strong>불변성 복사 및 데이터 방어</strong>
                <small>스프레드 · 옵셔널 체이닝 · 널 병합 연산자</small>
              </div>
            </div>
            <el-button type="primary" @click="runTask2">과제 2 가동</el-button>
          </div>
        </template>

        <div class="result-panel" aria-live="polite">
          <span>RESULT 2</span>
          <code>{{ result2 || '버튼을 눌러 결과를 확인하세요.' }}</code>
        </div>
      </el-card>

      <el-card class="challenge-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="task-meta">
              <el-tag type="primary" effect="plain">과제 3</el-tag>
              <div>
                <strong>비동기 연쇄 파이프라인</strong>
                <small>Promise · Async/Await · Try/Catch</small>
              </div>
            </div>
            <el-button type="primary" @click="runTask3">과제 3 가동</el-button>
          </div>
        </template>

        <div class="result-panel" aria-live="polite">
          <span>RESULT 3</span>
          <code>{{ result3 || '버튼을 눌러 결과를 확인하세요.' }}</code>
        </div>
      </el-card>
    </div>
  </section>
</template>

<style scoped>
.modern-challenge {
  padding: clamp(1.25rem, 3vw, 2rem);
  border: 1px solid #e4e7ed;
  border-radius: 18px;
  color: #303133;
  background:
    radial-gradient(circle at 0 0, rgb(64 158 255 / 9%), transparent 34%),
    #f8fafc;
}

.challenge-heading {
  margin-bottom: 1.25rem;
}

.challenge-heading h2 {
  margin: 0.55rem 0 0;
  color: #303133;
  font-size: clamp(1.45rem, 3vw, 1.85rem);
  font-weight: 750;
}

.challenge-heading p {
  margin: 0.35rem 0 0;
  color: #909399;
}

.challenge-list {
  display: grid;
  gap: 12px;
}

.challenge-card {
  border-radius: 12px;
}

.card-header,
.task-meta {
  display: flex;
  align-items: center;
}

.card-header {
  justify-content: space-between;
  gap: 1rem;
}

.task-meta {
  min-width: 0;
  gap: 12px;
}

.task-meta strong,
.task-meta small {
  display: block;
}

.task-meta strong {
  color: #303133;
  font-weight: 700;
}

.task-meta small {
  margin-top: 3px;
  color: #909399;
  font-size: 0.78rem;
}

.result-panel {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 12px;
  padding: 0.9rem 1rem;
  border: 1px solid #d9ecff;
  border-radius: 9px;
  color: #337ecc;
  background: #ecf5ff;
  align-items: start;
}

.result-panel span {
  color: #409eff;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.06em;
}

.result-panel code {
  min-width: 0;
  color: #606266;
  font-size: 0.82rem;
  overflow-wrap: anywhere;
}

@media (max-width: 640px) {
  .card-header,
  .task-meta {
    align-items: stretch;
    flex-direction: column;
  }

  .card-header :deep(.el-button) {
    width: 100%;
    margin-left: 0;
  }

  .result-panel {
    grid-template-columns: 1fr;
  }
}
</style>
