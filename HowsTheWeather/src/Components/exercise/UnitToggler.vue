<script setup>
import { computed } from 'vue'
import { useConfigStore } from '@/stores/configStore'

const configStore = useConfigStore()

const useFahrenheit = computed({
  get: () => configStore.unit === 'fahrenheit',
  set: (isFahrenheit) => configStore.setUnit(isFahrenheit ? 'fahrenheit' : 'celsius'),
})
</script>

<template>
  <div class="unit-toggler" role="group" aria-label="날씨 단위 선택">
    <el-switch
      v-model="useFahrenheit"
      class="unit-switch"
      inline-prompt
      active-text="°F"
      inactive-text="°C"
      aria-label="섭씨와 화씨 전환"
    />
  </div>
</template>

<style scoped>
.unit-toggler {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
  text-align: center;
}

.unit-switch {
  --el-switch-on-color: #409eff;
  --el-switch-off-color: #79bbff;
}

.unit-switch :deep(.el-switch__core) {
  min-width: 60px;
  height: 30px;
  padding: 0 9px;
  border: 0;
  border-radius: 999px;
  box-shadow: inset 0 1px 3px rgb(31 53 75 / 16%);
}

.unit-switch :deep(.el-switch__action) {
  left: 4px;
  width: 20px;
  height: 20px;
  box-shadow: 0 2px 5px rgb(31 53 75 / 18%);
}

.unit-switch.is-checked :deep(.el-switch__action) {
  left: calc(100% - 24px);
}

.unit-switch :deep(.el-switch__inner) {
  font-size: 12px;
  font-weight: 800;
}

@media (max-width: 700px) {
  .unit-toggler {
    justify-content: center;
    width: 100%;
    margin-left: 0;
  }
}
</style>
