import { z } from 'zod'

const username = z.string().trim().min(3, 'At least 3 characters')

export const loginSchema = z.object({
  username,
  password: z.string().min(1, 'Enter your password'),
})

export const registerSchema = z.object({
  username,
  password: z.string().min(8, 'At least 8 characters'),
})
