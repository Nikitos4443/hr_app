<script setup lang="ts">
import { ref } from 'vue'
import Button from 'primevue/button'
import Textarea from 'primevue/textarea'

const props = defineProps<{ blocked?: boolean; placeholder?: string }>()

const emit = defineEmits<{ send: [text: string] }>()

const text = ref('')

function submit() {
  const trimmed = text.value.trim()
  if (!trimmed || props.blocked) return
  emit('send', trimmed)
  text.value = ''
}

function onKeydown(event: KeyboardEvent) {
  if (event.key !== 'Enter' || event.shiftKey || event.isComposing) return
  event.preventDefault()
  submit()
}
</script>

<template>
  <form class="chat-input" @submit.prevent="submit">
    <Textarea
      v-model="text"
      class="chat-input__field"
      rows="1"
      auto-resize
      :placeholder="placeholder ?? 'Write your question...'"
      aria-label="Message"
      @keydown="onKeydown"
    />
    <Button
      type="submit"
      class="chat-input__send"
      icon="pi pi-send"
      aria-label="Send message"
      :disabled="blocked || !text.trim()"
    />
  </form>
</template>

<style scoped>
.chat-input {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.chat-input__send {
  flex: none;
  min-width: 44px;
  min-height: 44px;
}

.chat-input__field {
  min-height: 44px;
  flex: 1;
  max-height: 140px;
  resize: none;
}
</style>
