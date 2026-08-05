<script setup>
import { Bell, Clock, Location, Search } from '@element-plus/icons-vue'

const features = [
  {
    icon: Location,
    title: '내 지역 날씨',
    desc: '체감·습도·기압·풍속에 미세먼지·초미세먼지·일출·일몰까지 한 카드에서 확인합니다.',
  },
  {
    icon: Search,
    title: '지역별 검색',
    desc: '전국 주요 도시의 실시간 날씨를 검색하고, 원하는 지역을 내 지역으로 고정할 수 있습니다.',
  },
  {
    icon: Clock,
    title: '시간별·5일 예보',
    desc: '상세보기에서 24시간 예보와 5일간의 최저·최고 기온을 확인합니다.',
  },
  {
    icon: Bell,
    title: '기상특보',
    desc: '기상청 API로 내 지역에 발효 중인 폭염·열대야 특보를 알려드립니다.',
  },
]
</script>

<template>
  <div class="tuned-about">
    <header class="about-heading">
      <el-tag type="primary" effect="light" round>ABOUT</el-tag>
      <h1>나만의 날씨 대시보드 소개</h1>
      <p>OpenWeather·기상청 실시간 관측 데이터로 만든 개인용 날씨 서비스입니다.</p>
    </header>

    <el-card class="about-panel" shadow="hover">
      <div class="feature-grid">
        <div v-for="feature in features" :key="feature.title" class="feature-item">
          <span class="feature-icon" aria-hidden="true">
            <el-icon><component :is="feature.icon" /></el-icon>
          </span>
          <div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.desc }}</p>
          </div>
        </div>
      </div>

      <RouterLink to="/">
        <el-button class="home-button" type="primary" size="large">대시보드로 돌아가기</el-button>
      </RouterLink>
    </el-card>
  </div>
</template>

<style scoped>
.tuned-about {
  display: grid;
  gap: 22px;
  width: min(100%, 820px);
  margin: 0 auto;
}

.about-heading {
  padding: 8px 4px 0;
}

.about-heading h1 {
  margin: 10px 0 4px;
  color: #303133;
  font-size: clamp(1.75rem, 5vw, 2.45rem);
  letter-spacing: -0.04em;
}

.about-heading p {
  margin: 0;
  color: #909399;
}

.about-panel {
  border-color: #e4e7ed;
  border-radius: 16px;
  background: #fff;
}

.about-panel :deep(.el-card__body) {
  padding: 24px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.feature-icon {
  display: grid;
  flex: 0 0 auto;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: #ecf5ff;
  font-size: 20px;
  place-items: center;
}

.feature-item h3 {
  margin: 0;
  color: #2d4864;
  font-size: 16px;
}

.feature-item p {
  margin: 4px 0 0;
  color: #6b7d8f;
  font-size: 14px;
  line-height: 1.5;
}

.home-button {
  width: 100%;
  margin-top: 28px;
}

@media (max-width: 560px) {
  .about-panel :deep(.el-card__body) {
    padding: 18px;
  }
}
</style>
