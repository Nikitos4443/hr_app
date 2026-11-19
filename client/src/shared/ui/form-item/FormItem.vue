<script setup lang="ts">
import { computed, nextTick, onMounted, useId, watch } from 'vue'

const props = defineProps<{
  label: string
  for?: string
  required?: boolean
  hint?: string
  error?: string
}>()

defineSlots<{
  default?(props: {
    /** Space separated ids of the visible hint/error, or undefined. Bind to `aria-describedby`. */
    describedby: string | undefined
    /** True when an error is shown. Bind to `aria-invalid`. */
    invalid: boolean
    errorId: string
    hintId: string
  }): unknown
}>()

const uid = useId()
const base = computed(() => props.for ?? `fi-${uid}`)
const errorId = computed(() => `${base.value}-error`)
const hintId = computed(() => `${base.value}-hint`)
const describedby = computed(() =>
  props.error ? errorId.value : props.hint ? hintId.value : undefined,
)
const invalid = computed(() => Boolean(props.error))

// Existing usages do not bind the slot props, so link the control (found by `for`)
// to the hint/error automatically. Any other aria-describedby tokens are preserved.
function syncControl() {
  if (!props.for) return
  const el = document.getElementById(props.for)
  if (!el) return
  const own = new Set(
    (el.getAttribute('aria-describedby') ?? '')
      .split(/\s+/)
      .filter((t) => t && t !== errorId.value && t !== hintId.value),
  )
  if (describedby.value) own.add(describedby.value)
  if (own.size) el.setAttribute('aria-describedby', [...own].join(' '))
  else el.removeAttribute('aria-describedby')
  if (invalid.value) el.setAttribute('aria-invalid', 'true')
  else if (el.getAttribute('aria-invalid') === 'true') el.removeAttribute('aria-invalid')
}

onMounted(syncControl)
watch([describedby, invalid], () => nextTick(syncControl))
</script>

<template>
  <div class="form-item">
    <label :for="$props.for" class="form-item__label">
      {{ label }}
      <span v-if="required" class="form-item__required" aria-hidden="true">*</span>
    </label>
    <slot :describedby="describedby" :invalid="invalid" :error-id="errorId" :hint-id="hintId" />
    <small v-if="error" :id="errorId" class="form-item__error" role="alert">
      <i class="pi pi-exclamation-circle" aria-hidden="true" />
      {{ error }}
    </small>
    <small v-else-if="hint" :id="hintId" class="form-item__hint">{{ hint }}</small>
  </div>
</template>

<style scoped>
.form-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-item__label {
  font-size: 13px;
  font-weight: 600;
}

.form-item__required {
  color: var(--p-form-field-invalid-border-color);
}

.form-item__hint {
  color: var(--p-text-muted-color);
}

.form-item__error {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--p-form-field-invalid-border-color);
}
</style>
