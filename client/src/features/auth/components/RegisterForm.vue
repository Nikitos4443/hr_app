<script setup lang="ts">
import { computed, nextTick } from 'vue'
import { Form, type FormSubmitEvent } from '@primevue/forms'
import { zodResolver } from '@primevue/forms/resolvers/zod'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Password from 'primevue/password'

import { errorMessage } from '@/shared/api'
import { FormItem } from '@/shared/ui'

import { useAuthRedirect } from '../composables/useAuthRedirect'
import { useRegisterMutation } from '../api/auth.queries'
import { registerSchema } from '../lib/schemas'

const resolver = zodResolver(registerSchema)
const register = useRegisterMutation()
const { redirectAfterAuth } = useAuthRedirect()

const errorText = computed(() => (register.error.value ? errorMessage(register.error.value) : null))

// Wait for FormItem to sync aria-invalid onto the controls, then jump to the first one.
async function focusFirstInvalid() {
  await nextTick()
  await nextTick()
  const el = document.querySelector<HTMLElement>('.auth-form [aria-invalid="true"]')
  if (!el) return
  el.scrollIntoView({ block: 'center' })
  el.focus({ preventScroll: true })
}

function onSubmit({ valid, values }: FormSubmitEvent) {
  if (!valid) {
    focusFirstInvalid()
    return
  }
  register.mutate(
    {
      username: values.username.trim().toLowerCase(),
      password: values.password,
      confirm_password: values.password,
    },
    { onSuccess: redirectAfterAuth },
  )
}
</script>

<template>
  <Form
    v-slot="$form"
    :resolver="resolver"
    :validate-on-value-update="false"
    :validate-on-blur="true"
    class="auth-form"
    @submit="onSubmit"
  >
    <Message v-if="errorText" severity="error" icon="pi pi-exclamation-circle">
      <strong>Couldn't create the account.</strong> {{ errorText }}
    </Message>

    <FormItem
      label="Username"
      for="register-username"
      hint="Letters are saved in lower case"
      :error="$form.username?.error?.message"
    >
      <IconField>
        <InputIcon class="pi pi-user" />
        <InputText
          id="register-username"
          name="username"
          autocomplete="username"
          autocapitalize="none"
          fluid
        />
      </IconField>
    </FormItem>

    <FormItem
      label="Password"
      for="register-password"
      hint="Use a password you haven't used anywhere else"
      :error="$form.password?.error?.message"
    >
      <Password
        name="password"
        input-id="register-password"
        autocomplete="new-password"
        :feedback="false"
        toggle-mask
        fluid
      />
    </FormItem>

    <Button
      type="submit"
      label="Create account"
      size="large"
      :loading="register.isPending.value"
      fluid
    />
  </Form>
</template>

<style scoped>
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
