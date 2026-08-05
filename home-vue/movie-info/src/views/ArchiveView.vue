<script setup>
import { ref } from 'vue'
import archivePhotoData from '@/data/archivePhotos.js'
import ArchiveSearch from '@/components/ArchiveSearch.vue'
import PhotoGallery from '@/components/PhotoGallery.vue'
import PhotoDetailModal from '@/components/PhotoDetailModal.vue'

// 전체 사진
const archivePhotos = ref(archivePhotoData.map((photo) => ({ ...photo })))

// 화면 사진
const visiblePhotos = ref([...archivePhotos.value])

// 모달 상태
const selectedPhoto = ref(null)

// 하트 증가
function addFavorite(id) {
    const photo = archivePhotos.value.find((item) => item.id === id)
    if (photo) photo.favoriteCount += 1
}

// 사진 검색
function searchPhotos(keyword) {
    const searchText = keyword.trim().toLowerCase()

    if (!searchText) {
        resetPhotos()
        return
    }

    visiblePhotos.value = archivePhotos.value.filter((photo) => {
        const searchableText = [
            photo.title,
            photo.mood,
            photo.outfit,
            photo.note,
            ...photo.tags
        ].join(' ').toLowerCase()

        return searchableText.includes(searchText)
    })
}

// 전체 사진 표시
function resetPhotos() {
    visiblePhotos.value = [...archivePhotos.value]
}

// 상세 모달 열기
function selectPhoto(id) {
    selectedPhoto.value = archivePhotos.value.find((photo) => photo.id === id) ?? null
}

// 상세 모달 닫기
function closePhotoModal() {
    selectedPhoto.value = null
}
</script>

<template>
    <main class="archive-page">
        <header class="page-header">
            <p class="eyebrow">MY FAVORITE ARCHIVE</p>
            <h1>좋아하는 순간 보관함 ♡</h1>
            <p>보고 싶을 때마다 꺼내 보는 최애의 순간들</p>
        </header>

        <ArchiveSearch @search="searchPhotos" @reset="resetPhotos" />
        <PhotoGallery
            :photos="visiblePhotos"
            @favorite="addFavorite"
            @select="selectPhoto"
        />

        <PhotoDetailModal
            v-if="selectedPhoto"
            :photo="selectedPhoto"
            @close="closePhotoModal"
        />
    </main>
</template>

<style scoped>
.archive-page {
    padding: 20px 0 48px;
}

.page-header {
    margin: 28px 0 10px;
    text-align: center;
}

.eyebrow {
    margin: 0;
    color: #a66a85;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.18em;
}

h1 {
    margin: 8px 0;
    color: #3e3444;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: clamp(2rem, 5vw, 3.4rem);
    font-weight: 600;
}

.page-header > p:last-child {
    margin: 0;
    color: #84768b;
}
</style>
