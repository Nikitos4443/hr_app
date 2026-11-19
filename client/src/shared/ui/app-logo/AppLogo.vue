<script setup lang="ts">
withDefaults(defineProps<{ to?: string }>(), { to: '/' })
</script>

<template>
  <RouterLink :to="to" class="app-logo" aria-label="HR App">
    <span class="app-logo__mark">
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.6"
        stroke-linecap="round"
        stroke-linejoin="round"
        aria-hidden="true"
      >
        <path d="M6 4v16M18 12v8M6 12h12" />
        <path
          d="M18 3l.9 2.1L21 6l-2.1.9L18 9l-.9-2.1L15 6l2.1-.9z"
          fill="currentColor"
          stroke-width="1"
        />
      </svg>
    </span>
    <span class="app-logo__text">HR <em>App</em></span>
  </RouterLink>
</template>

<style scoped>
.app-logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  color: var(--p-text-color);
  text-decoration: none;
}

.app-logo__mark {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  background: var(--p-primary-color);
  color: var(--p-primary-contrast-color);
}

.app-logo__text em {
  font-style: normal;
  color: var(--p-primary-color);
}
</style>
