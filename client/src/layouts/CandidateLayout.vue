<script setup lang="ts">
import { RouterView } from 'vue-router'

import { AppLogo, SkipLink, ThemeToggle } from '@/shared/ui'
</script>

<template>
  <div class="candidate-layout">
    <SkipLink />
    <header class="candidate-layout__header">
      <AppLogo />
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
}

.candidate-layout__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
}

.candidate-layout__main {
  flex: 1;
  width: 100%;
  max-width: 880px;
  margin: 0 auto;
  padding: 0 16px 48px;
}
</style>
