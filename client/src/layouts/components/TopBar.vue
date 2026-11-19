<script setup lang="ts">
import { computed } from 'vue'

import { useCompanyQuery } from '@/features/companies'
import { UserMenu, useSessionStore } from '@/features/auth'
import { useMeQuery } from '@/features/users'
import { ThemeToggle } from '@/shared/ui'

const session = useSessionStore()
const isAdmin = computed(() => session.hasRole('company_admin'))

const me = useMeQuery()
const company = useCompanyQuery(() => (isAdmin.value ? me.data.value?.company_id : null))
</script>

<template>
  <header class="top-bar">
    <span v-if="company.data.value" class="top-bar__company">
      <i class="pi pi-building" aria-hidden="true" />
      {{ company.data.value.name }}
    </span>
    <div class="top-bar__actions">
      <ThemeToggle />
      <UserMenu />
    </div>
  </header>
</template>

<style scoped>
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 12px 32px;
  background: var(--p-content-background);
  border-bottom: 1px solid var(--p-content-border-color);
}

.top-bar__company {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.top-bar__actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
}

@media (max-width: 768px) {
  .top-bar {
    padding: 12px 16px;
  }
}
</style>
