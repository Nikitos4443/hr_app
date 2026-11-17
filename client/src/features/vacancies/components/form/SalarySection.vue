<script setup lang="ts">
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'

import { FormItem } from '@/shared/ui'

import type { Option } from '../../lib/labels'
import FormSection from './FormSection.vue'

defineProps<{
  currencies: Option[]
  errors: Record<string, string | undefined>
}>()
</script>

<template>
  <FormSection title="Salary range">
    <div class="grid">
      <FormItem label="Minimum" for="salary-min" :error="errors.salary_min">
        <InputNumber
          name="salary_min"
          input-id="salary-min"
          :min="0"
          :invalid="Boolean(errors.salary_max)"
          fluid
        />
      </FormItem>
      <FormItem label="Maximum" for="salary-max">
        <InputNumber
          name="salary_max"
          input-id="salary-max"
          :min="0"
          :invalid="Boolean(errors.salary_max)"
          fluid
        />
      </FormItem>
      <FormItem label="Currency" for="salary-currency" :error="errors.salary_currency">
        <Select
          name="salary_currency"
          input-id="salary-currency"
          :options="currencies"
          option-label="label"
          option-value="value"
          placeholder="Currency"
          show-clear
          fluid
        />
      </FormItem>
    </div>
    <small v-if="errors.salary_max" class="error" role="alert">
      <i class="pi pi-exclamation-circle" aria-hidden="true" />
      {{ errors.salary_max }}
    </small>
  </FormSection>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.error {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--p-form-field-invalid-border-color);
}
</style>
