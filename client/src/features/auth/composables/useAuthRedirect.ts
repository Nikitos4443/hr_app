import { useRoute, useRouter } from 'vue-router'

import { resolveRedirect } from '../lib/redirect'

export function useAuthRedirect() {
  const route = useRoute()
  const router = useRouter()

  return {
    redirectAfterAuth: () => router.replace(resolveRedirect(route.query.redirect)),
  }
}
