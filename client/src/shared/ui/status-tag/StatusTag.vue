<script setup lang="ts" generic="K extends StatusKind">
import Tag from 'primevue/tag'
import { computed } from 'vue'

import { STATUS_META, type StatusKind, type StatusMap, type StatusMeta } from './status-meta'

const props = defineProps<{
  kind: K
  status: StatusMap[K]
  /** Overrides the text, e.g. "In progress 2/4" */
  label?: string
}>()

const meta = computed<StatusMeta | undefined>(
  () => (STATUS_META[props.kind] as Record<string, StatusMeta>)[props.status as string],
)
</script>

<template>
  <!-- A status is always icon + text + color; color is never the only signal -->
  <Tag v-if="meta" :value="label ?? meta.label" :icon="meta.icon" :severity="meta.severity" />
</template>
