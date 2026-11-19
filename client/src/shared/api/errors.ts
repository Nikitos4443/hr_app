interface ValidationIssue {
  loc?: unknown[]
  msg?: string
}

export class ApiError extends Error {
  readonly status: number
  readonly detail: string
  readonly fieldErrors: Record<string, string>

  constructor(status: number, detail: string, fieldErrors: Record<string, string> = {}) {
    super(detail)
    this.name = 'ApiError'
    this.status = status
    this.detail = detail
    this.fieldErrors = fieldErrors
  }
}

function cleanMessage(msg: string): string {
  return msg.replace(/^Value error,\s*/i, '')
}

export function parseErrorBody(status: number, body: unknown): ApiError {
  const fallback = status === 0 ? 'Network error' : `Request failed (${status})`
  const detail = (body as { detail?: unknown } | null)?.detail

  if (typeof detail === 'string') return new ApiError(status, detail)

  if (Array.isArray(detail)) {
    const fieldErrors: Record<string, string> = {}
    const messages: string[] = []
    for (const issue of detail as ValidationIssue[]) {
      const msg = cleanMessage(issue.msg ?? 'Invalid value')
      messages.push(msg)
      const field = issue.loc?.at(-1)
      if (typeof field === 'string' && !(field in fieldErrors)) fieldErrors[field] = msg
    }
    return new ApiError(status, messages.join('; ') || fallback, fieldErrors)
  }

  return new ApiError(status, fallback)
}

export const isApiError = (e: unknown): e is ApiError => e instanceof ApiError
export const isUnauthorized = (e: unknown) => isApiError(e) && e.status === 401
export const isForbidden = (e: unknown) => isApiError(e) && e.status === 403
export const isNotFound = (e: unknown) => isApiError(e) && e.status === 404

export function errorMessage(error: unknown, fallback = 'Unexpected error'): string {
  return isApiError(error) ? error.detail : error instanceof Error ? error.message : fallback
}
