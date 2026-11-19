<script setup lang="ts">
import { RouterView } from 'vue-router'

import { AppLogo, SkipLink, ThemeToggle } from '@/shared/ui'
</script>

<template>
  <div class="auth-layout">
    <SkipLink />
    <div class="auth-layout__theme"><ThemeToggle /></div>
    <AppLogo />
    <main id="main" tabindex="-1" class="auth-layout__main"><RouterView /></main>
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
