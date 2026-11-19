<script setup lang="ts">
import { computed } from 'vue'
import Button from 'primevue/button'
import Skeleton from 'primevue/skeleton'
import { useRoute, useRouter } from 'vue-router'

import { ChatWindow } from '@/features/ai-chat'
import { usePublicVacancyQuery } from '@/features/vacancies'
import { isApiError } from '@/shared/api'
import { EmptyState } from '@/shared/ui'

const route = useRoute()
const router = useRouter()
const vacancyId = computed(() => Number(route.params.vacancyId))
const query = usePublicVacancyQuery(vacancyId)
const company = computed(() => query.data.value?.company ?? null)
const notFound = computed(() => isApiError(query.error.value) && query.error.value.status === 404)
</script>

<template>
  <div class="chat-page">
    <RouterLink
      v-if="!notFound"
      :to="{ name: 'public-vacancy', params: { vacancyId } }"
      custom
      v-slot="{ href, navigate }"
    >
      <Button
        as="a"
        :href="href"
        class="chat-page__back"
        label="Back to the vacancy"
        icon="pi pi-arrow-left"
        severity="secondary"
        variant="text"
        size="small"
        @click="navigate"
      />
    </RouterLink>

    <div v-if="query.isPending.value" class="chat-page__loading" role="status" aria-busy="true">
      <span class="visually-hidden">Loading the assistant...</span>
      <Skeleton height="100%" />
    </div>

    <EmptyState
      v-else-if="notFound"
      icon="pi pi-search"
      title="Vacancy not found"
      description="The link may be outdated or the vacancy was removed."
    >
      <Button label="Go back" icon="pi pi-arrow-left" severity="secondary" @click="router.back()" />
    </EmptyState>

    <ChatWindow v-else :key="vacancyId" :vacancy-id="vacancyId" :company="company" />
  </div>
</template>

<style scoped>
.chat-page {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 8px;
  min-height: 0;
}

.chat-page__back {
  align-self: flex-start;
  min-height: 44px;
  text-decoration: none;
}

.chat-page__loading {
  flex: 1;
  min-height: 240px;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}
</style>
