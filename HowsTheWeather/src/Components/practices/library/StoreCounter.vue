<script setup>
import { useCounterStore } from '@/stores/counter.js'

const counterStore = useCounterStore()
</script>

<template>
  <section class="library-practice" aria-labelledby="store-practice-title">
    <div class="section-heading">
      <el-tag type="primary" effect="light">과제 6 · PINIA STORE</el-tag>
      <h2 id="store-practice-title">Counter Store 활용 실습</h2>
      <p>State, Getters, Actions의 반응형 흐름을 확인합니다.</p>
    </div>

    <el-card class="practice-card" shadow="hover">
      <template #header>
        <strong>전역 상태 대시보드</strong>
      </template>

      <div class="metric-grid">
        <div class="metric-box">
          <span>STATE · 원본 카운트</span>
          <strong>{{ counterStore.count }}</strong>
        </div>
        <div class="metric-box">
          <span>GETTERS · 2배 연산</span>
          <strong>{{ counterStore.doubleCount }}</strong>
        </div>
      </div>

      <el-button type="primary" size="large" @click="counterStore.increment">
        Actions로 숫자 1 증가
      </el-button>
    </el-card>
  </section>
</template>

<style scoped>
.library-practice {
  padding: clamp(1.25rem, 3vw, 2.25rem);
  border: 1px solid #e7eaf0;
  border-radius: 20px;
  background:
    radial-gradient(circle at 0 0, rgb(64 158 255 / 10%), transparent 34%),
    #f8fafc;
}

.section-heading {
  margin-bottom: 1.5rem;
}

.section-heading h2 {
  margin: 0.55rem 0 0;
  color: #182230;
  font-size: clamp(1.55rem, 3vw, 2rem);
  font-weight: 800;
}

.section-heading p {
  margin: 0.4rem 0 0;
  color: #667085;
}

.practice-card {
  border-radius: 12px;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 1rem;
}

.metric-box {
  padding: 1.15rem;
  border: 1px solid #d9ecff;
  border-radius: 9px;
  background: #ecf5ff;
}

.metric-box span,
.metric-box strong {
  display: block;
}

.metric-box span {
  color: #409eff;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.06em;
}

.metric-box strong {
  margin-top: 0.35rem;
  color: #337ecc;
  font-size: 1.75rem;
  font-weight: 800;
}

@media (max-width: 560px) {
  .metric-grid {
    grid-template-columns: 1fr;
  }
}
</style>
