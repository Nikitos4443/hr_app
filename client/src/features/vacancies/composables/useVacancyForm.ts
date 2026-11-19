import { computed, ref, watch } from 'vue'
import { onBeforeRouteLeave, useRouter } from 'vue-router'
import type { FormSubmitEvent } from '@primevue/forms'
import { zodResolver } from '@primevue/forms/resolvers/zod'
import { useConfirm } from 'primevue/useconfirm'

import { errorMessage, isApiError } from '@/shared/api'
import { useNotify } from '@/shared/composables/useNotify'

import { useReplaceQuestionsMutation, useVacancyQuestionsQuery } from '../api/questions.queries'
import { useCreateVacancyMutation, useUpdateVacancyMutation } from '../api/vacancies.queries'
import { createVacancySchema, type VacancyFormValues } from '../lib/schemas'
import type { CreateVacancyPayload, Vacancy } from '../types/vacancy'
import { toQuestionInputs, useQuestionList } from './useQuestionList'
import { useStringList } from './useStringList'

interface FormStateProbe {
  states: Record<string, { dirty: boolean }>
}

function emptyToNull(value: string): string | null {
  const trimmed = value.trim()
  return trimmed ? trimmed : null
}

export function toFormValues(vacancy?: Vacancy): VacancyFormValues {
  return {
    title: vacancy?.title ?? '',
    location: vacancy?.location ?? '',
    employment_type: vacancy?.employment_type ?? null,
    experience_years_min: vacancy?.experience_years_min ?? null,
    description: vacancy?.description ?? '',
    salary_min: vacancy?.salary_min ?? null,
    salary_max: vacancy?.salary_max ?? null,
    salary_currency: vacancy?.salary_currency ?? (vacancy ? null : 'USD'),
    deadline_at: vacancy?.deadline_at ? new Date(vacancy.deadline_at) : null,
    status: vacancy?.status ?? 'open',
  }
}

export function toPayload(
  values: VacancyFormValues,
  lists: { responsibilities: string[]; requirements: string[]; nice_to_have: string[] },
  unchangedDeadline: number | null,
  isEdit: boolean,
): CreateVacancyPayload {
  const payload: CreateVacancyPayload = {
    title: values.title.trim(),
    location: emptyToNull(values.location),
    employment_type: values.employment_type,
    experience_years_min: values.experience_years_min,
    description: emptyToNull(values.description),
    salary_min: values.salary_min,
    salary_max: values.salary_max,
    salary_currency: values.salary_currency,
    status: values.status,
    ...lists,
  }
  const deadlineUnchanged = (values.deadline_at?.getTime() ?? null) === unchangedDeadline
  if (!(isEdit && deadlineUnchanged)) {
    payload.deadline_at = values.deadline_at ? values.deadline_at.toISOString() : null
  }
  return payload
}

