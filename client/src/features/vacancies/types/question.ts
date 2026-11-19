export type QuestionType = 'video' | 'text'

export interface VacancyQuestion {
  id: number | null
  vacancy_id: number
  order: number
  type: QuestionType
  text: string
  video_max_duration_sec: number | null
}

export interface QuestionInput {
  type: QuestionType
  text: string
  video_max_duration_sec: number | null
}
