import { computed, type Ref } from 'vue'
import { useRoute, useRouter, type LocationQueryValue } from 'vue-router'

import type { SelectionStatus, Vacancy, VacancyStatus } from '../types/vacancy'

export const PAGE_SIZE = 10

export type SortOrder = 'asc' | 'desc'

export interface VacancyFilterState {
  search: string
  status: VacancyStatus | null
  employmentType: string | null
  selection: SelectionStatus | null
  sort: SortOrder | null
  page: number
}

const STATUSES: VacancyStatus[] = ['open', 'closed']
const SELECTIONS: SelectionStatus[] = ['pending', 'running', 'done', 'failed']

function single(value: LocationQueryValue | LocationQueryValue[] | undefined): string | null {
  const first = Array.isArray(value) ? value[0] : value
  return first ? first : null
}

function oneOf<T extends string>(value: string | null, allowed: readonly T[]): T | null {
  return allowed.find((item) => item === value) ?? null
}

function deadlineTime(vacancy: Vacancy): number | null {
  return vacancy.deadline_at ? new Date(vacancy.deadline_at).getTime() : null
}

export function useVacancyFilters(vacancies: Ref<Vacancy[] | undefined>) {
  const route = useRoute()
  const router = useRouter()

  const state = computed<VacancyFilterState>(() => {
    const page = Number(single(route.query.page))
    return {
      search: single(route.query.q) ?? '',
      status: oneOf(single(route.query.status), STATUSES),
      employmentType: single(route.query.type),
      selection: oneOf(single(route.query.ai), SELECTIONS),
      sort: oneOf(single(route.query.sort), ['asc', 'desc'] as const),
      page: Number.isInteger(page) && page > 0 ? page : 1,
    }
  })

  const hasActiveFilters = computed(() => {
    const { search, status, employmentType, selection } = state.value
    return Boolean(search || status || employmentType || selection)
  })

  function update(patch: Partial<VacancyFilterState>, keepPage = false) {
    const next = { ...state.value, ...patch, page: keepPage ? (patch.page ?? 1) : 1 }
    const query: Record<string, string> = {}
    if (next.search) query.q = next.search
    if (next.status) query.status = next.status
    if (next.employmentType) query.type = next.employmentType
    if (next.selection) query.ai = next.selection
    if (next.sort) query.sort = next.sort
    if (next.page > 1) query.page = String(next.page)
    router.replace({ query })
  }

  function setPage(page: number) {
    update({ page }, true)
  }

  function toggleSort() {
    const order: SortOrder = state.value.sort === 'asc' ? 'desc' : 'asc'
    update({ sort: order }, true)
  }

  function reset() {
    router.replace({ query: state.value.sort ? { sort: state.value.sort } : {} })
  }

  const filtered = computed(() => {
    const { search, status, employmentType, selection, sort } = state.value
    const needle = search.trim().toLowerCase()
    const rows = (vacancies.value ?? []).filter((vacancy) => {
      if (status && vacancy.status !== status) return false
      if (employmentType && vacancy.employment_type !== employmentType) return false
      if (selection && vacancy.selection_status !== selection) return false
      if (!needle) return true
      return (
        vacancy.title.toLowerCase().includes(needle) ||
        (vacancy.location ?? '').toLowerCase().includes(needle)
      )
    })
    if (!sort) return rows
    const direction = sort === 'asc' ? 1 : -1
    return [...rows].sort((a, b) => {
      const left = deadlineTime(a)
      const right = deadlineTime(b)
      if (left === right) return 0
      if (left === null) return 1
      if (right === null) return -1
      return (left - right) * direction
    })
  })

  const pageCount = computed(() => Math.max(1, Math.ceil(filtered.value.length / PAGE_SIZE)))
  const currentPage = computed(() => Math.min(state.value.page, pageCount.value))
  const pageRows = computed(() =>
    filtered.value.slice((currentPage.value - 1) * PAGE_SIZE, currentPage.value * PAGE_SIZE),
  )

  return {
    state,
    hasActiveFilters,
    filtered,
    pageRows,
    currentPage,
    update,
    setPage,
    toggleSort,
    reset,
  }
}
