<script setup lang="ts">
import { computed } from 'vue'
import Button from 'primevue/button'
import { useRoute } from 'vue-router'

import { ApplyForm } from '@/features/applications'
import { isVacancyClosed, usePublicVacancyQuery, VacancyClosedBanner } from '@/features/vacancies'
import { EmptyState } from '@/shared/ui'

const route = useRoute()
const vacancyId = computed(() => Number(route.params.vacancyId))
const query = usePublicVacancyQuery(vacancyId)
const vacancy = computed(() => query.data.value)
const closed = computed(() => (vacancy.value ? isVacancyClosed(vacancy.value) : false))
</script>

<template>
  <section class="apply">
    <header v-if="vacancy" class="apply__head">
      <span class="apply__avatar" aria-hidden="true">{{ vacancy.company.slice(0, 2) }}</span>
      <div>
        <div class="apply__company">{{ vacancy.company }}</div>
        <div class="apply__title">{{ vacancy.title }}</div>
      </div>
    </header>

    <h1 class="apply__heading">Apply</h1>
    <p class="apply__lead">Just your email and resume, no registration needed.</p>

    <VacancyClosedBanner v-if="vacancy && closed" :company="vacancy.company" />

    <EmptyState
      v-else-if="query.isError.value"
      icon="pi pi-search"
      title="Vacancy not found"
      description="The link may be outdated or the vacancy was removed."
    >
      <RouterLink :to="{ name: 'home' }"><Button label="Back to home" /></RouterLink>
    </EmptyState>

    <ApplyForm v-else :vacancy-id="vacancyId" />

    <RouterLink
      v-if="vacancy"
      class="apply__back"
      :to="{ name: 'public-vacancy', params: { vacancyId } }"
    >
      <i class="pi pi-arrow-left" aria-hidden="true" /> Back to the vacancy
    </RouterLink>
  </section>
</template>

<style scoped>
.apply {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 560px;
  margin: 8px auto 0;
  padding: 24px;
  border: 1px solid var(--p-content-border-color);
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-background);
}

.apply__head {
  display: flex;
  align-items: center;
  gap: 12px;
}

.apply__avatar {
  display: grid;
  place-items: center;
  flex: none;
  width: 40px;
  height: 40px;
  border-radius: var(--p-content-border-radius);
  background: var(--p-highlight-background);
  color: var(--p-highlight-color);
  font-weight: 700;
  text-transform: uppercase;
}

.apply__company {
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.apply__title {
  font-weight: 600;
  overflow-wrap: anywhere;
}

.apply__heading {
  margin: 0;
  font-size: 24px;
}

.apply__lead {
  margin: -8px 0 0;
  color: var(--p-text-muted-color);
}

.apply__back {
  align-self: flex-start;
  color: var(--p-text-muted-color);
  font-size: 13px;
  text-decoration: none;
}

@media (max-width: 600px) {
  .apply {
    padding: 16px;
  }
}
</style>
