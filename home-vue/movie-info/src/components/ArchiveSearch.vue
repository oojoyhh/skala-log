<script setup>
import { ref } from 'vue'

// 검색어 상태
const searchText = ref('')

// 검색 이벤트
const emit = defineEmits(['search', 'reset'])

// 검색 실행
function submitSearch() {
    emit('search', searchText.value)
}

// 검색 초기화
function resetSearch() {
    searchText.value = ''
    emit('reset')
}
</script>

<template>
    <form class="archive-search" @submit.prevent="submitSearch">
        <input v-model="searchText" type="search" placeholder="분위기, 착장, 태그로 찾아보기">
        <button class="search-button" type="submit">검색</button>
        <button class="reset-button" type="button" @click="resetSearch">전체</button>
    </form>
</template>

<style scoped>
.archive-search {
    display: flex;
    gap: 8px;
    max-width: 680px;
    margin: 22px auto 30px;
    border: 1px solid rgba(177, 132, 154, 0.16);
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.78);
    padding: 8px;
    box-shadow: 0 10px 30px rgba(105, 76, 95, 0.08);
}

input {
    flex: 1;
    min-width: 0;
    border: 0;
    outline: 0;
    background: transparent;
    padding: 10px 12px;
    color: #554957;
}

button {
    border: 0;
    border-radius: 12px;
    padding: 9px 14px;
    font-weight: 700;
}

.search-button {
    background: #a36a84;
    color: white;
}

.reset-button {
    background: #f3e8ee;
    color: #846173;
}
</style>
