<script setup lang="ts">
import { computed, ref } from 'vue'
import Avatar from 'primevue/avatar'
import Menu from 'primevue/menu'
import Tag from 'primevue/tag'

import { ROLE_LABEL } from '../lib/roles'
import { useSessionStore } from '../stores/session.store'

const session = useSessionStore()
const open = ref(false)
const menu = ref<InstanceType<typeof Menu> | null>(null)

const initials = computed(() => (session.user?.username ?? '?').slice(0, 2).toUpperCase())
const roleLabel = computed(() => (session.user ? ROLE_LABEL[session.user.role] : ''))

const items = [{ label: 'Sign out', icon: 'pi pi-sign-out', command: () => session.logout() }]

function toggle(event: Event) {
  menu.value?.toggle(event)
}
</script>

<template>
  <div v-if="session.user" class="user-menu">
    <button
      type="button"
      class="user-menu__trigger"
      aria-haspopup="true"
      :aria-controls="open ? 'user-menu-popup' : undefined"
      :aria-expanded="open"
      :aria-label="`Account menu, ${session.user.username}`"
      @click="toggle"
    >
      <Avatar :label="initials" shape="circle" />
      <span class="user-menu__name">{{ session.user.username }}</span>
      <Tag :value="roleLabel" severity="secondary" />
      <i class="pi pi-angle-down" aria-hidden="true" />
    </button>
    <Menu
      id="user-menu-popup"
      ref="menu"
      :model="items"
      popup
      @show="open = true"
      @hide="open = false"
    />
  </div>
</template>

<style scoped>
.user-menu__trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  border: 0;
  border-radius: 10px;
  background: transparent;
  color: var(--p-text-color);
  font: inherit;
  cursor: pointer;
}

.user-menu__trigger:hover {
  background: var(--p-content-hover-background);
}

.user-menu__trigger:focus-visible {
  outline: 2px solid var(--p-primary-color);
  outline-offset: 2px;
}

.user-menu__name {
  font-weight: 600;
}

@media (max-width: 640px) {
  .user-menu__name {
    display: none;
  }
}
</style>
