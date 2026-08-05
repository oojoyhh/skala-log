<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const BASE_URL = 'https://jsonplaceholder.typicode.com/posts'

const items = ref([])
const textInput = ref('')
const isLoading = ref(false)
const lastResult = ref('버튼을 눌러 GET/POST/PUT/DELETE 결과를 확인하세요.')

const handleRead = async () => {
  isLoading.value = true

  try {
    const response = await axios.get(BASE_URL, { params: { _limit: 3 } })
    items.value = response.data
    console.log('GET 성공:', response.data)
    lastResult.value = `GET 성공 · ${response.data.length}건 불러옴`
  } catch (error) {
    console.error('GET 실패:', error)
    ElMessage.error('목록을 불러오지 못했습니다.')
    lastResult.value = 'GET 실패 · 목록을 불러오지 못했습니다.'
  } finally {
    isLoading.value = false
  }
}

const handleCreate = async () => {
  if (!textInput.value.trim()) {
    ElMessage.warning('저장할 텍스트를 입력하세요.')
    return
  }

  try {
    const payload = {
      title: textInput.value,
      body: '샘플 내용',
      userId: 1,
    }

    const response = await axios.post(BASE_URL, payload)
    console.log('POST 성공:', response.data)

    items.value.unshift(response.data)
    lastResult.value = `POST 성공 · "${textInput.value}" 추가됨 (id ${response.data.id})`
    textInput.value = ''
    ElMessage.success('새 데이터가 추가되었습니다.')
  } catch (error) {
    console.error('POST 실패:', error)
    ElMessage.error('데이터 추가에 실패했습니다.')
    lastResult.value = 'POST 실패 · 데이터 추가에 실패했습니다.'
  }
}

const handleUpdate = async (id) => {
  try {
    const editPayload = {
      title: '✨ 변조된 타이틀 데이터',
      body: '수정 완료',
      userId: 1,
    }

    const response = await axios.put(`${BASE_URL}/${id}`, editPayload)
    console.log('PUT 성공:', response.data)

    const index = items.value.findIndex((item) => item.id === id)

    if (index !== -1) {
      items.value[index] = response.data
    }

    lastResult.value = `PUT 성공 · id ${id} 데이터 수정 완료`
    ElMessage.success('데이터가 수정되었습니다.')
  } catch (error) {
    console.error('PUT 실패:', error)
    ElMessage.error('데이터 수정에 실패했습니다.')
    lastResult.value = 'PUT 실패 · 데이터 수정에 실패했습니다.'
  }
}

const handleDelete = async (id) => {
  try {
    const response = await axios.delete(`${BASE_URL}/${id}`)
    console.log('DELETE 성공. 상태 코드:', response.status)

    items.value = items.value.filter((item) => item.id !== id)
    lastResult.value = `DELETE 성공 · id ${id} 삭제 완료 (상태 코드 ${response.status})`
    ElMessage.success('데이터가 삭제되었습니다.')
  } catch (error) {
    console.error('DELETE 실패:', error)
    ElMessage.error('데이터 삭제에 실패했습니다.')
    lastResult.value = 'DELETE 실패 · 데이터 삭제에 실패했습니다.'
  }
}

onMounted(() => {
  handleRead()
})
</script>

<template>
  <section class="library-practice" aria-labelledby="axios-crud-title">
    <div class="section-heading">
      <el-tag type="primary" effect="light">과제 7 · AXIOS CRUD</el-tag>
      <h2 id="axios-crud-title">CRUD 프로토타입 훈련</h2>
      <p>GET, POST, PUT, DELETE 요청 결과를 화면 데이터와 동기화합니다.</p>
    </div>

    <el-card class="practice-card" shadow="hover" v-loading="isLoading">
      <template #header>
        <strong>JSONPlaceholder 데이터 관리</strong>
      </template>

      <div class="result-panel" aria-live="polite">
        <span>RESULT</span>
        <code>{{ lastResult }}</code>
      </div>

      <div class="input-zone">
        <el-input
          v-model.trim="textInput"
          size="large"
          placeholder="저장할 텍스트를 입력하세요"
          clearable
          @keyup.enter="handleCreate"
        />
        <el-button type="primary" size="large" @click="handleCreate">POST 추가</el-button>
      </div>

      <div v-if="items.length" class="item-list">
        <el-card v-for="item in items" :key="item.id" class="item-card" shadow="never">
          <div class="item-row">
            <div class="item-content">
              <el-tag size="small" effect="plain">ID {{ item.id }}</el-tag>
              <p>{{ item.title }}</p>
            </div>

            <div class="action-group">
              <el-button type="warning" plain @click="handleUpdate(item.id)">PUT 수정</el-button>
              <el-button type="danger" plain @click="handleDelete(item.id)">DEL 삭제</el-button>
            </div>
          </div>
        </el-card>
      </div>

      <el-empty v-else description="표시할 데이터가 없습니다." :image-size="90" />
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

.result-panel {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: start;
  gap: 12px;
  padding: 0.9rem 1rem;
  margin-bottom: 1rem;
  border: 1px solid #d9ecff;
  border-radius: 9px;
  color: #337ecc;
  background: #ecf5ff;
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

.input-zone {
  display: flex;
  gap: 10px;
  margin-bottom: 1rem;
}

.item-list {
  display: grid;
  gap: 10px;
}

.item-card {
  border-color: #ebeef5;
  background: #fafafa;
}

.item-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.item-content {
  min-width: 0;
}

.item-content p {
  margin: 0.45rem 0 0;
  overflow: hidden;
  color: #606266;
  font-size: 0.9rem;
  text-overflow: ellipsis;
  text-transform: capitalize;
  white-space: nowrap;
}

.action-group {
  display: flex;
  flex: 0 0 auto;
  gap: 8px;
}

@media (max-width: 640px) {
  .result-panel {
    grid-template-columns: 1fr;
  }

  .input-zone,
  .item-row,
  .action-group {
    align-items: stretch;
    flex-direction: column;
  }

  .action-group :deep(.el-button) {
    width: 100%;
    margin-left: 0;
  }
}
</style>
