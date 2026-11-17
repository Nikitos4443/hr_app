import { env } from '@/shared/config/env'

import { ApiError, parseErrorBody } from './errors'

export type AuthMode = 'staff' | 'none'

export interface HttpHooks {
  getToken: () => string | null
  onUnauthorized: () => void
}

let hooks: HttpHooks = { getToken: () => null, onUnauthorized: () => {} }

export function configureHttp(next: Partial<HttpHooks>) {
  hooks = { ...hooks, ...next }
}

type QueryValue = string | number | boolean | null | undefined

export interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  query?: Record<string, QueryValue>
  json?: unknown
  form?: Record<string, string>
  auth?: AuthMode
  signal?: AbortSignal
}

function buildUrl(path: string, query?: RequestOptions['query']): string {
  const url = `${env.apiUrl}${path.startsWith('/') ? path : `/${path}`}`
  if (!query) return url
  const params = new URLSearchParams()
  for (const [key, value] of Object.entries(query)) {
    if (value !== null && value !== undefined && value !== '') params.set(key, String(value))
  }
  const qs = params.toString()
  return qs ? `${url}?${qs}` : url
}

async function readBody(response: Response): Promise<unknown> {
  if (response.status === 204) return undefined
  const text = await response.text()
  if (!text) return undefined
  try {
    return JSON.parse(text)
  } catch {
    return text
  }
}

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', query, json, form, auth = 'staff', signal } = options

  const headers: Record<string, string> = { Accept: 'application/json' }
  let body: BodyInit | undefined

  if (form) {
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    body = new URLSearchParams(form)
  } else if (json !== undefined) {
    headers['Content-Type'] = 'application/json'
    body = JSON.stringify(json)
  }

  const token = auth === 'staff' ? hooks.getToken() : null
  if (token) headers.Authorization = `Bearer ${token}`

  let response: Response
  try {
    response = await fetch(buildUrl(path, query), { method, headers, body, signal })
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') throw error
    throw new ApiError(0, 'Network error. Check your connection and try again.')
  }

  const data = await readBody(response)

  if (!response.ok) {
    if (response.status === 401 && token) hooks.onUnauthorized()
    throw parseErrorBody(response.status, data)
  }

  return data as T
}

export const http = {
  get: <T>(path: string, options?: Omit<RequestOptions, 'method' | 'json' | 'form'>) =>
    request<T>(path, { ...options, method: 'GET' }),
  post: <T>(path: string, json?: unknown, options?: Omit<RequestOptions, 'method' | 'json'>) =>
    request<T>(path, { ...options, method: 'POST', json }),
  put: <T>(path: string, json?: unknown, options?: Omit<RequestOptions, 'method' | 'json'>) =>
    request<T>(path, { ...options, method: 'PUT', json }),
  patch: <T>(path: string, json?: unknown, options?: Omit<RequestOptions, 'method' | 'json'>) =>
    request<T>(path, { ...options, method: 'PATCH', json }),
  delete: <T = void>(path: string, options?: Omit<RequestOptions, 'method' | 'json' | 'form'>) =>
    request<T>(path, { ...options, method: 'DELETE' }),
}
