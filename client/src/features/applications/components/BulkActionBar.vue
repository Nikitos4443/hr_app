<script setup lang="ts">
import Button from 'primevue/button'

import { ACTION_ICONS, ACTION_LABELS } from '../lib/application-meta'
import type { ApplicationAction } from '../types/application'

defineProps<{ count: number; busy?: boolean }>()

const emit = defineEmits<{ action: [action: ApplicationAction]; clear: [] }>()
</script>

<template>
  <div class="bulk" role="region" aria-label="Bulk actions">
    <span class="bulk__count" role="status">
      <i class="pi pi-check-square" aria-hidden="true" />
      {{ count }} {{ count === 1 ? 'candidate' : 'candidates' }} selected
    </span>
    <div class="bulk__actions">
      <Button
        :label="ACTION_LABELS.invite"
        :icon="ACTION_ICONS.invite"
        size="small"
        severity="secondary"
        :disabled="busy"
        @click="emit('action', 'invite')"
      />
      <Button
        :label="ACTION_LABELS.shortlist"
        :icon="ACTION_ICONS.shortlist"
        size="small"
        severity="secondary"
        :disabled="busy"
        @click="emit('action', 'shortlist')"
      />
      <Button
        :label="ACTION_LABELS.reject"
        :icon="ACTION_ICONS.reject"
        size="small"
        severity="danger"
        outlined
        :disabled="busy"
        @click="emit('action', 'reject')"
      />
      <Button
        label="Clear"
        size="small"
        severity="secondary"
        text
        :disabled="busy"
        @click="emit('clear')"
      />
    </div>
  </div>
</template>

<style scoped>
.bulk {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 16px;
  border-radius: 10px;
  background: var(--p-highlight-background);
  color: var(--p-highlight-color);
}

.bulk__count {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.bulk__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
