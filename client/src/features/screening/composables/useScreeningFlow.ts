import { computed, ref, toValue, type MaybeRefOrGetter } from 'vue'
import { useRouter } from 'vue-router'

import { useScreeningQuestionsQuery, useScreeningQuery } from '../api/screening.queries'
import { useTokenState } from './useTokenState'

function storageKey(token: string) {
  return `screening-answered:${token}`
}

function loadAnswered(token: string): number[] {
  try {
    const raw = sessionStorage.getItem(storageKey(token))
    const parsed: unknown = raw ? JSON.parse(raw) : []
    return Array.isArray(parsed) ? parsed.filter((id): id is number => typeof id === 'number') : []
  } catch {
    return []
  }
}

function saveAnswered(token: string, ids: number[]) {
  try {
    sessionStorage.setItem(storageKey(token), JSON.stringify(ids))
  } catch {
    return
  }
}

export function useScreeningFlow(token: MaybeRefOrGetter<string>) {
  const router = useRouter()
  const session = useScreeningQuery(token)
  const questionsQuery = useScreeningQuestionsQuery(token)
  const finishing = ref(false)
  const answeredLocally = ref<number[]>(loadAnswered(toValue(token)))

  const tokenState = useTokenState(() => session.error.value ?? questionsQuery.error.value)

  const questions = computed(() =>
    [...(questionsQuery.data.value?.questions ?? [])].sort((a, b) => a.order - b.order),
  )
  const total = computed(() => questions.value.length)
  const isAnswered = (id: number, serverAnswered: boolean) =>
    serverAnswered || answeredLocally.value.includes(id)

  const currentIndex = computed(() =>
    questions.value.findIndex((question) => !isAnswered(question.id, question.answered)),
  )
  const current = computed(() =>
    currentIndex.value === -1 ? null : (questions.value[currentIndex.value] ?? null),
  )
  const isComplete = computed(() => total.value > 0 && currentIndex.value === -1)
  const answeredCount = computed(() => (isComplete.value ? total.value : currentIndex.value))
  const progressLabel = computed(() =>
    current.value ? `Question ${currentIndex.value + 1} of ${total.value}` : '',
  )

  const isLoading = computed(
    () => session.isPending.value || (!session.isError.value && questionsQuery.isPending.value),
  )
  const hasError = computed(() => session.isError.value || questionsQuery.isError.value)

  function finish() {
    finishing.value = true
    return router.push({ name: 'screening-done', params: { token: toValue(token) } })
  }

  function markAnswered(questionId: number) {
    if (!answeredLocally.value.includes(questionId)) {
      answeredLocally.value = [...answeredLocally.value, questionId]
      saveAnswered(toValue(token), answeredLocally.value)
    }
    if (currentIndex.value === -1) void finish()
  }

  function retry() {
    void session.refetch()
    void questionsQuery.refetch()
  }

  return {
    vacancyTitle: computed(() => questionsQuery.data.value?.vacancy_title ?? ''),
    companyName: computed(() => questionsQuery.data.value?.company_name ?? ''),
    current,
    currentIndex,
    total,
    answeredCount,
    progressLabel,
    isComplete,
    finishing,
    isLoading,
    hasError,
    tokenState,
    markAnswered,
    retry,
  }
}
