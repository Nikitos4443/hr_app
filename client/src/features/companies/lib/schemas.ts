import { z } from 'zod'

function isFullUrl(value: string): boolean {
  try {
    const url = new URL(value)
    return url.protocol === 'http:' || url.protocol === 'https:'
  } catch {
    return false
  }
}

export const companySchema = z.object({
  name: z.string().trim().min(1, 'Enter the company name'),
  description: z.string().optional(),
  website: z
    .string()
    .trim()
    .optional()
    .refine((value) => !value || isFullUrl(value), 'Enter a full link, e.g. https://example.com'),
})

export type CompanyFormValues = z.infer<typeof companySchema>
