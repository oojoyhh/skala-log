<script setup>
// 사진 목록
defineProps({
    photos: {
        type: Array,
        required: true
    }
})

// 사진 선택 이벤트
const emit = defineEmits(['favorite', 'select'])
</script>

<template>
    <section class="photo-grid">
        <article v-for="photo in photos" :key="photo.id" class="photo-card">
            <figure>
                <img :src="photo.imageUrl" :alt="photo.title">
                <button class="heart" type="button" @click="emit('favorite', photo.id)">
                    ♡ <span>{{ photo.favoriteCount }}</span>
                </button>
            </figure>

            <div class="photo-info">
                <h2>{{ photo.title }}</h2>
                <p class="mood">{{ photo.mood }}</p>

                <dl>
                    <div>
                        <dt>착장</dt>
                        <dd>{{ photo.outfit }}</dd>
                    </div>
                    <div>
                        <dt>한줄 메모</dt>
                        <dd>{{ photo.note }}</dd>
                    </div>
                </dl>

                <div class="tags">
                    <span v-for="tag in photo.tags" :key="tag">{{ tag }}</span>
                </div>

                <button class="detail-button" type="button" @click="emit('select', photo.id)">
                    사진 자세히 보기
                </button>
            </div>
        </article>

        <p v-if="photos.length === 0" class="empty">찾는 최애 사진이 없어요 🥺</p>
    </section>
</template>

<style scoped>
.photo-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 22px;
}

.photo-card {
    overflow: hidden;
    border: 1px solid rgba(170, 123, 145, 0.15);
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.84);
    box-shadow: 0 14px 38px rgba(115, 82, 104, 0.11);
    transition: transform 180ms ease, box-shadow 180ms ease;
}

.photo-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 44px rgba(115, 82, 104, 0.17);
}

figure {
    position: relative;
    margin: 0;
    background: #f3e8eb;
}

img {
    display: block;
    width: 100%;
    aspect-ratio: 4 / 5;
    object-fit: cover;
}

.photo-info {
    padding: 20px;
}

h2 {
    margin: 0 0 6px;
    color: #3f3544;
    font-size: 1.28rem;
}

.mood {
    margin: 0 0 16px;
    color: #a36a84;
    font-size: 0.88rem;
    font-weight: 700;
}

dl {
    margin: 0;
}

dl div {
    margin-bottom: 10px;
}

dt {
    margin-bottom: 2px;
    color: #a393a8;
    font-size: 0.72rem;
    font-weight: 700;
}

dd {
    margin: 0;
    color: #574d5c;
    font-size: 0.9rem;
    line-height: 1.55;
}

.tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin: 15px 0;
}

.tags span {
    border-radius: 999px;
    background: #f7edf2;
    color: #96667c;
    padding: 5px 9px;
    font-size: 0.72rem;
}

.heart {
    position: absolute;
    right: 12px;
    bottom: 12px;
    border: 1px solid rgba(255, 255, 255, 0.7);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.9);
    color: #d45f8c;
    padding: 8px 12px;
    box-shadow: 0 6px 18px rgba(72, 48, 62, 0.14);
    backdrop-filter: blur(8px);
}

.detail-button {
    width: 100%;
    border: 0;
    border-radius: 14px;
    background: linear-gradient(135deg, #e9a8bd, #b9a8df);
    color: white;
    padding: 11px 14px;
    font-weight: 700;
}

.empty {
    grid-column: 1 / -1;
    text-align: center;
}

@media (max-width: 880px) {
    .photo-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 580px) {
    .photo-grid {
        grid-template-columns: 1fr;
    }
}
</style>
