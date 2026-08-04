<script setup>
// components/LoadingSpinner.vue
// -----------------------------------------------------------------------------
// 데이터를 불러오는 동안 보여줄 "스캔 중" 표시 컴포넌트.
// 디자인 컨셉(포켓몬 스캐너 단말기)에 맞춰, 단순 원형 스피너 대신
// 좌우로 오가는 스캔 라인 애니메이션으로 표현합니다.
// -----------------------------------------------------------------------------
defineProps({
  label: {
    type: String,
    default: '스캔 중...',
  },
})
</script>

<template>
  <div class="scanner" role="status" aria-live="polite">
    <div class="scanner__track">
      <div class="scanner__beam"></div>
    </div>
    <span class="scanner__label">{{ label }}</span>
  </div>
</template>

<style scoped>
.scanner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 48px 0;
}

.scanner__track {
  width: 160px;
  height: 4px;
  border-radius: 2px;
  background: var(--surface-alt);
  overflow: hidden;
  position: relative;
}

.scanner__beam {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 40%;
  background: linear-gradient(90deg, transparent, var(--accent-scan), transparent);
  animation: sweep 1.1s ease-in-out infinite;
}

@keyframes sweep {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(250%); }
}

.scanner__label {
  font-family: var(--font-display);
  font-size: 12px;
  letter-spacing: 0.08em;
  color: var(--text-dim);
}
</style>
