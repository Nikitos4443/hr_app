<script setup lang="ts">
import { computed } from 'vue'
import Button from 'primevue/button'
import Skeleton from 'primevue/skeleton'
import { useRoute, useRouter } from 'vue-router'

import { PublicVacancyView, usePublicVacancyQuery } from '@/features/vacancies'
import { isApiError } from '@/shared/api'
import { EmptyState, ErrorState } from '@/shared/ui'

const route = useRoute()
const router = useRouter()
const vacancyId = computed(() => Number(route.params.vacancyId))
const query = usePublicVacancyQuery(vacancyId)

const notFound = computed(() => isApiError(query.error.value) && query.error.value.status === 404)

function openApply() {
  router.push({ name: 'apply', params: { vacancyId: vacancyId.value } })
}

function openChat() {
  router.push({ name: 'chat', params: { vacancyId: vacancyId.value } })
}
</script>

<template>
  <div v-if="query.isPending.value" class="page-skeleton" role="status" aria-busy="true">
    <span class="visually-hidden">Loading the vacancy...</span>
    <Skeleton width="40%" height="44px" />
    <Skeleton width="80%" height="36px" />
    <Skeleton height="120px" />
    <Skeleton height="200px" />
  </div>

  <EmptyState
    v-else-if="notFound"
    icon="pi pi-search"
    title="Vacancy not found"
    description="The link may be outdated or the vacancy was removed."
  />

  <ErrorState
    v-else-if="query.isError.value"
    title="Couldn't load the vacancy"
    description="Check your connection and try again."
  >
    <Button label="Try again" icon="pi pi-refresh" @click="query.refetch()" />
  </ErrorState>

  <PublicVacancyView
    v-else-if="query.data.value"
    :vacancy="query.data.value"
    @apply="openApply"
    @chat="openChat"
  />
</template>

<style scoped>
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}

.page-skeleton {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 820px;
  margin: 24px auto 0;
}
</style>
