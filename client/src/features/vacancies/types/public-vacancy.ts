import type { Vacancy } from './vacancy'

export interface PublicVacancy extends Vacancy {
  company_website: string | null
  company_description: string | null
}
