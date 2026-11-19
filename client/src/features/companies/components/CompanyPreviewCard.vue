<script setup lang="ts">
import { computed } from 'vue'

import { CompanyAvatar } from '@/shared/ui'

import type { Company } from '../types/company'

const props = defineProps<{ company: Company }>()

const host = computed(() => {
  const site = props.company.website
  if (!site) return null
  try {
    return new URL(site).host
  } catch {
    return site
  }
})
</script>

<template>
  <section class="preview">
    <span class="preview__label">How candidates see it</span>
    <div class="preview__head">
      <CompanyAvatar :name="company.name" />
      <div class="preview__name">
        <strong>{{ company.name }}</strong>
        <a
          v-if="host"
          class="preview__site"
          :href="company.website ?? undefined"
          target="_blank"
          rel="noopener noreferrer"
        >
          <i class="pi pi-globe" aria-hidden="true" />{{ host }}
        </a>
      </div>
    </div>
    <p v-if="company.description" class="preview__description">{{ company.description }}</p>
    <p v-else class="preview__description preview__description--empty">No description yet.</p>
  </section>
</template>

<style scoped>
.preview {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;
  border: 1px solid var(--p-content-border-color);
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-background);
}

.preview__label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--p-text-muted-color);
}

.preview__head {
  display: flex;
  align-items: center;
  gap: 12px;
}

.preview__name {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.preview__site {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--p-primary-color);
  text-decoration: none;
  overflow-wrap: anywhere;
}

.preview__description {
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
  color: var(--p-text-muted-color);
  white-space: pre-line;
}

.preview__description--empty {
  font-style: italic;
}
</style>
