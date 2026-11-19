<script setup lang="ts">
import Tag from 'primevue/tag'

import EndStateCard from './EndStateCard.vue'
</script>

<template>
  <EndStateCard
    icon="pi pi-check-square"
    tone="info"
    title="You have already completed the screening"
    description="We have received your answers. There is nothing more to do, just wait for our decision by email."
  >
    <Tag severity="success" icon="pi pi-check-circle" value="Answers received" />
  </EndStateCard>
</template>
