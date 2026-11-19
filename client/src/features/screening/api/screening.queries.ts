import { computed, toValue, type MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery } from '@tanstack/vue-query'

import { uploadToPresignedPost } from '@/shared/api'

import type { ScreeningQuestions, ScreeningSession } from '../types/screening'
import { screeningApi } from './screening.api'
import { screeningQuestionsApi } from './screening-questions.api'

export const screeningKeys = {
  all: ['screening'] as const,
  session: (token: string) => [...screeningKeys.all, 'session', token] as const,
  questions: (token: string) => [...screeningKeys.all, 'questions', token] as const,
}

export function useScreeningQuery(token: MaybeRefOrGetter<string | null | undefined>) {
  return useQuery<ScreeningSession>({
    queryKey: computed(() => screeningKeys.session(toValue(token) ?? '')),
    queryFn: () => screeningApi.get(toValue(token)!),
    enabled: computed(() => !!toValue(token)),
    retry: false,
  })
}

export function useScreeningQuestionsQuery(token: MaybeRefOrGetter<string | null | undefined>) {
  return useQuery<ScreeningQuestions>({
    queryKey: computed(() => screeningKeys.questions(toValue(token) ?? '')),
    queryFn: () => screeningQuestionsApi.get(toValue(token)!),
    enabled: computed(() => !!toValue(token)),
    retry: false,
    staleTime: Infinity,
  })
}

export function useSaveTextAnswerMutation(token: MaybeRefOrGetter<string>) {
  return useMutation({
    mutationFn: ({ questionId, answer }: { questionId: number; answer: string }) =>
      screeningApi.saveTextAnswer(toValue(token), questionId, answer),
  })
}

export interface UploadVideoInput {
  questionId: number
  video: Blob
  onProgress?: (percent: number) => void
  signal?: AbortSignal
}

export function useUploadVideoAnswerMutation(token: MaybeRefOrGetter<string>) {
  return useMutation({
    mutationFn: async ({ questionId, video, onProgress, signal }: UploadVideoInput) => {
      const post = await screeningApi.getVideoUploadUrl(toValue(token), questionId)
      const fields = { ...post.fields, 'Content-Type': video.type || 'video/webm' }
      await uploadToPresignedPost({ ...post, fields }, video, { onProgress, signal })
    },
  })
}
