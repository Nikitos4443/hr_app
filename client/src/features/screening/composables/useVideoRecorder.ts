import { onBeforeUnmount, ref, shallowRef, type MaybeRefOrGetter } from 'vue'

import { MAX_VIDEO_SIZE_BYTES } from '../lib/limits'
import { useCountdown } from './useCountdown'

export type RecorderState = 'idle' | 'denied' | 'ready' | 'recording' | 'review'
export type RecorderProblem = 'denied' | 'no-camera' | 'insecure' | 'unsupported' | 'too-large'

const MIME_CANDIDATES = [
  'video/webm;codecs=vp9,opus',
  'video/webm;codecs=vp8,opus',
  'video/webm',
  'video/mp4',
]
const VIDEO_BITS_PER_SECOND = 2_500_000

function pickMimeType(): string | undefined {
  if (typeof MediaRecorder === 'undefined') return undefined
  return MIME_CANDIDATES.find((type) => MediaRecorder.isTypeSupported(type))
}

function problemFromError(error: unknown): RecorderProblem {
  const name = error instanceof DOMException ? error.name : ''
  if (name === 'NotAllowedError' || name === 'SecurityError') return 'denied'
  if (name === 'NotFoundError' || name === 'OverconstrainedError') return 'no-camera'
  return 'unsupported'
}

export function useVideoRecorder(maxDurationSec: MaybeRefOrGetter<number>) {
  const state = ref<RecorderState>('idle')
  const problem = ref<RecorderProblem | null>(null)
  const stream = shallowRef<MediaStream | null>(null)
  const blob = shallowRef<Blob | null>(null)
  const previewUrl = ref<string | null>(null)
  const fileName = ref('answer.webm')

  let recorder: MediaRecorder | null = null
  let chunks: Blob[] = []

  const countdown = useCountdown(maxDurationSec, () => stopRecording())

  function releaseStream() {
    stream.value?.getTracks().forEach((track) => track.stop())
    stream.value = null
  }

  function revokePreview() {
    if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = null
  }

  function fail(reason: RecorderProblem) {
    releaseStream()
    problem.value = reason
    state.value = 'denied'
  }

  async function requestCamera() {
    problem.value = null
    if (!window.isSecureContext) return fail('insecure')
    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === 'undefined') {
      return fail('unsupported')
    }
    try {
      releaseStream()
      stream.value = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user' },
        audio: true,
      })
      state.value = 'ready'
    } catch (error) {
      fail(problemFromError(error))
    }
  }

  function startRecording() {
    const active = stream.value
    if (!active || state.value === 'recording') return
    chunks = []
    const mimeType = pickMimeType()
    try {
      recorder = new MediaRecorder(active, {
        ...(mimeType ? { mimeType } : {}),
        videoBitsPerSecond: VIDEO_BITS_PER_SECOND,
      })
    } catch {
      return fail('unsupported')
    }
    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) chunks.push(event.data)
    }
    recorder.onstop = () => {
      const type = recorder?.mimeType || mimeType || 'video/webm'
      recorder = null
      finalize(new Blob(chunks, { type }), `answer.${type.includes('mp4') ? 'mp4' : 'webm'}`)
    }
    recorder.start(1000)
    state.value = 'recording'
    countdown.start()
  }

  function stopRecording() {
    countdown.stop()
    if (recorder && recorder.state !== 'inactive') recorder.stop()
  }

  function finalize(video: Blob, name: string) {
    releaseStream()
    revokePreview()
    if (video.size > MAX_VIDEO_SIZE_BYTES) {
      blob.value = null
      problem.value = 'too-large'
      state.value = 'idle'
      return
    }
    problem.value = null
    blob.value = video
    fileName.value = name
    previewUrl.value = URL.createObjectURL(video)
    state.value = 'review'
  }

  function useFile(file: File) {
    if (!file.type.startsWith('video/')) return fail('unsupported')
    countdown.reset()
    finalize(file, file.name)
  }

  async function retake() {
    blob.value = null
    revokePreview()
    countdown.reset()
    await requestCamera()
  }

  function dismissProblem() {
    problem.value = null
    if (state.value === 'denied') state.value = 'idle'
  }

  onBeforeUnmount(() => {
    countdown.stop()
    if (recorder && recorder.state !== 'inactive') {
      recorder.onstop = null
      recorder.stop()
    }
    releaseStream()
    revokePreview()
  })

  return {
    state,
    problem,
    stream,
    blob,
    previewUrl,
    fileName,
    elapsedSec: countdown.elapsedSec,
    remainingSec: countdown.remainingSec,
    percentUsed: countdown.percent,
    requestCamera,
    startRecording,
    stopRecording,
    useFile,
    retake,
    dismissProblem,
  }
}
