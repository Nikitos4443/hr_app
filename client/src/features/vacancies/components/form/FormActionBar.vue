<script setup lang="ts">
import Button from 'primevue/button'

defineProps<{
  dirty: boolean
  saving: boolean
  errorCount: number
  submitLabel: string
}>()

defineEmits<{ cancel: [] }>()
</script>

<template>
  <div class="action-bar">
    <span class="action-bar__status" role="status">
      <template v-if="errorCount">
        <i class="pi pi-exclamation-circle action-bar__icon--error" aria-hidden="true" />
        {{ errorCount }} {{ errorCount === 1 ? 'error needs' : 'errors need' }} fixing
      </template>
      <template v-else-if="dirty">
        <i class="pi pi-pencil action-bar__icon--warn" aria-hidden="true" />
        Unsaved changes
      </template>
    </span>
    <div class="action-bar__buttons">
      <Button
        label="Cancel"
        severity="secondary"
        text
        :disabled="saving"
        @click="$emit('cancel')"
      />
      <Button type="submit" :label="submitLabel" icon="pi pi-check" :loading="saving" />
    </div>
  </div>
</template>

<style scoped>
.action-bar {
  position: sticky;
  bottom: 0;
  z-index: 5;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 24px;
  border: 1px solid var(--p-content-border-color);
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-background);
  box-shadow: 0 -4px 16px color-mix(in srgb, var(--p-text-color) 8%, transparent);
}

.action-bar__status {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--p-text-muted-color);
}

.action-bar__icon--warn {
  color: var(--p-orange-500);
}

.action-bar__icon--error {
  color: var(--p-form-field-invalid-border-color);
}

.action-bar__buttons {
  display: flex;
  gap: 8px;
  margin-left: auto;
}
</style>
