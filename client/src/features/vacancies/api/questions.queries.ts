import { computed, toValue, type MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'

import type { QuestionInput } from '../types/question'
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

export function useReplaceQuestionsMutation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ vacancyId, items }: { vacancyId: number; items: QuestionInput[] }) =>
      questionsApi.replace(vacancyId, items),
    onSuccess: (questions, { vacancyId }) => {
      queryClient.setQueryData(questionKeys.list(vacancyId), questions)
    },
  })
}
