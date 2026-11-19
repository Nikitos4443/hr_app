<script setup lang="ts">
import { computed } from 'vue'
import Button from 'primevue/button'
import Message from 'primevue/message'

import { AiSummary, ScoreBar } from '@/shared/ui'

import type { ResumeDetail } from '../../types/application'

const props = defineProps<{ resume: ResumeDetail }>()

const score = computed(() => props.resume.score ?? props.resume.review?.score ?? null)
const done = computed(() => props.resume.status === 'done')
const notAResume = computed(() => props.resume.review?.is_resume === false)
</script>

<template>
  <section class="resume" aria-labelledby="resume-title">
    <h3 id="resume-title" class="resume__title">
      <i class="pi pi-sparkles" aria-hidden="true" /> AI resume review
    </h3>

    <Message v-if="!resume.status" severity="secondary" :closable="false">
      No resume was found for this application.
    </Message>
    <Message v-else-if="!done" severity="info" :closable="false">
      The resume is still being analysed. Check back in a moment.
    </Message>

    <template v-else>
      <Message v-if="notAResume" severity="warn" :closable="false">
        The uploaded file does not look like a resume.
      </Message>

      <div class="resume__grid">
        <div v-if="score != null" class="resume__score">
          <span class="resume__score-label">Overall score</span>
          <span class="resume__score-value">{{ Math.round(score) }}</span>
          <span class="resume__score-label">out of 100</span>
          <ScoreBar :value="score" :show-value="false" label="Resume score" />
        </div>
        <AiSummary v-if="resume.review?.description" title="Review">
          {{ resume.review.description }}
        </AiSummary>
      </div>
    </template>

    <div class="resume__file">
      <i class="pi pi-file-pdf resume__file-icon" aria-hidden="true" />
      <div class="resume__file-text">
        <span class="resume__file-name">Resume (PDF)</span>
        <span v-if="!resume.file_url" class="resume__file-hint">File is not available</span>
      </div>
      <Button
        v-if="resume.file_url"
        as="a"
        :href="resume.file_url"
        target="_blank"
        rel="noopener noreferrer"
        label="View PDF"
        icon="pi pi-external-link"
        severity="secondary"
        size="small"
      />
    </div>
  </section>
</template>

<style scoped>
.resume {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.resume__title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 16px;
}

.resume__title i {
  color: var(--p-highlight-color);
}

.resume__grid {
  display: grid;
  grid-template-columns: 200px minmax(0, 1fr);
  gap: 16px;
  align-items: start;
}

@media (max-width: 640px) {
  .resume__grid {
    grid-template-columns: 1fr;
  }
}

.resume__score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 16px;
  border-radius: 10px;
  background: var(--p-highlight-background);
  text-align: center;
}

.resume__score-label {
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.resume__score-value {
  color: var(--p-highlight-color);
  font-size: 48px;
  font-weight: 700;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.resume__file {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: 1px solid var(--p-content-border-color);
  border-radius: 10px;
}

.resume__file-icon {
  color: var(--p-text-muted-color);
  font-size: 24px;
}

.resume__file-text {
  display: flex;
  flex: 1;
  flex-direction: column;
}

.resume__file-name {
  font-weight: 600;
}

.resume__file-hint {
  color: var(--p-text-muted-color);
  font-size: 13px;
}
</style>
