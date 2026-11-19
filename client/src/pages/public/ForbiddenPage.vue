<script setup lang="ts">
import Button from 'primevue/button'
import { useRouter } from 'vue-router'

import { ErrorState } from '@/shared/ui'

const router = useRouter()

const canGoBack = Boolean(window.history.state?.back)
</script>

<template>
  <div class="error-page">
    <p class="error-page__code" aria-hidden="true">403</p>
    <ErrorState
      icon="pi pi-lock"
      title="You don't have access"
      description="Your role doesn't allow you to open this page."
    >
      <Button
        v-if="canGoBack"
        label="Back"
        icon="pi pi-arrow-left"
        severity="secondary"
        @click="router.back()"
      />
      <RouterLink :to="{ name: 'vacancies' }"><Button label="Back to vacancies" /></RouterLink>
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
