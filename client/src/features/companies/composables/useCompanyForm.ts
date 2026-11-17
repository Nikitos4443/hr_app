import { computed, ref, type Ref } from 'vue'
import { zodResolver } from '@primevue/forms/resolvers/zod'
import type { FormSubmitEvent } from '@primevue/forms'

import { useQueryClient } from '@tanstack/vue-query'

import { isApiError } from '@/shared/api'
import { useNotify } from '@/shared/composables/useNotify'
import { userKeys } from '@/features/users'

import { useCreateCompanyMutation, useUpdateCompanyMutation } from '../api/companies.queries'
import { companySchema, type CompanyFormValues } from '../lib/schemas'
import type { Company } from '../types/company'

export function useCompanyForm(company: Ref<Company | null>) {
  const resolver = zodResolver(companySchema)
  const notify = useNotify()
  const queryClient = useQueryClient()
  const createMutation = useCreateCompanyMutation()
  const updateMutation = useUpdateCompanyMutation()
  const serverErrors = ref<Record<string, string>>({})
  const formError = ref<string | null>(null)

  const isEdit = computed(() => company.value !== null)
  const isPending = computed(() => createMutation.isPending.value || updateMutation.isPending.value)

  const initialValues = computed<CompanyFormValues>(() => ({
    name: company.value?.name ?? '',
    description: company.value?.description ?? '',
    website: company.value?.website ?? '',
  }))

  function clearErrors() {
    serverErrors.value = {}
    formError.value = null
  }

  function handleError(error: unknown) {
    if (isApiError(error)) {
      serverErrors.value = error.fieldErrors
      formError.value = Object.keys(error.fieldErrors).length > 0 ? null : error.detail
      return
    }
    formError.value = error instanceof Error ? error.message : 'Unexpected error'
  }

  function submit({ valid, values }: FormSubmitEvent) {
    if (!valid) return
    clearErrors()
    const name = String(values.name).trim()
    const description = String(values.description ?? '').trim()
    const website = String(values.website ?? '').trim()

    if (company.value) {
      updateMutation.mutate(
        { id: company.value.id, payload: { name, description, website } },
        {
          onSuccess: () => notify.success('Company profile saved'),
          onError: handleError,
        },
      )
      return
    }

    createMutation.mutate(
      { name, description: description || null, website: website || null },
      {
        onSuccess: () => {
          notify.success('Company created')
          void queryClient.invalidateQueries({ queryKey: userKeys.all })
        },
        onError: handleError,
      },
    )
  }

  return {
    resolver,
    initialValues,
    isEdit,
    isPending,
    serverErrors,
    formError,
    submit,
    clearErrors,
  }
}
