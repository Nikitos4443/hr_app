<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'

defineProps<{ email: string }>()

const title = ref<HTMLElement | null>(null)

onMounted(() => nextTick(() => title.value?.focus()))
</script>

<template>
  <div class="success">
    <span class="success__icon"><i class="pi pi-check" aria-hidden="true" /></span>
    <h1 ref="title" class="success__title" tabindex="-1">Thank you for applying!</h1>
    <p class="success__text">
      We will review your resume and email you at <strong>{{ email }}</strong
      >.
    </p>
    <div class="success__next">
      <strong><i class="pi pi-sparkles" aria-hidden="true" /> What happens next</strong>
      <p>
        If your profile is a match, you will receive a link to a short screening. Please check your
        spam folder too.
      </p>
    </div>
  </div>
</template>

<style scoped>
.success {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
}

.success__icon {
  display: grid;
  place-items: center;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--p-highlight-background);
  color: var(--p-highlight-color);
  font-size: 28px;
}

.success__title {
  margin: 0;
}

.success__title:focus {
  outline: none;
}

.success__text {
  margin: 0;
  overflow-wrap: anywhere;
  color: var(--p-text-muted-color);
}

.success__next {
  align-self: stretch;
  padding: 16px;
  border-radius: var(--p-content-border-radius);
  background: var(--p-content-hover-background);
  text-align: left;
}

.success__next p {
  margin: 6px 0 0;
  color: var(--p-text-muted-color);
}
</style>
