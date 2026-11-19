import { definePreset } from '@primeuix/themes'
import Aura from '@primeuix/themes/aura'

// Separate variable: custom palettes (cobalt, stone) are not part of the Primitive type
const primitive = {
  cobalt: {
    50: '#EFF4FF',
    100: '#DFE9FF',
    200: '#C3D4FF',
    300: '#9AB5FF',
    400: '#7C98FF',
    500: '#4D6BEA',
    600: '#3350D6',
    700: '#2A41B0',
    800: '#263A8C',
    900: '#243470',
    950: '#172048',
  },
  stone: {
    50: '#FAF9F7',
    100: '#F4F2EE',
    200: '#E9E6E0',
    300: '#D6D2CA',
    400: '#A8A39A',
    500: '#7A756C',
    600: '#66615A',
    700: '#45413B',
    800: '#2E2B27',
    900: '#1E1C19',
    950: '#131211',
  },
  borderRadius: { none: '0', xs: '4px', sm: '6px', md: '8px', lg: '10px', xl: '12px' },
}

// Aura 5 builds light and dark schemes with light-dark(light, dark);
// dark mode is switched on by the .app-dark class (darkModeSelector).
export default definePreset(Aura, {
  primitive,
  semantic: {
    primary: {
      50: '{cobalt.50}',
      100: '{cobalt.100}',
      200: '{cobalt.200}',
      300: '{cobalt.300}',
      400: '{cobalt.400}',
      500: '{cobalt.500}',
      600: '{cobalt.600}',
      700: '{cobalt.700}',
      800: '{cobalt.800}',
      900: '{cobalt.900}',
      950: '{cobalt.950}',
      color: 'light-dark({cobalt.600}, {cobalt.400})',
      contrastColor: 'light-dark(#FFFFFF, #0E1330)',
      hoverColor: 'light-dark({cobalt.700}, {cobalt.300})',
      activeColor: 'light-dark({cobalt.800}, {cobalt.200})',
    },
    surface: {
      0: 'light-dark(#FFFFFF, #F2EFEA)',
      50: 'light-dark({stone.50}, #E9E6E0)',
      100: 'light-dark({stone.100}, #D6D2CA)',
      200: 'light-dark({stone.200}, #BDB8AF)',
      300: 'light-dark({stone.300}, #A9A39A)',
      400: 'light-dark({stone.400}, #A9A39A)',
      500: 'light-dark({stone.500}, #858077)',
      600: 'light-dark({stone.600}, #5F5A53)',
      700: 'light-dark({stone.700}, #3D3A36)',
      800: 'light-dark({stone.800}, #2F2C29)',
      900: 'light-dark({stone.900}, #1C1A18)',
      950: 'light-dark({stone.950}, #131211)',
    },
    highlight: {
      background: 'light-dark({cobalt.50}, #1F2748)',
      focusBackground: 'light-dark({cobalt.100}, #2C3763)',
      color: 'light-dark({cobalt.700}, #A9BEFF)',
      focusColor: 'light-dark({cobalt.800}, #DFE9FF)',
    },
    formField: {
      borderColor: 'light-dark(#8F8A81, #858077)',
      hoverBorderColor: 'light-dark({stone.600}, #A9A39A)',
      focusBorderColor: '{primary.color}',
      invalidBorderColor: 'light-dark(#B42318, #FF8F85)',
      placeholderColor: 'light-dark({stone.500}, #8F8981)',
    },
    text: {
      color: 'light-dark({stone.900}, #F2EFEA)',
      hoverColor: 'light-dark({stone.900}, #F2EFEA)',
      mutedColor: 'light-dark({stone.600}, #A9A39A)',
    },
  },
  components: {
    button: {
      root: {
        borderRadius: '{border.radius.lg}',
        paddingX: '1rem',
        paddingY: '0.625rem',
        label: { fontWeight: '600' },
      },
    },
    card: {
      root: {
        borderRadius: '{border.radius.xl}',
        shadow: '0 1px 2px rgba(30,28,25,.06), 0 4px 12px rgba(30,28,25,.05)',
      },
    },
    inputtext: { root: { borderRadius: '{border.radius.lg}' } },
    tag: {
      root: { fontWeight: '600', borderRadius: '99px' },
      success: {
        background: 'light-dark(#E6F4EA, #16291F)',
        color: 'light-dark(#176B3A, #6FD39A)',
      },
      warn: {
        background: 'light-dark(#FEF1D6, #33260F)',
        color: 'light-dark(#8A4B08, #F2B45C)',
      },
      danger: {
        background: 'light-dark(#FDECEA, #35191A)',
        color: 'light-dark(#B42318, #FF8F85)',
      },
      info: {
        background: 'light-dark(#E3F4F9, #112A33)',
        color: 'light-dark(#0B6A85, #6CC9E4)',
      },
    },
  },
})
