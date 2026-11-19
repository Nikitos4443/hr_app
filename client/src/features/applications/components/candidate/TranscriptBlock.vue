<script setup lang="ts">
import { computed, ref } from 'vue'
import Button from 'primevue/button'

const COLLAPSE_AFTER = 320

const props = defineProps<{ text: string | null }>()

const expanded = ref(false)
const long = computed(() => (props.text?.length ?? 0) > COLLAPSE_AFTER)
</script>

<template>
  <div class="transcript">
    <span class="transcript__label">Transcript</span>
    <template v-if="text">
      <p class="transcript__text" :class="{ 'transcript__text--clamped': long && !expanded }">
        {{ text }}
      </p>
      <Button
        v-if="long"
        :label="expanded ? 'Show less' : 'Show more'"
        :icon="expanded ? 'pi pi-chevron-up' : 'pi pi-chevron-down'"
        severity="secondary"
        text
        size="small"
        class="transcript__toggle"
        :aria-expanded="expanded"
        @click="expanded = !expanded"
      />
    </template>
    <p v-else class="transcript__empty">The transcript is not ready yet.</p>
  </div>
</template>

<style scoped>
.transcript {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  padding: 12px 14px;
  border-radius: 10px;
  background: var(--p-content-hover-background);
}

.transcript__label {
  color: var(--p-text-muted-color);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.transcript__text {
  margin: 0;
  font-size: 14px;
  line-height: 22px;
  white-space: pre-line;
}

.transcript__text--clamped {
  display: -webkit-box;
  overflow: hidden;
  -webkit-line-clamp: 5;
  -webkit-box-orient: vertical;
}

.transcript__empty {
  margin: 0;
  color: var(--p-text-muted-color);
}

.transcript__toggle {
  padding-inline: 0;
}
</style>
