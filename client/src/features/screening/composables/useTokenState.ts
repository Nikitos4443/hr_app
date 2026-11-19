import { computed, toValue, type MaybeRefOrGetter } from 'vue'

import { isApiError } from '@/shared/api'

import { useScreeningQuery } from '../api/screening.queries'
import type { EndState, TokenState } from '../types/screening'

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

const TRUSTED_REQUESTED_STATES: readonly EndState[] = ['done', 'completed', 'in_review']

/**
 * Resolves the end screen from the real screening session instead of trusting `?state=`.
 * Errors from the API decide invalid/rejected/processing; the query string may only pick
 * between the "positive" end states once the token is confirmed to be valid.
 */
export function useScreeningEndState(
  token: MaybeRefOrGetter<string>,
  requested: MaybeRefOrGetter<string | undefined>,
) {
  const session = useScreeningQuery(token)

  const state = computed<EndState | null>(() => {
    if (session.isPending.value) return null
    if (session.isError.value) return tokenStateFromError(session.error.value)
    const wanted = toValue(requested) as EndState | undefined
    return wanted && TRUSTED_REQUESTED_STATES.includes(wanted) ? wanted : 'done'
  })

  return {
    state,
    isLoading: session.isPending,
    hasError: computed(() => session.isError.value && state.value === null),
    retry: () => session.refetch(),
  }
}
