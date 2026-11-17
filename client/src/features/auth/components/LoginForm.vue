<script setup lang="ts">
import { computed } from 'vue'
import { Form, type FormSubmitEvent } from '@primevue/forms'
import { zodResolver } from '@primevue/forms/resolvers/zod'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Password from 'primevue/password'

import { isApiError } from '@/shared/api'
import { FormItem } from '@/shared/ui'

import { useAuthRedirect } from '../composables/useAuthRedirect'
import { useLoginMutation } from '../api/auth.queries'
import { loginSchema } from '../lib/schemas'

const resolver = zodResolver(loginSchema)
const login = useLoginMutation()
const { redirectAfterAuth } = useAuthRedirect()

const errorText = computed(() => {
  const error = login.error.value
  if (!error) return null
  if (isApiError(error) && (error.status === 400 || error.status === 401)) {
    return 'Check your username and password.'
  }
  return error instanceof Error ? error.message : 'Unexpected error'
})

function onSubmit({ valid, values }: FormSubmitEvent) {
  if (!valid) return
  login.mutate(
    { username: values.username.trim().toLowerCase(), password: values.password },
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
      <strong>Couldn't sign in.</strong> {{ errorText }}
    </Message>

    <FormItem label="Username" for="login-username" :error="$form.username?.error?.message">
      <IconField>
        <InputIcon class="pi pi-user" />
        <InputText
          id="login-username"
          name="username"
          autocomplete="username"
          autocapitalize="none"
          fluid
        />
      </IconField>
    </FormItem>

    <FormItem label="Password" for="login-password" :error="$form.password?.error?.message">
      <Password
        name="password"
        input-id="login-password"
        autocomplete="current-password"
        :feedback="false"
        toggle-mask
        fluid
      />
    </FormItem>

    <Button type="submit" label="Sign in" size="large" :loading="login.isPending.value" fluid />
  </Form>
</template>

<style scoped>
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
