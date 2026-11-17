import { useMutation } from '@tanstack/vue-query'

import { useSessionStore } from '../stores/session.store'
import type { LoginPayload, RegisterPayload, TokenResponse } from '../types/auth'
import { authApi } from './auth.api'

function useStartSession() {
  const session = useSessionStore()
  return (response: TokenResponse) => {
    if (!session.setToken(response.access_token)) {
      throw new Error('The server returned an invalid token')
    }
  }
}

export function useLoginMutation() {
  const startSession = useStartSession()
  return useMutation({
    mutationFn: (payload: LoginPayload) => authApi.login(payload),
    onSuccess: startSession,
  })
}

export function useRegisterMutation() {
  const startSession = useStartSession()
  return useMutation({
    mutationFn: (payload: RegisterPayload) => authApi.register(payload),
    onSuccess: startSession,
  })
}
