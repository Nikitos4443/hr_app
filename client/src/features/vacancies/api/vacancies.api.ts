import { http } from '@/shared/api'

import type { CreateVacancyPayload, UpdateVacancyPayload, Vacancy } from '../types/vacancy'

export const vacanciesApi = {
  list: () => http.get<Vacancy[]>('/vacancies/'),
  get: (id: number) => http.get<Vacancy>(`/vacancies/${id}`),
  create: (payload: CreateVacancyPayload) => http.post<Vacancy>('/vacancies/', payload),
  update: (id: number, payload: UpdateVacancyPayload) =>
    http.patch<Vacancy>(`/vacancies/${id}`, payload),
  remove: (id: number) => http.delete(`/vacancies/${id}`),
}
