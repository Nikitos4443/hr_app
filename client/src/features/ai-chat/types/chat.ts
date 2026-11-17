export type ChatRole = 'user' | 'bot'

export interface ChatMessage {
  id: number
  role: ChatRole
  text: string
}

export type ConnectionState = 'connecting' | 'connected' | 'reconnecting' | 'disconnected'

export interface ChatStartedPayload {
  vacancy_id: number
  title: string
}

export interface ChatErrorPayload {
  error: string
}

export interface BotMessagePayload {
  text: string
}

export interface ServerToClientEvents {
  chat_started: (payload: ChatStartedPayload) => void
  chat_error: (payload: ChatErrorPayload) => void
  bot_typing: () => void
  bot_message: (payload: BotMessagePayload) => void
}

export interface ClientToServerEvents {
  chat_start: (payload: { vacancy_id: number }) => void
  msg_event: (payload: { text: string }) => void
}
