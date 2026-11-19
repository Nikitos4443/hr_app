<script setup lang="ts">
import { computed, watch } from 'vue'
import { Form, type FormSubmitEvent } from '@primevue/forms'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import ProgressBar from 'primevue/progressbar'

import { FormItem } from '@/shared/ui'

import { useApplyForm } from '../composables/useApplyForm'
import { formatFileSize } from '../lib/resume'
import ApplySuccess from './ApplySuccess.vue'
import ResumeDropzone from './ResumeDropzone.vue'

const props = defineProps<{ vacancyId: number }>()
const emit = defineEmits<{ success: [] }>()

const form = useApplyForm(() => props.vacancyId)

watch(
  () => form.status.value,
  (status) => {
    if (status === 'success') emit('success')
  },
)

// Announce upload progress in coarse steps so screen readers are not flooded.
const progressAnnouncement = computed(() => {
  const step = Math.min(100, Math.floor(form.percent.value / 25) * 25)
  return `Uploading your application, ${step}%`
})

function onSubmit({ valid, values }: FormSubmitEvent) {
  form.submit(values as { email?: string }, valid)
}
</script>

<template>
  <ApplySuccess v-if="form.status.value === 'success'" :email="form.email.value" />

  <div v-else-if="form.status.value === 'uploading'" class="apply-progress">
    <p class="visually-hidden" role="status">{{ progressAnnouncement }}</p>
    <div class="apply-progress__head">
      <h2>Sending your application...</h2>
      <p>Please keep this page open until the upload finishes.</p>
    </div>
    <dl class="apply-progress__details">
      <dt>Email</dt>
      <dd>{{ form.email.value }}</dd>
    </dl>
    <div v-if="form.resume.value" class="apply-progress__file">
      <i class="pi pi-file-pdf" aria-hidden="true" />
      <span class="apply-progress__name">{{ form.resume.value.name }}</span>
      <span class="apply-progress__size">{{ formatFileSize(form.resume.value.size) }}</span>
    </div>
    <ProgressBar :value="form.percent.value" aria-label="Resume upload progress" />
  </div>

  <Form
    v-else
    :key="form.status.value === 'error' ? 'error' : 'form'"
    :resolver="form.resolver"
    :initial-values="{ email: form.email.value }"
    :validate-on-value-update="false"
    :validate-on-blur="true"
    class="apply-form"
    @submit="onSubmit"
  >
    <template #default="$form">
      <Message
        v-if="form.status.value === 'error'"
        severity="error"
        icon="pi pi-exclamation-circle"
      >
        <strong>Could not send your application.</strong> {{ form.errorText.value }} Your data is
        saved, please try again.
      </Message>

      <FormItem label="Your email" for="apply-email" required :error="$form.email?.error?.message">
        <InputText
          id="apply-email"
          name="email"
          type="email"
          autocomplete="email"
          placeholder="name@example.com"
          fluid
        />
      </FormItem>

      <FormItem label="Resume (PDF)" required :error="form.resumeError.value ?? undefined">
        <template #default="{ describedby, invalid }">
          <ResumeDropzone
            :file="form.resume.value"
            :invalid="invalid"
            :described-by="describedby"
            @select="form.selectResume"
            @remove="form.removeResume"
          />
        </template>
      </FormItem>

      <p class="apply-form__privacy">
        <i class="pi pi-lock" aria-hidden="true" />
        We use your data only to review this application. The resume is assessed by AI, and the
        final decision is made by a person.
      </p>

      <div class="apply-form__actions">
        <Button
          type="submit"
          :label="form.status.value === 'error' ? 'Try again' : 'Submit application'"
          :icon="form.status.value === 'error' ? 'pi pi-refresh' : undefined"
          size="large"
          fluid
        />
      </div>
    </template>
  </Form>
</template>

<style scoped>
.apply-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.apply-form__privacy {
  display: flex;
  gap: 8px;
  margin: 0;
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.apply-form__privacy i {
  margin-top: 3px;
}

.apply-form__actions {
  display: flex;
  flex-direction: column;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}

@media (max-width: 600px) {
  .apply-form__actions {
    position: sticky;
    bottom: 0;
    z-index: 5;
    margin: 0 -16px;
    padding: 12px 16px calc(12px + env(safe-area-inset-bottom));
    border-top: 1px solid var(--p-content-border-color);
    background: var(--p-content-background);
  }
}

.apply-progress {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.apply-progress__head h2 {
  margin: 0 0 4px;
}

.apply-progress__head p {
  margin: 0;
  color: var(--p-text-muted-color);
}

.apply-progress__details {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 12px;
  margin: 0;
}

.apply-progress__details dt {
  color: var(--p-text-muted-color);
}

.apply-progress__details dd {
  margin: 0;
  overflow-wrap: anywhere;
  font-weight: 600;
}

.apply-progress__file {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.apply-progress__name {
  overflow: hidden;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.apply-progress__size {
  color: var(--p-text-muted-color);
  font-size: 13px;
}
</style>
