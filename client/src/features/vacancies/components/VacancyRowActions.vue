<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import Menu from 'primevue/menu'
import type { MenuItem } from 'primevue/menuitem'
import { useConfirm } from 'primevue/useconfirm'

import { useNotify } from '@/shared/composables/useNotify'

import { useDeleteVacancyMutation, useUpdateVacancyMutation } from '../api/vacancies.queries'
import type { Vacancy } from '../types/vacancy'

const props = defineProps<{ vacancy: Vacancy }>()

const router = useRouter()
const confirm = useConfirm()
const notify = useNotify()
const update = useUpdateVacancyMutation()
const remove = useDeleteVacancyMutation()

const menu = ref<InstanceType<typeof Menu> | null>(null)
const isOpen = computed(() => props.vacancy.status === 'open')
const busy = computed(() => update.isPending.value || remove.isPending.value)

function edit() {
  router.push({ name: 'vacancy-edit', params: { id: props.vacancy.id } })
}

async function copyLink() {
  const link = `${location.origin}/vacancies/${props.vacancy.id}`
  try {
    await navigator.clipboard.writeText(link)
    notify.success('Link copied')
  } catch {
    notify.error(new Error('Copy the link manually: ' + link), 'Could not copy the link')
  }
}

function toggleStatus() {
  const status = isOpen.value ? 'closed' : 'open'
  update.mutate(
    { id: props.vacancy.id, payload: { status } },
    {
      onSuccess: () => notify.success(status === 'closed' ? 'Vacancy closed' : 'Vacancy reopened'),
      onError: (error) => notify.error(error),
    },
  )
}

function askDelete() {
  confirm.require({
    header: 'Delete vacancy?',
    message: `"${props.vacancy.title}" will be permanently deleted.`,
    icon: 'pi pi-trash',
    acceptLabel: 'Delete',
    acceptProps: { severity: 'danger' },
    rejectLabel: 'Cancel',
    rejectProps: { severity: 'secondary', outlined: true },
    accept: () =>
      remove.mutate(props.vacancy.id, {
        onSuccess: () => notify.success('Vacancy deleted'),
        onError: (error) => notify.error(error, 'Could not delete the vacancy'),
      }),
  })
}

const items = computed<MenuItem[]>(() => [
  { label: 'Copy public link', icon: 'pi pi-link', command: copyLink },
  {
    label: isOpen.value ? 'Close vacancy' : 'Reopen vacancy',
    icon: isOpen.value ? 'pi pi-lock' : 'pi pi-lock-open',
    command: toggleStatus,
  },
  { separator: true },
  { label: 'Delete', icon: 'pi pi-trash', class: 'row-actions__danger', command: askDelete },
])
</script>

<template>
  <div class="row-actions">
    <Button
      icon="pi pi-pencil"
      severity="secondary"
      text
      rounded
      aria-label="Edit vacancy"
      @click="edit"
    />
    <Button
      icon="pi pi-ellipsis-v"
      severity="secondary"
      text
      rounded
      aria-label="More actions"
      aria-haspopup="true"
      :loading="busy"
      @click="menu?.toggle($event)"
    />
    <Menu ref="menu" :model="items" popup />
  </div>
</template>

<style scoped>
.row-actions {
  display: flex;
  justify-content: flex-end;
  gap: 2px;
}

:global(.row-actions__danger) {
  color: var(--p-red-500);
}
</style>
