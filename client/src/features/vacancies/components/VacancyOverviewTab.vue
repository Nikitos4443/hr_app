<script setup lang="ts">
import { computed } from 'vue'

import { formatDate, formatSalaryRange } from '@/shared/utils/format'

import { employmentTypeLabel } from '../lib/labels'
import type { Vacancy } from '../types/vacancy'

const props = defineProps<{ vacancy: Vacancy }>()

const facts = computed(() => [
  { label: 'Employment type', value: employmentTypeLabel(props.vacancy.employment_type) },
  {
    label: 'Experience',
    value:
      props.vacancy.experience_years_min != null
        ? `From ${props.vacancy.experience_years_min} years`
        : '—',
  },
  {
    label: 'Salary',
    value: formatSalaryRange(
      props.vacancy.salary_min,
      props.vacancy.salary_max,
      props.vacancy.salary_currency,
    ),
  },
  { label: 'Deadline', value: formatDate(props.vacancy.deadline_at) },
])

const lists = computed(() =>
  [
    { title: 'Responsibilities', items: props.vacancy.responsibilities },
    { title: 'Requirements', items: props.vacancy.requirements },
    { title: 'Nice to have', items: props.vacancy.nice_to_have },
  ].filter((list) => list.items.length > 0),
)
</script>

<template>
  <div class="overview">
    <dl class="overview__facts">
      <div v-for="fact in facts" :key="fact.label" class="overview__fact">
        <dt>{{ fact.label }}</dt>
        <dd>{{ fact.value }}</dd>
      </div>
    </dl>

    <section v-if="vacancy.description" class="overview__section">
      <h2>Description</h2>
      <p class="overview__description">{{ vacancy.description }}</p>
    </section>

    <section v-for="list in lists" :key="list.title" class="overview__section">
      <h2>{{ list.title }}</h2>
      <ul>
        <li v-for="item in list.items" :key="item">{{ item }}</li>
      </ul>
    </section>
  </div>
</template>

<style scoped>
.overview {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 800px;
}

.overview__facts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin: 0;
}

.overview__fact {
  padding: 12px 16px;
  border: 1px solid var(--p-content-border-color);
  border-radius: 10px;
}

.overview__fact dt {
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.overview__fact dd {
  margin: 2px 0 0;
  font-weight: 600;
}

.overview__section h2 {
  margin: 0 0 8px;
  font-size: 16px;
}

.overview__section ul {
  margin: 0;
  padding-left: 20px;
  line-height: 24px;
}

.overview__description {
  margin: 0;
  line-height: 24px;
  white-space: pre-line;
}
</style>
