<script setup lang="ts">
import { computed } from 'vue'
import Button from 'primevue/button'
import Skeleton from 'primevue/skeleton'
import { useRoute } from 'vue-router'

import { ScreeningEndState, useScreeningEndState } from '@/features/screening'
import { ErrorState } from '@/shared/ui'

const route = useRoute()
const token = computed(() => String(route.params.token ?? ''))
const requested = computed(() =>
  typeof route.query.state === 'string' ? route.query.state : undefined,
)

const end = useScreeningEndState(token, requested)
</script>

<template>
  <div v-if="end.isLoading.value" class="end-skeleton" role="status" aria-busy="true">
    <span class="visually-hidden">Loading...</span>
    <Skeleton shape="circle" size="72px" />
    <Skeleton width="70%" height="32px" />
    <Skeleton width="90%" height="48px" />
  </div>

  <ErrorState
    v-else-if="end.hasError.value"
    title="Could not load this page"
    description="Check your connection and try again."
  >
    <Button label="Try again" icon="pi pi-refresh" @click="end.retry()" />
  </ErrorState>

  <ScreeningEndState v-else-if="end.state.value" :state="end.state.value" @retry="end.retry()" />
</template>

<style scoped>
.end-skeleton {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 40px 8px;
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
