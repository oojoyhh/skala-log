<script setup>
// 선택 사진
defineProps({
    photo: {
        type: Object,
        required: true
    }
})

// 닫기 이벤트
const emit = defineEmits(['close'])
</script>

<template>
    <div class="modal" @click.self="emit('close')">
        <div class="modal-content">
            <p class="label">FAVORITE PHOTO</p>
            <h2>{{ photo.title }}</h2>
            <img :src="photo.imageUrl" :alt="photo.title">
            <p class="mood">{{ photo.mood }}</p>
            <p><strong>착장</strong> {{ photo.outfit }}</p>
            <p><strong>메모</strong> {{ photo.note }}</p>
            <button type="button" @click="emit('close')">닫기</button>
        </div>
    </div>
</template>

<style scoped>
.modal {
    position: fixed;
    inset: 0;
    z-index: 30;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    background: rgba(62, 43, 57, 0.58);
    backdrop-filter: blur(8px);
}

.modal-content {
    width: min(92%, 480px);
    max-height: 90vh;
    overflow-y: auto;
    border: 1px solid rgba(255, 255, 255, 0.7);
    border-radius: 26px;
    background: #fffafc;
    padding: 24px;
    box-shadow: 0 24px 70px rgba(44, 25, 38, 0.28);
}

.label {
    margin: 0;
    color: #ad748d;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.15em;
}

h2 {
    margin: 6px 0 16px;
}

img {
    display: block;
    width: 100%;
    max-height: 430px;
    border-radius: 18px;
    object-fit: cover;
}

.mood {
    color: #a56883;
    font-weight: 700;
}

strong {
    display: inline-block;
    min-width: 48px;
    color: #8f7182;
}

button {
    width: 100%;
    margin-top: 12px;
    border: 0;
    border-radius: 14px;
    background: #4b404d;
    color: white;
    padding: 11px;
}
</style>
