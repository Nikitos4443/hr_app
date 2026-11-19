<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
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

const DRAFT_DELAY_MS = 600
const NEAR_LIMIT_RATIO = 0.9

const draftKey = `screening-draft:${props.token}:${props.question.id}`

function loadDraft(): string {
  try {
    return sessionStorage.getItem(draftKey) ?? ''
  } catch {
    return ''
  }
}

function storeDraft(value: string) {
  try {
    if (value) sessionStorage.setItem(draftKey, value)
    else sessionStorage.removeItem(draftKey)
  } catch {
    return
  }
}

const answer = ref(loadDraft())
const draftSaved = ref(answer.value.length > 0)
const save = useSaveTextAnswerMutation(() => props.token)
let draftTimer: ReturnType<typeof setTimeout> | null = null

watch(answer, (value) => {
  draftSaved.value = false
  if (draftTimer) clearTimeout(draftTimer)
  draftTimer = setTimeout(() => {
    storeDraft(value)
    draftSaved.value = value.length > 0
  }, DRAFT_DELAY_MS)
})

onBeforeUnmount(() => {
  if (draftTimer) clearTimeout(draftTimer)
})

const trimmed = computed(() => answer.value.trim())
const canSubmit = computed(() => trimmed.value.length > 0 && !save.isPending.value)
const nearLimit = computed(() => answer.value.length >= MAX_TEXT_ANSWER_LENGTH * NEAR_LIMIT_RATIO)

function submit() {
  if (!canSubmit.value) return
  save.mutate(
    { questionId: props.question.id, answer: trimmed.value },
    {
      onSuccess: () => {
        if (draftTimer) clearTimeout(draftTimer)
        storeDraft('')
        emit('answered')
      },
    },
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
    <div class="text-answer__meta">
      <span role="status">
        <template v-if="draftSaved"
          ><i class="pi pi-check" aria-hidden="true" /> Draft saved on this device</template
        >
      </span>
      <span class="text-answer__counter" :role="nearLimit ? 'status' : undefined">
        {{ answer.length.toLocaleString('en-US') }} /
        {{ MAX_TEXT_ANSWER_LENGTH.toLocaleString('en-US') }}
      </span>
    </div>

    <Message
      v-if="save.isError.value"
      severity="error"
      icon="pi pi-exclamation-circle"
      role="alert"
    >
      {{ errorMessage(save.error.value, 'Could not save your answer.') }}
    </Message>

    <div class="text-answer__actions">
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
    </div>
  </form>
</template>

<style scoped>
.text-answer {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.text-answer__meta {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  min-height: 18px;
  font-size: 12px;
  color: var(--p-text-muted-color);
}

.text-answer__counter {
  margin-left: auto;
  font-variant-numeric: tabular-nums;
}

@media (max-width: 600px) {
  .text-answer__actions {
    position: sticky;
    bottom: 0;
    z-index: 5;
    margin: 0 -16px;
    padding: 12px 16px calc(12px + env(safe-area-inset-bottom));
    border-top: 1px solid var(--p-content-border-color);
    background: var(--p-content-background);
  }
}
</style>
