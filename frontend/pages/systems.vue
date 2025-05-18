<!--
 Copyright 2025 James G Willmore
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
     https://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { Row } from '@tanstack/vue-table'
import { v4 as uuidv4 } from 'uuid'

const UDropdownMenu = resolveComponent('UDropdownMenu')
const UButton = resolveComponent('UButton')

const { systemsApi } = useApi()

const systems = ref<System[]>([])
const editing = ref<System | null>(null)
const form = reactive<System>({
    id: '',
    name: ''
})

function getRowItems(row: Row<System>) {
    return [
        {
            label: 'Edit',
            onSelect: () => editSystem(row.original)
        },
        {
            label: 'Delete',
            onSelect: () => deleteSystem(row.original.id)
        }
    ]
}

const columns: TableColumn<System>[] = [
    { accessorKey: 'id', header: () => h('div', { class: 'text-black' }, 'ID'), },
    { accessorKey: 'name', header: () => h('div', { class: 'text-black' }, 'Name'), },
    {
        id: 'actions',
        header: () => h('div', { class: 'text-black text-right' }, 'Actions'),
        cell: ({ row }) => {
            return h(
                'div',
                { class: 'text-right' },
                h(
                    UDropdownMenu,
                    {
                        content: {
                            align: 'end'
                        },
                        items: getRowItems(row),
                        'aria-label': 'Actions dropdown'
                    },
                    () =>
                        h(UButton, {
                            icon: 'bi-list',
                            color: 'primary',
                            size: 'lg',
                            'aria-label': 'Actions dropdown'
                        })
                )
            )
        }
    }
]

const tableLoading = ref(false)

const loadSystems = async () => {
    tableLoading.value = true
    systems.value = await systemsApi.getAll()
    tableLoading.value = false
}

const resetForm = () => {
    editing.value = null
    form.id = ''
    form.name = ''
}

const saveSystem = async () => {
    if (editing.value) {
        await systemsApi.update(editing.value.id, form)
    } else {
        form.id = uuidv4()
        await systemsApi.create(form)
    }
    await loadSystems()
    resetForm()
}

const editSystem = (system: System) => {
    editing.value = system
    form.id = system.id
    form.name = system.name
}

const deleteSystem = async (id: string) => {
    if (confirm('Are you sure you want to delete this system?')) {
        await systemsApi.delete(id)
        await loadSystems()
    }
}

onMounted(loadSystems)
</script>

<template>
    <UContainer>
        <h1 class="text-2xl font-bold">Systems</h1>

        <form class="space-y-4 bg-white p-4 rounded shadow" @submit.prevent="saveSystem">
            <UInput v-model="form.id" type="text" placeholder="ID" class="w-full border p-2 rounded" disabled />
            <UInput v-model="form.name" type="text" placeholder="Name" class="w-full border p-2 rounded" required />

            <div class="flex gap-2">
                <UButton type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">
                    {{ editing ? 'Update' : 'Create' }}
                </UButton>
                <UButton v-if="editing" class="bg-gray-400 text-white px-4 py-2 rounded" @click="resetForm">Cancel
                </UButton>
            </div>
        </form>

        <UTable ref="table" :loading="tableLoading" :data="systems" :columns="columns" class="flex-1" />
    </UContainer>
</template>
