<script setup lang="ts">
import { nextTick, ref, useId, watch } from 'vue'
import Button from 'primevue/button'

import { formatFileSize, MAX_RESUME_SIZE_BYTES, RESUME_CONTENT_TYPE } from '../lib/resume'

const props = defineProps<{
  file: File | null
  invalid?: boolean
  disabled?: boolean
  /** Space separated ids of the visible hint/error, from FormItem. */
  describedBy?: string
}>()

const emit = defineEmits<{ select: [file: File]; remove: [] }>()

const uid = useId()
const titleId = `${uid}-title`
const hintId = `${uid}-hint`
const prefixId = `${uid}-prefix`

const input = ref<HTMLInputElement | null>(null)
const dropzone = ref<HTMLElement | null>(null)
const removeButton = ref<{ $el: HTMLElement } | null>(null)
const dragging = ref(false)

// Keep keyboard focus on a live control when the dropzone and the file card swap.
watch(
  () => props.file,
  (file, previous) => {
    if (!!file === !!previous) return
    nextTick(() => {
      if (file) removeButton.value?.$el.focus()
      else dropzone.value?.focus()
    })
  },
)

function pick() {
  if (!props.disabled) input.value?.click()
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
  if (file && !props.disabled) emit('select', file)
}
</script>

<template>
  <div
    v-if="file"
    class="resume-file"
    :class="{ 'resume-file--invalid': invalid }"
    role="group"
    aria-label="Selected resume"
    :aria-describedby="describedBy"
  >
    <i class="pi pi-file-pdf resume-file__icon" aria-hidden="true" />
    <div class="resume-file__info">
      <span class="resume-file__name">{{ file.name }}</span>
      <span class="resume-file__size">{{ formatFileSize(file.size) }}</span>
    </div>
    <Button
      ref="removeButton"
      icon="pi pi-times"
      severity="secondary"
      variant="text"
      rounded
      :aria-label="`Remove ${file.name}`"
      :disabled="disabled"
      @click="emit('remove')"
    />
  </div>

  <div
    v-else
    ref="dropzone"
    class="dropzone"
    :class="{ 'dropzone--active': dragging, 'dropzone--invalid': invalid }"
    role="button"
    tabindex="0"
    :aria-labelledby="`${prefixId} ${titleId}`"
    :aria-describedby="[describedBy, hintId].filter(Boolean).join(' ')"
    :aria-invalid="invalid ? 'true' : undefined"
    :aria-disabled="disabled ? 'true' : undefined"
    @click="pick"
    @keydown.enter.prevent="pick"
    @keydown.space.prevent="pick"
    @dragover.prevent="dragging = true"
    @dragleave.prevent="dragging = false"
    @drop.prevent="onDrop"
  >
    <span :id="prefixId" class="visually-hidden">Resume (PDF):</span>
    <i class="pi pi-upload dropzone__icon" aria-hidden="true" />
    <span :id="titleId" class="dropzone__title">Drag a PDF here or click to choose a file</span>
    <span :id="hintId" class="dropzone__hint"
      >Up to {{ formatFileSize(MAX_RESUME_SIZE_BYTES) }}</span
    >
  </div>

  <span class="visually-hidden" role="status">{{
    file ? `Selected ${file.name}, ${formatFileSize(file.size)}` : ''
  }}</span>

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
.dropzone--active {
  border-color: var(--p-primary-color);
  background: var(--p-highlight-background);
}

.dropzone:focus-visible {
  border-color: var(--p-primary-color);
  outline: 2px solid var(--p-primary-color);
  outline-offset: 2px;
}

.resume-file:focus {
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
