<script setup lang="ts">
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'

import { FormItem } from '@/shared/ui'

import type { Option } from '../../lib/labels'
import FormSection from './FormSection.vue'

defineProps<{
  employmentOptions: Option[]
  errors: Record<string, string | undefined>
}>()
</script>

<template>
  <FormSection title="Basics">
    <FormItem label="Vacancy title" for="vacancy-title" required :error="errors.title">
      <InputText id="vacancy-title" name="title" autocomplete="off" fluid />
    </FormItem>
    <div class="grid">
      <FormItem label="Location" for="vacancy-location" :error="errors.location">
        <IconField>
          <InputIcon class="pi pi-map-marker" />
          <InputText id="vacancy-location" name="location" autocomplete="off" fluid />
        </IconField>
      </FormItem>
      <FormItem label="Employment type" for="vacancy-type" :error="errors.employment_type">
        <Select
          name="employment_type"
          input-id="vacancy-type"
          :options="employmentOptions"
          option-label="label"
          option-value="value"
          placeholder="Select type"
          show-clear
          fluid
        />
      </FormItem>
      <FormItem
        label="Minimum experience, years"
        for="vacancy-exp"
        :error="errors.experience_years_min"
      >
        <InputNumber
          name="experience_years_min"
          input-id="vacancy-exp"
          :min="0"
          :max="60"
          show-buttons
          fluid
        />
      </FormItem>
    </div>
  </FormSection>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}
</style>
