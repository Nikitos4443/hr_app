<script setup lang="ts">
import { computed } from 'vue'
import Message from 'primevue/message'

import type { RecorderProblem } from '../composables/useVideoRecorder'

const props = defineProps<{ problem: RecorderProblem | null }>()

const content = computed(() => {
  switch (props.problem) {
    case 'no-camera':
      return {
        title: 'No camera found.',
        text: 'Connect a camera or microphone and try again, or upload a video file instead.',
      }
    case 'insecure':
      return {
        title: 'Camera needs a secure connection.',
        text: 'Open this page over HTTPS to record in the browser, or upload a video file instead.',
      }
    case 'unsupported':
      return {
        title: 'Recording is not supported in this browser.',
        text: 'Try a recent version of Chrome, Edge, Firefox or Safari, or upload a video file instead.',
      }
    default:
      return {
        title: 'Camera access is blocked.',
        text: 'Allow the camera and microphone for this site, then press "Try again".',
      }
  }
})
</script>

<template>
  <div class="denied">
    <Message severity="warn" icon="pi pi-video" role="alert">
      <strong>{{ content.title }}</strong> {{ content.text }}
    </Message>
    <ol v-if="problem === 'denied'" class="denied__steps">
      <li>Click the lock or camera icon next to the address bar.</li>
      <li>Set Camera and Microphone to "Allow".</li>
      <li>Press "Try again" below.</li>
    </ol>
    <p class="denied__hint">
      No camera? Record a video on your phone and upload the file, it counts the same.
    </p>
  </div>
</template>

<style scoped>
.denied {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.denied__steps {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin: 0;
  padding-left: 20px;
  color: var(--p-text-muted-color);
}

.denied__hint {
  margin: 0;
  color: var(--p-text-muted-color);
}
</style>
