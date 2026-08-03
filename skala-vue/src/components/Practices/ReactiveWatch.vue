<script setup>
import { reactive, ref, watch } from 'vue';

const state = reactive({
    productName: '노트북',
    price: 1000,
})

const logAutoDeep = ref('대기 중...')
const logTarget = ref('대기 중...')

// 1) 변수명 그대로 감시 (자동 딥트루 작동)
watch(state, (newVal, oldVal) => {
    // newVal = oldVal = 2000
    logAutoDeep.value = `[자동 deep] 가격 변동! 이전가격인척하는: ${oldVal.price}원 => 현재가격: ${newVal.price}원`
    }
)

// 2) 화살표 함수로 특정 속성만 감시 (이전값추적가능)
watch(
    () => state.price,
    (newPrice, oldPrice) => {
        // 특정 알맹이 값만 추출했으므로 진짜 과거 가격 정상 보존
        logTarget.value = `[타겟 조준] 가격이 진짜 올랐음! 옛날값: ${oldPrice}원 => 바뀐값: ${newPrice}원`
    }
)
</script>

<template>
    <div class="practice-section">
        <h2>reactive() 데이터 watch 감시 규칙</h2>
        <h3>상품 정보 관리 (reactive)</h3>
        <p>상품명: {{ state.productName }} / 가격 {{ state.price }}원</p>
        <button @click="state.price += 500">가격 500원 인상</button>

        <div class="monitor auto">
            <p> 1) state 변수 통째로 감시 (deep 자동화)</p>
            <p>{{ logAutoDeep }}</p>
            <small>주의: 이전 값과 현재 값이 똑같이 찍힌다.</small>
        </div>

        <div class="monitor target">
            <p>2) () => state.price 콕 집어 감시</p>
            <p>{{ logTarget }}</p>
            <small>성공: 과거의 원본 가격이 칼같이 보존된다.</small>
        </div>
    </div>
</template>