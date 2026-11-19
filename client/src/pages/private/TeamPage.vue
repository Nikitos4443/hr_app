<script setup lang="ts">
import { computed, ref } from 'vue'
import Button from 'primevue/button'
import Skeleton from 'primevue/skeleton'

import { CreateHrDialog, UsersTable, useMeQuery, useUsersQuery } from '@/features/users'
import { errorMessage } from '@/shared/api'
import { EmptyState, ErrorState, PageHeader } from '@/shared/ui'

const me = useMeQuery()
const hasNoCompany = computed(() => me.isSuccess.value && me.data.value?.company_id == null)
const users = useUsersQuery()
const dialogVisible = ref(false)

const isLoading = computed(
  () => me.isPending.value || (!hasNoCompany.value && users.isPending.value),
)
const error = computed(() => me.error.value ?? (hasNoCompany.value ? null : users.error.value))
const list = computed(() => users.data.value ?? [])
const subtitle = computed(() => (list.value.length === 1 ? '1 user' : `${list.value.length} users`))

function retry() {
  void me.refetch()
  void users.refetch()
}
</script>

<template>
  <div class="team-page">
    <PageHeader
      title="Team"
      :subtitle="
        hasNoCompany ? undefined : `${subtitle} · HR managers see vacancies and candidates`
      "
    >
      <Button
        label="Add HR"
        icon="pi pi-user-plus"
        :disabled="hasNoCompany || isLoading"
        @click="dialogVisible = true"
      />
    </PageHeader>

    <div v-if="isLoading" class="team-page__skeleton">
      <Skeleton v-for="row in 4" :key="row" height="48px" />
    </div>

    <ErrorState
      v-else-if="error"
      title="Could not load the team"
      :description="errorMessage(error)"
    >
      <Button label="Retry" icon="pi pi-refresh" @click="retry" />
    </ErrorState>

    <EmptyState
      v-else-if="hasNoCompany"
      icon="pi pi-building"
      title="Create a company first"
      description="Your team becomes available once your company profile exists."
    >
      <Button
        label="Go to company profile"
        icon="pi pi-arrow-right"
        @click="$router.push({ name: 'company' })"
      />
    </EmptyState>

    <EmptyState
      v-else-if="list.length === 0"
      icon="pi pi-users"
      title="No team members yet"
      description="Create an HR account to share vacancies and candidates."
    >
      <Button label="Add HR" icon="pi pi-user-plus" @click="dialogVisible = true" />
    </EmptyState>

    <UsersTable v-else :users="list" :current-user-id="me.data.value?.id" />

    <CreateHrDialog v-model:visible="dialogVisible" />
  </div>
</template>

<style scoped>
.team-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.team-page__skeleton {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
