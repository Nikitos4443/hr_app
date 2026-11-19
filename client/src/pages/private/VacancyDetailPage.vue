<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Button from 'primevue/button'
import Skeleton from 'primevue/skeleton'

import { isNotFound } from '@/shared/api'
import { ErrorState } from '@/shared/ui'
import { CandidatesPanel, useApplicationCountsQuery } from '@/features/applications'
import {
  useVacancyQuery,
  useVacancyQuestionsQuery,
  VacancyDetailHeader,
  VacancyOverviewTab,
  VacancyQuestionsTab,
  VacancyTabs,
  type VacancyTabKey,
} from '@/features/vacancies'

const TABS: VacancyTabKey[] = ['overview', 'candidates', 'questions']

const route = useRoute()
const router = useRouter()

const vacancyId = computed(() => Number(route.params.id))
const vacancy = useVacancyQuery(vacancyId)
const counts = useApplicationCountsQuery(vacancyId)
const questions = useVacancyQuestionsQuery(vacancyId)

const tab = computed<VacancyTabKey>(() => {
  const raw = Array.isArray(route.query.tab) ? route.query.tab[0] : route.query.tab
  return TABS.find((key) => key === raw) ?? 'candidates'
})

// Switching tabs drops list filters and the open candidate; they belong to the Candidates tab.
function selectTab(next: VacancyTabKey) {
  router.replace({ query: next === 'candidates' ? {} : { tab: next } })
}
</script>

<template>
  <div class="detail">
    <div v-if="vacancy.isPending.value" class="detail__skeleton" role="status">
      <Skeleton width="50%" height="32px" />
      <Skeleton height="40px" />
      <Skeleton height="240px" />
      <span class="detail__loading">Loading vacancy…</span>
    </div>

    <ErrorState
      v-else-if="vacancy.isError.value"
      :title="isNotFound(vacancy.error.value) ? 'Vacancy not found' : 'Could not load the vacancy'"
      :description="
        isNotFound(vacancy.error.value)
          ? 'It may have been deleted, or you do not have access to it.'
          : 'Check your connection and try again.'
      "
    >
      <Button
        v-if="!isNotFound(vacancy.error.value)"
        label="Retry"
        icon="pi pi-refresh"
        @click="vacancy.refetch()"
      />
      <Button
        v-else
        label="Back to vacancies"
        severity="secondary"
        @click="router.push({ name: 'vacancies' })"
      />
    </ErrorState>

    <template v-else-if="vacancy.data.value">
      <VacancyDetailHeader :vacancy="vacancy.data.value" />
      <VacancyTabs
        :model-value="tab"
        :candidates="counts.data.value?.all"
        :questions="questions.data.value?.length"
        @update:model-value="selectTab"
      >
        <template #overview><VacancyOverviewTab :vacancy="vacancy.data.value" /></template>
        <template #candidates><CandidatesPanel :vacancy-id="vacancy.data.value.id" /></template>
        <template #questions><VacancyQuestionsTab :vacancy-id="vacancy.data.value.id" /></template>
      </VacancyTabs>
    </template>
  </div>
</template>

<style scoped>
.detail {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail__skeleton {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail__loading {
  color: var(--p-text-muted-color);
  font-size: 13px;
}
</style>
