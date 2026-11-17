<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Button from 'primevue/button'
import Skeleton from 'primevue/skeleton'

import { ErrorState, PageHeader } from '@/shared/ui'
import { isNotFound } from '@/shared/api'
import { useVacancyQuery, VacancyForm } from '@/features/vacancies'

const route = useRoute()

const vacancyId = computed(() => (route.params.id ? Number(route.params.id) : null))
const isEdit = computed(() => vacancyId.value !== null)
const vacancy = useVacancyQuery(vacancyId)
</script>

<template>
  <div class="form-page">
    <PageHeader
      :title="isEdit ? 'Edit vacancy' : 'New vacancy'"
      :subtitle="isEdit ? vacancy.data.value?.title : undefined"
    />

    <div v-if="isEdit && vacancy.isPending.value" class="form-page__skeleton">
      <Skeleton v-for="n in 3" :key="n" height="160px" />
    </div>

    <ErrorState
      v-else-if="isEdit && vacancy.isError.value"
      :title="isNotFound(vacancy.error.value) ? 'Vacancy not found' : 'Could not load the vacancy'"
      :description="
        isNotFound(vacancy.error.value)
          ? 'It may have been deleted.'
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
        label="Back to vacancies"
        severity="secondary"
        outlined
        @click="$router.push({ name: 'vacancies' })"
      />
    </ErrorState>

    <VacancyForm v-else :key="vacancyId ?? 'new'" :vacancy="vacancy.data.value" />
  </div>
</template>

<style scoped>
.form-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-page__skeleton {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 1000px;
}
</style>
