<script setup lang="ts">
import Message from 'primevue/message'

import EndStateCard from './EndStateCard.vue'
</script>

<template>
  <EndStateCard
    icon="pi pi-link"
    tone="warn"
    title="This link no longer works"
    description="It may have expired or the address was copied incompletely. Open the invitation email again and follow the button in it."
  >
    <Message severity="info" icon="pi pi-question-circle" class="invalid__message">
      Still stuck? Reply to the invitation email and we will help.
    </Message>
  </EndStateCard>
</template>

<style scoped>
.invalid__message {
  width: 100%;
  text-align: left;
}
</style>
