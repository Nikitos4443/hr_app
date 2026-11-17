<script setup lang="ts">
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Tag from 'primevue/tag'

import { ROLE_LABEL } from '@/features/auth'
import { initials } from '@/shared/utils/format'

import { useDeleteUser } from '../composables/useDeleteUser'
import type { User } from '../types/user'

defineProps<{ users: User[]; currentUserId?: number | null }>()

const { requestDelete, isPending } = useDeleteUser()
</script>

<template>
  <DataTable :value="users" data-key="id" class="users-table">
    <Column header="User">
      <template #body="{ data }: { data: User }">
        <div class="users-table__user">
          <span class="users-table__avatar" aria-hidden="true">{{ initials(data.username) }}</span>
          <div class="users-table__name">
            <strong>{{ data.username }}</strong>
            <small v-if="data.id === currentUserId" class="users-table__me">You</small>
          </div>
        </div>
      </template>
    </Column>
    <Column header="Role">
      <template #body="{ data }: { data: User }">
        <Tag
          :value="ROLE_LABEL[data.role]"
          :icon="data.role === 'company_admin' ? 'pi pi-shield' : 'pi pi-id-card'"
          :severity="data.role === 'company_admin' ? 'info' : 'secondary'"
        />
      </template>
    </Column>
    <Column header="Actions" header-class="users-table__actions-head" style="width: 72px">
      <template #body="{ data }: { data: User }">
        <Button
          icon="pi pi-trash"
          severity="secondary"
          text
          rounded
          :aria-label="`Delete user ${data.username}`"
          :disabled="data.id === currentUserId || isPending"
          @click="requestDelete(data)"
        />
      </template>
    </Column>
  </DataTable>
</template>

<style scoped>
.users-table__user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.users-table__avatar {
  display: grid;
  place-items: center;
  flex: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 600;
  background: var(--p-highlight-background);
  color: var(--p-highlight-color);
}

.users-table__name {
  display: flex;
  flex-direction: column;
}

.users-table__me {
  color: var(--p-text-muted-color);
}
</style>
