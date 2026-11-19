import type { App } from 'vue'
import { QueryClient, VueQueryPlugin } from '@tanstack/vue-query'

import { isApiError } from '@/shared/api'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: (failureCount, error) =>
        failureCount < 1 && !(isApiError(error) && error.status >= 400 && error.status < 500),
      refetchOnWindowFocus: false,
    },
    mutations: { retry: false },
  },
})

export function setupQuery(app: App) {
  app.use(VueQueryPlugin, { queryClient })
}
