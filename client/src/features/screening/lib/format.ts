export function formatClock(totalSeconds: number): string {
  const safe = Math.max(0, Math.round(totalSeconds))
  const minutes = Math.floor(safe / 60)
  const seconds = safe % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
}

export function formatMegabytes(bytes: number): string {
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export function formatLimit(totalSeconds: number): string {
  if (totalSeconds < 60) return `${totalSeconds} sec`
  const minutes = totalSeconds / 60
  return `${Number.isInteger(minutes) ? minutes : minutes.toFixed(1)} min`
}
