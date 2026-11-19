<script setup lang="ts">
import { computed } from 'vue'

export type SelectionStatus = 'pending' | 'running' | 'done' | 'failed'

const props = defineProps<{ status: SelectionStatus }>()

const META: Record<SelectionStatus, { label: string; icon: string }> = {
  pending: { label: 'Pending', icon: 'pi pi-hourglass' },
  running: { label: 'Selection in progress…', icon: 'pi pi-sparkles' },
  done: { label: 'Done', icon: 'pi pi-check-circle' },
  failed: { label: 'Failed', icon: 'pi pi-exclamation-circle' },
}

const meta = computed(() => META[props.status])
</script>

<template>
  <span
    class="ai-status"
    :class="`ai-status--${status}`"
    :role="status === 'running' ? 'status' : undefined"
  >
    <i :class="meta.icon" aria-hidden="true" />
    {{ meta.label }}
  </span>
</template>

<style scoped>
.ai-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 99px;
  font-size: 13px;
  font-weight: 600;
  line-height: 20px;
  white-space: nowrap;
}

.ai-status i {
  font-size: 14px;
}

.ai-status--pending {
  background: var(--p-content-hover-background);
  color: var(--p-text-muted-color);
}

.ai-status--done {
  background: var(--p-tag-success-background);
  color: var(--p-tag-success-color);
}

.ai-status--failed {
  background: var(--p-tag-danger-background);
  color: var(--p-tag-danger-color);
}

/* Shimmer only while the AI is working */
.ai-status--running {
  color: var(--p-highlight-color);
  background-color: var(--p-highlight-background);
  background-image: linear-gradient(
    100deg,
    transparent 30%,
    color-mix(in srgb, var(--p-primary-color) 22%, transparent) 50%,
    transparent 70%
  );
  background-size: 200% 100%;
  animation: ai-shimmer 1.8s linear infinite;
}

@keyframes ai-shimmer {
  from {
    background-position: 200% 0;
  }
  to {
    background-position: -200% 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ai-status--running {
    animation: none;
    background-image: none;
  }
}
</style>
