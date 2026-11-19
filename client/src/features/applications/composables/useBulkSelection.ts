import { computed, ref, watch, type Ref } from 'vue'

/** Row selection for the visible page; ids that leave the page are dropped from the selection. */
export function useBulkSelection(visibleIds: Ref<number[]>) {
  const selected = ref<Set<number>>(new Set())

  watch(visibleIds, (ids) => {
    const visible = new Set(ids)
    const kept = [...selected.value].filter((id) => visible.has(id))
    if (kept.length !== selected.value.size) selected.value = new Set(kept)
  })

  const count = computed(() => selected.value.size)
  const allSelected = computed(
    () => visibleIds.value.length > 0 && visibleIds.value.every((id) => selected.value.has(id)),
  )
  const someSelected = computed(() => count.value > 0 && !allSelected.value)

  function isSelected(id: number) {
    return selected.value.has(id)
  }

  function toggle(id: number) {
    const next = new Set(selected.value)
    if (!next.delete(id)) next.add(id)
    selected.value = next
  }

  function toggleAll() {
    selected.value = allSelected.value ? new Set() : new Set(visibleIds.value)
  }

  function clear() {
    selected.value = new Set()
  }

  return {
    ids: computed(() => [...selected.value]),
    count,
    allSelected,
    someSelected,
    isSelected,
    toggle,
    toggleAll,
    clear,
  }
}
