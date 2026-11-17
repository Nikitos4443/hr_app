import type { SelectionStatus, VacancyStatus } from '../types/vacancy'

export interface Option<T extends string = string> {
  value: T
  label: string
}

export const EMPLOYMENT_TYPE_OPTIONS: Option[] = [
  { value: 'full_time', label: 'Full-time' },
  { value: 'part_time', label: 'Part-time' },
  { value: 'contract', label: 'Contract' },
  { value: 'internship', label: 'Internship' },
  { value: 'freelance', label: 'Freelance' },
]

export const CURRENCY_OPTIONS: Option[] = [
  { value: 'USD', label: 'USD ($)' },
  { value: 'EUR', label: 'EUR (€)' },
  { value: 'UAH', label: 'UAH (₴)' },
]

export const VACANCY_STATUS_OPTIONS: Option<VacancyStatus>[] = [
  { value: 'open', label: 'Open' },
  { value: 'closed', label: 'Closed' },
]

export const SELECTION_STATUS_OPTIONS: Option<SelectionStatus>[] = [
  { value: 'pending', label: 'Pending' },
  { value: 'running', label: 'In progress' },
  { value: 'done', label: 'Done' },
  { value: 'failed', label: 'Failed' },
]

export function employmentTypeLabel(value: string | null | undefined): string {
  if (!value) return '—'
  return EMPLOYMENT_TYPE_OPTIONS.find((option) => option.value === value)?.label ?? value
}

export function employmentTypeOptions(current?: string | null): Option[] {
  if (!current || EMPLOYMENT_TYPE_OPTIONS.some((option) => option.value === current)) {
    return EMPLOYMENT_TYPE_OPTIONS
  }
  return [...EMPLOYMENT_TYPE_OPTIONS, { value: current, label: current }]
}

export function currencyOptions(current?: string | null): Option[] {
  if (!current || CURRENCY_OPTIONS.some((option) => option.value === current)) {
    return CURRENCY_OPTIONS
  }
  return [...CURRENCY_OPTIONS, { value: current, label: current }]
}
