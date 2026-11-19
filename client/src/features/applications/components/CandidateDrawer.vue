<script setup lang="ts">
import { computed } from 'vue'
import Button from 'primevue/button'
import Drawer from 'primevue/drawer'
import Skeleton from 'primevue/skeleton'

import { isNotFound } from '@/shared/api'
import { AiSummary, ErrorState } from '@/shared/ui'

import { useApplicationQuery } from '../api/applications.queries'
import { useApplicationActions } from '../composables/useApplicationActions'
import { candidateName } from '../lib/application-meta'
import type { ApplicationAction } from '../types/application'
import ApplicationTimeline from './candidate/ApplicationTimeline.vue'
import CandidateHeader from './candidate/CandidateHeader.vue'
import ResumeAnalysisCard from './candidate/ResumeAnalysisCard.vue'
import ScreeningAnswers from './candidate/ScreeningAnswers.vue'
import CandidateActions from './CandidateActions.vue'

const props = defineProps<{ applicationId: number | null }>()

const emit = defineEmits<{ close: [] }>()

const query = useApplicationQuery(() => props.applicationId)
const actions = useApplicationActions()

const visible = computed({
  get: () => props.applicationId !== null,
  set: (value) => {
    if (!value) emit('close')
  },
})

function onAction(action: ApplicationAction) {
  const application = query.data.value
  if (application) actions.run({ id: application.id, name: candidateName(application) }, action)
}
</script>

<template>
  <Drawer
    v-model:visible="visible"
    position="right"
    :header="query.data.value ? candidateName(query.data.value) : 'Candidate'"
    :style="{ width: 'min(900px, 100vw)' }"
  >
    <div v-if="query.isPending.value" class="drawer__loading" role="status">
      <Skeleton width="60%" height="32px" />
      <Skeleton height="120px" />
      <Skeleton height="200px" />
      <span class="drawer__sr">Loading candidate…</span>
    </div>

    <ErrorState
      v-else-if="query.isError.value"
      :title="
        isNotFound(query.error.value) ? 'Candidate not found' : 'Could not load the candidate'
      "
      :description="
        isNotFound(query.error.value)
          ? 'This application no longer exists.'
          : 'Check your connection and try again.'
      "
    >
      <Button
        v-if="!isNotFound(query.error.value)"
        label="Retry"
        icon="pi pi-refresh"
        @click="query.refetch()"
      />
      <Button v-else label="Close" severity="secondary" @click="emit('close')" />
    </ErrorState>

    <div v-else-if="query.data.value" class="drawer__content">
      <CandidateHeader :application="query.data.value" />
      <CandidateActions
        :status="query.data.value.status"
        :resume-status="query.data.value.resume.status"
        :busy="actions.busy.value"
        @action="onAction"
      />
      <hr class="drawer__rule" />
      <ResumeAnalysisCard :resume="query.data.value.resume" />
      <hr class="drawer__rule" />
      <ScreeningAnswers :answers="query.data.value.answers" />
      <hr class="drawer__rule" />
      <div class="drawer__split">
        <AiSummary title="Overall AI summary">
          {{ query.data.value.ai_summary ?? 'The overall ranking is not available yet.' }}
        </AiSummary>
        <ApplicationTimeline :events="query.data.value.timeline" />
      </div>
    </div>
  </Drawer>
</template>

<style scoped>
.drawer__loading,
.drawer__content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.drawer__sr {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
}

.drawer__rule {
  width: 100%;
  margin: 0;
  border: 0;
  border-top: 1px solid var(--p-content-border-color);
}

.drawer__split {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 24px;
  align-items: start;
}

@media (max-width: 720px) {
  .drawer__split {
    grid-template-columns: 1fr;
  }
}
</style>
