<script setup lang="ts">
import { ref } from 'vue'
import Button from 'primevue/button'

import { formatFileSize, MAX_RESUME_SIZE_BYTES, RESUME_CONTENT_TYPE } from '../lib/resume'

defineProps<{ file: File | null; invalid?: boolean; disabled?: boolean }>()

const emit = defineEmits<{ select: [file: File]; remove: [] }>()

const input = ref<HTMLInputElement | null>(null)
const dragging = ref(false)

function pick() {
  input.value?.click()
}

function onChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) emit('select', file)
  target.value = ''
}

function onDrop(event: DragEvent) {
  dragging.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file) emit('select', file)
}
</script>

<template>
  <div v-if="file" class="resume-file" :class="{ 'resume-file--invalid': invalid }">
    <i class="pi pi-file-pdf resume-file__icon" aria-hidden="true" />
    <div class="resume-file__info">
      <span class="resume-file__name">{{ file.name }}</span>
      <span class="resume-file__size">{{ formatFileSize(file.size) }}</span>
    </div>
    <Button
      icon="pi pi-times"
      severity="secondary"
      variant="text"
      rounded
      aria-label="Remove file"
      :disabled="disabled"
      @click="emit('remove')"
    />
  </div>

  <div
    v-else
    class="dropzone"
    :class="{ 'dropzone--active': dragging, 'dropzone--invalid': invalid }"
    role="button"
    tabindex="0"
    aria-label="Choose a PDF resume"
    @click="pick"
    @keydown.enter.prevent="pick"
    @keydown.space.prevent="pick"
    @dragover.prevent="dragging = true"
    @dragleave.prevent="dragging = false"
    @drop.prevent="onDrop"
  >
    <i class="pi pi-upload dropzone__icon" aria-hidden="true" />
    <span class="dropzone__title">Drag a PDF here or click to choose a file</span>
    <span class="dropzone__hint">Up to {{ formatFileSize(MAX_RESUME_SIZE_BYTES) }}</span>
  </div>

  <input
    ref="input"
    class="visually-hidden"
    type="file"
    :accept="`${RESUME_CONTENT_TYPE},.pdf`"
    tabindex="-1"
    aria-hidden="true"
    @change="onChange"
  />
</template>

<style scoped>
.dropzone {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 28px 16px;
  border: 2px dashed var(--p-content-border-color);
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-background);
  text-align: center;
  cursor: pointer;
  transition:
    border-color 0.15s,
    background 0.15s;
}

.dropzone:hover,
.dropzone:focus-visible,
.dropzone--active {
  border-color: var(--p-primary-color);
  background: var(--p-highlight-background);
  outline: none;
}

.dropzone--invalid {
  border-color: var(--p-form-field-invalid-border-color);
}

.dropzone__icon {
  font-size: 24px;
  color: var(--p-primary-color);
}

.dropzone__title {
  font-weight: 600;
}

.dropzone__hint {
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.resume-file {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 12px 12px 16px;
  border: 1px solid var(--p-content-border-color);
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-background);
}

.resume-file--invalid {
  border-color: var(--p-form-field-invalid-border-color);
}

.resume-file__icon {
  font-size: 22px;
  color: var(--p-primary-color);
}

.resume-file__info {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
}

.resume-file__name {
  overflow: hidden;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.resume-file__size {
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
}
</style>
