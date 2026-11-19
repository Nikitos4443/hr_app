<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'

import { useAiChat } from '../composables/useAiChat'
import ChatErrorBanner from './ChatErrorBanner.vue'
import ChatGreeting from './ChatGreeting.vue'
import ChatInput from './ChatInput.vue'
import ChatMessageBubble from './ChatMessageBubble.vue'
import TypingIndicator from './TypingIndicator.vue'

const props = defineProps<{ vacancyId: number; company?: string | null }>()

const chat = useAiChat(() => props.vacancyId)

const list = ref<HTMLElement | null>(null)

const statusLabel = computed(() => {
  switch (chat.connection.value) {
    case 'connected':
      return chat.ready.value ? null : 'Starting the chat...'
    case 'connecting':
      return 'Connecting...'
    case 'reconnecting':
      return 'Connection lost. Reconnecting...'
    default:
      return 'Disconnected'
  }
})

const inputPlaceholder = computed(() =>
  chat.canSend.value || chat.botTyping.value
    ? 'Write your question...'
    : 'Waiting for the connection...',
)

function scrollToEnd() {
  nextTick(() => {
    if (list.value) list.value.scrollTop = list.value.scrollHeight
  })
}

watch(() => [chat.messages.value.length, chat.botTyping.value, chat.error.value], scrollToEnd)
</script>

<template>
  <section class="chat" aria-label="AI assistant">
    <header class="chat__head">
      <i class="pi pi-sparkles chat__head-icon" aria-hidden="true" />
      <div class="chat__head-text">
        <strong>AI assistant</strong>
        <span>About the vacancy and the company</span>
      </div>
      <span v-if="statusLabel" class="chat__status" role="status">{{ statusLabel }}</span>
    </header>

    <div
      ref="list"
      class="chat__list"
      role="log"
      aria-label="Conversation"
      aria-live="polite"
      aria-relevant="additions"
    >
      <ChatGreeting
        :title="chat.vacancyTitle.value"
        :company="company"
        :disabled="!chat.canSend.value"
        @suggest="chat.send"
      />
      <ChatMessageBubble
        v-for="message in chat.messages.value"
        :key="message.id"
        :message="message"
      />
      <TypingIndicator v-if="chat.botTyping.value" />
    </div>

    <div class="chat__footer">
      <ChatErrorBanner v-if="chat.error.value" :message="chat.error.value" @retry="chat.retry" />
      <ChatInput :blocked="!chat.canSend.value" :placeholder="inputPlaceholder" @send="chat.send" />
      <p class="chat__note">
        <i class="pi pi-info-circle" aria-hidden="true" />
        Answers are based only on the vacancy and company information.
      </p>
    </div>
  </section>
</template>

<style scoped>
.chat {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  border: 1px solid var(--p-content-border-color);
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-background);
}

.chat__head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--p-content-border-color);
}

.chat__head-icon {
  color: var(--p-primary-color);
}

.chat__head-text {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
}

.chat__head-text span {
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.chat__status {
  color: var(--p-text-muted-color);
  font-size: 13px;
}

.chat__list {
  display: flex;
  min-height: 0;
  flex: 1;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  overflow-y: auto;
}

.chat__footer {
  display: flex;
  flex: none;
  flex-direction: column;
  gap: 10px;
  padding: 12px 16px 16px;
  border-top: 1px solid var(--p-content-border-color);
}

.chat__note {
  display: flex;
  gap: 6px;
  margin: 0;
  color: var(--p-text-muted-color);
  font-size: 12px;
}
</style>
