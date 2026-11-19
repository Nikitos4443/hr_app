<script setup lang="ts">
import { computed, watch } from 'vue'
import Button from 'primevue/button'
import Skeleton from 'primevue/skeleton'

import { EmptyState, ErrorState } from '@/shared/ui'

import { useApplicationsQuery } from '../api/applications.queries'
import { useApplicationActions } from '../composables/useApplicationActions'
import { useApplicationFilters } from '../composables/useApplicationFilters'
import { useBulkSelection } from '../composables/useBulkSelection'
import { useCandidateDrawer } from '../composables/useCandidateDrawer'
import type { ApplicationAction } from '../types/application'
import ApplicationFilters from './ApplicationFilters.vue'
import ApplicationsTable from './ApplicationsTable.vue'
import BulkActionBar from './BulkActionBar.vue'
import CandidateDrawer from './CandidateDrawer.vue'
import StatusTabs from './StatusTabs.vue'

const props = defineProps<{ vacancyId: number }>()

const filters = useApplicationFilters()
const list = useApplicationsQuery(() => props.vacancyId, filters.params)
const drawer = useCandidateDrawer()
const actions = useApplicationActions()

const items = computed(() => list.data.value?.items ?? [])
const total = computed(() => list.data.value?.total ?? 0)
const counts = computed(() => list.data.value?.counts)
const selection = useBulkSelection(computed(() => items.value.map((item) => item.id)))

// A shared link may point past the last page (e.g. after rows were rejected): go back to page 1.
watch(list.data, (data) => {
  if (data && data.items.length === 0 && data.total > 0 && filters.state.value.page > 1) {
    filters.setPage(1)
  }
})

function onBulk(action: ApplicationAction) {
  actions.runBulk(props.vacancyId, selection.ids.value, action, selection.clear)
}
</script>

<template>
  <div class="panel">
    <div v-if="list.isPending.value" class="panel__skeleton" role="status">
      <Skeleton v-for="n in 5" :key="n" height="52px" />
      <span class="panel__loading">Loading candidates…</span>
    </div>

    <ErrorState
      v-else-if="list.isError.value"
      title="Could not load candidates"
      description="Check your connection and try again."
    >
      <Button label="Retry" icon="pi pi-refresh" @click="list.refetch()" />
    </ErrorState>

    <EmptyState
      v-else-if="counts?.all === 0"
      icon="pi pi-users"
      title="No applications yet"
      description="Candidates appear here as soon as they apply through the public vacancy page."
    />

    <template v-else>
      <StatusTabs
        :active="filters.state.value.status"
        :counts="counts"
        @change="filters.update({ status: $event })"
      />
      <ApplicationFilters :state="filters.state.value" @change="filters.update" />

      <BulkActionBar
        v-if="selection.count.value > 0"
        :count="selection.count.value"
        :busy="actions.busy.value"
        @action="onBulk"
        @clear="selection.clear"
      />

      <EmptyState
        v-if="items.length === 0"
        icon="pi pi-search"
        title="Nothing found"
        description="No candidates match the current filters."
      >
        <Button
          v-if="filters.hasActiveFilters.value"
          label="Reset filters"
          severity="secondary"
          outlined
          @click="filters.reset()"
        />
      </EmptyState>
      <ApplicationsTable
        v-else
        :rows="items"
        :total="total"
        :page="filters.state.value.page"
        :loading="list.isFetching.value"
        :is-selected="selection.isSelected"
        :all-selected="selection.allSelected.value"
        :some-selected="selection.someSelected.value"
        @page="filters.setPage"
        @open="drawer.open"
        @toggle="selection.toggle"
        @toggle-all="selection.toggleAll"
      />
    </template>

    <CandidateDrawer :application-id="drawer.candidateId.value" @close="drawer.close" />
  </div>
</template>

<style scoped>
.panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.panel__skeleton {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.panel__loading {
  color: var(--p-text-muted-color);
  font-size: 13px;
}
</style>
