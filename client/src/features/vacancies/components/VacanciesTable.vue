<script setup lang="ts">
import { RouterLink } from 'vue-router'
import Column from 'primevue/column'
import DataTable, { type DataTablePageEvent } from 'primevue/datatable'

import { formatDate, formatSalaryRange } from '@/shared/utils/format'
import { AiStatus, StatusTag } from '@/shared/ui'

import { PAGE_SIZE, type SortOrder } from '../composables/useVacancyFilters'
import { employmentTypeLabel } from '../lib/labels'
import type { Vacancy } from '../types/vacancy'
import VacancyRowActions from './VacancyRowActions.vue'

const props = defineProps<{
  rows: Vacancy[]
  total: number
  page: number
  sort: SortOrder | null
}>()

const emit = defineEmits<{
  page: [page: number]
  'toggle-sort': []
}>()

function onPage(event: DataTablePageEvent) {
  emit('page', event.page + 1)
}

const sortIcon = () =>
  props.sort === 'asc'
    ? 'pi-sort-amount-up-alt'
    : props.sort === 'desc'
      ? 'pi-sort-amount-down'
      : 'pi-sort-alt'
</script>

<template>
  <div class="table-card">
    <DataTable
      :value="rows"
      data-key="id"
      lazy
      :paginator="total > PAGE_SIZE"
      :rows="PAGE_SIZE"
      :first="(page - 1) * PAGE_SIZE"
      :total-records="total"
      current-page-report-template="{first}–{last} of {totalRecords}"
      paginator-template="CurrentPageReport PrevPageLink PageLinks NextPageLink"
      table-style="min-width: 960px"
      @page="onPage"
    >
      <Column header="Vacancy">
        <template #body="{ data }">
          <div class="cell-title">
            <RouterLink
              :to="{ name: 'vacancy-detail', params: { id: data.id } }"
              class="cell-title__link"
            >
              {{ data.title }}
            </RouterLink>
            <span v-if="data.location" class="cell-title__meta">
              <i class="pi pi-map-marker" aria-hidden="true" />
              {{ data.location }}
            </span>
          </div>
        </template>
      </Column>
      <Column header="Employment type">
        <template #body="{ data }">{{ employmentTypeLabel(data.employment_type) }}</template>
      </Column>
      <Column header="Salary">
        <template #body="{ data }">
          {{ formatSalaryRange(data.salary_min, data.salary_max, data.salary_currency) }}
        </template>
      </Column>
      <Column>
        <template #header>
          <button
            type="button"
            class="sort-button"
            :aria-label="`Sort by deadline${sort ? ', ' + (sort === 'asc' ? 'ascending' : 'descending') : ''}`"
            @click="emit('toggle-sort')"
          >
            Deadline
            <i :class="['pi', sortIcon()]" aria-hidden="true" />
          </button>
        </template>
        <template #body="{ data }">{{ formatDate(data.deadline_at) }}</template>
      </Column>
      <Column header="Status">
        <template #body="{ data }"><StatusTag kind="vacancy" :status="data.status" /></template>
      </Column>
      <Column header="AI selection">
        <template #body="{ data }"><AiStatus :status="data.selection_status" /></template>
      </Column>
      <Column header-style="width: 7rem">
        <template #body="{ data }"><VacancyRowActions :vacancy="data" /></template>
      </Column>
    </DataTable>
  </div>
</template>

<style scoped>
.table-card {
  overflow-x: auto;
  border: 1px solid var(--p-content-border-color);
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-background);
}

.cell-title {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.cell-title__link {
  font-weight: 600;
  color: var(--p-text-color);
  text-decoration: none;
}

.cell-title__link:hover {
  color: var(--p-primary-color);
}

.cell-title__meta {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.sort-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0;
  border: 0;
  background: none;
  color: inherit;
  font: inherit;
  cursor: pointer;
}
</style>
