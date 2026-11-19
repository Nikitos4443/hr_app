<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from 'vue'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'

import type { ApplicationFilterState } from '../composables/useApplicationFilters'
import { SORT_OPTIONS } from '../lib/application-meta'

const props = defineProps<{ state: ApplicationFilterState }>()

const emit = defineEmits<{ change: [patch: Partial<ApplicationFilterState>] }>()

const SEARCH_DEBOUNCE_MS = 300

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
  <div class="app-filters" role="search">
    <IconField class="app-filters__search">
      <InputIcon class="pi pi-search" />
      <InputText
        :model-value="search"
        placeholder="Name or email"
        aria-label="Search candidates"
        fluid
        @update:model-value="onSearch"
      />
    </IconField>
    <Select
      :model-value="state.sort"
      :options="SORT_OPTIONS"
      option-label="label"
      option-value="value"
      aria-label="Sort candidates"
      class="app-filters__sort"
      @update:model-value="emit('change', { sort: $event })"
    />
  </div>
</template>

<style scoped>
.app-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.app-filters__search {
  flex: 1 1 220px;
  width: 260px;
}

.app-filters__sort {
  flex: 0 1 200px;
}
</style>
