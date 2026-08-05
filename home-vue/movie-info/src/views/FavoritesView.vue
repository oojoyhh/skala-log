<script setup>
import { favoriteProfile } from '@/data/profile.js'
import archivePhotos from '@/data/archivePhotos.js'

// 대표 사진
const featuredPhoto = archivePhotos[0]

// 미니 사진 목록
const favoriteMoments = archivePhotos.slice(1)
</script>

<template>
    <main class="favorites-page">
        <section class="favorite-hero">
            <div class="hero-copy">
                <p class="eyebrow">MY ONE & ONLY</p>
                <span class="symbol">{{ favoriteProfile.symbol }}</span>
                <h1>{{ favoriteProfile.name }}</h1>
                <p class="korean-name">{{ favoriteProfile.koreanName }} · {{ favoriteProfile.group }}</p>
                <p class="tagline">{{ favoriteProfile.tagline }}</p>
                <p class="introduction">{{ favoriteProfile.introduction }}</p>
                <RouterLink class="archive-link" to="/archive">사진 보러 가기 →</RouterLink>
            </div>

            <figure class="hero-photo">
                <img :src="featuredPhoto.imageUrl" :alt="featuredPhoto.title">
                <figcaption>favorite no. 01</figcaption>
            </figure>
        </section>

        <section class="charms-section">
            <p class="eyebrow">WHY I LOVE</p>
            <h2>내가 좋아하는 이유</h2>

            <div class="charms-grid">
                <article v-for="charm in favoriteProfile.charms" :key="charm.title">
                    <span>{{ charm.icon }}</span>
                    <h3>{{ charm.title }}</h3>
                    <p>{{ charm.text }}</p>
                </article>
            </div>
        </section>

        <section class="moments-section">
            <div>
                <p class="eyebrow">FAVORITE MOMENTS</p>
                <h2>반전 매력이 담긴 순간들</h2>
            </div>

            <div class="moment-photos">
                <figure v-for="photo in favoriteMoments" :key="photo.id">
                    <img :src="photo.imageUrl" :alt="photo.title">
                    <figcaption>{{ photo.mood }}</figcaption>
                </figure>
            </div>
        </section>
    </main>
</template>

<style scoped>
.favorites-page {
    padding: 38px 0 60px;
}

.favorite-hero {
    display: grid;
    grid-template-columns: 1.1fr 0.9fr;
    gap: 48px;
    align-items: center;
    min-height: 620px;
    border-radius: 32px;
    background: linear-gradient(135deg, rgba(255, 246, 249, 0.9), rgba(239, 233, 255, 0.9));
    padding: clamp(28px, 6vw, 68px);
}

.eyebrow {
    margin: 0 0 8px;
    color: #a36a84;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.18em;
}

.symbol {
    display: inline-block;
    margin-top: 14px;
    font-size: 2rem;
}

h1 {
    margin: 0;
    color: #3f3544;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: clamp(4rem, 10vw, 7.5rem);
    font-weight: 500;
    line-height: 0.95;
}

.korean-name {
    color: #8f7182;
    font-weight: 700;
}

.tagline {
    max-width: 520px;
    margin: 30px 0 12px;
    color: #4d414f;
    font-size: 1.25rem;
    font-weight: 700;
    line-height: 1.6;
}

.introduction {
    max-width: 520px;
    color: #766a78;
    line-height: 1.8;
}

.archive-link {
    display: inline-block;
    margin-top: 20px;
    border-radius: 999px;
    background: #4c414e;
    color: white;
    padding: 12px 18px;
    text-decoration: none;
}

.hero-photo {
    position: relative;
    margin: 0;
    transform: rotate(2deg);
}

.hero-photo img {
    display: block;
    width: 100%;
    aspect-ratio: 4 / 5;
    border: 10px solid white;
    border-bottom-width: 54px;
    border-radius: 6px;
    object-fit: cover;
    box-shadow: 0 24px 50px rgba(74, 47, 65, 0.2);
}

.hero-photo figcaption {
    position: absolute;
    bottom: 18px;
    left: 22px;
    color: #806879;
    font-family: cursive;
}

.charms-section,
.moments-section {
    margin-top: 72px;
}

h2 {
    margin: 4px 0 26px;
    color: #443947;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: clamp(2rem, 4vw, 3rem);
}

.charms-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
}

.charms-grid article {
    border: 1px solid rgba(171, 127, 148, 0.14);
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.78);
    padding: 26px;
    box-shadow: 0 12px 30px rgba(102, 75, 93, 0.08);
}

.charms-grid article > span {
    color: #c07294;
    font-size: 1.6rem;
}

.charms-grid h3 {
    margin-bottom: 8px;
}

.charms-grid p {
    margin: 0;
    color: #7c6f7e;
    line-height: 1.7;
}

.moments-section {
    display: grid;
    grid-template-columns: 0.8fr 1.2fr;
    gap: 36px;
    align-items: center;
}

.moment-photos {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
}

.moment-photos figure {
    margin: 0;
    border-radius: 22px;
    background: white;
    padding: 8px 8px 14px;
    box-shadow: 0 14px 30px rgba(95, 66, 85, 0.12);
}

.moment-photos img {
    display: block;
    width: 100%;
    aspect-ratio: 1 / 1.18;
    border-radius: 16px;
    object-fit: cover;
}

.moment-photos figcaption {
    padding: 10px 6px 0;
    color: #8c7181;
    font-size: 0.82rem;
    text-align: center;
}

@media (max-width: 760px) {
    .favorite-hero,
    .moments-section {
        grid-template-columns: 1fr;
    }

    .charms-grid {
        grid-template-columns: 1fr;
    }
}
</style>
