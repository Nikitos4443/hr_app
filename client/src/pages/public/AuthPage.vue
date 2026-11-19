<script setup lang="ts">
import { computed } from 'vue'
import Card from 'primevue/card'
import { useRoute, useRouter } from 'vue-router'

import { AuthTabs, LoginForm, RegisterForm, type AuthMode } from '@/features/auth'

const route = useRoute()
const router = useRouter()

const mode = computed<AuthMode>({
  get: () => (route.query.mode === 'register' ? 'register' : 'login'),
  set: (value) => {
    const query = { ...route.query }
    if (value === 'register') query.mode = value
    else delete query.mode
    router.replace({ query })
  },
})

const heading = computed(() => (mode.value === 'login' ? 'Welcome back' : 'Create an account'))
const subheading = computed(() =>
  mode.value === 'login'
    ? 'Sign in to manage vacancies and candidates.'
    : 'Registering a company takes a minute.',
)
</script>

<template>
  <Card>
    <template #content>
      <div class="auth-card">
        <div>
          <h1 class="auth-card__title">{{ heading }}</h1>
          <p class="auth-card__subtitle">{{ subheading }}</p>
        </div>
        <AuthTabs v-model="mode">
          <template #login><LoginForm /></template>
          <template #register><RegisterForm /></template>
        </AuthTabs>
      </div>
    </template>
  </Card>
</template>

<style scoped>
.auth-card {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 8px;
}

.auth-card__title {
  margin: 0;
  font-size: 22px;
}

.auth-card__subtitle {
  margin: 4px 0 0;
  color: var(--p-text-muted-color);
}
</style>
