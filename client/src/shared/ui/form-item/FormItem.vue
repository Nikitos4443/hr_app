<script setup lang="ts">
defineProps<{
  label: string
  for?: string
  required?: boolean
  hint?: string
  error?: string
}>()
</script>

<template>
  <div class="form-item">
    <label :for="$props.for" class="form-item__label">
      {{ label }}
      <span v-if="required" class="form-item__required" aria-hidden="true">*</span>
    </label>
    <slot />
    <small v-if="error" class="form-item__error" role="alert">
      <i class="pi pi-exclamation-circle" aria-hidden="true" />
      {{ error }}
    </small>
    <small v-else-if="hint" class="form-item__hint">{{ hint }}</small>
  </div>
</template>

<style scoped>
.form-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-item__label {
  font-size: 13px;
  font-weight: 600;
}

.form-item__required {
  color: var(--p-form-field-invalid-border-color);
}

.form-item__hint {
  color: var(--p-text-muted-color);
}

.form-item__error {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--p-form-field-invalid-border-color);
}
</style>
