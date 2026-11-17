import type { ScreeningQuestions } from '../types/screening'

export const isScreeningMockEnabled = () => import.meta.env.VITE_USE_MOCKS === 'true'

export const screeningQuestionsFixture: ScreeningQuestions = {
  vacancy_title: 'Senior Vue.js Developer',
  company_name: 'Lime Technologies',
  questions: [
    {
      id: 1,
      order: 1,
      type: 'video',
      text: 'Tell us about the Vue project you are most proud of.',
      video_max_duration_sec: 120,
      answered: false,
    },
    {
      id: 2,
      order: 2,
      type: 'video',
      text: 'Describe a difficult bug you tracked down and how you found the cause.',
      video_max_duration_sec: 90,
      answered: false,
    },
    {
      id: 3,
      order: 3,
      type: 'text',
      text: 'Why does this role interest you and what do you expect from the team?',
      video_max_duration_sec: null,
      answered: false,
    },
  ],
}

export function mockScreeningQuestions(): Promise<ScreeningQuestions> {
  return new Promise((resolve) => {
    setTimeout(() => resolve(structuredClone(screeningQuestionsFixture)), 300)
  })
}
