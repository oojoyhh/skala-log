<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  homeTo: {
    type: [String, Object],
    default: '/',
  },
})

const router = useRouter()

const handleGoHome = () => {
  router.push(props.homeTo)
}
</script>

<template>
  <div>
    <h3>서비스 소개</h3>
    <hr />

    <div class="description-box">
      <p>
        본 앱은 <strong>Vue 3</strong> 및 <strong>Vue Router 4</strong> 기반 제작된 실습용 기상
        관측 대시보드 시스템 입니다.
      </p>
      <ul>
        <li><code>components/</code> 폴더 내부의 독립 부품 연동</li>
        <li>클라이언트 사이드 라우팅을 통한 새로고침 없는 화면 전환</li>
        <li>URL 쿼리 스트링 매핑을 활용한 실시간 검색 상태 동기화</li>
      </ul>
    </div>

    <button class="home-btn" type="button" @click="handleGoHome">대시보드 홈으로 이동</button>
  </div>
</template>

<style scoped>
.description-box {
  padding: 12px;
  border-radius: 6px;
  font-size: 14px;
  line-height: 1.5;
  background-color: #f8f9fa;
}

ul {
  padding-left: 20px;
  margin: 8px 0 0;
}

li {
  margin-bottom: 6px;
  color: #555;
}

code {
  padding: 2px 4px;
  border-radius: 4px;
  color: #d63031;
  background-color: #ffeaa7;
}

.home-btn {
  width: 100%;
  padding: 10px;
  margin-top: 15px;
  border: none;
  border-radius: 4px;
  color: white;
  background-color: #3498db;
  font-weight: bold;
  cursor: pointer;
}
</style>
