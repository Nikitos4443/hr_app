import { z } from 'zod'

export const RESUME_CONTENT_TYPE = 'application/pdf'
export const MAX_RESUME_SIZE_BYTES = 5 * 1024 * 1024

export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function isPdf(file: File): boolean {
  return file.type === RESUME_CONTENT_TYPE || file.name.toLowerCase().endsWith('.pdf')
}

export const resumeSchema = z
  .instanceof(File, { error: 'Attach your resume as a PDF file' })
  .refine(isPdf, { error: 'Only PDF files are supported' })
  .refine((file) => file.size <= MAX_RESUME_SIZE_BYTES, {
    error: `Resume is too large. Maximum size is ${formatFileSize(MAX_RESUME_SIZE_BYTES)}`,
  })
  .refine((file) => file.size > 0, { error: 'The selected file is empty' })

export const applyEmailSchema = z.object({
  email: z.string().trim().min(1, 'Enter your email').pipe(z.email('Enter a valid email address')),
})

export function validateResume(file: File | null): string | null {
  const result = resumeSchema.safeParse(file)
  return result.success ? null : (result.error.issues[0]?.message ?? 'Invalid file')
}
