import { useConfirm } from 'primevue/useconfirm'

import { useNotify } from '@/shared/composables/useNotify'

import { useDeleteUserMutation } from '../api/users.queries'
import type { User } from '../types/user'

export function useDeleteUser() {
  const confirm = useConfirm()
  const notify = useNotify()
  const mutation = useDeleteUserMutation()

  function requestDelete(user: User) {
    confirm.require({
      header: 'Delete user?',
      message: `${user.username} will lose access to vacancies and candidates. This action cannot be undone.`,
      icon: 'pi pi-trash',
      rejectProps: { label: 'Cancel', severity: 'secondary', text: true },
      acceptProps: { label: 'Delete', icon: 'pi pi-trash', severity: 'danger' },
      accept: () =>
        mutation.mutate(user.id, {
          onSuccess: () => notify.success('User deleted', user.username),
          onError: (error) => notify.error(error, 'Could not delete user'),
        }),
    })
  }

  return { requestDelete, isPending: mutation.isPending }
}
