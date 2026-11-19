import { http } from '@/shared/api'

import type {
  ApplicationAction,
  ApplicationActionResult,
  ApplicationDetail,
  ApplicationList,
  ApplicationListParams,
  BulkActionResult,
} from '../types/application'

export const applicationsApi = {
  listByVacancy: (vacancyId: number, params: ApplicationListParams) =>
    http.get<ApplicationList>(`/vacancies/${vacancyId}/applications`, {
      query: {
        status: params.status,
        search: params.search,
        sort: params.sort,
        order: params.order,
        limit: params.limit,
        offset: params.offset,
      },
    }),

  get: (id: number) => http.get<ApplicationDetail>(`/applications/${id}`),

  act: (id: number, action: ApplicationAction) =>
    http.post<ApplicationActionResult>(`/applications/${id}/${action}`),

  bulk: (vacancyId: number, ids: number[], action: ApplicationAction) =>
    http.post<BulkActionResult>(`/vacancies/${vacancyId}/applications/bulk`, { ids, action }),
}