export function useVacancyForm(vacancy?: Vacancy) {
  const router = useRouter()
  const confirm = useConfirm()
  const notify = useNotify()
  const create = useCreateVacancyMutation()
  const update = useUpdateVacancyMutation()
  const replaceQuestions = useReplaceQuestionsMutation()

  const isEdit = vacancy !== undefined
  const unchangedDeadline = vacancy?.deadline_at ? new Date(vacancy.deadline_at).getTime() : null

  const initialValues = toFormValues(vacancy)
  const resolver = zodResolver(createVacancySchema(unchangedDeadline))

  const formRef = ref<FormStateProbe | null>(null)
  const responsibilities = useStringList(vacancy?.responsibilities)
  const requirements = useStringList(vacancy?.requirements)
  const niceToHave = useStringList(vacancy?.nice_to_have)
  const questions = useQuestionList()
  const questionsQuery = useVacancyQuestionsQuery(() => vacancy?.id)

  // Prefill once the existing questions arrive, unless the user already started editing.
  watch(
    () => questionsQuery.data.value,
    (data) => {
      if (data && !questions.touched.value) questions.reset(data)
    },
    { immediate: true },
  )

  // Set once the vacancy itself is stored, so a retry never creates a duplicate.
  const savedVacancyId = ref<number | null>(vacancy?.id ?? null)

  const serverErrors = ref<Record<string, string>>({})
  const serverMessage = ref<string | null>(null)
  const saved = ref(false)

  const isDirty = computed(
    () =>
      Object.values(formRef.value?.states ?? {}).some((field) => field.dirty) ||
      responsibilities.dirty.value ||
      requirements.dirty.value ||
      niceToHave.dirty.value ||
      questions.dirty.value,
  )

  const isSaving = computed(
    () => create.isPending.value || update.isPending.value || replaceQuestions.isPending.value,
  )

  function finish() {
    saved.value = true
    notify.success(isEdit ? 'Vacancy updated' : 'Vacancy created')
    router.push({ name: 'vacancies' })
  }

  function saveQuestions(vacancyId: number) {
    // Do not overwrite existing questions with an empty list if they never loaded.
    const loaded = !isEdit || questionsQuery.isSuccess.value
    if (!loaded || (isEdit && !questions.dirty.value)) {
      finish()
      return
    }
    if (!isEdit && !questions.items.value.length) {
      finish()
      return
    }
    replaceQuestions.mutate(
      { vacancyId, items: toQuestionInputs(questions.items.value) },
      {
        onSuccess: () => {
          questions.reset(replaceQuestions.data.value ?? [])
          finish()
        },
        onError: (error) => {
          notify.error(error, 'Vacancy saved, but the screening questions were not. Try again.')
          if (isApiError(error)) serverMessage.value = error.detail
        },
      },
    )
  }

  function onError(error: unknown) {
    if (isApiError(error)) {
      serverErrors.value = error.fieldErrors
      serverMessage.value = Object.keys(error.fieldErrors).length ? null : error.detail
      if (Object.keys(error.fieldErrors).length) notify.error(error, 'Check the highlighted fields')
      return
    }
    serverMessage.value = errorMessage(error)
  }

  function submit({ valid, values }: FormSubmitEvent) {
    serverErrors.value = {}
    serverMessage.value = null
    const questionsValid = questions.validate()
    if (!valid || !questionsValid) return
    const payload = toPayload(
      values as VacancyFormValues,
      {
        responsibilities: responsibilities.values.value,
        requirements: requirements.values.value,
        nice_to_have: niceToHave.values.value,
      },
      unchangedDeadline,
      isEdit,
    )
    if (isEdit && !questionsQuery.isSuccess.value && questions.touched.value) {
      serverMessage.value = 'Existing questions are still loading. Please try again in a moment.'
      return
    }
    if (savedVacancyId.value !== null) {
      update.mutate(
        { id: savedVacancyId.value, payload },
        { onSuccess: (saved) => saveQuestions(saved.id), onError },
      )
      return
    }
    create.mutate(payload, {
      onSuccess: (created) => {
        savedVacancyId.value = created.id
        saveQuestions(created.id)
      },
      onError,
    })
  }

  function cancel() {
    router.push({ name: 'vacancies' })
  }

  onBeforeRouteLeave(() => {
    if (saved.value || !isDirty.value) return true
    return new Promise<boolean>((resolve) => {
      confirm.require({
        header: 'Discard changes?',
        message: 'You have unsaved changes. If you leave now, they will be lost.',
        icon: 'pi pi-exclamation-triangle',
        acceptLabel: 'Leave',
        rejectLabel: 'Keep editing',
        rejectProps: { severity: 'secondary', outlined: true },
        accept: () => resolve(true),
        reject: () => resolve(false),
        onHide: () => resolve(false),
      })
    })
  })

  return {
    isEdit,
    initialValues,
    resolver,
    formRef,
    responsibilities,
    requirements,
    niceToHave,
    questions,
    serverErrors,
    serverMessage,
    isDirty,
    isSaving,
    submit,
    cancel,
  }
}
