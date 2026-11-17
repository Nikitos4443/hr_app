const CURRENCY_SYMBOL: Record<string, string> = { USD: '$', EUR: '€', UAH: '₴' }

const numberFormat = new Intl.NumberFormat('en-US')
const dateFormat = new Intl.DateTimeFormat('en-US', {
  day: 'numeric',
  month: 'short',
  year: 'numeric',
})
const dateTimeFormat = new Intl.DateTimeFormat('en-US', {
  day: 'numeric',
  month: 'short',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
})

const EMPTY = '—'

function money(amount: number, currency: string | null): string {
  const value = numberFormat.format(amount)
  if (!currency) return value
  const symbol = CURRENCY_SYMBOL[currency]
  return symbol ? `${symbol}${value}` : `${value} ${currency}`
}

export function formatSalaryRange(
  min: number | null,
  max: number | null,
  currency: string | null,
): string {
  if (min == null && max == null) return EMPTY
  if (min != null && max != null) {
    if (min === max) return money(min, currency)
    const symbol = currency ? CURRENCY_SYMBOL[currency] : undefined
    if (symbol) return `${symbol}${numberFormat.format(min)} – ${numberFormat.format(max)}`
    return `${numberFormat.format(min)} – ${money(max, currency)}`
  }
  return min != null ? `from ${money(min, currency)}` : `up to ${money(max as number, currency)}`
}

export function formatDate(value: string | Date | null | undefined, withTime = false): string {
  if (!value) return EMPTY
  const date = value instanceof Date ? value : new Date(value)
  if (Number.isNaN(date.getTime())) return EMPTY
  return (withTime ? dateTimeFormat : dateFormat).format(date)
}
