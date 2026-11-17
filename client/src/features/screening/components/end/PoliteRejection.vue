<script setup lang="ts">
import Button from 'primevue/button'

import EndStateCard from './EndStateCard.vue'
</script>

<template>
  <EndStateCard
    icon="pi pi-heart"
    tone="neutral"
    title="Thank you for your time"
    description="This time we will move forward with other candidates for this role. The decision applies only to this vacancy and is not an assessment of you as a professional."
  >
    <p class="rejection__hint">
      Another position may suit you, check the current vacancies on the company website.
    </p>
    <RouterLink to="/" custom v-slot="{ navigate }">
      <Button
        label="Browse vacancies"
        icon="pi pi-arrow-right"
        icon-pos="right"
        severity="secondary"
        size="large"
        fluid
        @click="navigate"
      />
    </RouterLink>
  </EndStateCard>
</template>

<style scoped>
.rejection__hint {
  margin: 0;
  color: var(--p-text-muted-color);
}
</style>
