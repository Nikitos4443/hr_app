import { z } from 'zod'

export const createHrSchema = z.object({
  username: z.string().trim().min(3, 'At least 3 characters'),
  password: z.string().min(8, 'At least 8 characters'),
})

export type CreateHrValues = z.infer<typeof createHrSchema>
