<script setup lang="ts">
import Button from 'primevue/button'

defineProps<{ message: string }>()

const emit = defineEmits<{ retry: [] }>()
</script>

<template>
  <div class="error-banner" role="alert">
    <i class="pi pi-exclamation-circle error-banner__icon" aria-hidden="true" />
    <div class="error-banner__body">
      <strong>The assistant did not respond</strong>
      <span class="error-banner__text">{{ message }}</span>
    </div>
    <Button
      label="Retry"
      icon="pi pi-refresh"
      size="small"
      severity="secondary"
      @click="emit('retry')"
    />
  </div>
</template>

<style scoped>
.error-banner {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border: 1px solid var(--p-form-field-invalid-border-color);
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-background);
}

.error-banner__icon {
  color: var(--p-form-field-invalid-border-color);
}

.error-banner__body {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 160px;
}

.error-banner__text {
  color: var(--p-text-muted-color);
  font-size: 13px;
}
</style>
