<script setup lang="ts">
defineProps<{ title: string; subtitle?: string }>()
</script>

<template>
  <header class="page-header">
    <div class="page-header__text">
      <h1 class="page-header__title">{{ title }}</h1>
      <p v-if="subtitle" class="page-header__subtitle">{{ subtitle }}</p>
    </div>
    <div v-if="$slots.default" class="page-header__actions"><slot /></div>
  </header>
</template>

<style scoped>
.page-header {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.page-header__title {
  margin: 0;
  font-size: 24px;
  line-height: 32px;
}

.page-header__subtitle {
  margin: 2px 0 0;
  color: var(--p-text-muted-color);
}

.page-header__actions {
  display: flex;
  gap: 8px;
}
</style>
