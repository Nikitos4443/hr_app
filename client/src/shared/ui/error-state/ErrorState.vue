<script setup lang="ts">
withDefaults(defineProps<{ title: string; description?: string; icon?: string }>(), {
  icon: 'pi pi-exclamation-triangle',
  description: undefined,
})
</script>

<template>
  <div class="state" role="alert">
    <span class="state__icon"><i :class="icon" aria-hidden="true" /></span>
    <h2 class="state__title">{{ title }}</h2>
    <p v-if="description" class="state__description">{{ description }}</p>
    <div v-if="$slots.default" class="state__actions"><slot /></div>
  </div>
</template>

<style scoped>
.state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 32px 24px;
  text-align: center;
}

.state__icon {
  display: grid;
  place-items: center;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  font-size: 24px;
  background: var(--p-tag-danger-background);
  color: var(--p-tag-danger-color);
}

.state__title {
  margin: 0;
  font-size: 16px;
}

.state__description {
  margin: 0;
  max-width: 360px;
  color: var(--p-text-muted-color);
}

.state__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
}
</style>
