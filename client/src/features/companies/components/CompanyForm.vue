<script setup lang="ts">
import { ref, toRef } from 'vue'
import { Form } from '@primevue/forms'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Textarea from 'primevue/textarea'

import { FormItem } from '@/shared/ui'

import { useCompanyForm } from '../composables/useCompanyForm'
import type { Company } from '../types/company'

const props = defineProps<{ company: Company | null }>()

const formRef = ref<InstanceType<typeof Form> | null>(null)
const { resolver, initialValues, isEdit, isPending, serverErrors, formError, submit, clearErrors } =
  useCompanyForm(toRef(props, 'company'))

const websitePlaceholder = 'https://example.com'

function cancel() {
  formRef.value?.reset()
  clearErrors()
}
</script>

<template>
  <Form
    ref="formRef"
    v-slot="$form"
    :initial-values="initialValues"
    :resolver="resolver"
    :validate-on-value-update="false"
    :validate-on-blur="true"
    class="company-form card"
    @submit="submit"
  >
    <Message v-if="formError" severity="error" icon="pi pi-exclamation-circle">
      {{ formError }}
    </Message>

    <FormItem
      label="Company name"
      for="company-name"
      required
      :error="$form.name?.error?.message ?? serverErrors.name"
    >
      <InputText id="company-name" name="name" fluid />
    </FormItem>

    <FormItem
      label="Description"
      for="company-description"
      hint="The assistant answers candidates based on this text"
      :error="$form.description?.error?.message ?? serverErrors.description"
    >
      <Textarea id="company-description" name="description" rows="6" auto-resize fluid />
    </FormItem>

    <FormItem
      label="Website"
      for="company-website"
      :error="$form.website?.error?.message ?? serverErrors.website"
    >
      <IconField>
        <InputIcon class="pi pi-globe" />
        <InputText
          id="company-website"
          name="website"
          type="url"
          :placeholder="websitePlaceholder"
          autocapitalize="none"
          fluid
        />
      </IconField>
    </FormItem>

    <div class="company-form__actions">
      <Button
        v-if="isEdit"
        type="button"
        label="Cancel"
        severity="secondary"
        text
        :disabled="!$form.dirty || isPending"
        @click="cancel"
      />
      <Button
        type="submit"
        :label="isEdit ? 'Save changes' : 'Create company'"
        :disabled="isEdit && !$form.dirty"
        :loading="isPending"
      />
    </div>
  </Form>
</template>

<style scoped>
.company-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px;
  border: 1px solid var(--p-content-border-color);
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-background);
}

.company-form__actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
