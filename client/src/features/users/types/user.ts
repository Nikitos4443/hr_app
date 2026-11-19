import type { UserRole } from '@/features/auth'

export interface User {
  id: number
  username: string
  role: UserRole
  company_id: number | null
  created_at?: string | null
}

export interface CreateUserPayload {
  username: string
  password: string
  role?: UserRole
}

export interface UpdateUserPayload {
  username?: string
  password?: string
  role?: UserRole
}
