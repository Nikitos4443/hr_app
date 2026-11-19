import { computed, ref } from 'vue'

import {
  DEFAULT_VIDEO_DURATION_SEC,
  MAX_QUESTIONS,
  MAX_TEXT_ANSWER_LENGTH,
  screeningQuestionSchema,
} from '../lib/schemas'
import type { QuestionInput, VacancyQuestion } from '../types/question'

export type QuestionType = 'video' | 'text'

export function toQuestionInputs(items: QuestionDraft[]): QuestionInput[] {
  return items.map((item) => ({
    type: item.type,
    text: item.text.trim(),
    video_max_duration_sec: item.type === 'video' ? item.max_duration_sec : null,
  }))
}

export interface QuestionDraft {
  id: number
  type: QuestionType
  text: string
  max_duration_sec: number | null
}

export interface QuestionErrors {
  text?: string
  max_duration_sec?: string
}

let nextId = 0

export function useQuestionList() {
  const items = ref<QuestionDraft[]>([])
  const errors = ref<Record<number, QuestionErrors>>({})
  const baseline = ref(JSON.stringify([]))
  const touched = ref(false)

  const dirty = computed(() => JSON.stringify(toQuestionInputs(items.value)) !== baseline.value)
  const canAdd = computed(() => items.value.length < MAX_QUESTIONS)

  function reset(source: VacancyQuestion[]) {
    items.value = [...source]
      .sort((a, b) => a.order - b.order)
      .map((question) => ({
        id: nextId++,
        type: question.type,
        text: question.text,
        max_duration_sec: question.type === 'video' ? question.video_max_duration_sec : null,
      }))
    errors.value = {}
    touched.value = false
    baseline.value = JSON.stringify(toQuestionInputs(items.value))
  }

  function add(type: QuestionType) {
    if (!canAdd.value) return
    touched.value = true
    items.value.push({
      id: nextId++,
      type,
      text: '',
      max_duration_sec: type === 'video' ? DEFAULT_VIDEO_DURATION_SEC : null,
    })
  }

  function remove(id: number) {
    touched.value = true
    items.value = items.value.filter((item) => item.id !== id)
    delete errors.value[id]
  }

  function move(index: number, offset: -1 | 1) {
    const target = index + offset
    if (target < 0 || target >= items.value.length) return
    touched.value = true
    const next = [...items.value]
    next.splice(target, 0, ...next.splice(index, 1))
    items.value = next
  }

  function changeType(id: number, type: QuestionType) {
    const item = items.value.find((entry) => entry.id === id)
    if (!item) return
    touched.value = true
    item.type = type
    item.max_duration_sec = type === 'video' ? DEFAULT_VIDEO_DURATION_SEC : null
    delete errors.value[id]
  }

  function update(id: number, patch: Partial<Pick<QuestionDraft, 'text' | 'max_duration_sec'>>) {
    const item = items.value.find((entry) => entry.id === id)
    if (!item) return
    touched.value = true
    Object.assign(item, patch)
  }

  function validateItem(item: QuestionDraft): QuestionErrors {
    const result = screeningQuestionSchema.safeParse(
      item.type === 'video'
        ? { type: 'video', text: item.text, max_duration_sec: item.max_duration_sec }
        : { type: 'text', text: item.text, max_length: MAX_TEXT_ANSWER_LENGTH },
    )
    if (result.success) return {}
    const found: QuestionErrors = {}
    for (const issue of result.error.issues) {
      const key = issue.path[0]
      if (key === 'text' && !found.text) found.text = issue.message
      if (key === 'max_duration_sec' && !found.max_duration_sec) {
        found.max_duration_sec = issue.message
      }
    }
    return found
  }

  function validateOne(id: number) {
    const item = items.value.find((entry) => entry.id === id)
    if (item) errors.value[id] = validateItem(item)
  }

  function validate(): boolean {
    const next: Record<number, QuestionErrors> = {}
    for (const item of items.value) next[item.id] = validateItem(item)
    errors.value = next
    return Object.values(next).every((entry) => Object.keys(entry).length === 0)
  }

  const invalidCount = computed(
    () => Object.values(errors.value).filter((entry) => Object.keys(entry).length > 0).length,
  )

  return {
    items,
    errors,
    dirty,
    touched,
    canAdd,
    reset,
    invalidCount,
    add,
    remove,
    move,
    changeType,
    update,
    validate,
    validateOne,
  }
}

export type QuestionList = ReturnType<typeof useQuestionList>
