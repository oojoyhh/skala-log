<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

// 배너 문구
const props = defineProps({
    messages: {
        type: Array,
        required: true
    }
})

// 배너 상태
const isVisible = ref(true)
const messageIndex = ref(0)
let timerId

// 현재 문구
const currentMessage = computed(() => props.messages[messageIndex.value] ?? '')

// 문구 자동 순환
onMounted(() => {
    timerId = setInterval(() => {
        messageIndex.value = (messageIndex.value + 1) % props.messages.length
    }, 3000)
})

// 타이머 정리
onUnmounted(() => clearInterval(timerId))
</script>

<template>
    <div v-if="isVisible" class="banner">
        <p>{{ currentMessage }}</p>
        <button type="button" aria-label="배너 닫기" @click="isVisible = false">×</button>
    </div>
</template>

<style scoped>
.banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 14px;
    border-radius: 16px;
    background: linear-gradient(135deg, #d99db7, #a999d2);
    color: white;
    padding: 11px 16px;
    box-shadow: 0 10px 26px rgba(156, 109, 139, 0.14);
}

.banner p {
    margin: 0;
    font-size: 0.875rem;
}

.banner button {
    border: 0;
    background: transparent;
    color: white;
    font-size: 1.2rem;
}
</style>
