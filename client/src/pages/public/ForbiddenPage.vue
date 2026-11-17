<script setup lang="ts">
import Button from 'primevue/button'

import { ErrorState } from '@/shared/ui'
</script>

<template>
  <ErrorState
    icon="pi pi-lock"
    title="You don't have access"
    description="Your role doesn't allow you to open this page."
  >
    <RouterLink :to="{ name: 'vacancies' }"><Button label="Back to vacancies" /></RouterLink>
  </ErrorState>
</template>
