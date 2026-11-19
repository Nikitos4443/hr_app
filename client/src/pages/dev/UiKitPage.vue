<script setup lang="ts">
import Button from 'primevue/button'

import { useTheme } from '@/shared/composables/useTheme'
import { AiStatus, AiSummary, ScoreBar, StatusTag } from '@/shared/ui'

const { isDark, toggleTheme } = useTheme()
</script>

<template>
  <main style="padding: 2rem; display: flex; flex-direction: column; gap: 1.5rem; max-width: 720px">
    <h1 style="margin: 0">HR App · shared/ui</h1>
    <Button
      label="Toggle theme"
      :icon="isDark ? 'pi pi-sun' : 'pi pi-moon'"
      severity="secondary"
      @click="toggleTheme"
    />

    <section style="display: flex; flex-wrap: wrap; gap: 8px">
      <StatusTag kind="vacancy" status="open" />
      <StatusTag kind="vacancy" status="closed" />
      <StatusTag kind="application" status="pending" />
      <StatusTag kind="application" status="invited" />
      <StatusTag kind="application" status="shortlisted" />
      <StatusTag kind="application" status="rejected" />
      <StatusTag kind="screening" status="in_progress" label="In progress 2/4" />
      <StatusTag kind="screening" status="completed" />
    </section>

    <section style="display: flex; flex-wrap: wrap; gap: 8px">
      <AiStatus status="pending" />
      <AiStatus status="running" />
      <AiStatus status="done" />
      <AiStatus status="failed" />
    </section>

    <section style="display: flex; flex-direction: column; gap: 12px">
      <ScoreBar :value="92" />
      <ScoreBar :value="71" />
      <ScoreBar :value="38" />
    </section>

    <AiSummary>
      Strong experience with Vue 3 and TypeScript; lacks SSR experience. Recommend inviting to
      screening.
    </AiSummary>
  </main>
</template>
