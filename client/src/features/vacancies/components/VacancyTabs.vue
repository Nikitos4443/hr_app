<script lang="ts">
export type VacancyTabKey = 'overview' | 'candidates' | 'questions'
</script>

<script setup lang="ts">
import Badge from 'primevue/badge'
import Tab from 'primevue/tab'
import TabList from 'primevue/tablist'
import TabPanel from 'primevue/tabpanel'
import TabPanels from 'primevue/tabpanels'
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
  <Tabs :value="modelValue" lazy @update:value="onChange">
    <TabList aria-label="Vacancy sections">
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
    <TabPanels class="tabs__panels">
      <TabPanel value="overview"><slot name="overview" /></TabPanel>
      <TabPanel value="candidates"><slot name="candidates" /></TabPanel>
      <TabPanel value="questions"><slot name="questions" /></TabPanel>
    </TabPanels>
  </Tabs>
</template>

<style scoped>
.tabs__panels {
  padding: 20px 0 0;
}

.tab {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
</style>
