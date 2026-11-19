import { computed } from 'vue'
import { useConfirm } from 'primevue/useconfirm'

import { useNotify } from '@/shared/composables/useNotify'

import { useApplicationActionMutation, useBulkActionMutation } from '../api/applications.queries'
import type { ApplicationAction } from '../types/application'

const SUCCESS_MESSAGE: Record<ApplicationAction, string> = {
  invite: 'Screening invitation sent',
  shortlist: 'Candidate shortlisted',
  reject: 'Candidate rejected',
}

const BULK_VERB: Record<ApplicationAction, string> = {
  invite: 'invited',
  shortlist: 'shortlisted',
  reject: 'rejected',
}

/** Invite / shortlist / reject for one candidate or a selection, with confirmation for reject. */
export function useApplicationActions() {
  const confirm = useConfirm()
  const notify = useNotify()
  const single = useApplicationActionMutation()
  const bulk = useBulkActionMutation()

  const busy = computed(() => single.isPending.value || bulk.isPending.value)

  function askReject(message: string, accept: () => void) {
    confirm.require({
      header: 'Reject candidate?',
      message,
      icon: 'pi pi-times-circle',
      acceptLabel: 'Reject',
      acceptProps: { severity: 'danger' },
      rejectLabel: 'Cancel',
      rejectProps: { severity: 'secondary', outlined: true },
      accept,
    })
  }

  function execute(id: number, action: ApplicationAction) {
    single.mutate(
      { id, action },
      {
        onSuccess: () => notify.success(SUCCESS_MESSAGE[action]),
        onError: (error) => notify.error(error, `Could not ${action} the candidate`),
      },
    )
  }

  function run(target: { id: number; name: string }, action: ApplicationAction) {
    if (action !== 'reject') return execute(target.id, action)
    askReject(
      `${target.name} will be notified by email and their personal data will be removed. This cannot be undone.`,
      () => execute(target.id, action),
    )
  }

  function executeBulk(
    vacancyId: number,
    ids: number[],
    action: ApplicationAction,
    onDone?: () => void,
  ) {
    bulk.mutate(
      { vacancyId, ids, action },
      {
        onSuccess: ({ updated, failed }) => {
          if (failed.length === 0) {
            notify.success(`${updated.length} candidates ${BULK_VERB[action]}`)
          } else if (updated.length > 0) {
            notify.info(
              `${updated.length} ${BULK_VERB[action]}, ${failed.length} skipped`,
              failed[0]?.detail,
            )
          } else {
            notify.error(
              new Error(failed[0]?.detail ?? 'Nothing was updated'),
              'No candidates updated',
            )
          }
          onDone?.()
        },
        onError: (error) => notify.error(error, `Could not ${action} the selected candidates`),
      },
    )
  }

  function runBulk(
    vacancyId: number,
    ids: number[],
    action: ApplicationAction,
    onDone?: () => void,
  ) {
    if (action !== 'reject') return executeBulk(vacancyId, ids, action, onDone)
    askReject(
      `${ids.length} candidates will be notified by email and their personal data will be removed. This cannot be undone.`,
      () => executeBulk(vacancyId, ids, action, onDone),
    )
  }

  return { busy, run, runBulk }
}
