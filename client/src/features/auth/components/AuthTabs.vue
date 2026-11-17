<script setup lang="ts">
import Tab from 'primevue/tab'
import TabList from 'primevue/tablist'
import Tabs from 'primevue/tabs'

export type AuthMode = 'login' | 'register'

const mode = defineModel<AuthMode>({ required: true })
</script>

<template>
  <Tabs v-model:value="mode">
    <TabList>
      <Tab value="login">Sign in</Tab>
      <Tab value="register">Sign up</Tab>
    </TabList>
  </Tabs>
</template>
