import { http, uploadToPresignedPost, type PresignedPost } from '@/shared/api'

import type { CreateApplicationPayload } from '../types/application'

export interface SubmitApplicationInput extends CreateApplicationPayload {
  resume: File
  onProgress?: (percent: number) => void
}

export const applyApi = {
  createApplication: (payload: CreateApplicationPayload) =>
    http.post<PresignedPost>('/flow/resume-get-presigned-post-url', payload, { auth: 'none' }),

  async submit({ resume, onProgress, ...payload }: SubmitApplicationInput): Promise<void> {
    const post = await applyApi.createApplication(payload)
    await uploadToPresignedPost(post, resume, { onProgress })
  },
}
