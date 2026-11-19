<script setup lang="ts">
import { computed } from 'vue'
import Button from 'primevue/button'
import { RouterView, useRoute } from 'vue-router'

import { useSessionStore } from '@/features/auth'
import { AppLogo, SkipLink, ThemeToggle } from '@/shared/ui'

const session = useSessionStore()
const route = useRoute()

// Candidate-facing pages (vacancy, apply, 404) must not show HR-facing chrome.
const showHrChrome = computed(() => route.name === 'home' || route.name === 'forbidden')
</script>

<template>
  <div class="public-layout">
    <SkipLink />
    <header class="public-layout__header">
      <AppLogo v-if="showHrChrome" />
      <div class="public-layout__actions">
        <ThemeToggle />
        <RouterLink v-if="showHrChrome && session.isAuthenticated" :to="{ name: 'vacancies' }">
          <Button label="Open app" />
        </RouterLink>
        <RouterLink v-else-if="showHrChrome" :to="{ name: 'auth' }"
          ><Button label="Sign in"
        /></RouterLink>
      </div>
    </header>
    <main id="main" tabindex="-1" class="public-layout__main"><RouterView /></main>
  </div>
</template>

<style scoped>
.public-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.public-layout__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: 16px 24px;
}

.public-layout__actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 12px;
}

.public-layout__main {
  flex: 1;
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 24px 48px;
}
</style>
