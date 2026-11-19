<script setup lang="ts">
import Button from 'primevue/button'
import Skeleton from 'primevue/skeleton'
import Tag from 'primevue/tag'

import { EmptyState, ErrorState } from '@/shared/ui'

import { useVacancyQuestionsQuery } from '../api/questions.queries'

const props = defineProps<{ vacancyId: number }>()

const questions = useVacancyQuestionsQuery(() => props.vacancyId)

function formatSeconds(total: number): string {
  const minutes = Math.floor(total / 60)
  const seconds = String(total % 60).padStart(2, '0')
  return `${minutes}:${seconds}`
}
</script>

<template>
  <div v-if="questions.isPending.value" class="questions__skeleton" role="status">
    <Skeleton v-for="n in 3" :key="n" height="64px" />
    <span class="questions__loading">Loading questions…</span>
  </div>

  <ErrorState
    v-else-if="questions.isError.value"
    title="Could not load screening questions"
    description="Check your connection and try again."
  >
    <Button label="Retry" icon="pi pi-refresh" @click="questions.refetch()" />
  </ErrorState>

  <EmptyState
    v-else-if="!questions.data.value?.length"
    icon="pi pi-comments"
    title="No screening questions"
    description="Candidates are not asked any questions after the resume review for this vacancy."
  />

  <ol v-else class="questions">
    <li
      v-for="(question, index) in questions.data.value"
      :key="question.id ?? index"
      class="question"
    >
      <span class="question__num">{{ index + 1 }}</span>
      <div class="question__body">
        <span class="question__text">{{ question.text }}</span>
        <Tag
          v-if="question.type === 'video'"
          :value="`Video · up to ${formatSeconds(question.video_max_duration_sec ?? 0)}`"
          icon="pi pi-video"
          severity="secondary"
        />
        <Tag v-else value="Text answer" icon="pi pi-align-left" severity="secondary" />
      </div>
    </li>
  </ol>
</template>

<style scoped>
.questions__skeleton {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.questions__loading {
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.questions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 800px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.question {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--p-content-border-color);
  border-radius: 10px;
}

.question__num {
  display: grid;
  flex: none;
  place-items: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--p-highlight-background);
  color: var(--p-highlight-color);
  font-size: 13px;
  font-weight: 700;
}

.question__body {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.question__text {
  font-weight: 600;
}
</style>
