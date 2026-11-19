<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router'
import Button from 'primevue/button'

import { useNotify } from '@/shared/composables/useNotify'
import { AiStatus, StatusTag } from '@/shared/ui'
import { formatDate, formatSalaryRange } from '@/shared/utils/format'

import type { Vacancy } from '../types/vacancy'

const props = defineProps<{ vacancy: Vacancy }>()

const router = useRouter()
const notify = useNotify()

async function copyLink() {
  const link = `${location.origin}/vacancies/${props.vacancy.id}`
  try {
    await navigator.clipboard.writeText(link)
    notify.success('Link copied')
  } catch {
    notify.error(new Error('Copy the link manually: ' + link), 'Could not copy the link')
  }
}
</script>

<template>
  <header class="head">
    <nav class="head__crumbs" aria-label="Breadcrumb">
      <RouterLink :to="{ name: 'vacancies' }">Vacancies</RouterLink>
      <i class="pi pi-chevron-right" aria-hidden="true" />
      <span aria-current="page">{{ vacancy.title }}</span>
    </nav>

    <div class="head__row">
      <div class="head__main">
        <h1 class="head__title">{{ vacancy.title }}</h1>
        <div class="head__meta">
          <StatusTag kind="vacancy" :status="vacancy.status" />
          <AiStatus :status="vacancy.selection_status" />
          <span v-if="vacancy.deadline_at" class="head__fact">
            <i class="pi pi-calendar" aria-hidden="true" />
            Deadline: {{ formatDate(vacancy.deadline_at) }}
          </span>
          <span v-if="vacancy.location" class="head__fact">
            <i class="pi pi-map-marker" aria-hidden="true" />
            {{ vacancy.location }}
          </span>
          <span v-if="vacancy.salary_min != null || vacancy.salary_max != null" class="head__fact">
            <i class="pi pi-wallet" aria-hidden="true" />
            {{ formatSalaryRange(vacancy.salary_min, vacancy.salary_max, vacancy.salary_currency) }}
          </span>
        </div>
      </div>

      <div class="head__actions">
        <Button label="Copy public link" icon="pi pi-link" severity="secondary" @click="copyLink" />
        <Button
          label="Edit"
          icon="pi pi-pencil"
          @click="router.push({ name: 'vacancy-edit', params: { id: vacancy.id } })"
        />
      </div>
    </div>
  </header>
</template>

<style scoped>
.head {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.head__crumbs {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.head__crumbs a {
  color: inherit;
}

.head__crumbs i {
  font-size: 10px;
}

.head__row {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.head__main {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.head__title {
  margin: 0;
  font-size: 24px;
  line-height: 32px;
}

.head__meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 12px;
}

.head__fact {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.head__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
