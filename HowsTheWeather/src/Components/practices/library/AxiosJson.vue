<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

// 1. 백엔드 공용 주소
const BASE_URL = 'https://jsonplaceholder.typicode.com/posts'

// 2. 반응형 상태 데이터
const items = ref([])
const textInput = ref('')

// [READ] GET: 데이터 가져오기
const handleRead = async () => {
  try {
    const response = await axios.get(BASE_URL, { params: { _limit: 3 } })
    items.value = response.data
    console.log('GET 성공:', response.data)
  } catch (error) {
    console.error('GET 실패:', error)
  }
}

// [CREATE] POST: 데이터 추가하기
const handleCreate = async () => {
  if (!textInput.value.trim()) return

  try {
    const payload = {
      title: textInput.value,
      body: '샘플 내용',
      userId: 1,
    }

    const response = await axios.post(BASE_URL, payload)
    console.log('POST 성공:', response.data)

    items.value.unshift(response.data)
    textInput.value = ''
  } catch (error) {
    console.error('POST 실패:', error)
  }
}

// [UPDATE] PUT: 특정 데이터 수정하기
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
  } catch (error) {
    console.error('PUT 실패:', error)
  }
}

// [DELETE] DELETE: 특정 데이터 삭제하기
const handleDelete = async (id) => {
  try {
    const response = await axios.delete(`${BASE_URL}/${id}`)
    console.log('DELETE 성공. 상태 코드:', response.status)

    items.value = items.value.filter((item) => item.id !== id)
  } catch (error) {
    console.error('DELETE 실패:', error)
  }
}

// 컴포넌트가 켜지면 자동으로 GET 호출
onMounted(() => {
  handleRead()
})
</script>

<template>
  <div class="practice-section">
    <h2>⚡ Axios CRUD 프로토타입 훈련</h2>

    <div class="input-zone">
      <input v-model="textInput" placeholder="저장할 텍스트를 입력하세요" />
      <button class="btn-post" @click="handleCreate">POST (추가)</button>
    </div>

    <ul class="item-list">
      <li v-for="item in items" :key="item.id" class="item-card">
        <div class="content">
          <span class="id-tag">ID: {{ item.id }}</span>
          <p class="title-text">{{ item.title }}</p>
        </div>

        <div class="btn-group">
          <button class="btn-put" @click="handleUpdate(item.id)">PUT (수정)</button>
          <button class="btn-delete" @click="handleDelete(item.id)">DEL (삭제)</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.input-zone {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
}

button {
  padding: 8px 14px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: bold;
  cursor: pointer;
}

.btn-post {
  color: white;
  background: #22c55e;
}

.item-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 0;
  margin: 0;
  list-style: none;
}

.item-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #f8fafc;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding-right: 15px;
}

.id-tag {
  color: #64748b;
  font-size: 11px;
  font-weight: bold;
}

.title-text {
  margin: 0;
  color: #334155;
  font-size: 14px;
  text-transform: capitalize;
}

.btn-group {
  display: flex;
  gap: 4px;
}

.btn-put {
  color: white;
  background: #eab308;
}

.btn-delete {
  color: white;
  background: #ef4444;
}

button:hover {
  opacity: 0.9;
}
</style>
