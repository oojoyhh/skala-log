<script setup>
import ClassBinding from './components/Practices/ClassBinding.vue/index.js'
import ComponentLocal from './components/Practices/ComponentLocal.vue/index.js'
import Computed from './components/Practices/Computed.vue'
import DeepWatch from './components/Practices/DeepWatch.vue'
import EventModifier from './components/Practices/EventModifier.vue'
import EventObject from './components/Practices/EventObject.vue'
import FormElementsHandling from './components/Practices/FormElementsHandling.vue'
import LifecycleHook from './components/component/LifecycleHook.vue/index.js'
import MultiSourceWatch from './components/Practices/Multi-SourceWatch.vue/index.js'
import Reactive from './components/Practices/Reactive.vue/index.js'
import ReactiveWatch from './components/Practices/ReactiveWatch.vue'
import Ref from './components/Practices/Ref.vue'
import SampleOne from './components/Practices/SampleOne.vue'
import SampleTwo from './components/Practices/SampleTwo.vue'
import StyleBinding from './components/Practices/StyleBinding.vue'
import VueDirective from './components/Practices/VueDirective.vue/index.js'
import VueStyle from './components/Practices/VueStyle.vue/index.js'
import Watch from './components/Practices/Watch.vue/index.js'
import WatchEffect from './components/Practices/WatchEffect.vue/index.js'
import VBind from './components/Practices/v-bind.vue'
import VCloak from './components/Practices/v-cloak.vue'
import VHtml from './components/Practices/v-html.vue/index.js'
import VIfElse from './components/Practices/v-ifelse.vue/index.js'
import VMemo from './components/Practices/v-memo.vue/index.js'
import VModel from './components/Practices/v-model.vue/index.js'
import VModelModifiers from './components/Practices/v-modelModifiers.vue/index.js'
import VOnEventHandler from './components/Practices/v-onEventHandler.vue/index.js'
import VOnce from './components/Practices/v-once.vue/index.js'
import VPre from './components/Practices/v-pre.vue/index.js'
import VShow from './components/Practices/v-show.vue/index.js'
import VText from './components/Practices/v-textv-text.vue/index.js'
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
    <Ref />
    <Reactive />
    <Computed />
    <Watch />
    <Multi-SourceWatch />
    <DeepWatch />
    <ReactiveWatch />
    <WatchEffect />
    <ComponentLocal />
    <LifecycleHook />
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
