
export interface TextAnswerResult {
  question_id: number
  status: string
}

export type ScreeningQuestionType = 'video' | 'text'

export interface ScreeningQuestion {
  id: number
  order: number
  type: ScreeningQuestionType
  text: string
  video_max_duration_sec: number | null
  answered: boolean
}

export interface ScreeningSession {
  vacancy_title: string
  company_name: string
  status: string
  screening_progress: 'in_progress' | 'completed'
  questions: ScreeningQuestion[]
}

export type TokenState = 'invalid' | 'rejected' | 'completed' | 'in_review' | 'processing'

export type EndState = 'done' | TokenState
