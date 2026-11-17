<script setup lang="ts">
import Button from 'primevue/button'

import EndStateCard from './EndStateCard.vue'

const emit = defineEmits<{ retry: [] }>()
</script>

<template>
  <EndStateCard
    icon="pi pi-hourglass"
    tone="info"
    title="We are still preparing your screening"
    description="Your resume is being processed. This usually takes a few minutes, please check again shortly."
  >
    <Button label="Check again" icon="pi pi-refresh" severity="secondary" @click="emit('retry')" />
  </EndStateCard>
</template>
