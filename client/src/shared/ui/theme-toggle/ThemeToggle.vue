<script setup lang="ts">
import Button from 'primevue/button'

import { useTheme } from '@/shared/composables/useTheme'

const { isDark, toggleTheme } = useTheme()
</script>

<template>
  <Button
    :icon="isDark ? 'pi pi-sun' : 'pi pi-moon'"
    severity="secondary"
    variant="text"
    rounded
    :aria-label="isDark ? 'Switch to light theme' : 'Switch to dark theme'"
    @click="toggleTheme"
  />
</template>
