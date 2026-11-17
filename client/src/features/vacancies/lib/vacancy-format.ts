import type { Vacancy } from '../types/vacancy'

const DAY_MS = 24 * 60 * 60 * 1000

export function isVacancyClosed(vacancy: Pick<Vacancy, 'status' | 'deadline_at'>): boolean {
  if (vacancy.status === 'closed') return true
  if (!vacancy.deadline_at) return false
  return new Date(vacancy.deadline_at).getTime() < Date.now()
}

export function formatSalary(vacancy: Vacancy): string | null {
  const { salary_min: min, salary_max: max, salary_currency: currency } = vacancy
  if (min == null && max == null) return null
  const format = (value: number) => new Intl.NumberFormat('en-US').format(value)
  const unit = currency ? `${currency} ` : ''
  if (min != null && max != null) return `${unit}${format(min)} – ${format(max)}`
  if (min != null) return `From ${unit}${format(min)}`
  return `Up to ${unit}${format(max!)}`
}

export function formatDate(iso: string): string {
  return new Intl.DateTimeFormat('en-GB', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(new Date(iso))
}

export function daysLeft(iso: string): number {
  return Math.max(0, Math.ceil((new Date(iso).getTime() - Date.now()) / DAY_MS))
}
