<script setup lang="ts">
import { computed, ref } from 'vue'
import Message from 'primevue/message'
import ProgressBar from 'primevue/progressbar'

import { errorMessage } from '@/shared/api'

import { useUploadVideoAnswerMutation } from '../api/screening.queries'
import { useVideoRecorder } from '../composables/useVideoRecorder'
import { formatClock, formatMegabytes } from '../lib/format'
import {
  DEFAULT_VIDEO_MAX_DURATION_SEC,
  MAX_VIDEO_SIZE_BYTES,
  RECORDING_WARNING_SEC,
} from '../lib/limits'
import type { ScreeningQuestion } from '../types/screening'
import CameraDeniedState from './CameraDeniedState.vue'
import CameraPreview from './CameraPreview.vue'
import RecordControls from './RecordControls.vue'
import UploadingState from './UploadingState.vue'

const props = defineProps<{ token: string; question: ScreeningQuestion }>()
const emit = defineEmits<{ answered: [] }>()

const maxDuration = computed(
  () => props.question.video_max_duration_sec ?? DEFAULT_VIDEO_MAX_DURATION_SEC,
)
const recorder = useVideoRecorder(maxDuration)
const upload = useUploadVideoAnswerMutation(() => props.token)

const fileInput = ref<HTMLInputElement | null>(null)
const uploadPercent = ref(0)
const showUpload = ref(false)

const maxFileMb = Math.round(MAX_VIDEO_SIZE_BYTES / (1024 * 1024))
const isRecording = computed(() => recorder.state.value === 'recording')
const nearLimit = computed(
  () => isRecording.value && recorder.remainingSec.value <= RECORDING_WARNING_SEC,
)
const showPreview = computed(() =>
  ['idle', 'ready', 'recording', 'review'].includes(recorder.state.value),
)

const problemText = computed(() =>
  recorder.problem.value === 'too-large'
    ? `This video is larger than ${maxFileMb} MB. Record a shorter answer or upload a smaller file.`
    : '',
)

function pickFile() {
  fileInput.value?.click()
}

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (file) recorder.useFile(file)
}

function send() {
  const video = recorder.blob.value
  if (!video) return
  uploadPercent.value = 0
  showUpload.value = true
  upload.mutate(
    {
      questionId: props.question.id,
      video,
      onProgress: (percent) => {
        uploadPercent.value = percent
      },
    },
    { onSuccess: () => emit('answered') },
  )
}

function backToReview() {
  upload.reset()
  showUpload.value = false
}

async function retake() {
  backToReview()
  await recorder.retake()
}
</script>

<template>
  <section class="video-answer">
    <UploadingState
      v-if="showUpload"
      :percent="uploadPercent"
      :file-name="recorder.fileName.value"
      :size-bytes="recorder.blob.value?.size ?? 0"
      :failed="upload.isError.value"
      :error-text="errorMessage(upload.error.value, 'Could not upload the video.')"
      @retry="send"
      @back="backToReview"
    />

    <template v-else>
      <CameraDeniedState
        v-if="recorder.state.value === 'denied'"
        :problem="recorder.problem.value"
      />

      <Message v-if="problemText" severity="error" icon="pi pi-exclamation-circle" role="alert">
        {{ problemText }}
      </Message>

      <CameraPreview
        v-if="showPreview"
        :stream="recorder.stream.value"
        :src="recorder.previewUrl.value"
        :recording="isRecording"
        :elapsed-label="formatClock(recorder.elapsedSec.value)"
        :limit-label="formatClock(maxDuration)"
        caption="Camera is not on yet"
      />

      <div v-if="isRecording" class="video-answer__timer">
        <ProgressBar
          :value="recorder.percentUsed.value"
          :show-value="false"
          :aria-label="`${recorder.percentUsed.value}% of time used`"
        />
        <div class="video-answer__timer-row">
          <span>{{ formatClock(recorder.remainingSec.value) }} left</span>
          <span v-if="nearLimit" role="status">Recording stops automatically at the limit</span>
        </div>
      </div>

      <Message
        v-if="recorder.state.value === 'idle' && !problemText"
        severity="info"
        icon="pi pi-lightbulb"
      >
        Don't worry, you can record again. Up to {{ formatClock(maxDuration) }} is enough.
      </Message>
      <Message
        v-if="recorder.state.value === 'review'"
        severity="success"
        icon="pi pi-check-circle"
      >
        Recording is ready
        <template v-if="recorder.blob.value"
          >({{ formatMegabytes(recorder.blob.value.size) }})</template
        >. Watch it or record it again.
      </Message>

      <RecordControls
        :state="recorder.state.value"
        :max-file-mb="maxFileMb"
        @allow="recorder.requestCamera"
        @record="recorder.startRecording"
        @stop="recorder.stopRecording"
        @send="send"
        @retake="retake"
        @pick-file="pickFile"
      />
    </template>

    <input
      ref="fileInput"
      class="video-answer__file"
      type="file"
      accept="video/*"
      tabindex="-1"
      aria-hidden="true"
      @change="onFileChange"
    />
  </section>
</template>

<style scoped>
.video-answer {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.video-answer__timer {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.video-answer__timer-row {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  font-size: 12px;
  color: var(--p-text-muted-color);
  font-variant-numeric: tabular-nums;
}

.video-answer__file {
  display: none;
}
</style>
