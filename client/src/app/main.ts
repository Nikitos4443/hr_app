import 'primeicons/primeicons.css'
import '@/assets/main.css'

import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import { setupPrimeVue } from './providers/primevue'
import { setupQuery } from './providers/query'

export function bootstrap() {
  const app = createApp(App)

  app.use(router)
  setupPrimeVue(app)
  setupQuery(app)

  app.mount('#app')
}
