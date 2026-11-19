export type UserRole = 'company_admin' | 'hr'

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface JwtClaims {
  id: number
  sub: string
  role: UserRole
  exp?: number
}

export interface AuthUser {
  id: number
  username: string
  role: UserRole
}

export interface LoginPayload {
  username: string
  password: string
}

export interface RegisterPayload {
  username: string
  password: string
  confirm_password: string
}
