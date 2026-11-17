import { watch } from 'vue'

import { useSessionStore } from '@/features/auth'
import { configureHttp } from '@/shared/api'

import { queryClient } from './query'

export function setupHttp() {
  const session = useSessionStore()

  configureHttp({
    getToken: () => session.token,
    onUnauthorized: () => session.logout(),
  })

  session.restore()

  watch(
    () => session.isAuthenticated,
    (authenticated) => {
      if (!authenticated) queryClient.clear()
    },
  )
}
