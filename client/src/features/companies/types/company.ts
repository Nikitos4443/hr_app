export interface Company {
  id: number
  name: string
  description: string | null
  website: string | null
  created_at: string | null
}

export interface CreateCompanyPayload {
  name: string
  description?: string | null
  website?: string | null
}

export type UpdateCompanyPayload = Partial<CreateCompanyPayload>
