import { computed, ref } from 'vue'
import { zodResolver } from '@primevue/forms/resolvers/zod'

import { errorMessage } from '@/shared/api'

import { useSubmitApplicationMutation } from '../api/apply.queries'
import { applyEmailSchema, validateResume } from '../lib/resume'

export type ApplyStatus = 'idle' | 'selected' | 'uploading' | 'success' | 'error'

export function useApplyForm(vacancyId: () => number) {
  const mutation = useSubmitApplicationMutation()

  const resolver = zodResolver(applyEmailSchema)
  const resume = ref<File | null>(null)
  const resumeError = ref<string | null>(null)
  const email = ref('')
  const percent = ref(0)

  const status = computed<ApplyStatus>(() => {
    if (mutation.isPending.value) return 'uploading'
    if (mutation.isSuccess.value) return 'success'
    if (mutation.isError.value) return 'error'
    return resume.value ? 'selected' : 'idle'
  })

  const errorText = computed(() =>
    mutation.error.value ? errorMessage(mutation.error.value) : null,
  )

  function selectResume(file: File | null) {
    resume.value = file
    resumeError.value = file ? validateResume(file) : null
    if (mutation.isError.value) mutation.reset()
  }

  function removeResume() {
    selectResume(null)
  }

  function send() {
    const file = resume.value
    resumeError.value = validateResume(file)
    if (!file || resumeError.value) return
    percent.value = 0
    mutation.mutate({
      vacancy_id: vacancyId(),
      email: email.value,
      resume: file,
      onProgress: (value) => {
        percent.value = value
      },
    })
  }

  function submit(values: { email?: string }, valid: boolean) {
    email.value = (values.email ?? '').trim()
    if (!valid) {
      resumeError.value = validateResume(resume.value)
      return
    }
    send()
  }

  return {
    resolver,
    resume,
    resumeError,
    email,
    percent,
    status,
    errorText,
    selectResume,
    removeResume,
    submit,
  }
}
