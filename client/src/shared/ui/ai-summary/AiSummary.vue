<script setup lang="ts">
withDefaults(defineProps<{ title?: string }>(), { title: 'AI summary' })
</script>

<template>
  <div class="ai-summary">
    <div class="ai-summary__title">
      <i class="pi pi-sparkles" aria-hidden="true" />
      {{ title }}
    </div>
    <p class="ai-summary__body"><slot /></p>
  </div>
</template>

<style scoped>
.ai-summary {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px 14px;
  border-radius: 10px;
  background: var(--p-highlight-background);
}

.ai-summary__title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--p-highlight-color);
}

.ai-summary__body {
  margin: 0;
  font-size: 13px;
  line-height: 19px;
  color: var(--p-text-color);
}
</style>
