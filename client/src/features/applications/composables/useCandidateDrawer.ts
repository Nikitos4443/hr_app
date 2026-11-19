import { computed } from 'vue'
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

  function open(id: number) {
    router.replace({ query: { ...route.query, candidate: String(id) } })
  }

  function close() {
    const query = { ...route.query }
    delete query.candidate
    router.replace({ query })
  }

  return { candidateId, open, close }
}
