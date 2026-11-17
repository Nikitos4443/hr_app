import type { PublicVacancy } from '../types/public-vacancy'

const DAY_MS = 24 * 60 * 60 * 1000

function daysFromNow(days: number): string {
  return new Date(Date.now() + days * DAY_MS).toISOString()
}

const openVacancy: PublicVacancy = {
  id: 1,
  title: 'Senior Vue.js Developer',
  company: 'Lime Technologies',
  company_id: 1,
  company_website: 'lime-tech.ua',
  company_description:
    'Product company building recruiting software used by thousands of recruiters.',
  location: 'Kyiv, remote possible',
  employment_type: 'Full-time',
  experience_years_min: 4,
  description:
    'You will build interfaces for thousands of recruiters, design the frontend architecture and mentor middle-level developers.',
  responsibilities: [
    'Build interfaces with Vue 3 and TypeScript',
    'Code review and mentoring',
    'Design reusable component libraries',
    'Work closely with designers and backend engineers',
  ],
  requirements: [
    '4+ years of experience with Vue and TypeScript',
    'Experience with Pinia and Vite',
    'Solid understanding of web accessibility',
  ],
  nice_to_have: ['Nuxt and SSR', 'Experience with design systems'],
  salary_min: 3500,
  salary_max: 4800,
  salary_currency: 'USD',
  status: 'open',
  created_by: 1,
  deadline_at: daysFromNow(15),
  selection_status: 'pending',
  created_at: daysFromNow(-10),
}

const closedVacancy: PublicVacancy = {
  ...openVacancy,
  id: 2,
  title: 'QA Engineer (Automation)',
  location: 'Kyiv',
  experience_years_min: null,
  description:
    'The description stays available so you can review the requirements and wait for new openings.',
  responsibilities: ['Write and maintain automated tests'],
  requirements: ['Experience with Playwright or Cypress'],
  nice_to_have: [],
  salary_min: 2000,
  salary_max: 2800,
  status: 'closed',
  deadline_at: daysFromNow(-3),
}

const fixtures = new Map<number, PublicVacancy>([
  [openVacancy.id, openVacancy],
  [closedVacancy.id, closedVacancy],
])

export function getMockPublicVacancy(id: number): Promise<PublicVacancy> {
  const vacancy = fixtures.get(id) ?? { ...openVacancy, id }
  return new Promise((resolve) => setTimeout(() => resolve(vacancy), 300))
}
