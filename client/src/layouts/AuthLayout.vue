<script setup lang="ts">
import { RouterView } from 'vue-router'

import { AppLogo, ThemeToggle } from '@/shared/ui'
</script>

<template>
  <div class="auth-layout">
    <div class="auth-layout__theme"><ThemeToggle /></div>
    <AppLogo />
    <main class="auth-layout__main"><RouterView /></main>
  </div>
</template>

<style scoped>
.auth-layout {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  min-height: 100vh;
  padding: 48px 16px 64px;
}

.auth-layout__theme {
  position: absolute;
  top: 16px;
  right: 16px;
}

.auth-layout__main {
  width: 100%;
  max-width: 440px;
}
</style>
