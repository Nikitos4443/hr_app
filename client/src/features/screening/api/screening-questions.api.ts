import { http } from '@/shared/api'

import type { ScreeningQuestions } from '../types/screening'
import { isScreeningMockEnabled, mockScreeningQuestions } from './screening.mock'

export const screeningQuestionsApi = {
  get: (token: string): Promise<ScreeningQuestions> =>
    isScreeningMockEnabled()
      ? mockScreeningQuestions()
      : http.get<ScreeningQuestions>(`/flow/screening/${encodeURIComponent(token)}/questions`, {
          auth: 'none',
        }),
}
