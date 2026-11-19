import { computed, toValue, type MaybeRefOrGetter } from 'vue'
import { keepPreviousData, useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'

import type { ApplicationAction, ApplicationListParams } from '../types/application'
import { applicationsApi } from './applications.api'

export const applicationKeys = {
  all: ['applications'] as const,
  list: (vacancyId: number, params: ApplicationListParams) =>
    [...applicationKeys.all, 'list', vacancyId, params] as const,
  counts: (vacancyId: number) => [...applicationKeys.all, 'counts', vacancyId] as const,
  detail: (id: number) => [...applicationKeys.all, 'detail', id] as const,
}

export function useApplicationsQuery(
  vacancyId: MaybeRefOrGetter<number>,
  params: MaybeRefOrGetter<ApplicationListParams>,
) {
  return useQuery({
    queryKey: computed(() => applicationKeys.list(toValue(vacancyId), toValue(params))),
    queryFn: () => applicationsApi.listByVacancy(toValue(vacancyId), toValue(params)),
    placeholderData: keepPreviousData,
  })
}

/** Per-status totals for a vacancy (one-row page, only `counts` is used). */
export function useApplicationCountsQuery(vacancyId: MaybeRefOrGetter<number>) {
  return useQuery({
    queryKey: computed(() => applicationKeys.counts(toValue(vacancyId))),
    queryFn: () =>
      applicationsApi.listByVacancy(toValue(vacancyId), {
        sort: 'created_at',
        order: 'desc',
        limit: 1,
        offset: 0,
      }),
    select: (data) => data.counts,
  })
}

export function useApplicationQuery(id: MaybeRefOrGetter<number | null | undefined>) {
  return useQuery({
    queryKey: computed(() => applicationKeys.detail(toValue(id) ?? -1)),
    queryFn: () => applicationsApi.get(toValue(id)!),
    enabled: computed(() => toValue(id) != null),
  })
}

export function useApplicationActionMutation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, action }: { id: number; action: ApplicationAction }) =>
      applicationsApi.act(id, action),
    // Statuses, counts and ranks all change together, so refetch every application query.
    onSuccess: () => queryClient.invalidateQueries({ queryKey: applicationKeys.all }),
  })
}

export function useBulkActionMutation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      vacancyId,
      ids,
      action,
    }: {
      vacancyId: number
      ids: number[]
      action: ApplicationAction
    }) => applicationsApi.bulk(vacancyId, ids, action),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: applicationKeys.all }),
  })
}
