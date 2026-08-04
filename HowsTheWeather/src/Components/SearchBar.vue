<script setup>
// 상위로 입력 텍스트를 전달할 커스텀 이벤트 등록
defineEmits(['update-query'])

// 상위로부터 현재 검색 상태 값을 수신
defineProps({
  currentQuery: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <div class="search-inner">
    <h3>🔍 도시 검색</h3>
    <input
      type="text"
      :value="currentQuery"
      placeholder="검색할 도시 이름 입력"
      @input="$emit('update-query', $event.target.value)"
    />
    <p>
      검색 중인 도시: <strong>{{ currentQuery }}</strong>
    </p>
  </div>
</template>
