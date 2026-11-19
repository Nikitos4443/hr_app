<script setup lang="ts">
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'

import type { StringList } from '../../composables/useStringList'
import FormSection from './FormSection.vue'

const props = defineProps<{
  responsibilities: StringList
  requirements: StringList
  niceToHave: StringList
}>()

const lists = [
  { key: 'responsibilities', label: 'Responsibilities', placeholder: 'New responsibility' },
  { key: 'requirements', label: 'Requirements', placeholder: 'New requirement' },
  { key: 'niceToHave', label: 'Nice to have', placeholder: 'New item' },
] as const
</script>

<template>
  <FormSection title="Lists" hint="Add, remove and reorder rows">
    <div class="grid">
      <div v-for="list in lists" :key="list.key" class="list">
        <span class="list__label">{{ list.label }}</span>
        <div v-for="(item, index) in props[list.key].items.value" :key="item.id" class="list__row">
          <InputText
            v-model="item.value"
            :placeholder="list.placeholder"
            :aria-label="`${list.label}, row ${index + 1}`"
            fluid
          />
          <Button
            icon="pi pi-arrow-up"
            severity="secondary"
            text
            size="small"
            :aria-label="`Move ${list.label} row ${index + 1} up`"
            :disabled="index === 0"
            @click="props[list.key].move(index, -1)"
          />
          <Button
            icon="pi pi-arrow-down"
            severity="secondary"
            text
            size="small"
            :aria-label="`Move ${list.label} row ${index + 1} down`"
            :disabled="index === props[list.key].items.value.length - 1"
            @click="props[list.key].move(index, 1)"
          />
          <Button
            icon="pi pi-times"
            severity="secondary"
            text
            size="small"
            :aria-label="`Remove ${list.label} row ${index + 1}`"
            @click="props[list.key].remove(item.id)"
          />
        </div>
        <Button
          label="Add row"
          :aria-label="`Add ${list.label} row`"
          icon="pi pi-plus"
          severity="secondary"
          text
          size="small"
          class="list__add"
          @click="props[list.key].add()"
        />
      </div>
    </div>
  </FormSection>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  align-items: start;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.list__label {
  font-size: 13px;
  font-weight: 600;
}

.list__row {
  display: flex;
  align-items: center;
  gap: 2px;
}

.list__add {
  align-self: flex-start;
}
</style>
