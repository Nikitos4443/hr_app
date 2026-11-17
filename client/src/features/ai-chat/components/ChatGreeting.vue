<script setup lang="ts">
import Button from 'primevue/button'

defineProps<{ title: string | null; company?: string | null; disabled?: boolean }>()

const emit = defineEmits<{ suggest: [text: string] }>()

const suggestions = [
  'Can I work remotely?',
  'What is the next hiring stage?',
  'What technologies does the team use?',
]
</script>

<template>
  <div class="greeting">
    <div class="greeting__bubble">
      Hi! I can answer questions about
      <template v-if="title">the "{{ title }}" vacancy</template>
      <template v-else>this vacancy</template>
      <template v-if="company"> and {{ company }}</template
      >.
    </div>
    <p class="greeting__label">Try asking:</p>
    <div class="greeting__chips">
      <Button
        v-for="text in suggestions"
        :key="text"
        :label="text"
        severity="secondary"
        variant="outlined"
        rounded
        size="small"
        :disabled="disabled"
        @click="emit('suggest', text)"
      />
    </div>
  </div>
</template>

<style scoped>
.greeting {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
}

.greeting__bubble {
  max-width: min(90%, 560px);
  padding: 10px 14px;
  border-radius: 16px 16px 16px 4px;
  background: var(--p-content-hover-background);
  line-height: 1.5;
}

.greeting__label {
  margin: 4px 0 0;
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.greeting__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
