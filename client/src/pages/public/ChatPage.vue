<script setup lang="ts">
import { computed } from 'vue'
import Button from 'primevue/button'
import { useRoute } from 'vue-router'

import { ChatWindow } from '@/features/ai-chat'
import { usePublicVacancyQuery } from '@/features/vacancies'

const route = useRoute()
const vacancyId = computed(() => Number(route.params.vacancyId))
const query = usePublicVacancyQuery(vacancyId)
const company = computed(() => query.data.value?.company ?? null)
</script>

<template>
  <div class="chat-page">
    <RouterLink :to="{ name: 'public-vacancy', params: { vacancyId } }">
      <Button
        label="Back to the vacancy"
        icon="pi pi-arrow-left"
        severity="secondary"
        variant="text"
        size="small"
      />
    </RouterLink>
    <ChatWindow :key="vacancyId" :vacancy-id="vacancyId" :company="company" />
  </div>
</template>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
