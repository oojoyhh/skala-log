<script setup>
import { onBeforeUnmount, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 실습 1: 회원가입 폼과 유효성 검사
const userForm = ref({
  email: '',
  agree: false,
})

const handleRegister = () => {
  if (!userForm.value.email.includes('@')) {
    ElMessage.error('❌ 올바른 이메일 형식이 아닙니다.')
    return
  }

  if (!userForm.value.agree) {
    ElMessage.warning('⚠️ 이용약관에 동의하셔야 합니다.')
    return
  }

  ElMessage.success('🎉 가입 신청이 정상적으로 완료되었습니다!')
}

// 실습 2: 상품 수량과 별점
const productQuantity = ref(1)
const productRate = ref(4)

// 실습 3: 파일 삭제 확인창과 진행률 애니메이션
const downloadProgress = ref(0)
const isDownloading = ref(false)
let downloadTimer

const confirmDelete = () => {
  ElMessageBox.confirm('서버에서 해당 파일을 영구히 삭제하시겠습니까?', '🔥 최종 경고', {
    confirmButtonText: '네, 삭제합니다',
    cancelButtonText: '취소',
    type: 'danger',
  })
    .then(() => {
      ElMessage.success('🗑️ 파일이 안전하게 파쇄되었습니다.')
    })
    .catch(() => {
      ElMessage.info('❌ 삭제 작업이 취소되었습니다.')
    })
}

const startDownload = () => {
  if (isDownloading.value) return

  isDownloading.value = true
  downloadProgress.value = 0

  // 400ms마다 20%씩 증가시켜 2초 안에 100%를 채움
  downloadTimer = window.setInterval(() => {
    downloadProgress.value = Math.min(downloadProgress.value + 20, 100)

    if (downloadProgress.value === 100) {
      window.clearInterval(downloadTimer)
      downloadTimer = undefined
      isDownloading.value = false
      ElMessage.success('💾 대용량 데이터 로드가 완료되었습니다!')
    }
  }, 400)
}

onBeforeUnmount(() => {
  if (downloadTimer) window.clearInterval(downloadTimer)
})
</script>

<template>
  <section class="element-practice" aria-labelledby="element-plus-title">
    <div class="section-heading">
      <el-tag type="primary" effect="light">과제 8 · ELEMENT PLUS</el-tag>
      <h2 id="element-plus-title">Element Plus 활용 실습</h2>
      <p>폼 검증부터 커머스 입력, 시스템 피드백까지 한 화면에서 확인해 보세요.</p>
    </div>

    <div class="practice-grid">
      <el-card class="practice-card register-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span class="card-icon" aria-hidden="true">✉️</span>
            <div>
              <strong>회원가입 Form</strong>
              <small>입력값 검증과 메시지 피드백</small>
            </div>
          </div>
        </template>

        <form class="card-content" @submit.prevent="handleRegister">
          <label class="field-label" for="register-email">이메일 주소</label>
          <el-input
            id="register-email"
            v-model.trim="userForm.email"
            type="email"
            size="large"
            placeholder="example@email.com"
            clearable
          />

          <div class="agreement-row">
            <el-switch
              v-model="userForm.agree"
              aria-label="이용약관 동의"
              inline-prompt
              active-text="동의"
              inactive-text="미동의"
            />
            <span>개인정보 수집 및 필수 이용약관에 동의합니다.</span>
          </div>

          <el-button type="success" size="large" native-type="submit">
            회원가입 신청
          </el-button>
        </form>
      </el-card>

      <el-card class="practice-card product-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span class="card-icon" aria-hidden="true">🛍️</span>
            <div>
              <strong>상품 옵션</strong>
              <small>수량 및 만족도 반응형 데이터</small>
            </div>
          </div>
        </template>

        <div class="card-content">
          <div class="option-row">
            <div>
              <span class="field-label">구매 수량</span>
              <small>한 번에 최대 10개까지 구매 가능</small>
            </div>
            <el-input-number v-model="productQuantity" :min="1" :max="10" />
          </div>

          <div class="option-row rate-row">
            <div>
              <span class="field-label">상품 만족도</span>
              <small>별점을 선택해 주세요</small>
            </div>
            <el-rate v-model="productRate" show-score score-template="{value}점" />
          </div>

          <div class="summary-box" aria-live="polite">
            <span>실시간 선택 요약</span>
            <strong>{{ productQuantity }}개 · {{ productRate }}점</strong>
          </div>
        </div>
      </el-card>

      <el-card class="practice-card feedback-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span class="card-icon" aria-hidden="true">⚙️</span>
            <div>
              <strong>시스템 피드백</strong>
              <small>확인창과 진행률 애니메이션</small>
            </div>
          </div>
        </template>

        <div class="card-content">
          <div class="action-row">
            <el-button type="danger" plain size="large" @click="confirmDelete">
              파일 삭제 테스트
            </el-button>
            <el-button
              type="primary"
              size="large"
              :loading="isDownloading"
              :disabled="isDownloading"
              @click="startDownload"
            >
              {{ isDownloading ? '동기화 중...' : '동기화 시작' }}
            </el-button>
          </div>

          <div class="progress-panel" aria-live="polite">
            <div class="progress-label">
              <span>데이터 동기화</span>
              <strong>{{ downloadProgress }}%</strong>
            </div>
            <el-progress
              :percentage="downloadProgress"
              :stroke-width="12"
              :show-text="false"
              :status="downloadProgress === 100 ? 'success' : undefined"
              striped
              :striped-flow="isDownloading"
            />
          </div>
        </div>
      </el-card>
    </div>
  </section>
</template>

<style scoped>
.element-practice {
  --practice-ink: #182230;
  --practice-muted: #667085;
  padding: clamp(1.25rem, 3vw, 2.25rem);
  border: 1px solid #e7eaf0;
  border-radius: 20px;
  color: var(--practice-ink);
  background:
    radial-gradient(circle at 0 0, rgb(64 158 255 / 10%), transparent 34%),
    #f8fafc;
}

.section-heading {
  margin-bottom: 1.5rem;
}

.section-heading h2 {
  padding: 0;
  margin: 0.55rem 0 0;
  border: 0;
  color: var(--practice-ink);
  font-size: clamp(1.55rem, 3vw, 2rem);
  font-weight: 800;
}

.section-heading p {
  margin: 0.4rem 0 0;
  color: var(--practice-muted);
}

.practice-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.practice-card {
  border: 1px solid #e5e9f0;
  border-radius: 14px;
}

.feedback-card {
  grid-column: 1 / -1;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.card-icon {
  display: grid;
  flex: 0 0 2.5rem;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 10px;
  background: #ecf5ff;
  place-items: center;
}

.card-header strong,
.card-header small {
  display: block;
}

.card-header strong {
  font-size: 1rem;
  font-weight: 750;
}

.card-header small,
.option-row small {
  margin-top: 0.1rem;
  color: var(--practice-muted);
  font-size: 0.78rem;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.field-label {
  display: block;
  color: #344054;
  font-size: 0.86rem;
  font-weight: 700;
}

.agreement-row {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  color: #475467;
  font-size: 0.84rem;
}

.option-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  min-height: 3.25rem;
}

.option-row > div:first-child,
.summary-box span {
  display: flex;
  flex-direction: column;
}

.rate-row {
  padding-top: 1rem;
  border-top: 1px solid #eef0f4;
}

.summary-box,
.progress-panel {
  padding: 0.9rem 1rem;
  border: 1px solid #d9ecff;
  border-radius: 9px;
  background: #ecf5ff;
}

.summary-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #606266;
  font-size: 0.82rem;
}

.summary-box > span,
.progress-label > span {
  color: #409eff;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.06em;
}

.summary-box strong,
.progress-label strong {
  color: #337ecc;
  font-weight: 750;
}

.action-row {
  display: flex;
  gap: 0.75rem;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.6rem;
  color: #475467;
  font-size: 0.84rem;
}

@media (max-width: 720px) {
  .practice-grid {
    grid-template-columns: 1fr;
  }

  .feedback-card {
    grid-column: auto;
  }

  .option-row,
  .summary-box {
    align-items: flex-start;
    flex-direction: column;
  }

  .action-row {
    flex-direction: column;
  }

  .action-row :deep(.el-button) {
    width: 100%;
    margin-left: 0;
  }
}
</style>
