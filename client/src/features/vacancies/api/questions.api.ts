import { http } from '@/shared/api'

import type { VacancyQuestion } from '../types/question'

export const questionsApi = {
  list: (vacancyId: number) => http.get<VacancyQuestion[]>(`/vacancies/${vacancyId}/questions`),
}
