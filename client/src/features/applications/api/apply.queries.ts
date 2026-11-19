import { useMutation } from '@tanstack/vue-query'

import { applyApi, type SubmitApplicationInput } from './apply.api'

export function useSubmitApplicationMutation() {
  return useMutation({ mutationFn: (input: SubmitApplicationInput) => applyApi.submit(input) })
}
