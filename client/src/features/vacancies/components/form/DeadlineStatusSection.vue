<script setup lang="ts">
import DatePicker from 'primevue/datepicker'
import Select from 'primevue/select'

import { FormItem } from '@/shared/ui'

import { VACANCY_STATUS_OPTIONS } from '../../lib/labels'
import FormSection from './FormSection.vue'

defineProps<{ errors: Record<string, string | undefined> }>()

const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone
</script>

<template>
  <FormSection title="Deadline and status">
    <div class="grid">
      <FormItem
        label="Deadline"
        for="vacancy-deadline"
        :hint="`Time zone: ${timeZone}`"
        :error="errors.deadline_at"
      >
        <DatePicker
          name="deadline_at"
          input-id="vacancy-deadline"
          show-time
          hour-format="24"
          show-icon
          show-button-bar
          date-format="d M yy"
          fluid
        />
      </FormItem>
      <FormItem label="Status" for="vacancy-status" :error="errors.status">
        <Select
          name="status"
          input-id="vacancy-status"
          :options="VACANCY_STATUS_OPTIONS"
          option-label="label"
          option-value="value"
          fluid
        />
      </FormItem>
    </div>
  </FormSection>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}
</style>
