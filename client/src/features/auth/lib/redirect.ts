export const DEFAULT_AUTH_REDIRECT = '/app/vacancies'

export function resolveRedirect(value: unknown): string {
  if (typeof value !== 'string') return DEFAULT_AUTH_REDIRECT
  if (!value.startsWith('/') || value.startsWith('//')) return DEFAULT_AUTH_REDIRECT
  return value
}
