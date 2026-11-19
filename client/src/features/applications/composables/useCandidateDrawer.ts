import { computed, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'

/** The open candidate lives in `?candidate=<applicationId>` so a card can be linked to directly. */
export function useCandidateDrawer() {
  const route = useRoute()
  const router = useRouter()

  const candidateId = computed(() => {
    const raw = route.query.candidate
    const value = Number(Array.isArray(raw) ? raw[0] : raw)
    return Number.isInteger(value) && value > 0 ? value : null
  })

  // Element that opened the drawer, so focus can return to it on close.
  let opener: HTMLElement | null = null

  function open(id: number) {
    opener = document.activeElement instanceof HTMLElement ? document.activeElement : null
    router.replace({ query: { ...route.query, candidate: String(id) } })
  }

  function close() {
    const query = { ...route.query }
    delete query.candidate
    router.replace({ query })
    const target = opener
    opener = null
    if (target) void nextTick(() => target.isConnected && target.focus())
  }

  return { candidateId, open, close }
}
