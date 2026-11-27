import { http, type PresignedPost } from '@/shared/api'

import type { ScreeningSession, TextAnswerResult } from '../types/screening'
import { isScreeningMockEnabled, mockScreeningSession } from './screening.mock'

const base = (token: string) => `/flow/screening/${encodeURIComponent(token)}`

export const screeningApi = {
  get: (token: string): Promise<ScreeningSession> =>
    isScreeningMockEnabled()
      ? mockScreeningSession()
      : http.get<ScreeningSession>(base(token), { auth: 'none' }),

  getVideoUploadUrl: (token: string, questionId: number) =>
    http.post<PresignedPost>(`${base(token)}/questions/${questionId}/video-upload-url`, undefined, {
      auth: 'none',
    }),

  saveTextAnswer: (token: string, questionId: number, answer: string) =>
    http.put<TextAnswerResult>(
      `${base(token)}/questions/${questionId}/text-answer`,
      { answer },
      { auth: 'none' },
    ),
}
