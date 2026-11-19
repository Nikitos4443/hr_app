import { computed, onMounted, onUnmounted, ref, toValue, type MaybeRefOrGetter } from 'vue'

import { createChatSocket, type ChatSocket } from '../api/chat.socket'
import type { ChatMessage, ConnectionState } from '../types/chat'

const FRIENDLY_ERROR = 'Something went wrong while answering. Please try again.'
const CONNECTION_ERROR = 'Could not reach the assistant. Check your connection and try again.'

export function useAiChat(vacancyId: MaybeRefOrGetter<number>) {
  const messages = ref<ChatMessage[]>([])
  const connection = ref<ConnectionState>('connecting')
  const ready = ref(false)
  const botTyping = ref(false)
  const vacancyTitle = ref<string | null>(null)
  const error = ref<string | null>(null)

  let socket: ChatSocket | null = null
  let nextId = 1
  let pendingText: string | null = null

  const canSend = computed(
    () => connection.value === 'connected' && ready.value && !botTyping.value,
  )

  function startChat() {
    ready.value = false
    socket?.emit('chat_start', { vacancy_id: toValue(vacancyId) })
  }

  function bind(target: ChatSocket) {
    target.on('connect', () => {
      connection.value = 'connected'
      error.value = null
      startChat()
    })
    target.on('disconnect', () => {
      connection.value = 'disconnected'
      ready.value = false
      botTyping.value = false
    })
    target.io.on('reconnect_attempt', () => {
      connection.value = 'reconnecting'
    })
    target.on('connect_error', () => {
      connection.value = target.active ? 'reconnecting' : 'disconnected'
      error.value = CONNECTION_ERROR
    })
    target.on('chat_started', (payload) => {
      vacancyTitle.value = payload.title
      ready.value = true
      resendPending()
    })
    target.on('bot_typing', () => {
      botTyping.value = true
    })
    target.on('bot_message', (payload) => {
      botTyping.value = false
      messages.value.push({ id: nextId++, role: 'bot', text: payload.text })
    })
    target.on('chat_error', () => {
      botTyping.value = false
      error.value = FRIENDLY_ERROR
    })
  }

  function connect() {
    disconnect()
    connection.value = 'connecting'
    socket = createChatSocket()
    bind(socket)
    socket.connect()
  }

  function disconnect() {
    if (!socket) return
    socket.removeAllListeners()
    socket.io.removeAllListeners()
    socket.disconnect()
    socket = null
  }

  function send(text: string): boolean {
    const trimmed = text.trim()
    if (!trimmed || !canSend.value || !socket) return false
    error.value = null
    messages.value.push({ id: nextId++, role: 'user', text: trimmed })
    socket.emit('msg_event', { text: trimmed })
    return true
  }

  function resendPending() {
    if (!pendingText || !socket) return
    const text = pendingText
    pendingText = null
    botTyping.value = true
    socket.emit('msg_event', { text })
  }

  // Re-sends the last user message when it never got an answer, otherwise restarts the chat.
  function retry() {
    error.value = null
    const last = messages.value[messages.value.length - 1]
    pendingText = last?.role === 'user' ? last.text : null
    if (socket?.connected && ready.value) {
      if (pendingText) resendPending()
      else startChat()
    } else if (socket?.connected) startChat()
    else connect()
  }

  function dismissError() {
    error.value = null
  }

  onMounted(connect)
  onUnmounted(disconnect)

  return {
    messages,
    connection,
    ready,
    botTyping,
    vacancyTitle,
    error,
    canSend,
    send,
    retry,
    dismissError,
  }
}
