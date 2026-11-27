import { computed, toValue, type MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery } from '@tanstack/vue-query'

import { uploadToPresignedPost } from '@/shared/api'

import type { ScreeningSession } from '../types/screening'
import { screeningApi } from './screening.api'

export const screeningKeys = {
  all: ['screening'] as const,
  session: (token: string) => [...screeningKeys.all, 'session', token] as const,
}

export function useScreeningQuery(token: MaybeRefOrGetter<string | null | undefined>) {
  return useQuery<ScreeningSession>({
    queryKey: computed(() => screeningKeys.session(toValue(token) ?? '')),
    queryFn: () => screeningApi.get(toValue(token)!),
    enabled: computed(() => !!toValue(token)),
    retry: false,
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
      // S3 checks POST-policy `starts-with` on Content-Type per comma-separated part, so a
      // recorder type like "video/webm;codecs=vp8,opus" fails; send only the base MIME type.
      const contentType = video.type.split(';')[0]?.trim() || 'video/webm'
      const fields = { ...post.fields, 'Content-Type': contentType }
      await uploadToPresignedPost({ ...post, fields }, video, { onProgress, signal })
    },
  })
}
