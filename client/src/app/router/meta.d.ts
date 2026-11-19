import type { UserRole } from '@/features/auth'

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    guestOnly?: boolean
    roles?: UserRole[]
    /** Page title; empty string means the bare app name. */
    title?: string
  }
}
