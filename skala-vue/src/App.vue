<script setup>
import ClassBinding from './components/ClassBinding.vue'
import EventModifier from './components/EventModifier.vue'
import EventObject from './components/EventObject.vue'
import FormElementsHandling from './components/FormElementsHandling.vue'
import SampleOne from './components/SampleOne.vue'
import SampleTwo from './components/SampleTwo.vue'
import StyleBinding from './components/StyleBinding.vue'
import VueDirective from './components/VueDirective.vue'
import VueStyle from './components/VueStyle.vue'
import VBind from './components/v-bind.vue'
import VCloak from './components/v-cloak.vue'
import VHtml from './components/v-html.vue'
import VIfElse from './components/v-ifelse.vue'
import VMemo from './components/v-memo.vue'
import VModel from './components/v-model.vue'
import VModelModifiers from './components/v-modelModifiers.vue'
import VOnEventHandler from './components/v-onEventHandler.vue'
import VOnce from './components/v-once.vue'
import VPre from './components/v-pre.vue'
import VShow from './components/v-show.vue'
import VText from './components/v-textv-text.vue'
</script>

<template>
  <main class="practice-app">
    <h1>SKALA Vue 실습</h1>

    <SampleOne />
    <SampleTwo />
    <VText />
    <VHtml />
    <VBind />
    <ClassBinding />
    <StyleBinding />
    <VIfElse />
    <VShow />
    <VOnEventHandler />
    <EventObject />
    <EventModifier />
    <VModel />
    <VModelModifiers />
    <FormElementsHandling />
    <VOnce />
    <VPre />
    <VCloak />
    <VMemo />
    <VueDirective />
    <VueStyle />
  </main>
</template>

<style>
#app {
  display: block;
  width: 100%;
  padding: 2rem;
}

.practice-app {
  display: grid;
  gap: 1.5rem;
  width: min(100%, 960px);
  margin: 0 auto;
}

.practice-app > h1 {
  text-align: center;
  font-weight: 700;
}

.practice-section {
  padding: 1.5rem;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  background: var(--color-background-soft);
}

.practice-section h2 {
  color: #42b883;
  padding-bottom: 8px;
  margin-bottom: 16px;
  border-bottom: 2px solid #42b883;
}
</style>
