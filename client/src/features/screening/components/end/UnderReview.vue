<script setup lang="ts">
import EndStateCard from './EndStateCard.vue'

const steps = [
  { label: 'Application received', done: true },
  { label: 'Resume reviewed', done: true },
  { label: 'Screening completed', done: true },
  { label: 'Answers being evaluated', done: false, note: 'Usually takes up to 2 working days' },
]
</script>

<template>
  <EndStateCard
    icon="pi pi-sparkles"
    tone="primary"
    title="We are reviewing your application"
    description="Thanks for your patience. Here is where things stand."
  >
    <ol class="steps">
      <li v-for="step in steps" :key="step.label" class="steps__item">
        <span class="steps__dot" :class="{ 'steps__dot--todo': !step.done }">
          <i :class="step.done ? 'pi pi-check' : 'pi pi-ellipsis-h'" aria-hidden="true" />
        </span>
        <span class="steps__text">
          <strong>{{ step.label }}</strong>
          <small v-if="step.note">{{ step.note }}</small>
        </span>
      </li>
    </ol>
  </EndStateCard>
</template>

<style scoped>
.steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  margin: 0;
  padding: 0;
  list-style: none;
  text-align: left;
}

.steps__item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.steps__dot {
  display: grid;
  flex: none;
  place-items: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 12px;
  background: var(--p-primary-color);
  color: var(--p-primary-contrast-color);
}

.steps__dot--todo {
  background: var(--p-content-hover-background);
  color: var(--p-text-muted-color);
}

.steps__text {
  display: flex;
  flex-direction: column;
}

.steps__text small {
  color: var(--p-text-muted-color);
}
</style>
