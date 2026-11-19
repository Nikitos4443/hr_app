<script setup lang="ts">
import Message from 'primevue/message'

import EndStateCard from './EndStateCard.vue'
</script>

<template>
  <EndStateCard
    icon="pi pi-check-circle"
    tone="success"
    title="Thank you, you did great!"
    description="All your answers have been sent. We will review them carefully and email you with the result soon."
  >
    <Message severity="info" icon="pi pi-envelope" class="done__message">
      The result will arrive by email. You can close this page.
    </Message>
  </EndStateCard>
</template>

<style scoped>
.done__message {
  width: 100%;
  text-align: left;
}
</style>
