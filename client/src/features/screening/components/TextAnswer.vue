<script setup lang="ts">
import { computed, ref } from 'vue'
import Button from 'primevue/button'
import Message from 'primevue/message'
import Textarea from 'primevue/textarea'

import { errorMessage } from '@/shared/api'
import { FormItem } from '@/shared/ui'

import { useSaveTextAnswerMutation } from '../api/screening.queries'
import { MAX_TEXT_ANSWER_LENGTH } from '../lib/limits'
import type { ScreeningQuestion } from '../types/screening'

const props = defineProps<{ token: string; question: ScreeningQuestion }>()
const emit = defineEmits<{ answered: [] }>()

const answer = ref('')
const save = useSaveTextAnswerMutation(() => props.token)

const trimmed = computed(() => answer.value.trim())
const canSubmit = computed(() => trimmed.value.length > 0 && !save.isPending.value)

function submit() {
  if (!canSubmit.value) return
  save.mutate(
    { questionId: props.question.id, answer: trimmed.value },
    { onSuccess: () => emit('answered') },
  )
}
</script>

<template>
  <form class="text-answer" @submit.prevent="submit">
    <FormItem label="Your answer" for="screening-text-answer">
      <Textarea
        id="screening-text-answer"
        v-model="answer"
        :maxlength="MAX_TEXT_ANSWER_LENGTH"
        rows="9"
        auto-resize
        fluid
        placeholder="Write your answer here"
      />
    </FormItem>
    <div class="text-answer__counter" role="status">
      {{ answer.length.toLocaleString('en-US') }} /
      {{ MAX_TEXT_ANSWER_LENGTH.toLocaleString('en-US') }}
    </div>

    <Message
      v-if="save.isError.value"
      severity="error"
      icon="pi pi-exclamation-circle"
      role="alert"
    >
      {{ errorMessage(save.error.value, 'Could not save your answer.') }}
    </Message>

    <Button
      type="submit"
      label="Send answer"
      icon="pi pi-check"
      icon-pos="right"
      size="large"
      fluid
      :loading="save.isPending.value"
      :disabled="!canSubmit"
    />
  </form>
</template>

<style scoped>
.text-answer {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.text-answer__counter {
  align-self: flex-end;
  font-size: 12px;
  color: var(--p-text-muted-color);
  font-variant-numeric: tabular-nums;
}
</style>
