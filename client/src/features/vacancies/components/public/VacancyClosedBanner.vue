<script setup lang="ts">
defineProps<{ company: string; closedOn?: string | null }>()
</script>

<template>
  <div class="closed-banner" role="status">
    <i class="pi pi-lock closed-banner__icon" aria-hidden="true" />
    <div>
      <strong>Applications are closed</strong>
      <p class="closed-banner__text">
        <template v-if="closedOn">This vacancy closed on {{ closedOn }}. </template>
        Thank you for your interest in {{ company }}!
      </p>
    </div>
  </div>
</template>

<style scoped>
.closed-banner {
  display: flex;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--p-content-border-color);
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-hover-background);
}

.closed-banner__icon {
  margin-top: 2px;
  color: var(--p-text-muted-color);
}

.closed-banner__text {
  margin: 4px 0 0;
  color: var(--p-text-muted-color);
}
</style>
