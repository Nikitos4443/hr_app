import { http } from '@/shared/api'

import type { LoginPayload, RegisterPayload, TokenResponse } from '../types/auth'

export const authApi = {
  login: (payload: LoginPayload) =>
    http.post<TokenResponse>('/auth/token', undefined, { form: { ...payload }, auth: 'none' }),

  register: (payload: RegisterPayload) =>
    http.post<TokenResponse>('/auth/', payload, { auth: 'none' }),
}
