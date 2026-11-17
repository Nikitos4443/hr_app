<script setup lang="ts">
defineProps<{ title: string; hint?: string }>()
</script>

<template>
  <section class="form-section">
    <div class="form-section__head">
      <div class="form-section__text">
        <h2 class="form-section__title">{{ title }}</h2>
        <span v-if="hint" class="form-section__hint">{{ hint }}</span>
      </div>
      <slot name="aside" />
    </div>
    <slot />
  </section>
</template>

<style scoped>
.form-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px;
  border: 1px solid var(--p-content-border-color);
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-background);
}

.form-section__head {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}

.form-section__text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.form-section__title {
  margin: 0;
  font-size: 18px;
}

.form-section__hint {
  color: var(--p-text-muted-color);
  font-size: 13px;
}
</style>
