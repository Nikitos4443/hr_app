<script setup lang="ts">
import { computed } from 'vue'

import { useSessionStore, type UserRole } from '@/features/auth'
import { AppLogo } from '@/shared/ui'

interface NavItem {
  label: string
  icon: string
  to: string
  roles?: UserRole[]
}

const session = useSessionStore()

const items: NavItem[] = [
  { label: 'Vacancies', icon: 'pi pi-briefcase', to: '/app/vacancies' },
  { label: 'Company', icon: 'pi pi-building', to: '/app/company', roles: ['company_admin'] },
  { label: 'Team', icon: 'pi pi-users', to: '/app/team', roles: ['company_admin'] },
]

const visibleItems = computed(() =>
  items.filter((item) => !item.roles || session.hasRole(...item.roles)),
)
</script>

<template>
  <aside class="side-nav">
    <AppLogo to="/app/vacancies" class="side-nav__logo" />
    <nav class="side-nav__list" aria-label="Main">
      <RouterLink v-for="item in visibleItems" :key="item.to" :to="item.to" class="side-nav__item">
        <i :class="item.icon" aria-hidden="true" />
        {{ item.label }}
      </RouterLink>
    </nav>
  </aside>
</template>

<style scoped>
.side-nav {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px 12px;
  background: var(--p-content-background);
  border-right: 1px solid var(--p-content-border-color);
}

.side-nav__logo {
  padding: 4px 8px 12px;
}

.side-nav__list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.side-nav__item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  color: var(--p-text-muted-color);
  font-weight: 600;
  text-decoration: none;
}

.side-nav__item:hover {
  background: var(--p-content-hover-background);
  color: var(--p-text-color);
}

.side-nav__item.router-link-active {
  background: var(--p-highlight-background);
  color: var(--p-highlight-color);
}

@media (max-width: 768px) {
  .side-nav {
    flex-direction: row;
    align-items: center;
    flex-wrap: wrap;
    border-right: 0;
    border-bottom: 1px solid var(--p-content-border-color);
  }

  .side-nav__logo {
    padding: 0 8px;
  }

  .side-nav__list {
    flex-direction: row;
  }
}
</style>
