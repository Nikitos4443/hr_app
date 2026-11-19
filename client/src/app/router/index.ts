import { nextTick } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import { routes } from './routes'

const APP_NAME = 'HR App'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    // Same page, only the query changed (filters, drawers): keep the scroll position.
    if (to.path === from.path) return false
    return { top: 0 }
  },
})

router.afterEach((to, from) => {
  const title = [...to.matched].reverse().find((r) => r.meta.title !== undefined)?.meta.title
  document.title = title ? `${title} \u00b7 ${APP_NAME}` : APP_NAME

  if (to.path === from.path) return
  void nextTick(() => {
    document.getElementById('main')?.focus({ preventScroll: true })
  })
})

export default router
