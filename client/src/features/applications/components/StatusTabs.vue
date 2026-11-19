<script setup lang="ts">
import { STATUS_TABS } from '../lib/application-meta'
import type { ApplicationCounts, ApplicationStatus } from '../types/application'

const props = defineProps<{ active: ApplicationStatus | null; counts?: ApplicationCounts }>()

const emit = defineEmits<{ change: [status: ApplicationStatus | null] }>()

function countOf(value: ApplicationStatus | null): number | null {
  if (!props.counts) return null
  return value === null ? props.counts.all : props.counts[value]
}
</script>

<template>
  <div class="status-tabs" role="group" aria-label="Filter by status">
    <button
      v-for="tab in STATUS_TABS"
      :key="tab.label"
      type="button"
      class="status-tabs__chip"
      :class="{ 'status-tabs__chip--on': tab.value === active }"
      :aria-pressed="tab.value === active"
      @click="emit('change', tab.value)"
    >
      {{ tab.label
      }}<template v-if="countOf(tab.value) !== null"> · {{ countOf(tab.value) }}</template>
    </button>
  </div>
</template>

<style scoped>
.status-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.status-tabs__chip {
  padding: 6px 14px;
  border: 1px solid var(--p-content-border-color);
  border-radius: 99px;
  background: var(--p-content-background);
  color: var(--p-text-color);
  font: inherit;
  font-size: 14px;
  cursor: pointer;
}

.status-tabs__chip:hover {
  background: var(--p-content-hover-background);
}

.status-tabs__chip--on {
  border-color: var(--p-primary-color);
  background: var(--p-highlight-background);
  color: var(--p-highlight-color);
  font-weight: 600;
}

.status-tabs__chip:focus-visible {
  outline: 2px solid var(--p-primary-color);
  outline-offset: 2px;
}
</style>
