import { http } from '@/shared/api'

import type { PublicVacancy } from '../types/public-vacancy'
import { getMockPublicVacancy } from './public-vacancy.mock'

const useMocks = import.meta.env.VITE_USE_MOCKS === 'true'

export const publicVacancyApi = {
  get: (id: number): Promise<PublicVacancy> =>
    useMocks
      ? getMockPublicVacancy(id)
      : http.get<PublicVacancy>(`/vacancies/public/${id}`, { auth: 'none' }),
}
