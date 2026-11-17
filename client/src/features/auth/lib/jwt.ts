import type { JwtClaims } from '../types/auth'

export function decodeJwt(token: string): JwtClaims | null {
  try {
    const payload = token.split('.')[1]
    if (!payload) return null
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/')
    const json = new TextDecoder().decode(Uint8Array.from(atob(base64), (c) => c.charCodeAt(0)))
    const claims = JSON.parse(json) as Partial<JwtClaims>
    if (typeof claims.id !== 'number' || typeof claims.sub !== 'string' || !claims.role) return null
    return claims as JwtClaims
  } catch {
    return null
  }
}

export function isExpired(claims: JwtClaims, skewSeconds = 5): boolean {
  return claims.exp !== undefined && claims.exp - skewSeconds <= Date.now() / 1000
}
