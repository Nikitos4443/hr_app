<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from 'vue'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'

import type { VacancyFilterState } from '../composables/useVacancyFilters'
import {
  EMPLOYMENT_TYPE_OPTIONS,
  SELECTION_STATUS_OPTIONS,
  VACANCY_STATUS_OPTIONS,
} from '../lib/labels'

const props = defineProps<{ state: VacancyFilterState; active: boolean }>()

const emit = defineEmits<{
  change: [patch: Partial<VacancyFilterState>]
  reset: []
}>()

const SEARCH_DEBOUNCE_MS = 250

const search = ref(props.state.search)
let timer: ReturnType<typeof setTimeout> | undefined

watch(
  () => props.state.search,
  (value) => {
    if (value !== search.value) search.value = value
  },
)

function onSearch(value: string | undefined) {
  search.value = value ?? ''
  clearTimeout(timer)
  timer = setTimeout(() => emit('change', { search: search.value.trim() }), SEARCH_DEBOUNCE_MS)
}

onBeforeUnmount(() => clearTimeout(timer))
</script>

<template>
  <div class="filters" role="search">
    <IconField class="filters__search">
      <InputIcon class="pi pi-search" />
      <InputText
        :model-value="search"
        placeholder="Search by title or location"
        aria-label="Search vacancies"
        fluid
        @update:model-value="onSearch"
      />
    </IconField>
    <Select
      :model-value="state.status"
      :options="VACANCY_STATUS_OPTIONS"
      option-label="label"
      option-value="value"
      placeholder="Status: all"
      show-clear
      aria-label="Filter by status"
      class="filters__select"
      @update:model-value="emit('change', { status: $event ?? null })"
    />
    <Select
      :model-value="state.employmentType"
      :options="EMPLOYMENT_TYPE_OPTIONS"
      option-label="label"
      option-value="value"
      placeholder="Employment type: all"
      show-clear
      aria-label="Filter by employment type"
      class="filters__select"
      @update:model-value="emit('change', { employmentType: $event ?? null })"
    />
    <Select
      :model-value="state.selection"
      :options="SELECTION_STATUS_OPTIONS"
      option-label="label"
      option-value="value"
      placeholder="AI selection: all"
      show-clear
      aria-label="Filter by AI selection"
      class="filters__select"
      @update:model-value="emit('change', { selection: $event ?? null })"
    />
    <Button
      label="Reset"
      icon="pi pi-filter-slash"
      severity="secondary"
      text
      class="filters__reset"
      :disabled="!active"
      @click="emit('reset')"
    />
  </div>
</template>

<style scoped>
.filters {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
}

.filters__search {
  flex: 1 1 260px;
  max-width: 320px;
}

.filters__select {
  flex: 0 1 200px;
}

.filters__reset {
  margin-left: auto;
}
</style>
