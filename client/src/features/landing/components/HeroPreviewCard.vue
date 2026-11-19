<script setup lang="ts">
import Avatar from 'primevue/avatar'

import { AiStatus, AiSummary, ScoreBar } from '@/shared/ui'

// Static demo data, not fetched from the API
const CANDIDATES = [
  { initials: 'OM', name: 'Olena Melnyk', note: 'Screening completed', score: 92 },
  { initials: 'AK', name: 'Andrii Kravchenko', note: 'In progress · 2 of 4', score: 84 },
  { initials: 'IS', name: 'Iryna Shevchenko', note: 'Invited', score: 71 },
]
</script>

<template>
  <div class="hero-preview-card" aria-hidden="true">
    <div class="hero-preview-card__head">
      <span class="hero-preview-card__title">Senior Vue.js Developer</span>
      <AiStatus status="running" />
    </div>
    <ul class="hero-preview-card__list">
      <li v-for="c in CANDIDATES" :key="c.name" class="hero-preview-card__row">
        <Avatar :label="c.initials" shape="circle" />
        <div class="hero-preview-card__who">
          <b>{{ c.name }}</b>
          <span class="hero-preview-card__note">{{ c.note }}</span>
        </div>
        <ScoreBar class="hero-preview-card__score" :value="c.score" :label="c.name" />
      </li>
    </ul>
    <AiSummary>
      Three candidates match the requirements. Weaker ones automatically received a polite
      rejection.
    </AiSummary>
  </div>
</template>

<style scoped>
.hero-preview-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  max-width: 560px;
  padding: 24px;
  border: 1px solid var(--p-content-border-color);
  border-radius: 16px;
  background: var(--p-content-background);
  box-shadow: 0 8px 32px color-mix(in srgb, var(--p-text-color) 8%, transparent);
}

.hero-preview-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.hero-preview-card__title {
  font-size: 18px;
  font-weight: 600;
}

.hero-preview-card__list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.hero-preview-card__row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.hero-preview-card__who {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
}

.hero-preview-card__note {
  font-size: 12px;
  color: var(--p-text-muted-color);
}

.hero-preview-card__score {
  width: 150px;
  flex-shrink: 0;
}

@media (max-width: 480px) {
  .hero-preview-card {
    padding: 16px;
  }

  .hero-preview-card__score {
    width: 100px;
    min-width: 100px;
  }
}
</style>
