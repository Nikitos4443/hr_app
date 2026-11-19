<script setup lang="ts">
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import { computed } from 'vue'

import { useSessionStore } from '@/features/auth'

import HeroPreviewCard from './HeroPreviewCard.vue'

const session = useSessionStore()

const ctaTo = computed(() => (session.isAuthenticated ? '/app/vacancies' : '/auth'))
const ctaLabel = computed(() => (session.isAuthenticated ? 'Open app' : 'Sign in'))

const PERKS = ['No account needed for candidates', 'Video and text answers']
</script>

<template>
  <section class="hero-section">
    <div class="hero-section__copy">
      <Tag
        class="hero-section__tag"
        severity="info"
        icon="pi pi-sparkles"
        value="AI candidate screening"
      />
      <h1 class="hero-section__title">Find strong candidates, not mountains of resumes</h1>
      <p class="hero-section__lead">
        Publish a vacancy and HR App scores resumes, invites the best candidates to a video
        screening and builds a ranking. All that's left is to talk to the people who truly fit.
      </p>
      <div class="hero-section__actions">
        <RouterLink :to="ctaTo">
          <Button :label="ctaLabel" icon="pi pi-arrow-right" icon-pos="right" size="large" />
        </RouterLink>
      </div>
      <ul class="hero-section__perks">
        <li v-for="perk in PERKS" :key="perk" class="hero-section__perk">
          <i class="pi pi-check-circle" aria-hidden="true" />
          {{ perk }}
        </li>
      </ul>
    </div>
    <HeroPreviewCard class="hero-section__preview" />
  </section>
</template>

<style scoped>
.hero-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(480px, 100%), 1fr));
  gap: 56px;
  align-items: center;
  padding: 48px 0 56px;
}

.hero-section__copy {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 24px;
}

.hero-section__title {
  margin: 0;
  font-size: clamp(32px, 5vw, 52px);
  font-weight: 700;
  line-height: 1.08;
}

.hero-section__lead {
  max-width: 520px;
  margin: 0;
  font-size: 18px;
  line-height: 28px;
  color: var(--p-text-muted-color);
}

.hero-section__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.hero-section__perks {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 24px;
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: 14px;
  color: var(--p-text-muted-color);
}

.hero-section__perk {
  display: flex;
  align-items: center;
  gap: 6px;
}

.hero-section__perk i {
  color: var(--p-primary-color);
}

.hero-section__preview {
  justify-self: center;
}

@media (max-width: 640px) {
  .hero-section {
    gap: 32px;
    padding-top: 24px;
  }
}
</style>
