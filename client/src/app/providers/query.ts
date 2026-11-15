import type { App } from 'vue'
import { QueryClient, VueQueryPlugin } from '@tanstack/vue-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

export function setupQuery(app: App) {
  app.use(VueQueryPlugin, { queryClient })
}
