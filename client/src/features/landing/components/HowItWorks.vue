<script setup lang="ts">
const STEPS = [
  {
    icon: 'pi pi-file',
    title: '1. Resume',
    text: 'The candidate leaves an e-mail and a PDF. AI compares the resume with the vacancy.',
  },
  {
    icon: 'pi pi-video',
    title: '2. Screening',
    text: 'The best candidates get a unique link to video or text questions.',
  },
  {
    icon: 'pi pi-chart-bar',
    title: '3. Ranking',
    text: 'Videos are transcribed and answers scored, so candidates line up by score.',
  },
]
</script>

<template>
  <section class="how-it-works" aria-labelledby="how-it-works-title">
    <h2 id="how-it-works-title" class="how-it-works__heading">How it works</h2>
    <ol class="how-it-works__list">
      <li v-for="step in STEPS" :key="step.title" class="how-it-works__step">
        <i :class="step.icon" class="how-it-works__icon" aria-hidden="true" />
        <h3 class="how-it-works__title">{{ step.title }}</h3>
        <p class="how-it-works__text">{{ step.text }}</p>
      </li>
    </ol>
  </section>
</template>

<style scoped>
.how-it-works {
  padding-bottom: 24px;
}

.how-it-works__heading {
  margin: 0 0 16px;
  font-size: 24px;
  font-weight: 600;
}

.how-it-works__list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(260px, 100%), 1fr));
  gap: 16px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.how-it-works__step {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 24px;
  border-radius: 12px;
  background: var(--p-content-hover-background);
}

.how-it-works__icon {
  font-size: 24px;
  color: var(--p-primary-color);
}

.how-it-works__title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.how-it-works__text {
  margin: 0;
  font-size: 14px;
  line-height: 21px;
  color: var(--p-text-muted-color);
}
</style>
