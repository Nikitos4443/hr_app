<script setup lang="ts">
import type { EndState } from '../../types/screening'
import AlreadyCompleted from './AlreadyCompleted.vue'
import PoliteRejection from './PoliteRejection.vue'
import ResumeProcessing from './ResumeProcessing.vue'
import ScreeningDone from './ScreeningDone.vue'
import TokenInvalid from './TokenInvalid.vue'
import UnderReview from './UnderReview.vue'

defineProps<{ state: EndState }>()
const emit = defineEmits<{ retry: [] }>()
</script>

<template>
  <ScreeningDone v-if="state === 'done'" />
  <TokenInvalid v-else-if="state === 'invalid'" />
  <AlreadyCompleted v-else-if="state === 'completed'" />
  <UnderReview v-else-if="state === 'in_review'" />
  <PoliteRejection v-else-if="state === 'rejected'" />
  <ResumeProcessing v-else @retry="emit('retry')" />
</template>
