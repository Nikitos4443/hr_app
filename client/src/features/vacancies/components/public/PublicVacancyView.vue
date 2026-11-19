<script setup lang="ts">
import { computed } from 'vue'
import Button from 'primevue/button'
import Tag from 'primevue/tag'

import { CompanyAvatar } from '@/shared/ui'

import {
  daysLeft,
  formatDate,
  formatDaysLeft,
  formatSalary,
  isVacancyClosed,
} from '../../lib/vacancy-format'
import type { PublicVacancy } from '../../types/public-vacancy'
import VacancyClosedBanner from './VacancyClosedBanner.vue'

const props = defineProps<{ vacancy: PublicVacancy }>()

const emit = defineEmits<{ apply: []; chat: [] }>()

const closed = computed(() => isVacancyClosed(props.vacancy))
const salary = computed(() => formatSalary(props.vacancy))
const deadline = computed(() =>
  props.vacancy.deadline_at ? formatDate(props.vacancy.deadline_at) : null,
)
const remaining = computed(() =>
  props.vacancy.deadline_at ? daysLeft(props.vacancy.deadline_at) : null,
)
const websiteUrl = computed(() =>
  props.vacancy.company_website
    ? `https://${props.vacancy.company_website.replace(/^https?:\/\//, '')}`
    : null,
)

const sections = computed(() =>
  [
    { title: 'Responsibilities', icon: 'pi pi-check', items: props.vacancy.responsibilities },
    { title: 'Requirements', icon: 'pi pi-check', items: props.vacancy.requirements },
    { title: 'Nice to have', icon: 'pi pi-plus-circle', items: props.vacancy.nice_to_have },
  ].filter((section) => section.items.length > 0),
)
</script>

<template>
  <article class="vacancy">
    <header class="vacancy__head">
      <div class="vacancy__company">
        <CompanyAvatar :name="vacancy.company" />
        <div>
          <div class="vacancy__company-name">{{ vacancy.company }}</div>
          <a
            v-if="websiteUrl"
            class="vacancy__link"
            :href="websiteUrl"
            target="_blank"
            rel="noopener noreferrer"
          >
            <i class="pi pi-globe" aria-hidden="true" /> {{ vacancy.company_website }}
            <span class="vacancy__sr">(opens in a new tab)</span>
          </a>
        </div>
      </div>

      <h1 class="vacancy__title">{{ vacancy.title }}</h1>

      <ul class="vacancy__meta">
        <li v-if="vacancy.location">
          <i class="pi pi-map-marker" aria-hidden="true" /> {{ vacancy.location }}
        </li>
        <li v-if="vacancy.employment_type">
          <i class="pi pi-clock" aria-hidden="true" /> {{ vacancy.employment_type }}
        </li>
        <li v-if="vacancy.experience_years_min != null">
          <i class="pi pi-briefcase" aria-hidden="true" /> From
          {{ vacancy.experience_years_min }} years
        </li>
      </ul>
    </header>

    <VacancyClosedBanner v-if="closed" :company="vacancy.company" :closed-on="deadline" />

    <section v-if="salary || (deadline && !closed)" class="vacancy__facts">
      <div v-if="salary" class="vacancy__fact">
        <span class="vacancy__fact-label">Salary</span>
        <span class="vacancy__fact-value">{{ salary }}</span>
      </div>
      <div v-if="deadline && !closed" class="vacancy__fact">
        <span class="vacancy__fact-label">Applications open until</span>
        <span class="vacancy__fact-value">{{ deadline }}</span>
        <Tag v-if="remaining != null" severity="info" :value="formatDaysLeft(remaining)" />
      </div>
    </section>

    <section v-if="vacancy.description" class="vacancy__section">
      <h2>About the role</h2>
      <p class="vacancy__text">{{ vacancy.description }}</p>
    </section>

    <section v-for="section in sections" :key="section.title" class="vacancy__section">
      <h2>{{ section.title }}</h2>
      <ul class="vacancy__list">
        <li v-for="item in section.items" :key="item">
          <i :class="section.icon" aria-hidden="true" />
          <span>{{ item }}</span>
        </li>
      </ul>
    </section>

    <section v-if="vacancy.company_description" class="vacancy__section">
      <h2>About {{ vacancy.company }}</h2>
      <p class="vacancy__text">{{ vacancy.company_description }}</p>
    </section>

    <footer class="vacancy__cta">
      <Button
        label="Apply"
        icon="pi pi-send"
        size="large"
        :disabled="closed"
        :aria-describedby="closed ? 'vacancy-closed-note' : undefined"
        @click="emit('apply')"
      />
      <p v-if="closed" id="vacancy-closed-note" class="vacancy__closed-note">
        Applications for this vacancy are no longer accepted.
      </p>
      <Button
        label="Ask the assistant"
        icon="pi pi-sparkles"
        severity="secondary"
        variant="outlined"
        size="large"
        @click="emit('chat')"
      />
    </footer>
  </article>
</template>

<style scoped>
.vacancy {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 820px;
  margin: 0 auto;
  padding-top: 8px;
}

.vacancy__head {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.vacancy__company {
  display: flex;
  align-items: center;
  gap: 12px;
}

.vacancy__company-name {
  font-weight: 600;
}

.vacancy__link {
  position: relative;
  display: inline-block;
  padding: 4px 0;
  color: var(--p-text-muted-color);
  font-size: 13px;
  text-decoration: none;
}

.vacancy__sr {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}

.vacancy__title {
  margin: 0;
  font-size: clamp(24px, 5vw, 34px);
  line-height: 1.2;
  overflow-wrap: anywhere;
}

.vacancy__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 20px;
  margin: 0;
  padding: 0;
  list-style: none;
  color: var(--p-text-muted-color);
}

.vacancy__meta li {
  display: flex;
  align-items: center;
  gap: 6px;
}

.vacancy__facts {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.vacancy__fact {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  flex: 1 1 220px;
  padding: 14px 16px;
  border: 1px solid var(--p-content-border-color);
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-background);
}

.vacancy__fact-label {
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.vacancy__fact-value {
  font-size: 18px;
  font-weight: 600;
}

.vacancy__section h2 {
  margin: 0 0 8px;
  font-size: 18px;
}

.vacancy__text {
  margin: 0;
  line-height: 1.6;
  white-space: pre-line;
}

.vacancy__list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.vacancy__list li {
  display: flex;
  gap: 10px;
  line-height: 1.5;
}

.vacancy__list i {
  margin-top: 4px;
  color: var(--p-primary-color);
  font-size: 12px;
}

.vacancy__cta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
}

.vacancy__closed-note {
  margin: 0;
  color: var(--p-text-muted-color);
}

@media (max-width: 600px) {
  .vacancy__cta {
    position: sticky;
    bottom: 0;
    z-index: 5;
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
    margin: 0 -24px;
    padding: 12px 24px calc(12px + env(safe-area-inset-bottom));
    border-top: 1px solid var(--p-content-border-color);
    background: var(--p-content-background);
  }
}
</style>
