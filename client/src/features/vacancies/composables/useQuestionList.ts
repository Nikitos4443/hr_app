import { computed, ref } from 'vue'

import {
  DEFAULT_VIDEO_DURATION_SEC,
  MAX_TEXT_ANSWER_LENGTH,
  screeningQuestionSchema,
} from '../lib/schemas'

export type QuestionType = 'video' | 'text'

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
  const changed = ref(false)

  const dirty = computed(() => changed.value)

  function add(type: QuestionType) {
    changed.value = true
    items.value.push({
      id: nextId++,
      type,
      text: '',
      max_duration_sec: type === 'video' ? DEFAULT_VIDEO_DURATION_SEC : null,
    })
  }

  function remove(id: number) {
    changed.value = true
    items.value = items.value.filter((item) => item.id !== id)
    delete errors.value[id]
  }

  function move(index: number, offset: -1 | 1) {
    const target = index + offset
    if (target < 0 || target >= items.value.length) return
    changed.value = true
    const next = [...items.value]
    next.splice(target, 0, ...next.splice(index, 1))
    items.value = next
  }

  function changeType(id: number, type: QuestionType) {
    const item = items.value.find((entry) => entry.id === id)
    if (!item) return
    changed.value = true
    item.type = type
    item.max_duration_sec = type === 'video' ? DEFAULT_VIDEO_DURATION_SEC : null
    delete errors.value[id]
  }

  function update(id: number, patch: Partial<Pick<QuestionDraft, 'text' | 'max_duration_sec'>>) {
    const item = items.value.find((entry) => entry.id === id)
    if (!item) return
    changed.value = true
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
