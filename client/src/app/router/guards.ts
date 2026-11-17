import { watch } from 'vue'
import type { Router } from 'vue-router'

import { resolveRedirect, useSessionStore } from '@/features/auth'

export function installGuards(router: Router) {
  const session = useSessionStore()

  router.beforeEach((to) => {
    if (to.meta.guestOnly && session.isAuthenticated) {
      return resolveRedirect(to.query.redirect)
    }

    if (to.meta.requiresAuth && !session.isAuthenticated) {
      return { name: 'auth', query: { redirect: to.fullPath } }
    }

    if (to.meta.roles && !session.hasRole(...to.meta.roles)) {
      return { name: 'forbidden' }
    }
  })

  watch(
    () => session.isAuthenticated,
    (authenticated) => {
      const current = router.currentRoute.value
      if (authenticated || !current.meta.requiresAuth) return
      router.replace({
        name: 'auth',
        query: session.expired ? { redirect: current.fullPath } : undefined,
      })
    },
  )
}
