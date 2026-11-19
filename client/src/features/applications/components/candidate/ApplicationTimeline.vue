<script setup lang="ts">
import { formatDate } from '@/shared/utils/format'

import { TIMELINE_LABELS } from '../../lib/application-meta'
import type { TimelineEvent } from '../../types/application'

defineProps<{ events: TimelineEvent[] }>()
</script>

<template>
  <section class="timeline" aria-labelledby="timeline-title">
    <h3 id="timeline-title" class="timeline__title">Application timeline</h3>
    <p v-if="!events.length" class="timeline__empty">No events yet.</p>
    <ol v-else class="timeline__list">
      <li v-for="event in events" :key="`${event.type}-${event.at}`" class="timeline__item">
        <span class="timeline__dot"><i class="pi pi-check" aria-hidden="true" /></span>
        <div class="timeline__text">
          <span class="timeline__label">{{ TIMELINE_LABELS[event.type] }}</span>
          <time class="timeline__time" :datetime="event.at">{{ formatDate(event.at, true) }}</time>
        </div>
      </li>
    </ol>
  </section>
</template>

<style scoped>
.timeline {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.timeline__title {
  margin: 0;
  font-size: 16px;
}

.timeline__empty {
  margin: 0;
  color: var(--p-text-muted-color);
}

.timeline__list {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.timeline__list::before {
  content: '';
  position: absolute;
  top: 12px;
  bottom: 12px;
  left: 11px;
  width: 2px;
  background: var(--p-content-border-color);
}

.timeline__item {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.timeline__dot {
  z-index: 1;
  display: grid;
  flex: none;
  place-items: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--p-primary-color);
  color: var(--p-primary-contrast-color);
  font-size: 11px;
}

.timeline__text {
  display: flex;
  flex-direction: column;
}

.timeline__label {
  font-size: 14px;
  font-weight: 600;
}

.timeline__time {
  color: var(--p-text-muted-color);
  font-size: 12px;
}
</style>
