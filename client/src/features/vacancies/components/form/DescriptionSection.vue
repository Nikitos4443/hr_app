<script setup lang="ts">
import Textarea from 'primevue/textarea'

import { FormItem } from '@/shared/ui'

import FormSection from './FormSection.vue'

defineProps<{ errors: Record<string, string | undefined> }>()
</script>

<template>
  <FormSection title="Description">
    <FormItem label="About the vacancy" for="vacancy-description" :error="errors.description">
      <Textarea id="vacancy-description" name="description" rows="6" auto-resize fluid />
    </FormItem>
  </FormSection>
</template>
