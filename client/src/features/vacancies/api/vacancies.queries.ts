import { computed, toValue, type MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'

import type { CreateVacancyPayload, UpdateVacancyPayload } from '../types/vacancy'
import { vacanciesApi } from './vacancies.api'

export const vacancyKeys = {
  all: ['vacancies'] as const,
  list: () => [...vacancyKeys.all, 'list'] as const,
  detail: (id: number) => [...vacancyKeys.all, 'detail', id] as const,
}

export function useVacanciesQuery() {
  return useQuery({ queryKey: vacancyKeys.list(), queryFn: vacanciesApi.list })
}

export function useVacancyQuery(id: MaybeRefOrGetter<number | null | undefined>) {
  return useQuery({
    queryKey: computed(() => vacancyKeys.detail(toValue(id) ?? -1)),
    queryFn: () => vacanciesApi.get(toValue(id)!),
    enabled: computed(() => toValue(id) != null),
  })
}

export function useCreateVacancyMutation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateVacancyPayload) => vacanciesApi.create(payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: vacancyKeys.list() }),
  })
}

export function useUpdateVacancyMutation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: UpdateVacancyPayload }) =>
      vacanciesApi.update(id, payload),
    onSuccess: (vacancy) => {
      queryClient.setQueryData(vacancyKeys.detail(vacancy.id), vacancy)
      return queryClient.invalidateQueries({ queryKey: vacancyKeys.list() })
    },
  })
}

export function useDeleteVacancyMutation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => vacanciesApi.remove(id),
    onSuccess: (_, id) => {
      queryClient.removeQueries({ queryKey: vacancyKeys.detail(id) })
      return queryClient.invalidateQueries({ queryKey: vacancyKeys.list() })
    },
  })
}
