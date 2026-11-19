<script setup lang="ts">
import { ref, watchEffect } from 'vue'

const props = defineProps<{
  stream: MediaStream | null
  src: string | null
  recording: boolean
  elapsedLabel: string
  limitLabel: string
  icon?: string
  caption?: string
  reviewCaption?: string
}>()

const liveEl = ref<HTMLVideoElement | null>(null)

watchEffect(() => {
  if (liveEl.value) liveEl.value.srcObject = props.stream
})
</script>

<template>
  <div class="preview">
    <video
      v-if="src"
      class="preview__video"
      :src="src"
      controls
      playsinline
      aria-label="Recorded answer"
    />
    <video
      v-else-if="stream"
      ref="liveEl"
      class="preview__video preview__video--mirror"
      autoplay
      muted
      playsinline
      aria-label="Camera preview"
    />
    <div v-else class="preview__placeholder">
      <i :class="icon ?? 'pi pi-video'" aria-hidden="true" />
      <span v-if="caption">{{ caption }}</span>
    </div>

    <span v-if="src && reviewCaption" class="preview__pill preview__pill--start">{{
      reviewCaption
    }}</span>

    <template v-if="recording">
      <span class="preview__pill preview__pill--start">
        <span class="preview__dot" />
        Recording {{ elapsedLabel }}
      </span>
      <span class="preview__pill preview__pill--end">Limit {{ limitLabel }}</span>
    </template>
  </div>
</template>

<style scoped>
.preview {
  position: relative;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  border-radius: var(--p-content-border-radius);
  background: var(--p-surface-900);
  color: var(--p-surface-0);
}

.preview__video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview__video--mirror {
  transform: scaleX(-1);
}

.preview__placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 100%;
  padding: 16px;
  text-align: center;
  opacity: 0.8;
}

.preview__placeholder i {
  font-size: 32px;
}

.preview__pill {
  position: absolute;
  top: 10px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-variant-numeric: tabular-nums;
  background: color-mix(in srgb, var(--p-surface-950) 65%, transparent);
  color: var(--p-surface-0);
}

.preview__pill--start {
  left: 10px;
}

.preview__pill--end {
  right: 10px;
}

.preview__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--p-red-500);
  animation: blink 1s infinite;
}

@keyframes blink {
  50% {
    opacity: 0.3;
  }
}

@media (prefers-reduced-motion: reduce) {
  .preview__dot {
    animation: none;
  }
}
</style>
