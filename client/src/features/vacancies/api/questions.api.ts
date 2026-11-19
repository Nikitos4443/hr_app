import { http } from '@/shared/api'

import type { QuestionInput, VacancyQuestion } from '../types/question'

export const questionsApi = {
  list: (vacancyId: number) => http.get<VacancyQuestion[]>(`/vacancies/${vacancyId}/questions`),
  replace: (vacancyId: number, items: QuestionInput[]) =>
    http.put<VacancyQuestion[]>(`/vacancies/${vacancyId}/questions`, items),
}
