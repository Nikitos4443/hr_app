<script setup lang="ts">
import Button from 'primevue/button'

import { ACTION_ICONS, ACTION_LABELS, canApply } from '../lib/application-meta'
import type { ApplicationAction, ApplicationStatus } from '../types/application'

const props = defineProps<{
  status: ApplicationStatus
  resumeStatus: string | null
  busy?: boolean
}>()

const emit = defineEmits<{ action: [action: ApplicationAction] }>()

function allowed(action: ApplicationAction) {
  return canApply(action, { status: props.status, resumeStatus: props.resumeStatus })
}
</script>

<template>
  <div class="actions">
    <Button
      :label="ACTION_LABELS.shortlist"
      :icon="ACTION_ICONS.shortlist"
      :disabled="busy || !allowed('shortlist')"
      @click="emit('action', 'shortlist')"
    />
    <Button
      :label="ACTION_LABELS.invite"
      :icon="ACTION_ICONS.invite"
      severity="secondary"
      :disabled="busy || !allowed('invite')"
      @click="emit('action', 'invite')"
    />
    <Button
      :label="ACTION_LABELS.reject"
      :icon="ACTION_ICONS.reject"
      severity="danger"
      outlined
      :disabled="busy || !allowed('reject')"
      @click="emit('action', 'reject')"
    />
  </div>
</template>

<style scoped>
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
