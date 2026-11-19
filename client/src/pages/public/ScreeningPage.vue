<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import Button from 'primevue/button'
import Skeleton from 'primevue/skeleton'
import Tag from 'primevue/tag'

import {
  ScreeningEndState,
  ScreeningProgress,
  TextAnswer,
  VideoAnswer,
  formatLimit,
  useScreeningFlow,
} from '@/features/screening'
import { ErrorState } from '@/shared/ui'

const route = useRoute()
const token = computed(() => String(route.params.token ?? ''))

const flow = useScreeningFlow(token)

const heading = ref<HTMLElement | null>(null)
const questionTag = computed(() => {
  const question = flow.current.value
  if (!question) return ''
  if (question.type !== 'video') return 'Text answer'
  return question.video_max_duration_sec
    ? `Video answer · up to ${formatLimit(question.video_max_duration_sec)}`
    : 'Video answer'
})

// Move focus to the new question and start from the top when the question changes.
watch(
  () => flow.current.value?.id,
  (id, previous) => {
    if (id == null || previous == null) return
    window.scrollTo({ top: 0 })
    nextTick(() => heading.value?.focus({ preventScroll: true }))
  },
)
</script>

<template>
  <div class="screening">
    <div v-if="flow.isLoading.value" class="screening__loading" role="status" aria-busy="true">
      <span class="visually-hidden">Loading the screening...</span>
      <Skeleton height="6px" />
      <Skeleton width="40%" height="24px" />
      <Skeleton height="64px" />
      <Skeleton height="200px" />
    </div>

    <ScreeningEndState
      v-else-if="flow.tokenState.value"
      :state="flow.tokenState.value"
      @retry="flow.retry"
    />

    <ErrorState
      v-else-if="flow.hasError.value"
      title="Could not load the screening"
      description="Check your connection and try again."
    >
      <Button label="Try again" icon="pi pi-refresh" @click="flow.retry" />
    </ErrorState>

    <ScreeningEndState
      v-else-if="flow.isComplete.value && !flow.finishing.value"
      state="completed"
    />

    <template v-else-if="flow.current.value">
      <header class="screening__header">
        <p class="screening__context">
          Screening<template v-if="flow.vacancyTitle.value">
            · {{ flow.vacancyTitle.value }}</template
          >
        </p>
        <ScreeningProgress
          :total="flow.total.value"
          :answered="flow.answeredCount.value"
          :label="flow.progressLabel.value"
        />
        <span class="screening__step">{{ flow.progressLabel.value }}</span>
      </header>

      <div class="screening__question">
        <Tag
          severity="secondary"
          :icon="flow.current.value.type === 'video' ? 'pi pi-video' : 'pi pi-align-left'"
          :value="questionTag"
        />
        <h1 ref="heading" class="screening__title" tabindex="-1">{{ flow.current.value.text }}</h1>
      </div>

      <VideoAnswer
        v-if="flow.current.value.type === 'video'"
        :key="flow.current.value.id"
        :token="token"
        :question="flow.current.value"
        @answered="flow.markAnswered(flow.current.value.id)"
      />
      <TextAnswer
        v-else
        :key="flow.current.value.id"
        :token="token"
        :question="flow.current.value"
        @answered="flow.markAnswered(flow.current.value.id)"
      />
    </template>
  </div>
</template>

<style scoped>
.screening {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 560px;
  width: 100%;
  margin: 0 auto;
}

.screening__loading {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px 0;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}

.screening__header {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.screening__context {
  margin: 0;
  font-weight: 600;
}

.screening__step {
  font-size: 12px;
  color: var(--p-text-muted-color);
}

.screening__question {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.screening__title:focus {
  outline: none;
}

.screening__title {
  margin: 0;
  font-size: 20px;
  line-height: 1.35;
}
</style>
