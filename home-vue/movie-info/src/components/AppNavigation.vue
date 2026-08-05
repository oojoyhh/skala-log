<script setup>
// 페이지 메뉴
const navigationItems = [
    { label: 'Archive', to: '/archive' },
    { label: 'Favorites', to: '/favorites' },
    { label: 'About', to: '/about' }
]
</script>

<template>
    <nav class="navigation">
        <RouterLink class="brand" to="/archive">MY ♡ LOG</RouterLink>

        <div class="navigation-links">
            <RouterLink
                v-for="item in navigationItems"
                :key="item.to"
                :to="item.to"
            >
                {{ item.label }}
            </RouterLink>
        </div>
    </nav>
</template>

<style scoped>
.navigation {
    position: sticky;
    top: 14px;
    z-index: 20;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid rgba(181, 139, 160, 0.18);
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.78);
    padding: 14px 18px;
    box-shadow: 0 10px 30px rgba(107, 77, 98, 0.08);
    backdrop-filter: blur(14px);
}

.brand,
.navigation a {
    color: #655867;
    text-decoration: none;
}

.brand {
    color: #a65f7f;
    font-family: Georgia, 'Times New Roman', serif;
    font-weight: 700;
    letter-spacing: 0.08em;
}

.navigation-links {
    display: flex;
    gap: 6px;
}

.navigation-links a {
    border-radius: 999px;
    padding: 8px 12px;
    font-size: 0.86rem;
    transition: 160ms ease;
}

.navigation-links a:hover,
.navigation-links a.router-link-active {
    background: #f4e7ed;
    color: #9c5f7a;
}

@media (max-width: 580px) {
    .navigation {
        align-items: flex-start;
        flex-direction: column;
        gap: 10px;
    }

    .navigation-links {
        width: 100%;
        justify-content: space-between;
    }
}
</style>
