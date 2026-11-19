<script setup lang="ts">
import { RouterView } from 'vue-router'

import { SkipLink } from '@/shared/ui'

import SideNav from './components/SideNav.vue'
import TopBar from './components/TopBar.vue'
</script>

<template>
  <div class="app-shell">
    <SkipLink />
    <SideNav />
    <div class="app-shell__body">
      <TopBar />
      <main id="main" tabindex="-1" class="app-shell__main"><RouterView /></main>
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  display: grid;
  grid-template-columns: 232px minmax(0, 1fr);
  min-height: 100vh;
}

.app-shell__body {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.app-shell__main {
  display: flex;
  flex-direction: column;
  gap: 24px;
  flex: 1;
  padding: 32px;
}

@media (max-width: 768px) {
  .app-shell {
    grid-template-columns: minmax(0, 1fr);
  }

  .app-shell__main {
    padding: 16px;
  }
}
</style>
