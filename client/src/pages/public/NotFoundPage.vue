<script setup lang="ts">
import Button from 'primevue/button'

import { ErrorState } from '@/shared/ui'
</script>

<template>
  <ErrorState
    icon="pi pi-compass"
    title="Page not found"
    description="The page you are looking for doesn't exist or was moved."
  >
    <RouterLink to="/"><Button label="Go home" /></RouterLink>
  </ErrorState>
</template>
