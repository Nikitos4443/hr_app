import { http } from '@/shared/api'

import type { Company, CreateCompanyPayload, UpdateCompanyPayload } from '../types/company'

export const companiesApi = {
  get: (id: number) => http.get<Company>(`/companies/${id}`),
  create: (payload: CreateCompanyPayload) => http.post<Company>('/companies/', payload),
  update: (id: number, payload: UpdateCompanyPayload) =>
    http.patch<Company>(`/companies/${id}`, payload),
  remove: (id: number) => http.delete(`/companies/${id}`),
}
