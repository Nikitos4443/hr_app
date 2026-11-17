import { z } from 'zod'

export const MIN_VIDEO_DURATION_SEC = 10
export const MAX_TEXT_ANSWER_LENGTH = 5000
export const DEFAULT_VIDEO_DURATION_SEC = 120

const optionalAmount = z.number().int('Whole numbers only').min(0, 'Cannot be negative').nullable()

export function createVacancySchema(unchangedDeadline: number | null) {
  return z
    .object({
      title: z.string().trim().min(1, 'Enter the vacancy title'),
      location: z.string(),
      employment_type: z.string().nullable(),
      experience_years_min: z.number().int().min(0, 'Cannot be negative').nullable(),
      description: z.string(),
      salary_min: optionalAmount,
      salary_max: optionalAmount,
      salary_currency: z.string().nullable(),
      deadline_at: z.date().nullable(),
      status: z.enum(['open', 'closed']),
    })
    .superRefine((values, ctx) => {
      const { salary_min: min, salary_max: max, deadline_at: deadline } = values
      if (min != null && max != null && min > max) {
        ctx.addIssue({
          code: 'custom',
          path: ['salary_max'],
          message: 'Minimum cannot exceed maximum',
        })
      }
      if (
        deadline &&
        deadline.getTime() !== unchangedDeadline &&
        deadline.getTime() <= Date.now()
      ) {
        ctx.addIssue({
          code: 'custom',
          path: ['deadline_at'],
          message: 'Deadline must be in the future',
        })
      }
    })
}

export type VacancyFormValues = z.infer<ReturnType<typeof createVacancySchema>>

export const screeningQuestionSchema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('video'),
    text: z.string().trim().min(1, 'Enter the question'),
    max_duration_sec: z
      .number({ error: 'Enter a duration' })
      .int()
      .min(MIN_VIDEO_DURATION_SEC, `At least ${MIN_VIDEO_DURATION_SEC} seconds`),
  }),
  z.object({
    type: z.literal('text'),
    text: z.string().trim().min(1, 'Enter the question'),
    max_length: z.number().int().max(MAX_TEXT_ANSWER_LENGTH),
  }),
])
