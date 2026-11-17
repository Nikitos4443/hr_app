import { computed, toValue, type MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'

import type { CreateCompanyPayload, UpdateCompanyPayload } from '../types/company'
import { companiesApi } from './companies.api'

export const companyKeys = {
  all: ['companies'] as const,
  detail: (id: number) => [...companyKeys.all, 'detail', id] as const,
}

export function useCompanyQuery(id: MaybeRefOrGetter<number | null | undefined>) {
  return useQuery({
    queryKey: computed(() => companyKeys.detail(toValue(id) ?? -1)),
    queryFn: () => companiesApi.get(toValue(id)!),
    enabled: computed(() => toValue(id) != null),
  })
}

export function useCreateCompanyMutation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateCompanyPayload) => companiesApi.create(payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: companyKeys.all }),
  })
}

export function useUpdateCompanyMutation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: UpdateCompanyPayload }) =>
      companiesApi.update(id, payload),
    onSuccess: (company) => queryClient.setQueryData(companyKeys.detail(company.id), company),
  })
}
