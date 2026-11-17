<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import { ScreeningEndState, type EndState } from '@/features/screening'

const END_STATES: readonly EndState[] = [
  'done',
  'invalid',
  'rejected',
  'completed',
  'in_review',
  'processing',
]

const route = useRoute()

const state = computed<EndState>(() => {
  const requested = String(route.query.state ?? 'done') as EndState
  return END_STATES.includes(requested) ? requested : 'done'
})
</script>

<template>
  <ScreeningEndState :state="state" />
</template>
