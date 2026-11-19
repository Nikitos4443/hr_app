<script setup lang="ts">
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'

import { usePublicVacancyQuery } from '@/features/vacancies'
import { CompanyAvatar, SkipLink, ThemeToggle } from '@/shared/ui'

const route = useRoute()

// The chat fills the viewport and scrolls internally.
const fixedHeight = computed(() => route.name === 'chat')

// Candidates see only the company brand; the chat route carries the vacancy id.
const showBrand = computed(() => route.name === 'chat')

const vacancyId = computed(() => {
  const id = Number(route.params.vacancyId)
  return Number.isFinite(id) && id > 0 ? id : null
})
const brandQuery = usePublicVacancyQuery(vacancyId)
const brand = computed(() => (showBrand.value ? (brandQuery.data.value?.company ?? null) : null))
</script>

<template>
  <div class="candidate-layout" :class="{ 'candidate-layout--fixed': fixedHeight }">
    <SkipLink />
    <header class="candidate-layout__header">
      <div v-if="brand" class="brand">
        <CompanyAvatar :name="brand" :size="32" />
        <span class="brand__name">{{ brand }}</span>
      </div>
      <ThemeToggle />
    </header>
    <main id="main" tabindex="-1" class="candidate-layout__main"><RouterView /></main>
  </div>
</template>

<style scoped>
.candidate-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-height: 100dvh;
}

.candidate-layout--fixed {
  height: 100dvh;
  overflow: hidden;
}

.candidate-layout__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 24px;
}

.candidate-layout--fixed .candidate-layout__header {
  padding-block: 8px;
}

.candidate-layout__main {
  flex: 1;
  width: 100%;
  max-width: 880px;
  margin: 0 auto;
  padding: 0 16px 48px;
}

.candidate-layout--fixed .candidate-layout__main {
  display: flex;
  flex-direction: column;
  min-height: 0;
  padding-bottom: calc(16px + env(safe-area-inset-bottom));
}

.brand {
  margin-right: auto;
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  font-weight: 600;
}

.brand__name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
