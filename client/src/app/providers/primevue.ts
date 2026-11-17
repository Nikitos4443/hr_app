import type { App } from 'vue'
import PrimeVue from 'primevue/config'
import ConfirmationService from 'primevue/confirmationservice'
import ToastService from 'primevue/toastservice'

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
  app.use(ToastService)
  app.use(ConfirmationService)
}
