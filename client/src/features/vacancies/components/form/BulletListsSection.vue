<script setup lang="ts">
import { ref } from 'vue'
import Button from 'primevue/button'
import Menu from 'primevue/menu'
import type { MenuItem } from 'primevue/menuitem'
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

type ListKey = (typeof lists)[number]['key']

const menu = ref<InstanceType<typeof Menu> | null>(null)
const menuItems = ref<MenuItem[]>([])

// Narrow screens: the per-row actions collapse into one overflow menu to keep the input wide.
function openMenu(event: Event, key: ListKey, label: string, index: number) {
  const list = props[key]
  const last = list.items.value.length - 1
  const id = list.items.value[index]?.id
  menuItems.value = [
    {
      label: `Move ${label} row ${index + 1} up`,
      icon: 'pi pi-arrow-up',
      disabled: index === 0,
      command: () => list.move(index, -1),
    },
    {
      label: `Move ${label} row ${index + 1} down`,
      icon: 'pi pi-arrow-down',
      disabled: index === last,
      command: () => list.move(index, 1),
    },
    {
      label: `Remove ${label} row ${index + 1}`,
      icon: 'pi pi-times',
      command: () => id !== undefined && list.remove(id),
    },
  ]
  menu.value?.toggle(event)
}
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
            class="list__action"
            icon="pi pi-arrow-up"
            severity="secondary"
            text
            size="small"
            :aria-label="`Move ${list.label} row ${index + 1} up`"
            :disabled="index === 0"
            @click="props[list.key].move(index, -1)"
          />
          <Button
            class="list__action"
            icon="pi pi-arrow-down"
            severity="secondary"
            text
            size="small"
            :aria-label="`Move ${list.label} row ${index + 1} down`"
            :disabled="index === props[list.key].items.value.length - 1"
            @click="props[list.key].move(index, 1)"
          />
          <Button
            class="list__action"
            icon="pi pi-times"
            severity="secondary"
            text
            size="small"
            :aria-label="`Remove ${list.label} row ${index + 1}`"
            @click="props[list.key].remove(item.id)"
          />
          <Button
            class="list__more"
            icon="pi pi-ellipsis-v"
            severity="secondary"
            text
            size="small"
            :aria-label="`Actions for ${list.label} row ${index + 1}`"
            aria-haspopup="true"
            @click="openMenu($event, list.key, list.label, index)"
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
    <Menu ref="menu" :model="menuItems" popup />
  </FormSection>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
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

.list__more {
  display: none;
}

@media (max-width: 479px) {
  .list__action {
    display: none;
  }

  .list__more {
    display: inline-flex;
  }
}

.list__add {
  align-self: flex-start;
}
</style>
