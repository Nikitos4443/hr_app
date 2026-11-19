import { http } from '@/shared/api'

import type { CreateUserPayload, UpdateUserPayload, User } from '../types/user'

export const usersApi = {
  list: () => http.get<User[]>('/users/'),
  get: (id: number) => http.get<User>(`/users/${id}`),
  create: (payload: CreateUserPayload) => http.post<User>('/users/', payload),
  update: (id: number, payload: UpdateUserPayload) => http.patch<User>(`/users/${id}`, payload),
  remove: (id: number) => http.delete(`/users/${id}`),
}
