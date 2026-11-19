<script setup lang="ts">
import { computed } from 'vue'

import { initials } from '@/shared/utils/format'

const props = withDefaults(defineProps<{ name: string; size?: number }>(), { size: 44 })

const label = computed(() => initials(props.name))
const style = computed(() => ({
  width: `${props.size}px`,
  height: `${props.size}px`,
  fontSize: `${Math.round(props.size * 0.36)}px`,
}))
</script>

<template>
  <span class="company-avatar" :style="style" aria-hidden="true">{{ label }}</span>
</template>

<style scoped>
.company-avatar {
  display: inline-grid;
  place-items: center;
  flex: none;
  border-radius: 50%;
  background: var(--p-highlight-background);
  color: var(--p-highlight-color);
  font-weight: 600;
  text-transform: uppercase;
}
</style>
