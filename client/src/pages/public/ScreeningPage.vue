<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'
import Tag from 'primevue/tag'

import {
  ScreeningEndState,
  ScreeningProgress,
  TextAnswer,
  VideoAnswer,
  useScreeningFlow,
} from '@/features/screening'
import { ErrorState } from '@/shared/ui'

const route = useRoute()
const token = computed(() => String(route.params.token ?? ''))

const flow = useScreeningFlow(token)
</script>

<template>
  <div class="screening">
    <div v-if="flow.isLoading.value" class="screening__loading">
      <ProgressSpinner aria-label="Loading screening" />
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
          :value="flow.current.value.type === 'video' ? 'Video answer' : 'Text answer'"
        />
        <h1 class="screening__title">{{ flow.current.value.text }}</h1>
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
  margin: 0 auto;
}

.screening__loading {
  display: grid;
  place-items: center;
  padding: 64px 0;
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

.screening__title {
  margin: 0;
  font-size: 20px;
  line-height: 1.35;
}
</style>
