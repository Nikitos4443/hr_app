<script setup lang="ts">
import { computed } from 'vue'
import Avatar from 'primevue/avatar'
import Tag from 'primevue/tag'

import { StatusTag } from '@/shared/ui'
import { initials } from '@/shared/utils/format'

import { candidateName } from '../../lib/application-meta'
import type { ApplicationDetail } from '../../types/application'

const props = defineProps<{ application: ApplicationDetail }>()

const name = computed(() => candidateName(props.application))

const screening = computed(() => {
  const total = props.application.answers.length
  if (total === 0) return null
  const done = props.application.answers.filter((answer) => answer.status === 'done').length
  return { done, total, complete: done === total }
})
</script>

<template>
  <div class="header">
    <Avatar :label="initials(name)" size="xlarge" shape="circle" aria-hidden="true" />
    <div class="header__body">
      <h2 class="header__name">{{ name }}</h2>
      <span class="header__email">
        <i class="pi pi-envelope" aria-hidden="true" /> {{ application.email }}
      </span>
      <div class="header__tags">
        <StatusTag kind="application" :status="application.status" />
        <Tag
          v-if="screening"
          :value="`Screening ${screening.done}/${screening.total}`"
          :icon="screening.complete ? 'pi pi-check-circle' : 'pi pi-hourglass'"
          :severity="screening.complete ? 'success' : 'secondary'"
        />
        <Tag
          v-if="application.rank != null"
          :value="`Rank ${application.rank}`"
          severity="secondary"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.header__body {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.header__name {
  margin: 0;
  font-size: 22px;
  line-height: 28px;
}

.header__email {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--p-text-muted-color);
  overflow-wrap: anywhere;
}

.header__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 4px;
}
</style>
