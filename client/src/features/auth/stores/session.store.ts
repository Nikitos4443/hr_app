import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import { decodeJwt, isExpired } from '../lib/jwt'
import { readToken, writeToken } from '../lib/token-storage'
import type { AuthUser, UserRole } from '../types/auth'

export const useSessionStore = defineStore('session', () => {
  const token = ref<string | null>(null)
  const user = ref<AuthUser | null>(null)
  let expiryTimer: ReturnType<typeof setTimeout> | undefined

  const isAuthenticated = computed(() => token.value !== null && user.value !== null)

  function clearTimer() {
    if (expiryTimer) clearTimeout(expiryTimer)
    expiryTimer = undefined
  }

  function logout() {
    clearTimer()
    token.value = null
    user.value = null
    writeToken(null)
  }

  function setToken(next: string): boolean {
    const claims = decodeJwt(next)
    if (!claims || isExpired(claims)) {
      logout()
      return false
    }

    token.value = next
    user.value = { id: claims.id, username: claims.sub, role: claims.role }
    writeToken(next)

    clearTimer()
    if (claims.exp !== undefined) {
      const ms = Math.min(claims.exp * 1000 - Date.now(), 2 ** 31 - 1)
      expiryTimer = setTimeout(logout, Math.max(ms, 0))
    }
    return true
  }

  function restore() {
    const stored = readToken()
    if (stored) setToken(stored)
  }

  function hasRole(...roles: UserRole[]): boolean {
    return user.value !== null && roles.includes(user.value.role)
  }

  return { token, user, isAuthenticated, setToken, logout, restore, hasRole }
})
