import { computed, toValue, type MaybeRefOrGetter } from 'vue'

import { isApiError } from '@/shared/api'

import type { TokenState } from '../types/screening'

export function tokenStateFromError(error: unknown): TokenState | null {
  if (!isApiError(error)) return null
  switch (error.status) {
    case 404:
    case 410:
      return 'invalid'
    case 403:
      return 'rejected'
    case 409:
      return 'processing'
    default:
      return null
  }
}

export function useTokenState(error: MaybeRefOrGetter<unknown>) {
  return computed(() => tokenStateFromError(toValue(error)))
}
