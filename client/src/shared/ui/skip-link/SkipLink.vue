<script setup lang="ts">
withDefaults(defineProps<{ target?: string; label?: string }>(), {
  target: '#main',
  label: 'Skip to main content',
})
</script>

<template>
  <a :href="target" class="skip-link">{{ label }}</a>
</template>

<style scoped>
.skip-link {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 2000;
  padding: 8px 16px;
  border-radius: var(--p-border-radius-md, 8px);
  background: var(--p-primary-color);
  color: var(--p-primary-contrast-color);
  font-weight: 600;
  text-decoration: none;
  transform: translateY(-200%);
}

.skip-link:focus-visible {
  transform: none;
  outline: 2px solid var(--p-primary-contrast-color);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px var(--p-primary-color);
}
</style>
