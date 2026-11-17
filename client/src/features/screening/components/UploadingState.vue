<script setup lang="ts">
import Button from 'primevue/button'
import Message from 'primevue/message'
import ProgressBar from 'primevue/progressbar'

import { formatMegabytes } from '../lib/format'

defineProps<{
  percent: number
  fileName: string
  sizeBytes: number
  failed: boolean
  errorText: string
}>()

const emit = defineEmits<{ retry: []; back: [] }>()
</script>

<template>
  <div class="uploading">
    <h2 class="uploading__title">{{ failed ? 'Upload failed' : 'Sending your answer...' }}</h2>

    <div class="uploading__file">
      <i class="pi pi-video uploading__icon" aria-hidden="true" />
      <div class="uploading__meta">
        <span class="uploading__name">{{ fileName }}</span>
        <span class="uploading__size" role="status">
          {{ failed ? formatMegabytes(sizeBytes) : `${percent}% of ${formatMegabytes(sizeBytes)}` }}
        </span>
      </div>
    </div>
    <ProgressBar :value="percent" :show-value="false" aria-label="Video upload progress" />

    <Message v-if="failed" severity="error" icon="pi pi-exclamation-circle" role="alert">
      {{ errorText }}
    </Message>
    <p v-else class="uploading__hint">
      Please keep this page open. If the connection drops, we will let you retry.
    </p>

    <div v-if="failed" class="uploading__actions">
      <Button label="Retry upload" icon="pi pi-refresh" size="large" fluid @click="emit('retry')" />
      <Button
        label="Back to recording"
        icon="pi pi-arrow-left"
        severity="secondary"
        size="large"
        fluid
        @click="emit('back')"
      />
    </div>
  </div>
</template>

<style scoped>
.uploading {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.uploading__title {
  margin: 0;
  font-size: 20px;
}

.uploading__file {
  display: flex;
  align-items: center;
  gap: 12px;
}

.uploading__icon {
  font-size: 28px;
  color: var(--p-primary-color);
}

.uploading__meta {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.uploading__name {
  overflow: hidden;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.uploading__size,
.uploading__hint {
  margin: 0;
  color: var(--p-text-muted-color);
  font-variant-numeric: tabular-nums;
}

.uploading__actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
