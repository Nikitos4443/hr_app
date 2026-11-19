import { computed } from 'vue'
import { useRoute, useRouter, type LocationQueryValue } from 'vue-router'

import { DEFAULT_SORT, SORT_OPTIONS, sortOrder } from '../lib/application-meta'
import type {
  ApplicationListParams,
  ApplicationSort,
  ApplicationStatus,
} from '../types/application'

export const PAGE_SIZE = 10

export interface ApplicationFilterState {
  status: ApplicationStatus | null
  search: string
  sort: ApplicationSort
  page: number
}

const STATUSES: ApplicationStatus[] = ['pending', 'invited', 'shortlisted', 'rejected']
const SORTS = SORT_OPTIONS.map((option) => option.value)

function single(value: LocationQueryValue | LocationQueryValue[] | undefined): string | null {
  const first = Array.isArray(value) ? value[0] : value
  return first ? first : null
}

function oneOf<T extends string>(value: string | null, allowed: readonly T[]): T | null {
  return allowed.find((item) => item === value) ?? null
}

/**
 * Candidate list filters kept in `route.query` so the view is shareable.
 * Query keys that belong to other features (`tab`, `candidate`) are preserved on update.
 */
export function useApplicationFilters() {
  const route = useRoute()
  const router = useRouter()

  const state = computed<ApplicationFilterState>(() => {
    const page = Number(single(route.query.page))
    return {
      status: oneOf(single(route.query.status), STATUSES),
      search: single(route.query.q) ?? '',
      sort: oneOf(single(route.query.sort), SORTS) ?? DEFAULT_SORT,
      page: Number.isInteger(page) && page > 0 ? page : 1,
    }
  })

  const hasActiveFilters = computed(() => Boolean(state.value.status || state.value.search))

  const params = computed<ApplicationListParams>(() => ({
    status: state.value.status,
    search: state.value.search || undefined,
    sort: state.value.sort,
    order: sortOrder(state.value.sort),
    limit: PAGE_SIZE,
    offset: (state.value.page - 1) * PAGE_SIZE,
  }))

  function update(patch: Partial<ApplicationFilterState>, keepPage = false) {
    const next = { ...state.value, ...patch, page: keepPage ? (patch.page ?? 1) : 1 }
    const query = { ...route.query }
    const assign = (key: string, value: string | null) => {
      if (value) query[key] = value
      else delete query[key]
    }
    assign('status', next.status)
    assign('q', next.search || null)
    assign('sort', next.sort === DEFAULT_SORT ? null : next.sort)
    assign('page', next.page > 1 ? String(next.page) : null)
    router.replace({ query })
  }

  function setPage(page: number) {
    update({ page }, true)
  }

  function reset() {
    update({ status: null, search: '' })
  }

  return { state, params, hasActiveFilters, update, setPage, reset }
}
