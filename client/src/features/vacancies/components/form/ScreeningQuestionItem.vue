<script setup lang="ts">
import Button from 'primevue/button'
import InputNumber from 'primevue/inputnumber'
import SelectButton from 'primevue/selectbutton'
import Tag from 'primevue/tag'
import Textarea from 'primevue/textarea'

import { FormItem } from '@/shared/ui'

import type { QuestionDraft, QuestionErrors, QuestionType } from '../../composables/useQuestionList'
import { MAX_TEXT_ANSWER_LENGTH, MAX_VIDEO_DURATION_SEC } from '../../lib/schemas'

defineProps<{
  question: QuestionDraft
  index: number
  count: number
  errors: QuestionErrors
}>()

const emit = defineEmits<{
  'move-up': []
  'move-down': []
  remove: []
  'change-type': [type: QuestionType]
  'update-text': [text: string]
  'update-duration': [seconds: number | null]
  blur: []
}>()

const typeOptions = [
  { value: 'video', label: 'Video' },
  { value: 'text', label: 'Text' },
]
</script>

<template>
  <div class="question">
    <div class="question__head">
      <span class="question__number">{{ index + 1 }}</span>
      <span class="question__title">Question {{ index + 1 }}</span>
      <Tag
        :value="question.type === 'video' ? 'Video' : 'Text'"
        :icon="question.type === 'video' ? 'pi pi-video' : 'pi pi-align-left'"
        :severity="question.type === 'video' ? 'info' : 'secondary'"
      />
      <Button
        icon="pi pi-arrow-up"
        severity="secondary"
        text
        size="small"
        aria-label="Move up"
        :disabled="index === 0"
        @click="emit('move-up')"
      />
      <Button
        icon="pi pi-arrow-down"
        severity="secondary"
        text
        size="small"
        aria-label="Move down"
        :disabled="index === count - 1"
        @click="emit('move-down')"
      />
      <Button
        icon="pi pi-trash"
        severity="danger"
        text
        size="small"
        aria-label="Remove question"
        @click="emit('remove')"
      />
    </div>

    <FormItem
      label="Question text"
      :for="`question-text-${question.id}`"
      required
      :error="errors.text"
    >
      <Textarea
        :id="`question-text-${question.id}`"
        :model-value="question.text"
        rows="3"
        auto-resize
        :invalid="Boolean(errors.text)"
        fluid
        @update:model-value="emit('update-text', $event ?? '')"
        @blur="emit('blur')"
      />
    </FormItem>

    <div class="question__settings">
      <FormItem label="Format">
        <SelectButton
          :model-value="question.type"
          :options="typeOptions"
          option-label="label"
          option-value="value"
          :allow-empty="false"
          aria-label="Question format"
          @update:model-value="emit('change-type', $event)"
        />
      </FormItem>
      <FormItem
        v-if="question.type === 'video'"
        label="Max duration, seconds"
        :for="`question-duration-${question.id}`"
        :error="errors.max_duration_sec"
      >
        <InputNumber
          :input-id="`question-duration-${question.id}`"
          :model-value="question.max_duration_sec"
          :min="0"
          :max="MAX_VIDEO_DURATION_SEC"
          :invalid="Boolean(errors.max_duration_sec)"
          suffix=" sec"
          @update:model-value="emit('update-duration', $event)"
          @blur="emit('blur')"
        />
      </FormItem>
      <span v-else class="question__note">
        Answer up to {{ MAX_TEXT_ANSWER_LENGTH }} characters
      </span>
    </div>
  </div>
</template>

<style scoped>
.question {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--p-content-border-color);
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-hover-background);
}

.question__head {
  display: flex;
  align-items: center;
  gap: 8px;
}

.question__number {
  display: grid;
  place-items: center;
  flex: none;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 13px;
  font-weight: 700;
  background: var(--p-highlight-background);
  color: var(--p-highlight-color);
}

.question__title {
  flex: 1;
  font-weight: 600;
}

.question__settings {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 16px;
}

.question__note {
  align-self: center;
  color: var(--p-text-muted-color);
  font-size: 13px;
}
</style>
