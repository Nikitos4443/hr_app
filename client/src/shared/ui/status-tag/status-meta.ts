export type TagSeverity = 'secondary' | 'success' | 'info' | 'warn' | 'danger' | 'contrast'

export interface StatusMeta {
  label: string
  icon: string
  severity?: TagSeverity
}

export const STATUS_META = {
  vacancy: {
    open: { label: 'Open', icon: 'pi pi-check-circle', severity: 'success' },
    closed: { label: 'Closed', icon: 'pi pi-lock', severity: 'secondary' },
  },
  application: {
    pending: { label: 'Pending', icon: 'pi pi-clock', severity: 'warn' },
    invited: { label: 'Invited', icon: 'pi pi-envelope', severity: 'info' },
    shortlisted: { label: 'Shortlisted', icon: 'pi pi-star-fill', severity: 'success' },
    rejected: { label: 'Rejected', icon: 'pi pi-times-circle', severity: 'danger' },
  },
  screening: {
    not_invited: { label: 'Not invited', icon: 'pi pi-minus', severity: 'secondary' },
    invited: { label: 'Invited', icon: 'pi pi-send', severity: 'info' },
    in_progress: { label: 'In progress', icon: 'pi pi-hourglass' },
    completed: { label: 'Completed', icon: 'pi pi-check-circle', severity: 'success' },
  },
} as const satisfies Record<string, Record<string, StatusMeta>>

export type StatusMap = {
  [K in keyof typeof STATUS_META]: keyof (typeof STATUS_META)[K]
}
export type StatusKind = keyof StatusMap
