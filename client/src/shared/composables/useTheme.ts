import { computed, ref } from 'vue'

export type Theme = 'light' | 'dark'

const STORAGE_KEY = 'hr-theme'
// Must match `darkModeSelector` in app/providers/primevue.ts
const DARK_CLASS = 'app-dark'

// Module-level state: every useTheme() call shares the same theme
const theme = ref<Theme>('light')
let initialized = false

function readStored(): Theme | null {
  try {
    const value = localStorage.getItem(STORAGE_KEY)
    return value === 'light' || value === 'dark' ? value : null
  } catch {
    // Storage can be blocked (private mode, disabled cookies)
    return null
  }
}

function writeStored(value: Theme) {
  try {
    localStorage.setItem(STORAGE_KEY, value)
  } catch {
    // Ignore: the theme still works for this session
  }
}

function apply(value: Theme) {
  document.documentElement.classList.toggle(DARK_CLASS, value === 'dark')
}

export function initTheme() {
  if (initialized) return
  initialized = true

  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  theme.value = readStored() ?? (prefersDark ? 'dark' : 'light')
  apply(theme.value)
}

export function useTheme() {
  initTheme()

  function setTheme(value: Theme) {
    theme.value = value
    apply(value)
    writeStored(value)
  }

  function toggleTheme() {
    setTheme(theme.value === 'dark' ? 'light' : 'dark')
  }

  return {
    theme,
    isDark: computed(() => theme.value === 'dark'),
    setTheme,
    toggleTheme,
  }
}
