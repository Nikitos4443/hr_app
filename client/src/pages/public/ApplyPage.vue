<script setup lang="ts">
import { computed, ref } from 'vue'
import Button from 'primevue/button'
import Skeleton from 'primevue/skeleton'
import { useRoute, useRouter } from 'vue-router'

import { ApplyForm } from '@/features/applications'
import { isVacancyClosed, usePublicVacancyQuery, VacancyClosedBanner } from '@/features/vacancies'
import { isApiError } from '@/shared/api'
import { CompanyAvatar, EmptyState, ErrorState } from '@/shared/ui'

const route = useRoute()
const router = useRouter()
const vacancyId = computed(() => Number(route.params.vacancyId))
const query = usePublicVacancyQuery(vacancyId)
const vacancy = computed(() => query.data.value)
const closed = computed(() => (vacancy.value ? isVacancyClosed(vacancy.value) : false))
const notFound = computed(() => isApiError(query.error.value) && query.error.value.status === 404)
const submitted = ref(false)
</script>

<template>
  <section class="apply">
    <div v-if="query.isPending.value" class="apply__skeleton" role="status" aria-busy="true">
      <span class="visually-hidden">Loading the application form...</span>
      <Skeleton height="40px" width="60%" />
      <Skeleton height="28px" width="30%" />
      <Skeleton height="44px" />
      <Skeleton height="120px" />
      <Skeleton height="48px" />
    </div>

    <EmptyState
      v-else-if="notFound"
      icon="pi pi-search"
      title="Vacancy not found"
      description="The link may be outdated or the vacancy was removed."
    >
      <Button label="Go back" icon="pi pi-arrow-left" severity="secondary" @click="router.back()" />
    </EmptyState>

    <ErrorState
      v-else-if="query.isError.value"
      title="Couldn't load the application form"
      description="Check your connection and try again."
    >
      <Button label="Try again" icon="pi pi-refresh" @click="query.refetch()" />
    </ErrorState>

    <template v-else-if="vacancy">
      <header class="apply__head">
        <CompanyAvatar :name="vacancy.company" :size="40" />
        <div>
          <div class="apply__company">{{ vacancy.company }}</div>
          <div class="apply__title">{{ vacancy.title }}</div>
        </div>
      </header>

      <template v-if="!submitted">
        <h1 class="apply__heading">Apply</h1>
        <p class="apply__lead">Just your email and resume, no registration needed.</p>
      </template>

      <VacancyClosedBanner v-if="closed" :company="vacancy.company" />
      <ApplyForm v-else :vacancy-id="vacancyId" @success="submitted = true" />

      <RouterLink
        v-if="!submitted"
        class="apply__back"
        :to="{ name: 'public-vacancy', params: { vacancyId } }"
      >
        <i class="pi pi-arrow-left" aria-hidden="true" /> Back to the vacancy
      </RouterLink>
    </template>
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

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}

.apply__skeleton {
  display: flex;
  flex-direction: column;
  gap: 16px;
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
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 44px;
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
