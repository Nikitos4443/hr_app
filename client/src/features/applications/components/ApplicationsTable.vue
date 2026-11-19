<script setup lang="ts">
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import Column from 'primevue/column'
import DataTable, { type DataTablePageEvent } from 'primevue/datatable'

import { ScoreBar, StatusTag } from '@/shared/ui'
import { initials } from '@/shared/utils/format'

import { PAGE_SIZE } from '../composables/useApplicationFilters'
import { candidateName, screeningLabel } from '../lib/application-meta'
import type { ApplicationListItem } from '../types/application'

const props = defineProps<{
  rows: ApplicationListItem[]
  total: number
  page: number
  loading?: boolean
  isSelected: (id: number) => boolean
  allSelected: boolean
  someSelected: boolean
}>()

const emit = defineEmits<{
  page: [page: number]
  open: [id: number]
  toggle: [id: number]
  'toggle-all': []
}>()

function onPage(event: DataTablePageEvent) {
  emit('page', event.page + 1)
}

function rowClass(row: ApplicationListItem) {
  return props.isSelected(row.id) ? 'row-selected' : ''
}
</script>

<template>
  <div class="table-card focus-ring" tabindex="0" role="region" aria-label="Candidates table">
    <DataTable
      :value="rows"
      data-key="id"
      lazy
      :loading="loading"
      :row-class="rowClass"
      :paginator="total > PAGE_SIZE"
      :rows="PAGE_SIZE"
      :first="(page - 1) * PAGE_SIZE"
      :total-records="total"
      current-page-report-template="{first}–{last} of {totalRecords}"
      paginator-template="CurrentPageReport PrevPageLink PageLinks NextPageLink"
      table-style="min-width: 1100px"
      @page="onPage"
    >
      <Column header-style="width: 3rem">
        <template #header>
          <Checkbox
            binary
            :model-value="allSelected"
            :indeterminate="someSelected"
            aria-label="Select all candidates on this page"
            @update:model-value="emit('toggle-all')"
          />
        </template>
        <template #body="{ data }">
          <Checkbox
            binary
            :model-value="isSelected(data.id)"
            :aria-label="`Select ${candidateName(data)}`"
            @update:model-value="emit('toggle', data.id)"
          />
        </template>
      </Column>

      <Column header="Rank" header-style="width: 4.5rem">
        <template #body="{ data }">
          <b class="num">{{ data.rank ?? '—' }}</b>
        </template>
      </Column>

      <Column header="Candidate">
        <template #body="{ data }">
          <div class="candidate">
            <Avatar :label="initials(candidateName(data))" shape="circle" aria-hidden="true" />
            <div class="candidate__text">
              <button type="button" class="candidate__name" @click="emit('open', data.id)">
                {{ candidateName(data) }}
              </button>
              <span v-if="data.full_name" class="candidate__email">{{ data.email }}</span>
            </div>
          </div>
        </template>
      </Column>

      <Column header="Resume (0–100)" header-style="width: 12rem">
        <template #body="{ data }">
          <ScoreBar
            v-if="data.resume_score != null"
            :value="data.resume_score"
            label="Resume score"
          />
          <span v-else-if="data.resume_status && data.resume_status !== 'done'" class="muted">
            Analysing…
          </span>
          <span v-else class="muted">—</span>
        </template>
      </Column>

      <Column header="Screening">
        <template #body="{ data }">
          <StatusTag
            kind="screening"
            :status="data.screening_state"
            :label="screeningLabel(data)"
          />
        </template>
      </Column>

      <Column header="Status">
        <template #body="{ data }"><StatusTag kind="application" :status="data.status" /></template>
      </Column>

      <Column header="AI summary">
        <template #body="{ data }">
          <p v-if="data.ai_summary" class="summary">
            <i class="pi pi-sparkles summary__icon" aria-hidden="true" />
            <span>{{ data.ai_summary }}</span>
          </p>
          <span v-else class="muted">—</span>
        </template>
      </Column>

      <Column header-style="width: 4rem">
        <template #body="{ data }">
          <Button
            icon="pi pi-chevron-right"
            severity="secondary"
            text
            rounded
            :aria-label="`Open ${candidateName(data)}`"
            @click="emit('open', data.id)"
          />
        </template>
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

.num {
  font-variant-numeric: tabular-nums;
}

.candidate {
  display: flex;
  align-items: center;
  gap: 12px;
}

.candidate__text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.candidate__name {
  padding: 0;
  border: 0;
  background: none;
  color: var(--p-text-color);
  font: inherit;
  font-weight: 600;
  text-align: left;
  cursor: pointer;
}

.candidate__name:hover {
  color: var(--p-primary-color);
}

.candidate__email {
  color: var(--p-text-muted-color);
  font-size: 12px;
}

.muted {
  color: var(--p-text-muted-color);
}

.summary {
  display: -webkit-box;
  max-width: 320px;
  margin: 0;
  overflow: hidden;
  font-size: 13px;
  line-height: 19px;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.summary__icon {
  margin-right: 6px;
  color: var(--p-highlight-color);
  font-size: 12px;
}

:deep(.row-selected td) {
  background: var(--p-highlight-background);
}
</style>
