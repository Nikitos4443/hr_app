<script setup lang="ts">
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'

import { SkipLink, ThemeToggle } from '@/shared/ui'

const route = useRoute()

// The chat fills the viewport and scrolls internally.
const fixedHeight = computed(() => route.name === 'chat')
</script>

<template>
  <div class="candidate-layout" :class="{ 'candidate-layout--fixed': fixedHeight }">
    <SkipLink />
    <header class="candidate-layout__header">
      <ThemeToggle />
    </header>
    <main id="main" tabindex="-1" class="candidate-layout__main"><RouterView /></main>
  </div>
</template>

<style scoped>
.candidate-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-height: 100dvh;
}

.candidate-layout--fixed {
  height: 100dvh;
  overflow: hidden;
}

.candidate-layout__header {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 16px 24px;
}

.candidate-layout--fixed .candidate-layout__header {
  padding-block: 8px;
}

.candidate-layout__main {
  display: flex;
  flex: 1;
  flex-direction: column;
  width: 100%;
  min-height: 0;
  max-width: 880px;
  margin: 0 auto;
  padding: 0 16px 48px;
}

.candidate-layout--fixed .candidate-layout__main {
  padding-bottom: calc(16px + env(safe-area-inset-bottom));
}
</style>
