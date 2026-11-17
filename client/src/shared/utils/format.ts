export function initials(name: string, maxLetters = 2): string {
  const words = name
    .trim()
    .split(/[\s_.-]+/)
    .filter(Boolean)
  if (words.length === 0) return '?'
  const letters =
    words.length === 1
      ? (words[0] ?? '').slice(0, maxLetters)
      : words.map((word) => word.charAt(0)).join('')
  return letters.slice(0, maxLetters).toUpperCase()
}
