export interface CreateApplicationPayload {
  vacancy_id: number
  email: string
}

export type ApplicationStatus = 'pending' | 'invited' | 'shortlisted' | 'rejected'
export type ScreeningState = 'not_invited' | 'invited' | 'in_progress' | 'completed'
export type ApplicationAction = 'invite' | 'shortlist' | 'reject'
export type ApplicationSort = 'created_at' | 'resume_score' | 'rank'
export type SortDirection = 'asc' | 'desc'

export interface ApplicationListItem {
  id: number
  email: string
  full_name: string | null
  status: ApplicationStatus
  created_at: string | null
  resume_status: string | null
  resume_score: number | null
  screening_state: ScreeningState
  answered_count: number
  total_questions: number
  rank: number | null
  ai_summary: string | null
}

export interface ApplicationCounts {
  all: number
  pending: number
  invited: number
  shortlisted: number
  rejected: number
}

export interface ApplicationList {
  items: ApplicationListItem[]
  total: number
  counts: ApplicationCounts
}

export interface ApplicationListParams {
  status?: ApplicationStatus | null
  search?: string
  sort: ApplicationSort
  order: SortDirection
  limit: number
  offset: number
}

export interface ResumeReview {
  is_resume: boolean | null
  score: number | null
  description: string | null
}

export interface ResumeDetail {
  status: string | null
  score: number | null
  review: ResumeReview | null
  /** Short-lived presigned GET for the resume PDF */
  file_url: string | null
}

export interface AnswerDetail {
  question_id: number
  order: number
  type: 'video' | 'text'
  text: string
  /** pending | done */
  status: string
  answer: string | null
  transcription: string | null
}

export type TimelineEventType =
  | 'applied'
  | 'resume_processed'
  | 'screening_invited'
  | 'screening_completed'
  | 'shortlisted'
  | 'rejected'
  | 'rejection_notified'

export interface TimelineEvent {
  type: TimelineEventType
  at: string
}

export interface ApplicationDetail {
  id: number
  vacancy_id: number
  email: string
  full_name: string | null
  status: ApplicationStatus
  created_at: string | null
  resume: ResumeDetail
  rank: number | null
  ai_summary: string | null
  answers: AnswerDetail[]
  timeline: TimelineEvent[]
}

export interface ApplicationActionResult {
  id: number
  status: ApplicationStatus
  screening_invited_at: string | null
  status_changed_at: string | null
}

export interface BulkActionResult {
  updated: number[]
  failed: { id: number; detail: string }[]
}
