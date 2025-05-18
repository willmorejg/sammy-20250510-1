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
import { ComponentType, componentTypeOptions } from '~/models/models'

const UDropdownMenu = resolveComponent('UDropdownMenu')
const UButton = resolveComponent('UButton')

const { componentsApi } = useApi()

const componentItems = ref<ComponentItem[]>([])
const editing = ref<ComponentItem | null>(null)
const form = reactive<ComponentItem>({
    id: '',
    type: ComponentType.SOFTWARE,
    name: '',
    properties: []
})

function getRowItems(row: Row<ComponentItem>) {
    return [
        {
            label: 'Edit',
            onSelect: () => editComponentItem(row.original)
        },
        {
            label: 'Delete',
            onSelect: () => deleteComponentItem(row.original.id)
        }
    ]
}

const columns: TableColumn<ComponentItem>[] = [
    { accessorKey: 'id', header: () => h('div', { class: 'text-black' }, 'ID'), },
    { accessorKey: 'name', header: () => h('div', { class: 'text-black' }, 'Name'), },
    { accessorKey: 'type', header: () => h('div', { class: 'text-black' }, 'Type'), },
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

const loadComponentItems = async () => {
    tableLoading.value = true
    componentItems.value = await componentsApi.getAll()
    tableLoading.value = false
}

const resetForm = () => {
    editing.value = null
    form.id = ''
    form.name = ''
    form.properties = []
}

const saveComponentItem = async () => {
    if (editing.value) {
        await componentsApi.update(editing.value.id, form)
    } else {
        form.id = uuidv4()
        await componentsApi.create(form)
    }
    await loadComponentItems()
    resetForm()
}

const editComponentItem = (item: ComponentItem) => {
    editing.value = item
    form.id = item.id
    form.name = item.name
    form.type = item.type
    form.properties = item.properties
}

const deleteComponentItem = async (id: string) => {
    if (confirm('Are you sure you want to delete this component item?')) {
        await componentsApi.delete(id)
        await loadComponentItems()
    }
}

onMounted(loadComponentItems)
</script>

<template>
    <UContainer>
        <h1 class="text-2xl font-bold">Components</h1>

        <form class="space-y-4 bg-white p-4 rounded shadow" @submit.prevent="saveComponentItem">
            <UInput v-model="form.id" type="text" placeholder="ID" class="w-full border p-2 rounded" disabled />
            <UInput v-model="form.name" type="text" placeholder="Name" class="w-full border p-2 rounded" required />
            <USelect
                v-model="form.type"
                :items="componentTypeOptions"
                placeholder="Select a component type"
                required
            />

            <PropertiesEditor v-model="form.properties as Property[]" />

            <div class="flex gap-2">
                <UButton type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">
                    {{ editing ? 'Update' : 'Create' }}
                </UButton>
                <UButton v-if="editing" class="bg-gray-400 text-white px-4 py-2 rounded" @click="resetForm">
                    Cancel
                </UButton>
            </div>
        </form>

        <UTable ref="table" :loading="tableLoading" :data="componentItems" :columns="columns" class="flex-1" />
    </UContainer>
</template>
