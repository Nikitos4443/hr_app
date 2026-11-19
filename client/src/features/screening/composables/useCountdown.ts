import { computed, onBeforeUnmount, ref, toValue, type MaybeRefOrGetter } from 'vue'

const TICK_MS = 250

export function useCountdown(durationSec: MaybeRefOrGetter<number>, onExpire?: () => void) {
  const elapsedMs = ref(0)
  const running = ref(false)
  let timer: ReturnType<typeof setInterval> | null = null
  let startedAt = 0

  const elapsedSec = computed(() => Math.floor(elapsedMs.value / 1000))
  const remainingSec = computed(() => Math.max(0, toValue(durationSec) - elapsedSec.value))
  const percent = computed(() =>
    Math.min(100, Math.round((elapsedMs.value / (toValue(durationSec) * 1000)) * 100)),
  )

  function clear() {
    if (timer !== null) clearInterval(timer)
    timer = null
    running.value = false
  }

  function start() {
    clear()
    elapsedMs.value = 0
    startedAt = Date.now()
    running.value = true
    timer = setInterval(() => {
      elapsedMs.value = Date.now() - startedAt
      if (elapsedMs.value >= toValue(durationSec) * 1000) {
        elapsedMs.value = toValue(durationSec) * 1000
        clear()
        onExpire?.()
      }
    }, TICK_MS)
  }

  function stop() {
    clear()
  }

  function reset() {
    clear()
    elapsedMs.value = 0
  }

  onBeforeUnmount(clear)

  return { elapsedSec, remainingSec, percent, running, start, stop, reset }
}
