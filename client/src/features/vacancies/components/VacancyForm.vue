<script setup lang="ts">
import { Form } from '@primevue/forms'
import Message from 'primevue/message'

import { useVacancyForm } from '../composables/useVacancyForm'
import { currencyOptions, employmentTypeOptions } from '../lib/labels'
import type { Vacancy } from '../types/vacancy'
import BulletListsSection from './form/BulletListsSection.vue'
import DeadlineStatusSection from './form/DeadlineStatusSection.vue'
import DescriptionSection from './form/DescriptionSection.vue'
import FormActionBar from './form/FormActionBar.vue'
import SalarySection from './form/SalarySection.vue'
import ScreeningQuestionsSection from './form/ScreeningQuestionsSection.vue'
import VacancyBasicsSection from './form/VacancyBasicsSection.vue'

const props = defineProps<{ vacancy?: Vacancy }>()

const {
  isEdit,
  initialValues,
  resolver,
  formRef,
  responsibilities,
  requirements,
  niceToHave,
  questions,
  serverErrors,
  serverMessage,
  isDirty,
  isSaving,
  submit,
  cancel,
} = useVacancyForm(props.vacancy)

const employmentOptions = employmentTypeOptions(initialValues.employment_type)
const currencies = currencyOptions(initialValues.salary_currency)

const FIELDS = [
  'title',
  'location',
  'employment_type',
  'experience_years_min',
  'description',
  'salary_min',
  'salary_max',
  'salary_currency',
  'deadline_at',
  'status',
]

function collectErrors(form: Record<string, { error?: { message?: string } } | undefined>) {
  const errors: Record<string, string | undefined> = {}
  for (const field of FIELDS) {
    errors[field] = form[field]?.error?.message ?? serverErrors.value[field]
  }
  return errors
}

function countErrors(errors: Record<string, string | undefined>) {
  return Object.values(errors).filter(Boolean).length + questions.invalidCount.value
}
</script>

<template>
  <Form
    v-slot="$form"
    ref="formRef"
    :initial-values="initialValues"
    :resolver="resolver"
    :validate-on-value-update="false"
    :validate-on-blur="true"
    class="vacancy-form"
    @submit="submit"
  >
    <Message v-if="serverMessage" severity="error" icon="pi pi-exclamation-circle">
      {{ serverMessage }}
    </Message>

    <VacancyBasicsSection :employment-options="employmentOptions" :errors="collectErrors($form)" />
    <SalarySection :currencies="currencies" :errors="collectErrors($form)" />
    <DescriptionSection :errors="collectErrors($form)" />
    <BulletListsSection
      :responsibilities="responsibilities"
      :requirements="requirements"
      :nice-to-have="niceToHave"
    />
    <DeadlineStatusSection :errors="collectErrors($form)" />
    <ScreeningQuestionsSection :questions="questions" />

    <FormActionBar
      :dirty="isDirty"
      :saving="isSaving"
      :error-count="countErrors(collectErrors($form))"
      :submit-label="isEdit ? 'Save changes' : 'Create vacancy'"
      @cancel="cancel"
    />
  </Form>
</template>

<style scoped>
.vacancy-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 1000px;
}
</style>
