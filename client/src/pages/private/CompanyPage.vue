<script setup lang="ts">
import { computed } from 'vue'
import Message from 'primevue/message'
import Skeleton from 'primevue/skeleton'

import { CompanyForm, CompanyPreviewCard, useCompanyQuery } from '@/features/companies'
import { useMeQuery } from '@/features/users'
import { errorMessage } from '@/shared/api'
import { EmptyState, ErrorState, PageHeader } from '@/shared/ui'
import Button from 'primevue/button'

const me = useMeQuery()
const companyId = computed(() => me.data.value?.company_id)
const company = useCompanyQuery(companyId)

const hasNoCompany = computed(() => me.isSuccess.value && me.data.value?.company_id == null)
const isLoading = computed(
  () => me.isPending.value || (!hasNoCompany.value && company.isPending.value),
)
const error = computed(() => me.error.value ?? company.error.value)

function retry() {
  void me.refetch()
  void company.refetch()
}
</script>

<template>
  <div class="company-page">
    <PageHeader
      title="Company profile"
      subtitle="Candidates see this on the vacancy page and in the assistant chat."
    />

    <div v-if="isLoading" class="company-page__grid">
      <Skeleton height="380px" />
      <Skeleton height="180px" />
    </div>

    <ErrorState
      v-else-if="error"
      title="Could not load the company"
      :description="errorMessage(error)"
    >
      <Button label="Retry" icon="pi pi-refresh" @click="retry" />
    </ErrorState>

    <div v-else-if="hasNoCompany" class="company-page__create">
      <EmptyState
        icon="pi pi-building"
        title="Create your company"
        description="Add a company profile to start publishing vacancies and invite your team."
      />
      <CompanyForm :company="null" />
    </div>

    <div v-else-if="company.data.value" class="company-page__grid">
      <CompanyForm :company="company.data.value" />
      <aside class="company-page__side">
        <CompanyPreviewCard :company="company.data.value" />
        <Message severity="info" icon="pi pi-info-circle" :closable="false">
          Only a company admin can edit the profile.
        </Message>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.company-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.company-page__grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 24px;
  align-items: start;
  max-width: 1100px;
}

.company-page__create {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 560px;
}

.company-page__side {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

@media (max-width: 900px) {
  .company-page__grid {
    grid-template-columns: minmax(0, 1fr);
  }
}
</style>
