<script setup>
import { ownerProfile } from '@/data/profile.js'
import archivePhotos from '@/data/archivePhotos.js'

// 아카이브 통계
const archiveStats = [
    { value: archivePhotos.length, label: 'saved photos' },
    { value: '1', label: 'favorite person' },
    { value: '∞', label: 'favorite moments' }
]
</script>

<template>
    <main class="about-page">
        <section class="profile-card">
            <div class="profile-mark">H</div>

            <div class="profile-copy">
                <p class="eyebrow">ABOUT THE CURATOR</p>
                <h1>Hi, I'm {{ ownerProfile.name }}.</h1>
                <p class="role">{{ ownerProfile.role }}</p>
                <p class="bio">{{ ownerProfile.bio }}</p>

                <div class="interests">
                    <span v-for="interest in ownerProfile.interests" :key="interest">
                        {{ interest }}
                    </span>
                </div>
            </div>
        </section>

        <section class="about-grid">
            <article class="motto-card">
                <p class="eyebrow">MY MOTTO</p>
                <blockquote>“{{ ownerProfile.motto }}”</blockquote>
                <p>이 공간은 좋아하는 마음을 천천히 모으는 개인 아카이브입니다.</p>
            </article>

            <article class="stats-card">
                <p class="eyebrow">ARCHIVE NUMBERS</p>
                <div class="stats">
                    <div v-for="stat in archiveStats" :key="stat.label">
                        <strong>{{ stat.value }}</strong>
                        <span>{{ stat.label }}</span>
                    </div>
                </div>
            </article>
        </section>

        <section class="contact-card">
            <div>
                <p class="eyebrow">KEEP YOUR FAVORITES CLOSE</p>
                <h2>좋아하는 것을 오래 좋아하기 위한 기록</h2>
            </div>
            <RouterLink to="/archive">아카이브 둘러보기 →</RouterLink>
        </section>
    </main>
</template>

<style scoped>
.about-page {
    padding: 46px 0 60px;
}

.profile-card {
    display: grid;
    grid-template-columns: 240px 1fr;
    gap: 48px;
    align-items: center;
    border-radius: 32px;
    background: rgba(255, 255, 255, 0.8);
    padding: clamp(28px, 6vw, 64px);
    box-shadow: 0 18px 50px rgba(104, 75, 94, 0.1);
}

.profile-mark {
    display: grid;
    width: 220px;
    height: 220px;
    place-items: center;
    border-radius: 50%;
    background: linear-gradient(145deg, #edb4c8, #bcb1e3);
    color: white;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 7rem;
    box-shadow: 0 18px 40px rgba(132, 91, 116, 0.2);
}

.eyebrow {
    margin: 0 0 8px;
    color: #a36a84;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.18em;
}

h1,
h2 {
    color: #413543;
    font-family: Georgia, 'Times New Roman', serif;
}

h1 {
    margin: 0;
    font-size: clamp(2.6rem, 7vw, 5rem);
}

.role {
    color: #9b6b82;
    font-weight: 700;
}

.bio {
    max-width: 620px;
    color: #746777;
    line-height: 1.8;
}

.interests {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 22px;
}

.interests span {
    border-radius: 999px;
    background: #f5eaf0;
    color: #8c6276;
    padding: 7px 11px;
    font-size: 0.8rem;
}

.about-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 24px;
}

.motto-card,
.stats-card,
.contact-card {
    border: 1px solid rgba(171, 127, 148, 0.14);
    border-radius: 26px;
    background: rgba(255, 255, 255, 0.75);
    padding: 30px;
}

blockquote {
    margin: 24px 0;
    color: #4c3e4b;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.7rem;
    line-height: 1.55;
}

.motto-card > p:last-child {
    color: #807181;
    line-height: 1.7;
}

.stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 28px;
}

.stats div {
    text-align: center;
}

.stats strong,
.stats span {
    display: block;
}

.stats strong {
    color: #ad6d8a;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 2.2rem;
}

.stats span {
    margin-top: 6px;
    color: #9b899a;
    font-size: 0.72rem;
}

.contact-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    margin-top: 24px;
    background: linear-gradient(135deg, #fff4f7, #eee9ff);
}

.contact-card h2 {
    margin: 6px 0 0;
}

.contact-card a {
    flex-shrink: 0;
    border-radius: 999px;
    background: #4d414e;
    color: white;
    padding: 12px 18px;
    text-decoration: none;
}

@media (max-width: 760px) {
    .profile-card,
    .about-grid {
        grid-template-columns: 1fr;
    }

    .profile-mark {
        width: 150px;
        height: 150px;
        font-size: 5rem;
    }

    .contact-card {
        align-items: flex-start;
        flex-direction: column;
    }
}
</style>
