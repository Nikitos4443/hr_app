<script setup lang="ts">
import Button from 'primevue/button'
import Tag from 'primevue/tag'

import type { QuestionList } from '../../composables/useQuestionList'
import FormSection from './FormSection.vue'
import ScreeningQuestionItem from './ScreeningQuestionItem.vue'

defineProps<{ questions: QuestionList }>()
</script>

<template>
  <FormSection
    title="Screening questions"
    hint="Candidates answer in order. Use the arrows to change the sequence."
  >
    <template #aside>
      <Tag
        icon="pi pi-list"
        severity="secondary"
        :value="`${questions.items.value.length} questions`"
      />
    </template>

    <p v-if="!questions.items.value.length" class="empty">No questions yet.</p>

    <ScreeningQuestionItem
      v-for="(question, index) in questions.items.value"
      :key="question.id"
      :question="question"
      :index="index"
      :count="questions.items.value.length"
      :errors="questions.errors.value[question.id] ?? {}"
      @move-up="questions.move(index, -1)"
      @move-down="questions.move(index, 1)"
      @remove="questions.remove(question.id)"
      @change-type="questions.changeType(question.id, $event)"
      @update-text="questions.update(question.id, { text: $event })"
      @update-duration="questions.update(question.id, { max_duration_sec: $event })"
      @blur="questions.validateOne(question.id)"
    />

    <div class="actions">
      <Button
        label="Add video question"
        icon="pi pi-video"
        severity="secondary"
        @click="questions.add('video')"
      />
      <Button
        label="Add text question"
        icon="pi pi-align-left"
        severity="secondary"
        @click="questions.add('text')"
      />
    </div>
  </FormSection>
</template>

<style scoped>
.empty {
  margin: 0;
  color: var(--p-text-muted-color);
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
