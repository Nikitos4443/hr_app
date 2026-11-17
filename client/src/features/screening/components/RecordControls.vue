<script setup lang="ts">
import Button from 'primevue/button'

import type { RecorderState } from '../composables/useVideoRecorder'

defineProps<{ state: RecorderState; maxFileMb: number }>()

const emit = defineEmits<{
  allow: []
  record: []
  stop: []
  send: []
  retake: []
  pickFile: []
}>()
</script>

<template>
  <div class="controls">
    <template v-if="state === 'idle'">
      <Button
        label="Allow camera and start"
        icon="pi pi-video"
        size="large"
        fluid
        @click="emit('allow')"
      />
      <Button
        :label="`Upload a video file (up to ${maxFileMb} MB)`"
        icon="pi pi-upload"
        severity="secondary"
        size="large"
        fluid
        @click="emit('pickFile')"
      />
    </template>

    <template v-else-if="state === 'denied'">
      <Button label="Try again" icon="pi pi-refresh" size="large" fluid @click="emit('allow')" />
      <Button
        label="Upload a video file"
        icon="pi pi-upload"
        severity="secondary"
        size="large"
        fluid
        @click="emit('pickFile')"
      />
    </template>

    <Button
      v-else-if="state === 'ready'"
      label="Start recording"
      icon="pi pi-circle-fill"
      size="large"
      fluid
      @click="emit('record')"
    />

    <Button
      v-else-if="state === 'recording'"
      label="Finish recording"
      icon="pi pi-stop-circle"
      severity="danger"
      size="large"
      fluid
      @click="emit('stop')"
    />

    <template v-else>
      <Button
        label="Send and continue"
        icon="pi pi-send"
        size="large"
        fluid
        @click="emit('send')"
      />
      <Button
        label="Record again"
        icon="pi pi-replay"
        severity="secondary"
        size="large"
        fluid
        @click="emit('retake')"
      />
    </template>
  </div>
</template>

<style scoped>
.controls {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
