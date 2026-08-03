<script setup>
// 부모가 관리하는 현재 검색어를 읽는다.
const props = defineProps({
  query: {
    type: String,
    required: true,
  },
})

// 입력값을 부모에게 전달할 이벤트
const emit = defineEmits(['update-query'])

// 입력할 때마다 새 검색어를 부모에게 보낸다.
const handleInput = (event) => {
  emit('update-query', event.target.value)
}
</script>

<template>
  <div class="search-bar">
    <!-- props로 표시하고 input 이벤트로 변경값을 올려보낸다. -->
    <input
      type="text"
      placeholder="검색할 도시 이름 입력"
      :value="props.query"
      @input="handleInput"
    />
    <p>검색 중인 도시: <strong>{{ props.query }}</strong></p>
  </div>
</template>

<style scoped>
/* 검색 입력창 기본 디자인 */
.search-bar input {
  width: 100%;
  height: 44px;
  padding: 0 12px;
  border: 1px solid #9ba7b3;
  border-radius: 4px;
  color: #24364b;
  background: #fff;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

/* 입력창을 선택했을 때 강조한다. */
.search-bar input:focus {
  border-color: #438fd1;
  box-shadow: 0 0 0 3px rgb(67 143 209 / 18%);
}

.search-bar input::placeholder {
  color: #8b98a7;
}

/* 현재 검색어 표시 영역 */
.search-bar p {
  min-height: 24px;
  margin: 8px 0 0;
  font-size: 17px;
}
</style>
