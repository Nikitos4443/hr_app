<script setup lang="ts">
import { computed } from 'vue'
import Tag from 'primevue/tag'

import type { AnswerDetail } from '../../types/application'
import TranscriptBlock from './TranscriptBlock.vue'

const props = defineProps<{ answers: AnswerDetail[] }>()

const sorted = computed(() => [...props.answers].sort((a, b) => a.order - b.order))
const doneCount = computed(() => props.answers.filter((answer) => answer.status === 'done').length)
const complete = computed(
  () => props.answers.length > 0 && doneCount.value === props.answers.length,
)
</script>

<template>
  <section class="answers" aria-labelledby="answers-title">
    <div class="answers__head">
      <h3 id="answers-title" class="answers__title">Screening answers</h3>
      <Tag
        v-if="answers.length"
        :value="
          complete
            ? `All ${answers.length} answers received`
            : `${doneCount} of ${answers.length} answered`
        "
        :icon="complete ? 'pi pi-check-circle' : 'pi pi-hourglass'"
        :severity="complete ? 'success' : 'secondary'"
      />
    </div>

    <p v-if="!answers.length" class="answers__empty">This vacancy has no screening questions.</p>

    <ol v-else class="answers__list">
      <li v-for="(answer, index) in sorted" :key="answer.question_id" class="answer">
        <div class="answer__head">
          <span class="answer__num">{{ index + 1 }}</span>
          <div class="answer__question">
            <span class="answer__text">{{ answer.text }}</span>
            <span class="answer__type">
              <i
                :class="answer.type === 'video' ? 'pi pi-video' : 'pi pi-align-left'"
                aria-hidden="true"
              />
              {{ answer.type === 'video' ? 'Video answer' : 'Text answer' }}
            </span>
          </div>
          <Tag
            :value="answer.status === 'done' ? 'Answered' : 'Pending'"
            :icon="answer.status === 'done' ? 'pi pi-check-circle' : 'pi pi-clock'"
            :severity="answer.status === 'done' ? 'success' : 'warn'"
          />
        </div>

        <p v-if="answer.status !== 'done'" class="answer__pending">Not answered yet.</p>
        <TranscriptBlock v-else-if="answer.type === 'video'" :text="answer.transcription" />
        <p v-else class="answer__body">{{ answer.answer }}</p>
      </li>
    </ol>
  </section>
</template>

<style scoped>
.answers {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.answers__head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.answers__title {
  margin: 0;
  font-size: 16px;
}

.answers__empty {
  margin: 0;
  color: var(--p-text-muted-color);
}

.answers__list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.answer {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--p-content-border-color);
  border-radius: 10px;
}

.answer__head {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.answer__num {
  display: grid;
  flex: none;
  place-items: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--p-highlight-background);
  color: var(--p-highlight-color);
  font-size: 13px;
  font-weight: 700;
}

.answer__question {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.answer__text {
  font-weight: 600;
}

.answer__type {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.answer__pending {
  margin: 0;
  color: var(--p-text-muted-color);
}

.answer__body {
  margin: 0;
  padding: 12px 14px;
  border-radius: 10px;
  background: var(--p-content-hover-background);
  line-height: 22px;
  white-space: pre-line;
}
</style>
