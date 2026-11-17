import { io, type Socket } from 'socket.io-client'

import { env } from '@/shared/config/env'

import type { ClientToServerEvents, ServerToClientEvents } from '../types/chat'

export type ChatSocket = Socket<ServerToClientEvents, ClientToServerEvents>

export function createChatSocket(): ChatSocket {
  const options = { autoConnect: false, transports: ['websocket', 'polling'] }
  return env.socketUrl ? io(env.socketUrl, options) : io(options)
}
