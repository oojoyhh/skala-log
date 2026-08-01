<script setup>
import ClassBinding from './components/practices/ClassBinding.vue'
import EventModifier from './components/practices/EventModifier.vue'
import EventObject from './components/practices/EventObject.vue'
import FormElementsHandling from './components/practices/FormElementsHandling.vue'
import SampleOne from './components/practices/SampleOne.vue'
import SampleTwo from './components/practices/SampleTwo.vue'
import StyleBinding from './components/practices/StyleBinding.vue'
import VueDirective from './components/practices/VueDirective.vue'
import VueStyle from './components/practices/VueStyle.vue'
import VBind from './components/practices/v-bind.vue'
import VCloak from './components/practices/v-cloak.vue'
import VHtml from './components/practices/v-html.vue'
import VIfElse from './components/practices/v-ifelse.vue'
import VMemo from './components/practices/v-memo.vue'
import VModel from './components/practices/v-model.vue'
import VModelModifiers from './components/practices/v-modelModifiers.vue'
import VOnEventHandler from './components/practices/v-onEventHandler.vue'
import VOnce from './components/practices/v-once.vue'
import VPre from './components/practices/v-pre.vue'
import VShow from './components/practices/v-show.vue'
import VText from './components/practices/v-text.vue'
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
