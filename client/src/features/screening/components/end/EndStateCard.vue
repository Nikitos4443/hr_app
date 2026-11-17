<script setup lang="ts">
withDefaults(
  defineProps<{
    icon: string
    title: string
    description?: string
    tone?: 'success' | 'warn' | 'info' | 'primary' | 'neutral'
  }>(),
  { description: undefined, tone: 'neutral' },
)
</script>

<template>
  <div class="end-card">
    <span class="end-card__icon" :class="`end-card__icon--${tone}`">
      <i :class="icon" aria-hidden="true" />
    </span>
    <div class="end-card__text">
      <h1 class="end-card__title">{{ title }}</h1>
      <p v-if="description" class="end-card__description">{{ description }}</p>
    </div>
    <slot />
  </div>
</template>

<style scoped>
.end-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  max-width: 480px;
  margin: 0 auto;
  padding: 40px 8px;
  text-align: center;
}

.end-card__icon {
  display: grid;
  place-items: center;
  width: 72px;
  height: 72px;
  border-radius: 50%;
  font-size: 28px;
}

.end-card__icon--success {
  background: color-mix(in srgb, var(--p-green-500) 16%, transparent);
  color: var(--p-green-500);
}

.end-card__icon--warn {
  background: color-mix(in srgb, var(--p-orange-500) 16%, transparent);
  color: var(--p-orange-500);
}

.end-card__icon--info {
  background: color-mix(in srgb, var(--p-blue-500) 16%, transparent);
  color: var(--p-blue-500);
}

.end-card__icon--primary {
  background: var(--p-highlight-background);
  color: var(--p-highlight-color);
}

.end-card__icon--neutral {
  background: var(--p-content-hover-background);
  color: var(--p-text-muted-color);
}

.end-card__text {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.end-card__title {
  margin: 0;
  font-size: 24px;
}

.end-card__description {
  margin: 0;
  color: var(--p-text-muted-color);
}
</style>
