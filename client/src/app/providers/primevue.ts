import type { App } from 'vue'
import PrimeVue from 'primevue/config'

import HrPreset from './hr-preset'

export function setupPrimeVue(app: App) {
  app.use(PrimeVue, {
    theme: {
      preset: HrPreset,
      options: {
        darkModeSelector: '.app-dark',
        cssLayer: { name: 'primevue', order: 'theme, base, primevue' },
      },
    },
  })
}
