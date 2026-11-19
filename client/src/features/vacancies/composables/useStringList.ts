import { computed, ref } from 'vue'

export interface StringListItem {
  id: number
  value: string
}

let nextId = 0

function toItems(values: string[]): StringListItem[] {
  return values.map((value) => ({ id: nextId++, value }))
}

export function useStringList(initial: string[] = []) {
  const items = ref<StringListItem[]>(toItems(initial))
  const baseline = ref(JSON.stringify(initial))

  const values = computed(() => items.value.map((item) => item.value.trim()).filter(Boolean))
  const dirty = computed(() => JSON.stringify(values.value) !== baseline.value)

  function add() {
    items.value.push({ id: nextId++, value: '' })
  }

  function remove(id: number) {
    items.value = items.value.filter((item) => item.id !== id)
  }

  function move(index: number, offset: -1 | 1) {
    const target = index + offset
    if (target < 0 || target >= items.value.length) return
    const next = [...items.value]
    next.splice(target, 0, ...next.splice(index, 1))
    items.value = next
  }

  function reset(next: string[] = []) {
    items.value = toItems(next)
    baseline.value = JSON.stringify(next)
  }

  return { items, values, dirty, add, remove, move, reset }
}

export type StringList = ReturnType<typeof useStringList>
