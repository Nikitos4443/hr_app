import { computed, toValue, type MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'

import { useSessionStore } from '@/features/auth'

import type { CreateUserPayload, UpdateUserPayload } from '../types/user'
import { usersApi } from './users.api'

export const userKeys = {
  all: ['users'] as const,
  list: () => [...userKeys.all, 'list'] as const,
  detail: (id: number) => [...userKeys.all, 'detail', id] as const,
}

export function useUsersQuery() {
  return useQuery({ queryKey: userKeys.list(), queryFn: usersApi.list })
}

export function useUserQuery(id: MaybeRefOrGetter<number | null | undefined>) {
  return useQuery({
    queryKey: computed(() => userKeys.detail(toValue(id) ?? -1)),
    queryFn: () => usersApi.get(toValue(id)!),
    enabled: computed(() => toValue(id) != null),
  })
}

export function useMeQuery() {
  const session = useSessionStore()
  return useUserQuery(() => session.user?.id)
}

export function useCreateUserMutation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateUserPayload) => usersApi.create(payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: userKeys.list() }),
  })
}

export function useUpdateUserMutation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: UpdateUserPayload }) =>
      usersApi.update(id, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: userKeys.all }),
  })
}

export function useDeleteUserMutation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => usersApi.remove(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: userKeys.all }),
  })
}
