import { useToast } from 'primevue/usetoast'

import { errorMessage } from '@/shared/api'

const LIFE_MS = 5000

export function useNotify() {
  const toast = useToast()

  return {
    success: (summary: string, detail?: string) =>
      toast.add({ severity: 'success', summary, detail, life: LIFE_MS }),
    info: (summary: string, detail?: string) =>
      toast.add({ severity: 'info', summary, detail, life: LIFE_MS }),
    error: (error: unknown, summary = 'Something went wrong') =>
      toast.add({ severity: 'error', summary, detail: errorMessage(error), life: LIFE_MS }),
  }
}
