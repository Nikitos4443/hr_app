<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { Form, type FormSubmitEvent } from '@primevue/forms'
import { zodResolver } from '@primevue/forms/resolvers/zod'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Password from 'primevue/password'

import { isApiError } from '@/shared/api'
import { useNotify } from '@/shared/composables/useNotify'
import { FormItem } from '@/shared/ui'

import { useCreateUserMutation } from '../api/users.queries'
import { createHrSchema } from '../lib/schemas'

const visible = defineModel<boolean>('visible', { required: true })

const resolver = zodResolver(createHrSchema)
const notify = useNotify()
const mutation = useCreateUserMutation()
const formRef = ref<InstanceType<typeof Form> | null>(null)
const serverErrors = ref<Record<string, string>>({})
const formError = ref<string | null>(null)

let returnFocusTo: HTMLElement | null = null

watch(visible, (open) => {
  if (open) {
    returnFocusTo = document.activeElement instanceof HTMLElement ? document.activeElement : null
    return
  }
  const target = returnFocusTo
  returnFocusTo = null
  if (target?.isConnected) void nextTick(() => target.focus())
  formRef.value?.reset()
  serverErrors.value = {}
  formError.value = null
  mutation.reset()
})

function onSubmit({ valid, values }: FormSubmitEvent) {
  if (!valid) return
  serverErrors.value = {}
  formError.value = null
  const username = String(values.username).trim().toLowerCase()
  mutation.mutate(
    { username, password: String(values.password), role: 'hr' },
    {
      onSuccess: () => {
        notify.success('HR user created', username)
        visible.value = false
      },
      onError: (error) => {
        if (isApiError(error) && Object.keys(error.fieldErrors).length > 0) {
          serverErrors.value = error.fieldErrors
          return
        }
        formError.value = isApiError(error) ? error.detail : 'Could not create the user'
      },
    },
  )
}
</script>

<template>
  <Dialog
    v-model:visible="visible"
    modal
    header="Create HR user"
    :style="{ width: 'min(420px, calc(100vw - 2rem))' }"
  >
    <Form
      ref="formRef"
      v-slot="$form"
      :resolver="resolver"
      :validate-on-value-update="false"
      :validate-on-blur="true"
      class="hr-form"
      @submit="onSubmit"
    >
      <Message v-if="formError" severity="error" icon="pi pi-exclamation-circle">
        {{ formError }}
      </Message>

      <FormItem
        label="Username"
        for="hr-username"
        hint="At least 3 characters, stored in lower case"
        :error="$form.username?.error?.message ?? serverErrors.username"
      >
        <InputText
          id="hr-username"
          name="username"
          placeholder="e.g. ihor_hr"
          autocomplete="off"
          autocapitalize="none"
          fluid
        />
      </FormItem>

      <FormItem
        label="Temporary password"
        for="hr-password"
        :error="$form.password?.error?.message ?? serverErrors.password"
      >
        <Password
          name="password"
          input-id="hr-password"
          placeholder="At least 8 characters"
          autocomplete="new-password"
          :feedback="false"
          toggle-mask
          fluid
        />
      </FormItem>

      <div class="hr-form__actions">
        <Button
          type="button"
          label="Cancel"
          severity="secondary"
          text
          :disabled="mutation.isPending.value"
          @click="visible = false"
        />
        <Button
          type="submit"
          label="Create"
          icon="pi pi-user-plus"
          :loading="mutation.isPending.value"
        />
      </div>
    </Form>
  </Dialog>
</template>

<style scoped>
.hr-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.hr-form__actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
