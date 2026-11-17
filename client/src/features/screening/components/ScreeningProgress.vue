<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ total: number; answered: number; label: string }>()

const segments = computed(() => Array.from({ length: props.total }, (_, index) => index))
</script>

<template>
  <div
    class="progress"
    role="progressbar"
    :aria-valuenow="Math.min(answered + 1, total)"
    aria-valuemin="1"
    :aria-valuemax="total"
    :aria-label="label"
  >
    <span
      v-for="index in segments"
      :key="index"
      class="progress__segment"
      :class="{ 'progress__segment--on': index <= answered }"
    />
  </div>
</template>

<style scoped>
.progress {
  display: flex;
  gap: 6px;
}

.progress__segment {
  flex: 1;
  height: 6px;
  border-radius: 999px;
  background: var(--p-content-border-color);
  transition: background 0.2s;
}

.progress__segment--on {
  background: var(--p-primary-color);
}
</style>
