<script setup lang="ts">
import type { ChatMessage } from '../types/chat'

defineProps<{ message: ChatMessage }>()
</script>

<template>
  <div class="bubble-row" :class="`bubble-row--${message.role}`">
    <div class="bubble" :class="`bubble--${message.role}`">{{ message.text }}</div>
  </div>
</template>

<style scoped>
.bubble-row {
  display: flex;
}

.bubble-row--user {
  justify-content: flex-end;
}

.bubble {
  max-width: min(80%, 560px);
  padding: 10px 14px;
  overflow-wrap: anywhere;
  line-height: 1.5;
  white-space: pre-wrap;
}

.bubble--user {
  border-radius: 16px 16px 4px 16px;
  background: var(--p-primary-color);
  color: var(--p-primary-contrast-color);
}

.bubble--bot {
  border-radius: 16px 16px 16px 4px;
  background: var(--p-content-hover-background);
}

@media (max-width: 600px) {
  .bubble {
    max-width: 90%;
  }
}
</style>
