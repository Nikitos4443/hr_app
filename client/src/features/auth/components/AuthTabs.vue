<script setup lang="ts">
import Tab from 'primevue/tab'
import TabList from 'primevue/tablist'
import TabPanel from 'primevue/tabpanel'
import TabPanels from 'primevue/tabpanels'
import Tabs from 'primevue/tabs'

export type AuthMode = 'login' | 'register'

const mode = defineModel<AuthMode>({ required: true })

defineSlots<{ login?(): unknown; register?(): unknown }>()
</script>

<template>
  <Tabs v-model:value="mode" lazy>
    <TabList aria-label="Sign in or create an account">
      <Tab value="login">Sign in</Tab>
      <Tab value="register">Sign up</Tab>
    </TabList>
    <TabPanels class="auth-tabs__panels">
      <TabPanel value="login"><slot name="login" /></TabPanel>
      <TabPanel value="register"><slot name="register" /></TabPanel>
    </TabPanels>
  </Tabs>
</template>

<style scoped>
.auth-tabs__panels {
  padding: 20px 0 0;
}
</style>
