import { computed, toValue, type MaybeRefOrGetter } from 'vue'
import { useQuery } from '@tanstack/vue-query'

import { vacancyKeys } from './vacancies.queries'
import { questionsApi } from './questions.api'

export const questionKeys = {
  list: (vacancyId: number) => [...vacancyKeys.detail(vacancyId), 'questions'] as const,
}

export function useVacancyQuestionsQuery(vacancyId: MaybeRefOrGetter<number | null | undefined>) {
  return useQuery({
    queryKey: computed(() => questionKeys.list(toValue(vacancyId) ?? -1)),
    queryFn: () => questionsApi.list(toValue(vacancyId)!),
    enabled: computed(() => toValue(vacancyId) != null),
  })
}
