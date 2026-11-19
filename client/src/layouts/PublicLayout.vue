<script setup lang="ts">
import Button from 'primevue/button'
import { RouterView } from 'vue-router'

import { useSessionStore } from '@/features/auth'
import { AppLogo, SkipLink, ThemeToggle } from '@/shared/ui'

const session = useSessionStore()
</script>

<template>
  <div class="public-layout">
    <SkipLink />
    <header class="public-layout__header">
      <AppLogo />
      <div class="public-layout__actions">
        <ThemeToggle />
        <RouterLink v-if="session.isAuthenticated" :to="{ name: 'vacancies' }">
          <Button label="Open app" />
        </RouterLink>
        <RouterLink v-else :to="{ name: 'auth' }"><Button label="Sign in" /></RouterLink>
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
