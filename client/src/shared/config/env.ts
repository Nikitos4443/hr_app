export const env = {
  apiUrl: (import.meta.env.VITE_API_URL ?? '/api').replace(/\/+$/, ''),
  socketUrl: import.meta.env.VITE_SOCKET_URL ?? '',
} as const
