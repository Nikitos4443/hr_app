import { ApiError } from './errors'

export interface PresignedPost {
  url: string
  fields: Record<string, string>
}

export function uploadToPresignedPost(
  post: PresignedPost,
  file: Blob,
  options: { onProgress?: (percent: number) => void; signal?: AbortSignal } = {},
): Promise<void> {
  return new Promise((resolve, reject) => {
    const form = new FormData()
    for (const [key, value] of Object.entries(post.fields)) form.append(key, value)
    form.append('file', file)

    const xhr = new XMLHttpRequest()
    xhr.open('POST', post.url)

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable)
        options.onProgress?.(Math.round((event.loaded / event.total) * 100))
    }
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) resolve()
      else reject(new ApiError(xhr.status, 'File upload failed'))
    }
    xhr.onerror = () => reject(new ApiError(0, 'Network error during upload'))
    xhr.onabort = () => reject(new DOMException('Upload aborted', 'AbortError'))

    options.signal?.addEventListener('abort', () => xhr.abort(), { once: true })
    xhr.send(form)
  })
}
