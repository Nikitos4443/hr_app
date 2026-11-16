<script setup lang="ts">
import ProgressBar from 'primevue/progressbar'
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    /** 0–100 */
    value: number
    showValue?: boolean
    label?: string
  }>(),
  { showValue: true, label: 'Score' },
)

const score = computed(() => Math.round(Math.min(100, Math.max(0, props.value))))

// Thresholds: >= 80 high, 50-79 medium, < 50 low
const level = computed(() => (score.value >= 80 ? 'hi' : score.value >= 50 ? 'mid' : 'lo'))
</script>

<template>
  <div class="score-bar">
    <ProgressBar
      class="score-bar__track"
      :class="`score-bar__track--${level}`"
      :value="score"
      :show-value="false"
      :aria-label="`${label}: ${score} out of 100`"
    />
    <b v-if="showValue" class="score-bar__num">{{ score }}</b>
  </div>
</template>

<style scoped>
.score-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 120px;
}

.score-bar__track {
  flex: 1;
  --p-progressbar-height: 8px;
}

.score-bar__track--hi {
  --p-progressbar-value-background: var(--hr-score-hi);
}

.score-bar__track--mid {
  --p-progressbar-value-background: var(--hr-score-mid);
}

.score-bar__track--lo {
  --p-progressbar-value-background: var(--hr-score-lo);
}

.score-bar__num {
  min-width: 2ch;
  text-align: right;
  font-variant-numeric: tabular-nums;
}
</style>
