<script setup>
const content = '안녕하세요! <strong>Skala-Vue</strong>'
</script>

<template>
    <div class="practice-section">
        <h2>v-text 디렉티브 학습</h2>
        <h3>일반 보간법 사용 결과</h3>
        <p>{{ content }}</p>
        <br />

        <h3>2) v-text 디렉티브 결과</h3>
        <p v-text="'출력: ' + content"></p>
        <br />

        <h3>3) v-html 결과 비교</h3>
        <p v-html="content"></p>
    </div>
</template>
