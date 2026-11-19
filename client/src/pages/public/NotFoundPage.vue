<script setup lang="ts">
import Button from 'primevue/button'
import { useRouter } from 'vue-router'

import { useSessionStore } from '@/features/auth'
import { ErrorState } from '@/shared/ui'

const router = useRouter()
const session = useSessionStore()

const canGoBack = Boolean(window.history.state?.back)
</script>

<template>
  <div class="error-page">
    <p class="error-page__code" aria-hidden="true">404</p>
    <ErrorState
      icon="pi pi-compass"
      title="Page not found"
      description="The page you are looking for doesn't exist or was moved."
    >
      <Button
        v-if="canGoBack"
        label="Back"
        icon="pi pi-arrow-left"
        severity="secondary"
        @click="router.back()"
      />
      <RouterLink v-if="session.isAuthenticated" :to="{ name: 'vacancies' }">
        <Button label="Go home" />
      </RouterLink>
    </ErrorState>
  </div>
</template>

<style scoped>
.error-page__code {
  margin: 24px 0 0;
  color: var(--p-text-muted-color);
  font-size: clamp(56px, 16vw, 96px);
  font-weight: 700;
  line-height: 1;
  text-align: center;
}
</style>
