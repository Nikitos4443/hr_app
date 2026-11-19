import type {
  ApplicationAction,
  ApplicationListItem,
  ApplicationSort,
  ApplicationStatus,
  SortDirection,
  TimelineEventType,
} from '../types/application'

export const STATUS_TABS: { value: ApplicationStatus | null; label: string }[] = [
  { value: null, label: 'All' },
  { value: 'pending', label: 'Pending' },
  { value: 'invited', label: 'Invited' },
  { value: 'shortlisted', label: 'Shortlisted' },
  { value: 'rejected', label: 'Rejected' },
]

export const SORT_OPTIONS: { value: ApplicationSort; label: string; order: SortDirection }[] = [
  { value: 'resume_score', label: 'By resume score', order: 'desc' },
  { value: 'rank', label: 'By rank', order: 'asc' },
  { value: 'created_at', label: 'Newest first', order: 'desc' },
]

export const DEFAULT_SORT: ApplicationSort = 'resume_score'

export function sortOrder(sort: ApplicationSort): SortDirection {
  return SORT_OPTIONS.find((option) => option.value === sort)?.order ?? 'desc'
}

export const TIMELINE_LABELS: Record<TimelineEventType, string> = {
  applied: 'Application submitted',
  resume_processed: 'Resume reviewed',
  screening_invited: 'Screening invitation sent',
  screening_completed: 'Screening answers submitted',
  shortlisted: 'Added to shortlist',
  rejected: 'Rejected',
  rejection_notified: 'Rejection email sent',
}

export const ACTION_LABELS: Record<ApplicationAction, string> = {
  invite: 'Invite to screening',
  shortlist: 'Shortlist',
  reject: 'Reject',
}

export const ACTION_ICONS: Record<ApplicationAction, string> = {
  invite: 'pi pi-envelope',
  shortlist: 'pi pi-star',
  reject: 'pi pi-times-circle',
}

interface ActionTarget {
  status: ApplicationStatus
  /** Resume analysis status; an invitation is only possible once it is "done". */
  resumeStatus: string | null
}

/** Mirrors the server transition rules so unavailable actions are disabled up front. */
export function canApply(action: ApplicationAction, target: ActionTarget): boolean {
  switch (action) {
    case 'invite':
      return target.status === 'pending' && target.resumeStatus === 'done'
    case 'shortlist':
      return target.status === 'pending' || target.status === 'invited'
    case 'reject':
      return target.status !== 'rejected'
  }
}

export function candidateName(candidate: { full_name: string | null; email: string }): string {
  return candidate.full_name?.trim() || candidate.email
}

export function screeningLabel(item: ApplicationListItem): string | undefined {
  if (item.screening_state === 'in_progress' || item.screening_state === 'completed') {
    const progress = `${item.answered_count}/${item.total_questions}`
    return item.screening_state === 'completed'
      ? `Completed · ${progress}`
      : `In progress · ${progress}`
  }
  return undefined
}
