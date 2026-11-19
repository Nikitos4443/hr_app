export type VacancyStatus = 'open' | 'closed'
export type SelectionStatus = 'pending' | 'running' | 'done' | 'failed'

export interface Vacancy {
  id: number
  title: string
  company: string
  company_id: number | null
  location: string | null
  employment_type: string | null
  experience_years_min: number | null
  description: string | null
  responsibilities: string[]
  requirements: string[]
  nice_to_have: string[]
  salary_min: number | null
  salary_max: number | null
  salary_currency: string | null
  status: VacancyStatus
  created_by: number
  deadline_at: string | null
  selection_status: SelectionStatus
  created_at: string | null
}

export interface CreateVacancyPayload {
  title: string
  location?: string | null
  employment_type?: string | null
  experience_years_min?: number | null
  description?: string | null
  responsibilities?: string[]
  requirements?: string[]
  nice_to_have?: string[]
  salary_min?: number | null
  salary_max?: number | null
  salary_currency?: string | null
  status?: VacancyStatus
  deadline_at?: string | null
}

export type UpdateVacancyPayload = Partial<CreateVacancyPayload>
