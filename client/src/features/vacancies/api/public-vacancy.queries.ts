import { computed, toValue, type MaybeRefOrGetter } from 'vue'
import { useQuery } from '@tanstack/vue-query'

import { vacancyKeys } from './vacancies.queries'
import { publicVacancyApi } from './public-vacancy.api'

export function usePublicVacancyQuery(id: MaybeRefOrGetter<number | null | undefined>) {
  return useQuery({
    queryKey: computed(() => [...vacancyKeys.all, 'public', toValue(id) ?? -1] as const),
    queryFn: () => publicVacancyApi.get(toValue(id)!),
    enabled: computed(() => toValue(id) != null),
    retry: false,
  })
}
