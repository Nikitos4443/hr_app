<script setup lang="ts">
import { computed } from 'vue'
import Button from 'primevue/button'
import Skeleton from 'primevue/skeleton'

import { EmptyState, ErrorState, PageHeader } from '@/shared/ui'
import {
  useVacanciesQuery,
  useVacancyFilters,
  VacanciesTable,
  VacancyFilters,
} from '@/features/vacancies'

const vacancies = useVacanciesQuery()
const data = computed(() => vacancies.data.value)
const filters = useVacancyFilters(data)

const subtitle = computed(() => {
  const total = data.value?.length
  if (total === undefined) return undefined
  return `${total} ${total === 1 ? 'vacancy' : 'vacancies'}`
})
</script>

<template>
  <div class="vacancies-page">
    <PageHeader title="Vacancies" :subtitle="subtitle">
      <Button
        label="Create vacancy"
        icon="pi pi-plus"
        @click="$router.push({ name: 'vacancy-new' })"
      />
    </PageHeader>

    <div v-if="vacancies.isPending.value" class="vacancies-page__skeleton" role="status">
      <Skeleton v-for="n in 5" :key="n" height="44px" />
      <span class="vacancies-page__loading">Loading vacancies…</span>
    </div>

    <ErrorState
      v-else-if="vacancies.isError.value"
      title="Could not load vacancies"
      description="Check your connection and try again."
    >
      <Button label="Retry" icon="pi pi-refresh" @click="vacancies.refetch()" />
    </ErrorState>

    <EmptyState
      v-else-if="!data?.length"
      icon="pi pi-briefcase"
      title="No vacancies yet"
      description="Create your first vacancy. AI selection starts once applications arrive."
    >
      <Button
        label="Create vacancy"
        icon="pi pi-plus"
        @click="$router.push({ name: 'vacancy-new' })"
      />
    </EmptyState>

    <template v-else>
      <VacancyFilters
        :state="filters.state.value"
        :active="filters.hasActiveFilters.value"
        @change="filters.update"
        @reset="filters.reset"
      />
      <EmptyState
        v-if="!filters.filtered.value.length"
        icon="pi pi-search"
        title="Nothing found"
        description="No vacancies match the current filters."
      >
        <Button label="Reset filters" severity="secondary" outlined @click="filters.reset()" />
      </EmptyState>
      <VacanciesTable
        v-else
        :rows="filters.pageRows.value"
        :total="filters.filtered.value.length"
        :page="filters.currentPage.value"
        :sort="filters.state.value.sort"
        @page="filters.setPage"
        @toggle-sort="filters.toggleSort"
      />
    </template>
  </div>
</template>

<style scoped>
.vacancies-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.vacancies-page__skeleton {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.vacancies-page__loading {
  color: var(--p-text-muted-color);
  font-size: 13px;
}
</style>
