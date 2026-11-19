<script lang="ts">
export type VacancyTabKey = 'overview' | 'candidates' | 'questions'
</script>

<script setup lang="ts">
import Badge from 'primevue/badge'
import Tab from 'primevue/tab'
import TabList from 'primevue/tablist'
import Tabs from 'primevue/tabs'

defineProps<{
  modelValue: VacancyTabKey
  candidates?: number
  questions?: number
}>()

const emit = defineEmits<{ 'update:modelValue': [tab: VacancyTabKey] }>()

function onChange(value: string | number) {
  emit('update:modelValue', value as VacancyTabKey)
}
</script>

<template>
  <Tabs :value="modelValue" @update:value="onChange">
    <TabList>
      <Tab value="overview">Overview</Tab>
      <Tab value="candidates">
        <span class="tab">
          Candidates
          <Badge v-if="candidates !== undefined" :value="candidates" />
        </span>
      </Tab>
      <Tab value="questions">
        <span class="tab">
          Screening questions
          <Badge v-if="questions !== undefined" :value="questions" severity="secondary" />
        </span>
      </Tab>
    </TabList>
  </Tabs>
</template>

<style scoped>
.tab {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
</style>
